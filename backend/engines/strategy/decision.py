"""
Strategy Decision Engine
========================
Authoritative decision layer for strategy conversion.

Recommendation contract:
- Eligibility is evaluated with the actual financial context.
- Only Pass and Conditional candidates can reach investor-facing selection.
- Recommended is always Pass when at least one Pass exists.
- Conditional becomes Recommended only when no Pass strategy exists.
- At most one Alternative is exposed; it may be Pass or Conditional.
- Fail strategies are never investor-facing recommendations.
"""

from dataclasses import dataclass, field
from typing import Any

from models.defined_goal import DefinedGoal
from models.strategy import (
    InvestorPriorities,
    Scenario,
    StrategyArchitecture,
    StrategyDefinition,
)
from engines.rules.engine import GOAL_TYPE_ALIASES
from engines.strategy.eligibility import evaluate_eligibility


@dataclass
class ArchitectureEvaluation:
    architecture: StrategyArchitecture
    primary_strategy: StrategyDefinition
    baseline_scenario: Scenario
    is_eligible: bool
    ineligible_reasons: list[str]
    goal_fit_score: float
    horizon_fit_score: float
    funding_fit_score: float
    feasibility_score: float
    component_fit_score: float
    total_decision_score: float
    evidence: dict[str, Any]
    rationale: list[str]
    eligibility_status: str = "fail"  # pass | conditional | fail


@dataclass
class DecisionResult:
    recommended_strategy_id: str
    recommended_scenario_id: str
    recommended_architecture: StrategyArchitecture | None
    alternative_architectures: list[StrategyArchitecture]
    ordered_strategy_ids: list[str]
    evaluations: list[ArchitectureEvaluation] = field(default_factory=list)
    decision_rationale: list[str] = field(default_factory=list)
    complete_reasoning: str = ""
    feasibility_status: str = "feasible"
    constraints: list[str] = field(default_factory=list)


def _canonical_goal_type(goal_type: str | None) -> str:
    if not goal_type:
        return ""
    clean = goal_type.strip().lower()
    return GOAL_TYPE_ALIASES.get(clean, clean)


def _empty_result(message: str, constraints: list[str] | None = None) -> DecisionResult:
    reasons = constraints or [message]
    return DecisionResult(
        recommended_strategy_id="",
        recommended_scenario_id="",
        recommended_architecture=None,
        alternative_architectures=[],
        ordered_strategy_ids=[],
        decision_rationale=reasons,
        complete_reasoning=message,
        feasibility_status="infeasible",
        constraints=reasons,
    )


def evaluate_decision(
    strategies: list[StrategyDefinition],
    scenarios: list[Scenario],
    architectures: list[StrategyArchitecture],
    defined_goal: DefinedGoal,
    financial_context: dict | None = None,
    rule_assessment: Any | None = None,
    priorities: InvestorPriorities | None = None,
) -> DecisionResult:
    """Evaluate strategies and enforce the Pass/Conditional/Fail contract."""
    if not strategies or not architectures:
        return _empty_result("No applicable strategy available for the current goal and constraints.")

    context = {
        "duration_years": defined_goal.duration_years,
        "funding_status": defined_goal.funding_status,
        **(financial_context or {}),
    }

    strat_lookup = {s.strategy_id: s for s in strategies}
    scen_lookup: dict[str, Scenario] = {}
    for scenario in scenarios:
        if scenario.strategy_id not in scen_lookup or "standard" in scenario.scenario_id or "Recommended Baseline" in scenario.scenario_name:
            scen_lookup[scenario.strategy_id] = scenario

    canonical_goal = _canonical_goal_type(defined_goal.goal_type)
    duration = float(defined_goal.duration_years or 0.0)
    funding_status = defined_goal.funding_status or "Shortfall"
    funding_gap = float(defined_goal.funding_gap or 0.0)
    priority = (defined_goal.priority or "High").title()
    flexibility = (defined_goal.flexibility or "Fixed").title()
    total_liabilities = float(context.get("total_liabilities", 0.0) or 0.0)

    evaluations: list[ArchitectureEvaluation] = []

    for arch in architectures:
        primary = strat_lookup.get(arch.primary_strategy_id)
        baseline = scen_lookup.get(arch.primary_strategy_id)
        if not primary or not baseline:
            continue

        # IMPORTANT: pass the actual financial context. The previous implementation
        # passed None, so cash-flow/liquidity/debt/resource evidence was invisible here.
        eligible, eligibility_reasons = evaluate_eligibility(
            primary,
            defined_goal,
            financial_context=context,
            rule_assessment=rule_assessment,
        )

        if not eligible:
            evaluations.append(ArchitectureEvaluation(
                architecture=arch,
                primary_strategy=primary,
                baseline_scenario=baseline,
                is_eligible=False,
                ineligible_reasons=eligibility_reasons,
                goal_fit_score=0.0,
                horizon_fit_score=0.0,
                funding_fit_score=0.0,
                feasibility_score=0.0,
                component_fit_score=0.0,
                total_decision_score=-1000.0,
                evidence={"eligibility": "fail", "reasons": eligibility_reasons},
                rationale=eligibility_reasons,
                eligibility_status="fail",
            ))
            continue

        rationale: list[str] = []

        goal_fit = 0.0
        applicable_types = [t.strip().lower() for t in primary.applicable_goal_types]
        if canonical_goal in applicable_types:
            goal_fit += 25.0
            rationale.append(f"Explicit target match for {defined_goal.goal_type or canonical_goal.title()} goals.")
        elif "other" in applicable_types:
            goal_fit += 10.0
            rationale.append("General goal coverage applies to this goal type.")

        strat_chars = set(primary.applicable_goal_characteristics)
        if funding_status.lower() in strat_chars or (funding_status == "Shortfall" and "shortfall" in strat_chars):
            goal_fit += 5.0
        if duration >= 7 and "long_term" in strat_chars:
            goal_fit += 5.0
        elif duration <= 5 and "near_term" in strat_chars:
            goal_fit += 5.0
        if flexibility == "Fixed" and "fixed_timeline" in strat_chars:
            goal_fit += 5.0
        if priority in ("Critical", "High") and "high_priority" in strat_chars:
            goal_fit += 5.0

        if duration >= 10:
            if primary.strategy_id in ("strat-dynamic-accumulation", "strat-calibrated-growth"):
                horizon_fit = 30.0
            elif primary.strategy_id == "strat-high-liquidity-flex":
                horizon_fit = 20.0
            elif primary.strategy_id == "strat-cap-preservation":
                horizon_fit = 5.0
            else:
                horizon_fit = 15.0
        elif 4 <= duration < 10:
            if primary.strategy_id in ("strat-calibrated-growth", "strat-high-liquidity-flex"):
                horizon_fit = 30.0
            elif primary.strategy_id == "strat-cap-preservation":
                horizon_fit = 18.0
            elif primary.strategy_id == "strat-dynamic-accumulation":
                horizon_fit = 15.0
            else:
                horizon_fit = 15.0
        else:
            if primary.strategy_id in ("strat-cap-preservation", "strat-high-liquidity-flex"):
                horizon_fit = 30.0
            elif primary.strategy_id == "strat-calibrated-growth":
                horizon_fit = 15.0
            else:
                horizon_fit = 5.0

        funding_fit = 0.0
        if funding_status == "Shortfall":
            if total_liabilities > 0 and primary.strategy_id == "strat-debt-reduction":
                funding_fit = 25.0
            elif canonical_goal == "home purchase" and primary.strategy_id == "strat-credit-utilisation":
                funding_fit = 22.0
            elif primary.strategy_id in ("strat-calibrated-growth", "strat-dynamic-accumulation"):
                funding_fit = 20.0
            else:
                funding_fit = 10.0
        elif funding_status == "On Track":
            funding_fit = 25.0 if primary.strategy_id in ("strat-high-liquidity-flex", "strat-cap-preservation") else 20.0 if primary.strategy_id == "strat-goal-reprioritisation" else 15.0
        else:
            funding_fit = 25.0 if primary.strategy_id in ("strat-cap-preservation", "strat-high-liquidity-flex") else 12.0

        feasibility_score = 15.0 if arch.feasibility_status == "feasible" else 8.0 if arch.feasibility_status == "conditional" else 0.0
        component_fit = (10.0 if any("activated by component metadata" in r for r in arch.rationale) else 0.0) + (5.0 if arch.supporting_strategy_ids else 0.0)
        total_score = round(goal_fit + horizon_fit + funding_fit + feasibility_score + component_fit, 2)

        # Architecture feasibility is the explicit conditional signal. It never
        # outranks a Pass when selecting the Recommended strategy.
        status = "pass" if arch.feasibility_status == "feasible" else "conditional" if arch.feasibility_status == "conditional" else "fail"
        if status == "conditional":
            rationale.append("Strategy is usable only with the listed implementation changes/constraints.")

        evaluations.append(ArchitectureEvaluation(
            architecture=arch,
            primary_strategy=primary,
            baseline_scenario=baseline,
            is_eligible=status in {"pass", "conditional"},
            ineligible_reasons=[] if status != "fail" else list(arch.constraints),
            goal_fit_score=goal_fit,
            horizon_fit_score=horizon_fit,
            funding_fit_score=funding_fit,
            feasibility_score=feasibility_score,
            component_fit_score=component_fit,
            total_decision_score=total_score,
            evidence={
                "goal_fit_score": goal_fit,
                "horizon_fit_score": horizon_fit,
                "funding_fit_score": funding_fit,
                "feasibility_score": feasibility_score,
                "component_fit_score": component_fit,
                "total_decision_score": total_score,
                "eligibility_status": status,
            },
            rationale=rationale,
            eligibility_status=status,
        ))

    pass_evals = [e for e in evaluations if e.eligibility_status == "pass"]
    conditional_evals = [e for e in evaluations if e.eligibility_status == "conditional"]
    selectable = pass_evals or conditional_evals

    if not selectable:
        failure_reasons: list[str] = []
        for evaluation in evaluations:
            failure_reasons.extend(evaluation.ineligible_reasons)
        if not failure_reasons:
            failure_reasons = ["No strategy passed the eligibility requirements."]
        return DecisionResult(
            recommended_strategy_id="",
            recommended_scenario_id="",
            recommended_architecture=None,
            alternative_architectures=[],
            ordered_strategy_ids=[e.primary_strategy.strategy_id for e in evaluations],
            evaluations=evaluations,
            decision_rationale=failure_reasons,
            complete_reasoning="No Pass or Conditional strategy is available. The listed eligibility failures must be addressed before a strategy can be recommended.",
            feasibility_status="infeasible",
            constraints=failure_reasons,
        )

    # Pass always wins over Conditional. Conditional can be Recommended only
    # when there are zero Pass candidates.
    candidate_pool = pass_evals if pass_evals else conditional_evals
    candidate_pool.sort(key=lambda e: (-e.total_decision_score, e.primary_strategy.strategy_id))
    best = candidate_pool[0]

    # Exactly one Alternative, selected from the remaining Pass candidates first;
    # if none remain, use Conditional candidates.
    remaining_pass = [e for e in pass_evals if e is not best]
    remaining_conditional = [e for e in conditional_evals if e is not best]
    alternative_pool = remaining_pass or remaining_conditional
    alternative_pool.sort(key=lambda e: (-e.total_decision_score, e.primary_strategy.strategy_id))
    alternatives = [alternative_pool[0].architecture] if alternative_pool else []

    clean_reasons = list(best.rationale) or [f"Highest strategic fit for {defined_goal.goal_name}."]
    complete_reasoning = (
        f"For '{defined_goal.goal_name}', {best.primary_strategy.name} was selected after deterministic eligibility "
        f"and strategy-fit evaluation. Eligibility status: {best.eligibility_status}. "
        f"Goal Fit: {best.goal_fit_score:g}; Horizon Fit: {best.horizon_fit_score:g}; "
        f"Funding Fit: {best.funding_fit_score:g}. "
        f"Pass strategies take precedence over Conditional strategies; Conditional becomes Recommended only when no Pass exists."
    )

    return DecisionResult(
        recommended_strategy_id=best.primary_strategy.strategy_id,
        recommended_scenario_id=best.baseline_scenario.scenario_id,
        recommended_architecture=best.architecture,
        alternative_architectures=alternatives,
        ordered_strategy_ids=[e.primary_strategy.strategy_id for e in evaluations],
        evaluations=evaluations,
        decision_rationale=clean_reasons,
        complete_reasoning=complete_reasoning,
        feasibility_status="feasible" if best.eligibility_status == "pass" else "conditional",
        constraints=best.architecture.constraints,
    )
