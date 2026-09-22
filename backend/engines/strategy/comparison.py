from typing import Any
from models.strategy import Scenario, StrategyDefinition


def build_comparison_matrix(
    strategies: list[StrategyDefinition],
    scenarios: list[Scenario],
) -> dict[str, Any]:
    """
    Constructs a structured side-by-side comparison matrix. Statistical
    probability is only shown when a scenario supplies a real probability
    model; the current engine explicitly reports it as unavailable.
    """
    strat_lookup = {s.strategy_id: s for s in strategies}
    comparison_items: list[dict[str, Any]] = []

    for scen in scenarios:
        strat = strat_lookup.get(scen.strategy_id)
        if not strat:
            continue

        comparison_items.append(
            {
                "strategy_id": strat.strategy_id,
                "strategy_name": strat.name,
                "scenario_id": scen.scenario_id,
                "scenario_name": scen.scenario_name,
                "scenario_type": scen.scenario_type,
                "metrics": {
                    "safety": scen.metrics.get("safety_score", strat.baseline_safety_score),
                    "liquidity": scen.metrics.get("liquidity_score", strat.baseline_liquidity_score),
                    "growth": scen.metrics.get("growth_score", strat.baseline_growth_score),
                    "flexibility": scen.metrics.get("flexibility_score", strat.baseline_flexibility_score),
                    "probability_of_success": scen.metrics.get("probability_of_success"),
                    "success_probability_method": scen.metrics.get("success_probability_method", "not_estimated"),
                    "funding_gap": scen.metrics.get("funding_gap"),
                    "required_monthly_contribution": scen.metrics.get("required_monthly_contribution"),
                    "funding_return_assumption": scen.metrics.get("funding_return_assumption"),
                },
                "assumptions": scen.assumptions,
                "funding_structure": scen.funding_structure,
                "good_outcomes": strat.good_outcomes,
                "bad_outcomes": strat.bad_outcomes,
                "trade_offs": strat.trade_offs,
                "scenario_trade_off_notes": scen.trade_off_notes,
            }
        )

    return {
        "dimensions": ["safety", "liquidity", "growth", "flexibility"],
        "scenario_count": len(scenarios),
        "items": comparison_items,
    }
