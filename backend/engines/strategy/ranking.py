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
    # Eligibility gating – use the deterministic eligibility engine
    from .eligibility import evaluate_eligibility

    # NOTE: GoalSnapshot and FinancialState are not directly available here; they will be passed in by the caller (StrategyEngine) in a later refactor.
    # For now we use placeholder None values – the eligibility engine will treat missing context as "no constraints" and return eligible=True.

    norm_p = priorities.normalized()
    strat_lookup = {s.strategy_id: s for s in strategies}

    scored_items: list[dict] = []

    for scen in scenarios:
        strat = strat_lookup.get(scen.strategy_id)
        if not strat:
            continue

        # Run eligibility check
        eligible, reasons = evaluate_eligibility(strat, None, None)
        if not eligible:
            # Record ineligible item for diagnostics (no scores needed)
            scored_items.append(
                {
                    "strategy_id": strat.strategy_id,
                    "strategy_name": strat.name,
                    "scenario_id": scen.scenario_id,
                    "scenario_name": scen.scenario_name,
                    "is_eligible": False,
                    "ineligible_reasons": reasons,
                }
            )
            continue

        # Gather dimension scores (still kept as evidence but not primary ranking)
        safety = float(scen.metrics.get("safety_score", strat.baseline_safety_score))
        liquidity = float(scen.metrics.get("liquidity_score", strat.baseline_liquidity_score))
        growth = float(scen.metrics.get("growth_score", strat.baseline_growth_score))
        flexibility = float(scen.metrics.get("flexibility_score", strat.baseline_flexibility_score))

        # Build evidence tuple for ranking – order defined by spec
        evidence = {
            "safety": safety,
            "liquidity": liquidity,
            "growth": growth,
            "flexibility": flexibility,
            "funding_gap": scen.metrics.get("funding_gap", 0),
        }

        scored_items.append(
            {
                "strategy_id": strat.strategy_id,
                "strategy_name": strat.name,
                "scenario_id": scen.scenario_id,
                "scenario_name": scen.scenario_name,
                "is_eligible": True,
                "evidence_scores": evidence,
                "dimension_scores": {
                    "safety": safety,
                    "liquidity": liquidity,
                    "growth": growth,
                    "flexibility": flexibility,
                },
            }
        )

    # Separate eligible and ineligible items
    eligible_items = [i for i in scored_items if i.get("is_eligible")]
    ineligible_items = [i for i in scored_items if not i.get("is_eligible")]

    # Sort eligible items: investor priority alignment as primary decision factor,
    # followed by evidence dimensions and lower funding gap.
    def evidence_key(item: dict) -> tuple:
        dim = item["dimension_scores"]
        weighted_score = (
            norm_p.safety * dim.get("safety", 0.0)
            + norm_p.liquidity * dim.get("liquidity", 0.0)
            + norm_p.growth * dim.get("growth", 0.0)
            + norm_p.flexibility * dim.get("flexibility", 0.0)
        )
        ev = item["evidence_scores"]
        return (
            round(weighted_score, 4),
            -ev.get("funding_gap", 0),
        )

    eligible_items.sort(key=evidence_key, reverse=True)

    ranked: list[StrategyRankingItem] = []
    # Add eligible items with ranking
    for idx, item in enumerate(eligible_items, start=1):
        dim = item["dimension_scores"]
        comp = round(
            norm_p.safety * dim.get("safety", 0.0)
            + norm_p.liquidity * dim.get("liquidity", 0.0)
            + norm_p.growth * dim.get("growth", 0.0)
            + norm_p.flexibility * dim.get("flexibility", 0.0),
            4,
        )
        ranked.append(
            StrategyRankingItem(
                rank=idx,
                strategy_id=item["strategy_id"],
                scenario_id=item["scenario_id"],
                strategy_name=item["strategy_name"],
                scenario_name=item["scenario_name"],
                composite_score=comp,
                dimension_scores=item["dimension_scores"],
                is_recommended=(idx == 1),
                evidence_scores=item["evidence_scores"],
                is_eligible=True,
                ineligible_reasons=[],
            )
        )
    # Append ineligible items after eligible ones (no ranking relevance)
    start_rank = len(eligible_items) + 1
    for idx, item in enumerate(ineligible_items, start=start_rank):
        ranked.append(
            StrategyRankingItem(
                rank=idx,
                strategy_id=item["strategy_id"],
                scenario_id=item["scenario_id"],
                strategy_name=item["strategy_name"],
                scenario_name=item["scenario_name"],
                composite_score=0.0,
                dimension_scores={},
                is_recommended=False,
                evidence_scores={},
                is_eligible=False,
                ineligible_reasons=item.get("ineligible_reasons", []),
            )
        )

    return ranked
