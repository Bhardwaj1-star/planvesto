from typing import Any
from models.defined_goal import DefinedGoal
from models.strategy import (
    InvestorPriorities,
    Scenario,
    StrategyArchitecture,
    StrategyDefinition,
    StrategyRankingItem,
    StrategyRecommendation,
)
from engines.strategy.decision import DecisionResult, evaluate_decision


def generate_recommendation(
    ranked_items: list[StrategyRankingItem] | None = None,
    strategies: list[StrategyDefinition] | None = None,
    scenarios: list[Scenario] | None = None,
    defined_goal: DefinedGoal | None = None,
    priorities: InvestorPriorities | None = None,
    architectures: list[StrategyArchitecture] | None = None,
    rule_diagnostics: list[dict] | None = None,
    decision_result: DecisionResult | None = None,
    financial_context: dict | None = None,
    technique_outputs: list[dict[str, Any]] | None = None,
) -> StrategyRecommendation:
    """Generate a goal-level strategy recommendation based on decision evidence.

    Consumes the new DecisionResult from ComparisonDecisionEngine rather than
    blindly taking ranked_items[0] or deriving recommendations from legacy priority dimensions.
    """
    architectures = architectures or []
    strategies = strategies or []
    scenarios = scenarios or []
    diagnostics = rule_diagnostics or []

    # If decision_result is not passed, evaluate it from the available context
    if decision_result is None:
        if defined_goal and strategies and scenarios:
            decision_result = evaluate_decision(
                strategies=strategies,
                scenarios=scenarios,
                architectures=architectures,
                defined_goal=defined_goal,
                financial_context=financial_context,
                priorities=priorities,
                technique_outputs=technique_outputs,
            )
        elif ranked_items:
            # Fallback for mock/isolated calls with only ranked_items
            eligible_items = [r for r in ranked_items if getattr(r, "is_eligible", True)]
            if not eligible_items:
                return StrategyRecommendation(
                    recommended_strategy_id="",
                    recommended_scenario_id="",
                    short_reasons=["All candidate strategies were deemed ineligible by rule engine."],
                    complete_reasoning="All candidate strategies were filtered out by eligibility rules.",
                    feasibility_status="infeasible",
                    constraints=["Ineligible by rule constraints."],
                )
            top = eligible_items[0]
            matched_arch = next((a for a in architectures if a.primary_strategy_id == top.strategy_id), architectures[0] if architectures else None)
            return StrategyRecommendation(
                recommended_strategy_id=top.strategy_id,
                recommended_scenario_id=top.scenario_id,
                short_reasons=[f"Selected strategy architecture '{top.strategy_name}' best satisfies goal requirements."],
                complete_reasoning=f"Strategy architecture '{top.strategy_name}' was selected as the optimal pathway for this goal.",
                architecture=matched_arch,
                alternative_architecture_ids=[a.architecture_id for a in architectures if not matched_arch or a.architecture_id != matched_arch.architecture_id],
                feasibility_status=matched_arch.feasibility_status if matched_arch else "feasible",
                constraints=matched_arch.constraints if matched_arch else [],
            )
        else:
            return StrategyRecommendation(
                recommended_strategy_id="",
                recommended_scenario_id="",
                short_reasons=["No applicable strategy available for the current goal and constraints."],
                complete_reasoning="No eligible strategy architecture was found in the library for this goal.",
                feasibility_status="infeasible",
                constraints=["No eligible strategy found."],
            )

    # Ineligible / no-strategy case
    if not decision_result.recommended_strategy_id:
        return StrategyRecommendation(
            recommended_strategy_id="",
            recommended_scenario_id="",
            short_reasons=decision_result.decision_rationale or ["No applicable strategy available for current constraints."],
            complete_reasoning=decision_result.complete_reasoning or "All candidate strategies were filtered out by deterministic rules.",
            feasibility_status="infeasible",
            constraints=decision_result.constraints or ["No eligible strategy found."],
        )

    short_reasons: list[str] = list(decision_result.decision_rationale)

    # Funding context description
    if defined_goal:
        if defined_goal.funding_status == "Shortfall":
            short_reasons.append(
                f"Addresses the funding shortfall of ₹{defined_goal.funding_gap:,.2f} over a {defined_goal.duration_years:g}-year horizon."
            )
        elif defined_goal.funding_status == "On Track":
            short_reasons.append(
                f"Maintains the goal trajectory toward the required ₹{defined_goal.future_target:,.2f} target."
            )
        else:
            short_reasons.append(
                f"Preserves the current surplus of ₹{abs(defined_goal.funding_gap):,.2f} without exposing capital to unneeded market risk."
            )

    # Append financial-state diagnostics as explanatory evidence only
    for diagnostic in diagnostics:
        status = diagnostic.get("evidence", {}).get("status")
        if status in {"healthy", "excellent"}:
            short_reasons.append(diagnostic.get("message", "Financial-state health is supportive."))
        elif status == "critical":
            short_reasons.append(diagnostic.get("message", "A financial-state constraint should be addressed alongside the strategy."))

    arch = decision_result.recommended_architecture
    if arch and arch.supporting_strategy_ids:
        short_reasons.append("Combines a primary strategy with supporting strategies because one isolated strategy is not sufficient for the goal context.")

    strat_lookup = {s.strategy_id: s for s in strategies}
    top_strat = strat_lookup.get(decision_result.recommended_strategy_id)
    if top_strat and top_strat.good_outcomes:
        short_reasons.append(top_strat.good_outcomes[0])

    complete_reasoning = decision_result.complete_reasoning
    critical_notes = [d.get("message") for d in diagnostics if d.get("evidence", {}).get("status") == "critical" and d.get("message")]
    if critical_notes:
        complete_reasoning += " Financial-state considerations: " + " ".join(critical_notes)

    return StrategyRecommendation(
        recommended_strategy_id=decision_result.recommended_strategy_id,
        recommended_scenario_id=decision_result.recommended_scenario_id,
        short_reasons=short_reasons,
        complete_reasoning=complete_reasoning,
        architecture=arch,
        alternative_architecture_ids=[a.architecture_id for a in decision_result.alternative_architectures],
        feasibility_status=decision_result.feasibility_status,  # type: ignore
        constraints=decision_result.constraints,
    )
