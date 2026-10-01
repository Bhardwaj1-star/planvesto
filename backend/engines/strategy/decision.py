"""Authoritative Strategy Builder decision layer."""
from dataclasses import dataclass, field
from typing import Any
from models.defined_goal import DefinedGoal
from models.strategy import InvestorPriorities, Scenario, StrategyArchitecture, StrategyDefinition
from rules.goals import GOAL_TYPE_ALIASES, canonical_goal_type
from rules.strategy_decision import (
    calculate_component_score,
    calculate_feasibility_score,
    calculate_funding_fit_score,
    calculate_goal_fit_score,
    calculate_horizon_fit_score,
    evaluate_decision_score,
)
from engines.strategy.eligibility import evaluate_eligibility, evaluate_eligibility_fits, EligibilityStatus
from engines.constraints.models import ConstraintSet

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
    eligibility_status: str = "fail"
    scenario_evaluations: list[dict[str, Any]] = field(default_factory=list)

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
    return canonical_goal_type(goal_type)

def _empty(message: str) -> DecisionResult:
    return DecisionResult("", "", None, [], [], [], [message], message, "infeasible", [message])

def evaluate_decision(strategies: list[StrategyDefinition], scenarios: list[Scenario], architectures: list[StrategyArchitecture], defined_goal: DefinedGoal, financial_context: dict | None = None, rule_assessment: Any | None = None, priorities: InvestorPriorities | None = None, constraint_set: ConstraintSet | None = None) -> DecisionResult:
    if not strategies or not architectures: return _empty("No applicable strategy available for the current goal and constraints.")
    base={"duration_years":defined_goal.duration_years,"funding_status":defined_goal.funding_status,**(financial_context or {})}
    strat_lookup={s.strategy_id:s for s in strategies}
    scenarios_by_strategy: dict[str, list[Scenario]] = {}
    for scenario in scenarios:
        scenarios_by_strategy.setdefault(scenario.strategy_id, []).append(scenario)

    def _scenario_status_score(scenario: Scenario) -> float:
        """Score funding-variant feasibility without inventing investor preferences."""
        status = str((scenario.metrics or {}).get("funding_strategy_status", ""))
        if status == "feasible":
            return 15.0
        if status == "requires_upfront_capital":
            return 8.0
        if status == "constrained":
            return 0.0
        return 5.0

    def _select_goal_funding_variant(variants: list[Scenario]) -> Scenario:
        """Select a transparent default after evaluating every funding variant."""
        return max(
            enumerate(variants),
            key=lambda pair: (_scenario_status_score(pair[1]), -pair[0]),
        )[1]
    evaluations=[]
    for arch in architectures:
        primary=strat_lookup.get(arch.primary_strategy_id)
        candidate_scenarios=scenarios_by_strategy.get(arch.primary_strategy_id, [])
        if not primary or not candidate_scenarios: continue
        baseline = (
            _select_goal_funding_variant(candidate_scenarios)
            if primary.strategy_id == "strat-goal-funding"
            else next(
                (s for s in candidate_scenarios if "standard" in s.scenario_id or "Recommended Baseline" in s.scenario_name),
                candidate_scenarios[0],
            )
        )
        context=dict(base)
        context["strategy_required_monthly_contribution"]=(baseline.metrics or {}).get("required_monthly_contribution",getattr(defined_goal,"required_monthly_contribution",None))
        fit=evaluate_eligibility_fits(primary,goal=defined_goal,financial_context=context)
        gate_ok,gate_reasons=evaluate_eligibility(primary,defined_goal,financial_context=context,rule_assessment=rule_assessment,constraint_set=constraint_set)
        status=fit.status if gate_ok else EligibilityStatus.FAIL
        reasons=list(gate_reasons)+[r.reason for r in fit.failed_fits]
        if status==EligibilityStatus.CONDITIONAL: reasons.extend(fit.required_changes)
        canonical=_canonical_goal_type(defined_goal.goal_type); duration=float(defined_goal.duration_years or 0); funding=defined_goal.funding_status or "Shortfall"
        goal_fit = calculate_goal_fit_score(
            canonical_goal_type=canonical,
            applicable_types=primary.applicable_goal_types,
            applicable_characteristics=primary.applicable_goal_characteristics,
            duration_years=duration,
            funding_status=funding,
            flexibility=defined_goal.flexibility,
            priority=defined_goal.priority,
        )
        horizon = calculate_horizon_fit_score(duration, primary.strategy_id)
        funding_score = calculate_funding_fit_score(funding, context.get("total_liabilities", 0), primary.strategy_id)
        feasibility = calculate_feasibility_score(status)
        component = calculate_component_score(arch.rationale, arch.supporting_strategy_ids)
        score = evaluate_decision_score(
            status=status,
            goal_fit_score=goal_fit,
            horizon_fit_score=horizon,
            funding_fit_score=funding_score,
            feasibility_score=feasibility,
            component_fit_score=component,
        )
        rationale=[] if status==EligibilityStatus.FAIL else [f"Goal-specific eligibility evaluated for {defined_goal.goal_name}."]
        if status==EligibilityStatus.CONDITIONAL: rationale.append("Strategy requires the listed changes before implementation.")
        scenario_evaluations: list[dict[str, Any]] = []
        if primary.strategy_id == "strat-goal-funding":
            for candidate in candidate_scenarios:
                variant_status = str((candidate.metrics or {}).get("funding_strategy_status", ""))
                scenario_evaluations.append({
                    "scenario_id": candidate.scenario_id,
                    "funding_strategy_id": candidate.funding_strategy_id,
                    "scenario_name": candidate.scenario_name,
                    "status": variant_status,
                    "score": _scenario_status_score(candidate),
                    "funding_gap": candidate.metrics.get("funding_gap"),
                    "required_monthly_contribution": candidate.metrics.get("required_monthly_contribution"),
                    "required_lumpsum": candidate.metrics.get("required_lumpsum"),
                    "starting_monthly_contribution": candidate.metrics.get("starting_monthly_contribution"),
                    "annual_step_up": candidate.metrics.get("annual_step_up"),
                    "reason": candidate.trade_off_notes,
                    "selected_as_default": candidate.scenario_id == baseline.scenario_id,
                })
            rationale.append(
                "All Goal Funding variants were evaluated; feasibility status is authoritative and library order is used only for ties."
            )
        evidence={
            "eligibility_status":status.value,
            "fit_results":[{"fit":r.fit,"status":r.status.value,"reason":r.reason,"required_changes":list(r.required_changes)} for r in fit.results],
            "scenario_evaluations": scenario_evaluations,
        }
        evaluations.append(ArchitectureEvaluation(
            arch,primary,baseline,status!=EligibilityStatus.FAIL,reasons,goal_fit,horizon,funding_score,
            feasibility,component,score,evidence,rationale,status.value,scenario_evaluations
        ))
    passes=[e for e in evaluations if e.eligibility_status=="pass"]; conditionals=[e for e in evaluations if e.eligibility_status=="conditional"]
    pool=passes or conditionals
    if not pool:
        reasons=[r for e in evaluations for r in e.ineligible_reasons] or ["No viable strategy matched the eligibility requirements."]
        return DecisionResult("","",None,[],[e.primary_strategy.strategy_id for e in evaluations],evaluations,reasons,"No viable strategy was found. Review the eligibility failures and required changes.","infeasible",reasons)
    pool.sort(key=lambda e:(-e.total_decision_score,e.primary_strategy.strategy_id)); best=pool[0]
    alt_pool=[e for e in passes if e is not best] or [e for e in conditionals if e is not best]; alt_pool.sort(key=lambda e:(-e.total_decision_score,e.primary_strategy.strategy_id)); alternatives=[alt_pool[0].architecture] if alt_pool else []
    return DecisionResult(best.primary_strategy.strategy_id,best.baseline_scenario.scenario_id,best.architecture,alternatives,[e.primary_strategy.strategy_id for e in evaluations],evaluations,best.rationale,f"For '{defined_goal.goal_name}', {best.primary_strategy.name} is {best.eligibility_status} after all eight eligibility fits. Pass takes precedence; Conditional is recommended only when no Pass exists.","feasible" if best.eligibility_status=="pass" else "conditional",best.architecture.constraints)
