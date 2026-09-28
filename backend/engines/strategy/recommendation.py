from models.defined_goal import DefinedGoal
from models.strategy import Scenario, StrategyDefinition, StrategyRankingItem, StrategyRecommendation, InvestorPriorities, StrategyArchitecture


def generate_recommendation(
    ranked_items: list[StrategyRankingItem],
    strategies: list[StrategyDefinition],
    scenarios: list[Scenario],
    defined_goal: DefinedGoal,
    priorities: InvestorPriorities,
    architectures: list[StrategyArchitecture] | None = None,
    rule_diagnostics: list[dict] | None = None,
) -> StrategyRecommendation:
    """Generate a goal‑level recommendation based on the ranked items.

    The function now consumes the new evidence‑based ranking output:
    * ``is_eligible`` and ``ineligible_reasons`` are respected – if the first
      item is ineligible we fall back to a no‑strategy recommendation.
    * ``evidence_scores`` is used to surface the concrete rationale for the
      recommendation (safety, liquidity, growth, flexibility, funding_gap).
    """
    architectures = architectures or []
    if not ranked_items:
        return StrategyRecommendation(
            recommended_strategy_id="",
            recommended_scenario_id="",
            short_reasons=["No applicable strategy available for the current goal and constraints."],
            complete_reasoning="No eligible strategy was found. The goal or its constraints must be changed before a strategy can be recommended.",
            feasibility_status="infeasible",
        )

    # If the top ranked item is ineligible, treat as no‑strategy case
    top = ranked_items[0]
    if not getattr(top, "is_eligible", True):
        return StrategyRecommendation(
            recommended_strategy_id="",
            recommended_scenario_id="",
            short_reasons=top.ineligible_reasons or ["Strategy was deemed ineligible by rule engine."],
            complete_reasoning="All candidate strategies were filtered out by eligibility rules.",
            feasibility_status="infeasible",
        )

    strat_lookup = {s.strategy_id: s for s in strategies}
    scen_lookup = {s.scenario_id: s for s in scenarios}
    top_strat = strat_lookup.get(top.strategy_id)
    top_scen = scen_lookup.get(top.scenario_id)
    architecture = next((a for a in architectures if a.primary_strategy_id == top.strategy_id), architectures[0] if architectures else None)

    # Use evidence scores for priority explanation instead of legacy composite scores
    evidence = getattr(top, "evidence_scores", {})
    # Determine dominant priority based on the highest evidence value
    if evidence:
        dominant_priority, dominant_score = max(evidence.items(), key=lambda kv: kv[1])
    else:
        # Fallback to original priorities if evidence missing
        norm_p = priorities.normalized()
        dominant_priority = max(
            [("safety", norm_p.safety), ("liquidity", norm_p.liquidity), ("growth", norm_p.growth), ("flexibility", norm_p.flexibility)],
            key=lambda x: x[1],
        )[0]
        dominant_score = top.dimension_scores.get(dominant_priority, 7.0)

    short_reasons = [f"Strongly aligns with your priority for {dominant_priority.capitalize()} (score: {dominant_score}/10)."]
    if defined_goal.funding_status == "Shortfall":
        short_reasons.append(f"Addresses the current funding shortfall of ₹{defined_goal.funding_gap:,.2f} over {defined_goal.duration_years} years.")
    elif defined_goal.funding_status == "On Track":
        short_reasons.append(f"Maintains the goal trajectory toward the required ₹{defined_goal.future_target:,.2f} target.")
    else:
        short_reasons.append(f"Recognises the current surplus of ₹{abs(defined_goal.funding_gap):,.2f} and avoids blindly treating it as additional required funding.")

    # Financial‑state diagnostics are explanatory evidence only.
    diagnostics = rule_diagnostics or []
    for diagnostic in diagnostics:
        status = diagnostic.get("evidence", {}).get("status")
        if status in {"healthy", "excellent"}:
            short_reasons.append(diagnostic.get("message", "Financial-state health is supportive."))
        elif status == "critical":
            short_reasons.append(diagnostic.get("message", "A financial-state constraint should be addressed alongside the strategy."))

    if architecture and architecture.supporting_strategy_ids:
        short_reasons.append("Combines a primary strategy with supporting strategies because one isolated strategy is not sufficient for the goal context.")
    if top_strat and top_strat.good_outcomes:
        short_reasons.append(top_strat.good_outcomes[0])

    complete_reasoning = (
        f"For '{defined_goal.goal_name}', the {top.strategy_name} scenario ranks highest after evaluating goal fit and investor priorities. "
        f"The recommendation is a goal-level strategy architecture rather than a product or portfolio selection. "
        f"The goal is currently {defined_goal.funding_status.lower()} with a {defined_goal.duration_years}-year horizon. "
        f"The dominant stated priority is {dominant_priority}, with a strategy‑fit score of {round(dominant_score, 1)}/10. "
    )
    critical = [d.get("message") for d in diagnostics if d.get("evidence", {}).get("status") == "critical"]
    if critical:
        complete_reasoning += "Financial-state considerations: " + " ".join(critical) + " "
    complete_reasoning += f"Trade-off: {top_scen.trade_off_notes if top_scen else 'The selected architecture must be implemented downstream without changing the strategic objective.'}"

    return StrategyRecommendation(
        recommended_strategy_id=top.strategy_id,
        recommended_scenario_id=top.scenario_id,
        short_reasons=short_reasons,
        complete_reasoning=complete_reasoning,
        architecture=architecture,
        alternative_architecture_ids=[a.architecture_id for a in architectures if not architecture or a.architecture_id != architecture.architecture_id],
        feasibility_status=architecture.feasibility_status if architecture else "conditional",
        constraints=architecture.constraints if architecture else ["Financial-state context is incomplete."],
    )
