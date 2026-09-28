"""
Strategy Decision Engine
========================
Authoritative decision layer as specified in STRATEGY_CONVERSION_SPEC.md §3.7 & §3.8.

The decision engine compares ELIGIBLE strategy architectures using explicit evidence:
- Eligibility gate (ineligible strategies are disqualified)
- Goal fit (canonical goal type affinity & characteristic matching)
- Horizon fit (time-to-goal suitability)
- Funding fit (shortfall / on-track / overfunded mechanisms)
- Feasibility & constraint compatibility (inputs, blockers, diagnostics)
- Component activation preference

Dimension scores (safety, liquidity, growth, flexibility) and composite scores
are strictly descriptive evidence; they do NOT determine the strategy recommendation.
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


def evaluate_decision(
    strategies: list[StrategyDefinition],
    scenarios: list[Scenario],
    architectures: list[StrategyArchitecture],
    defined_goal: DefinedGoal,
    financial_context: dict | None = None,
    rule_assessment: Any | None = None,
    priorities: InvestorPriorities | None = None,
) -> DecisionResult:
    """Evaluate eligible strategy architectures and make an evidence-based recommendation.

    Dimension scores and composite scores are NOT used as decision authority.
    """
    if not strategies or not architectures:
        return DecisionResult(
            recommended_strategy_id="",
            recommended_scenario_id="",
            recommended_architecture=None,
            alternative_architectures=[],
            ordered_strategy_ids=[],
            decision_rationale=["No applicable strategy available for the current goal and constraints."],
            complete_reasoning="No eligible strategy architecture was found in the library for this goal.",
            feasibility_status="infeasible",
            constraints=["No eligible strategy found."],
        )

    context = {
        "duration_years": defined_goal.duration_years,
        "funding_status": defined_goal.funding_status,
        **(financial_context or {}),
    }

    strat_lookup = {s.strategy_id: s for s in strategies}
    scen_lookup: dict[str, Scenario] = {}
    for s in scenarios:
        if s.strategy_id not in scen_lookup:
            scen_lookup[s.strategy_id] = s
        elif "standard" in s.scenario_id or "Recommended Baseline" in s.scenario_name:
            scen_lookup[s.strategy_id] = s

    canonical_goal = _canonical_goal_type(defined_goal.goal_type)
    duration = float(defined_goal.duration_years or 0.0)
    funding_status = defined_goal.funding_status or "Shortfall"
    funding_gap = float(defined_goal.funding_gap or 0.0)
    priority = (defined_goal.priority or "High").title()
    flexibility = (defined_goal.flexibility or "Fixed").title()
    total_liabilities = float(context.get("total_liabilities", 0.0) or 0.0)

    evaluations: list[ArchitectureEvaluation] = []

    for arch in architectures:
        primary_strat = strat_lookup.get(arch.primary_strategy_id)
        if not primary_strat:
            continue

        baseline_scen = scen_lookup.get(primary_strat.strategy_id)
        if not baseline_scen:
            continue

        # 1. Eligibility Gate
        is_eligible, ineligible_reasons = evaluate_eligibility(primary_strat, defined_goal, None)
        if not is_eligible:
            evaluations.append(
                ArchitectureEvaluation(
                    architecture=arch,
                    primary_strategy=primary_strat,
                    baseline_scenario=baseline_scen,
                    is_eligible=False,
                    ineligible_reasons=ineligible_reasons,
                    goal_fit_score=0.0,
                    horizon_fit_score=0.0,
                    funding_fit_score=0.0,
                    feasibility_score=0.0,
                    component_fit_score=0.0,
                    total_decision_score=-1000.0,
                    evidence={"eligibility": "failed", "reasons": ineligible_reasons},
                    rationale=ineligible_reasons,
                )
            )
            continue

        rationale: list[str] = []

        # 2. Goal Fit Score (0 - 40 points)
        goal_fit = 0.0
        applicable_types = [t.strip().lower() for t in primary_strat.applicable_goal_types]
        if canonical_goal in applicable_types:
            goal_fit += 25.0
            rationale.append(f"Explicit target match for {defined_goal.goal_type or canonical_goal.title()} goals.")
        elif "other" in applicable_types:
            goal_fit += 10.0
            rationale.append("General goal coverage applies to this goal type.")

        # Goal characteristic matches
        strat_chars = set(primary_strat.applicable_goal_characteristics)
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

        # 3. Horizon Fit Score (0 - 30 points)
        horizon_fit = 0.0
        if duration >= 10:
            if primary_strat.strategy_id in ("strat-dynamic-accumulation", "strat-calibrated-growth"):
                horizon_fit += 30.0
                rationale.append(f"Long horizon of {duration:g} years enables sustained compounding and accumulation.")
            elif primary_strat.strategy_id == "strat-high-liquidity-flex":
                horizon_fit += 20.0
            elif primary_strat.strategy_id == "strat-cap-preservation":
                horizon_fit += 5.0
            else:
                horizon_fit += 15.0
        elif 4 <= duration < 10:
            if primary_strat.strategy_id in ("strat-calibrated-growth", "strat-high-liquidity-flex"):
                horizon_fit += 30.0
                rationale.append(f"Medium horizon of {duration:g} years is ideally suited for balanced goal funding and progressive transition.")
            elif primary_strat.strategy_id == "strat-cap-preservation":
                horizon_fit += 18.0
            elif primary_strat.strategy_id == "strat-dynamic-accumulation":
                horizon_fit += 15.0
            else:
                horizon_fit += 15.0
        else:  # duration < 4
            if primary_strat.strategy_id in ("strat-cap-preservation", "strat-high-liquidity-flex"):
                horizon_fit += 30.0
                rationale.append(f"Near-term horizon of {duration:g} years requires capital preservation and liquidity certainty.")
            elif primary_strat.strategy_id == "strat-calibrated-growth":
                horizon_fit += 15.0
            else:
                horizon_fit += 5.0

        # 4. Funding Fit Score (0 - 25 points)
        funding_fit = 0.0
        if funding_status == "Shortfall":
            if total_liabilities > 0 and primary_strat.strategy_id == "strat-debt-reduction":
                funding_fit += 25.0
                rationale.append("Addresses debt obligations that actively constrain savings surplus for this goal.")
            elif canonical_goal == "home purchase" and primary_strat.strategy_id == "strat-credit-utilisation":
                funding_fit += 22.0
                rationale.append("Leverages planned credit financing to bridge home acquisition gap.")
            elif primary_strat.strategy_id in ("strat-calibrated-growth", "strat-dynamic-accumulation"):
                funding_fit += 20.0
                rationale.append(f"Addresses funding shortfall of ₹{funding_gap:,.2f} through structured contribution and growth levers.")
            else:
                funding_fit += 10.0
        elif funding_status == "On Track":
            if primary_strat.strategy_id in ("strat-high-liquidity-flex", "strat-cap-preservation"):
                funding_fit += 25.0
                rationale.append("Protects on-track trajectory by locking in progress and de-risking as timeline elapses.")
            elif primary_strat.strategy_id == "strat-goal-reprioritisation":
                funding_fit += 20.0
            else:
                funding_fit += 15.0
        else:  # Overfunded
            if primary_strat.strategy_id in ("strat-cap-preservation", "strat-high-liquidity-flex"):
                funding_fit += 25.0
                rationale.append("Capital preservation locks in achieved surplus without taking unneeded market risk.")
            else:
                funding_fit += 12.0

        # 5. Feasibility & Constraint Compatibility (0 - 15 points)
        feasibility_score = 0.0
        if arch.feasibility_status == "feasible":
            feasibility_score += 15.0
        elif arch.feasibility_status == "conditional":
            feasibility_score += 8.0
        else:
            feasibility_score += 0.0

        # 6. Component Fit Score (0 - 15 points)
        component_fit = 0.0
        if any("activated by component metadata" in r for r in arch.rationale):
            component_fit += 10.0
        if arch.supporting_strategy_ids:
            component_fit += 5.0

        total_score = round(goal_fit + horizon_fit + funding_fit + feasibility_score + component_fit, 2)

        evidence = {
            "goal_fit_score": goal_fit,
            "horizon_fit_score": horizon_fit,
            "funding_fit_score": funding_fit,
            "feasibility_score": feasibility_score,
            "component_fit_score": component_fit,
            "total_decision_score": total_score,
            "is_eligible": True,
        }

        evaluations.append(
            ArchitectureEvaluation(
                architecture=arch,
                primary_strategy=primary_strat,
                baseline_scenario=baseline_scen,
                is_eligible=True,
                ineligible_reasons=[],
                goal_fit_score=goal_fit,
                horizon_fit_score=horizon_fit,
                funding_fit_score=funding_fit,
                feasibility_score=feasibility_score,
                component_fit_score=component_fit,
                total_decision_score=total_score,
                evidence=evidence,
                rationale=rationale,
            )
        )

    # Deterministic comparison sorting:
    # 1. Eligible first
    # 2. Highest total decision score (goal-fit, horizon-fit, funding-fit, feasibility)
    # 3. Feasibility status tie-breaker
    # 4. Strategy ID tie-breaker
    evaluations.sort(
        key=lambda e: (
            1 if e.is_eligible else 0,
            e.total_decision_score,
            1 if e.architecture.feasibility_status == "feasible" else 0,
            -len(e.architecture.constraints),
            e.primary_strategy.strategy_id,
        ),
        reverse=True,
    )

    eligible_evals = [e for e in evaluations if e.is_eligible]
    if not eligible_evals:
        # All candidates were ineligible
        first_ineligible = evaluations[0] if evaluations else None
        reasons = first_ineligible.ineligible_reasons if first_ineligible else ["No strategies passed eligibility."]
        return DecisionResult(
            recommended_strategy_id="",
            recommended_scenario_id="",
            recommended_architecture=None,
            alternative_architectures=[],
            ordered_strategy_ids=[e.primary_strategy.strategy_id for e in evaluations],
            evaluations=evaluations,
            decision_rationale=reasons,
            complete_reasoning="All candidate strategies were filtered out by deterministic eligibility rules.",
            feasibility_status="infeasible",
            constraints=reasons,
        )

    best = eligible_evals[0]
    alternatives = [e.architecture for e in eligible_evals[1:]]

    # Combine rationale cleanly
    clean_reasons = list(best.rationale)
    if not clean_reasons:
        clean_reasons.append(f"Highest strategic fit for {defined_goal.goal_name}.")

    complete_reasoning = (
        f"For '{defined_goal.goal_name}', {best.primary_strategy.name} was selected through deterministic "
        f"evidence comparison (Goal Fit: {best.goal_fit_score:g}, Horizon Fit: {best.horizon_fit_score:g}, "
        f"Funding Fit: {best.funding_fit_score:g}). "
        f"The goal is currently {funding_status.lower()} with a {duration:g}-year horizon. "
        f"Recommendation is governed by strategy architecture suitability rather than dimension score weighting. "
        f"Trade-off: {best.baseline_scenario.trade_off_notes or (best.primary_strategy.trade_offs[0] if best.primary_strategy.trade_offs else 'Downstream implementation parameters must align with this strategic objective.')}"
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
        feasibility_status=best.architecture.feasibility_status,
        constraints=best.architecture.constraints,
    )
