from models.strategy import InvestorPriorities, Scenario, StrategyDefinition, StrategyRankingItem


def rank_scenarios(
    strategies: list[StrategyDefinition],
    scenarios: list[Scenario],
    priorities: InvestorPriorities,
) -> list[StrategyRankingItem]:
    """
    Hybrid ranking engine:
    Composite Score = sum(Normalized Weight(d) * Dimension Score(s, d))
    Investor priority weights dynamically influence the ranking.
    """
    norm_p = priorities.normalized()
    strat_lookup = {s.strategy_id: s for s in strategies}

    scored_items: list[dict] = []

    for scen in scenarios:
        strat = strat_lookup.get(scen.strategy_id)
        if not strat:
            continue

        safety = float(scen.metrics.get("safety_score", strat.baseline_safety_score))
        liquidity = float(scen.metrics.get("liquidity_score", strat.baseline_liquidity_score))
        growth = float(scen.metrics.get("growth_score", strat.baseline_growth_score))
        flexibility = float(scen.metrics.get("flexibility_score", strat.baseline_flexibility_score))

        composite = (
            (norm_p.safety * safety)
            + (norm_p.liquidity * liquidity)
            + (norm_p.growth * growth)
            + (norm_p.flexibility * flexibility)
        )
        composite = round(composite, 2)

        scored_items.append(
            {
                "strategy_id": strat.strategy_id,
                "strategy_name": strat.name,
                "scenario_id": scen.scenario_id,
                "scenario_name": scen.scenario_name,
                "composite_score": composite,
                "dimension_scores": {
                    "safety": safety,
                    "liquidity": liquidity,
                    "growth": growth,
                    "flexibility": flexibility,
                },
            }
        )

    # Sort descending by composite score, then by safety as tie-breaker
    scored_items.sort(key=lambda x: (x["composite_score"], x["dimension_scores"]["safety"]), reverse=True)

    ranked: list[StrategyRankingItem] = []
    for idx, item in enumerate(scored_items, start=1):
        ranked.append(
            StrategyRankingItem(
                rank=idx,
                strategy_id=item["strategy_id"],
                scenario_id=item["scenario_id"],
                strategy_name=item["strategy_name"],
                scenario_name=item["scenario_name"],
                composite_score=item["composite_score"],
                dimension_scores=item["dimension_scores"],
                is_recommended=(idx == 1),
            )
        )

    return ranked
