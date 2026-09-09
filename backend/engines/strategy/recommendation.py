from models.defined_goal import DefinedGoal
from models.strategy import (
    InvestorPriorities,
    Scenario,
    StrategyDefinition,
    StrategyRankingItem,
    StrategyRecommendation,
)


def generate_recommendation(
    ranked_items: list[StrategyRankingItem],
    strategies: list[StrategyDefinition],
    scenarios: list[Scenario],
    defined_goal: DefinedGoal,
    priorities: InvestorPriorities,
) -> StrategyRecommendation:
    if not ranked_items:
        return StrategyRecommendation(
            recommended_strategy_id="",
            recommended_scenario_id="",
            short_reasons=["No applicable strategy available for this goal type."],
            complete_reasoning="No strategies in the catalog matched the specified goal type.",
        )

    top = ranked_items[0]
    strat_lookup = {s.strategy_id: s for s in strategies}
    scen_lookup = {s.scenario_id: s for s in scenarios}

    top_strat = strat_lookup.get(top.strategy_id)
    top_scen = scen_lookup.get(top.scenario_id)

    short_reasons: list[str] = []

    # Priority alignment reason
    norm_p = priorities.normalized()
    dominant_priority = max(
        [("safety", norm_p.safety), ("liquidity", norm_p.liquidity), ("growth", norm_p.growth), ("flexibility", norm_p.flexibility)],
        key=lambda x: x[1],
    )[0]

    dominant_score = top.dimension_scores.get(dominant_priority, 7.0)
    short_reasons.append(
        f"Strongly aligns with your priority for {dominant_priority.capitalize()} (score: {dominant_score}/10)."
    )

    # Goal status reason
    if defined_goal.funding_status == "Shortfall":
        short_reasons.append(
            f"Optimized to bridge the target-date shortfall of ₹{defined_goal.funding_gap:,.2f} over {defined_goal.duration_years} years."
        )
    elif defined_goal.funding_status == "On Track":
        short_reasons.append(
            f"Maintains disciplined corpus growth to secure the fully funded milestone of ₹{defined_goal.future_target:,.2f}."
        )
    else:
        short_reasons.append(
            f"Safeguards the surplus corpus of ₹{abs(defined_goal.funding_gap):,.2f} against unexpected market contractions."
        )

    # Outcome reason
    if top_strat and top_strat.good_outcomes:
        short_reasons.append(top_strat.good_outcomes[0])

    complete_reasoning = (
        f"Based on your goal '{defined_goal.goal_name}' ({defined_goal.goal_type}) with a target horizon of "
        f"{defined_goal.target_month:02d}/{defined_goal.target_year} ({defined_goal.duration_years} years), "
        f"the {top.strategy_name} ({top.scenario_name}) ranks highest with a composite score of {top.composite_score}/10. "
        f"This pathway directly incorporates your priority weighting ({dominant_priority.capitalize()}: {round(dominant_score, 1)}/10) "
        f"while addressing the goal's current {defined_goal.funding_status.lower()} position. "
        f"Trade-off note: {top_scen.trade_off_notes if top_scen else 'Standard market execution applies.'}"
    )

    return StrategyRecommendation(
        recommended_strategy_id=top.strategy_id,
        recommended_scenario_id=top.scenario_id,
        short_reasons=short_reasons,
        complete_reasoning=complete_reasoning,
    )
