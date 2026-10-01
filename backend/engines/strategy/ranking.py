"""
Strategy Ranking Engine
=======================
Ranks strategy scenarios using the authoritative DecisionResult.
Composite/dimension scores remain descriptive evidence only.
"""

from typing import Any
from models.defined_goal import DefinedGoal
from models.strategy import (
    InvestorPriorities,
    Scenario,
    StrategyArchitecture,
    StrategyDefinition,
    StrategyRankingItem,
)
from engines.strategy.decision import DecisionResult, evaluate_decision
from engines.strategy.eligibility import evaluate_eligibility
from engines.constraints.models import ConstraintSet


def rank_scenarios(
    strategies: list[StrategyDefinition],
    scenarios: list[Scenario],
    priorities: InvestorPriorities | None = None,
    decision_result: DecisionResult | None = None,
    defined_goal: DefinedGoal | None = None,
    financial_context: dict | None = None,
    architectures: list[StrategyArchitecture] | None = None,
    constraint_set: ConstraintSet | None = None,
) -> list[StrategyRankingItem]:
    if not strategies or not scenarios:
        return []

    if decision_result is None and defined_goal is not None and architectures is not None:
        decision_result = evaluate_decision(
            strategies=strategies,
            scenarios=scenarios,
            architectures=architectures,
            defined_goal=defined_goal,
            financial_context=financial_context,
            priorities=priorities,
            constraint_set=constraint_set,
        )

    norm_p = priorities.normalized() if priorities else InvestorPriorities().normalized()
    strat_lookup = {s.strategy_id: s for s in strategies}

    decision_order: dict[str, int] = {}
    recommended_strat_id = ""
    recommended_scen_id = ""
    alternative_ids: set[str] = set()
    if decision_result:
        recommended_strat_id = decision_result.recommended_strategy_id
        recommended_scen_id = decision_result.recommended_scenario_id
        alternative_ids = {a.primary_strategy_id for a in decision_result.alternative_architectures}
        for rank_idx, s_id in enumerate(decision_result.ordered_strategy_ids):
            decision_order[s_id] = rank_idx

    scored_items: list[dict[str, Any]] = []
    for scen in scenarios:
        strat = strat_lookup.get(scen.strategy_id)
        if not strat:
            continue

        eligible, reasons = evaluate_eligibility(
            strat,
            defined_goal,
            financial_context=financial_context,
            constraint_set=constraint_set,
        )
        if not eligible:
            scored_items.append({
                "strategy_id": strat.strategy_id,
                "strategy_name": strat.name,
                "scenario_id": scen.scenario_id,
                "scenario_name": scen.scenario_name,
                "is_eligible": False,
                "ineligible_reasons": reasons,
                "decision_rank": 9999,
                "dimension_scores": {},
                "evidence_scores": {},
                "composite_score": 0.0,
            })
            continue

        safety = float(scen.metrics.get("safety_score", strat.baseline_safety_score))
        liquidity = float(scen.metrics.get("liquidity_score", strat.baseline_liquidity_score))
        growth = float(scen.metrics.get("growth_score", strat.baseline_growth_score))
        flexibility = float(scen.metrics.get("flexibility_score", strat.baseline_flexibility_score))
        comp = round(
            norm_p.safety * safety
            + norm_p.liquidity * liquidity
            + norm_p.growth * growth
            + norm_p.flexibility * flexibility,
            4,
        )
        scored_items.append({
            "strategy_id": strat.strategy_id,
            "strategy_name": strat.name,
            "scenario_id": scen.scenario_id,
            "scenario_name": scen.scenario_name,
            "is_eligible": True,
            "ineligible_reasons": [],
            "decision_rank": decision_order.get(strat.strategy_id, 500),
            "dimension_scores": {
                "safety": safety,
                "liquidity": liquidity,
                "growth": growth,
                "flexibility": flexibility,
            },
            "evidence_scores": {
                "safety": safety,
                "liquidity": liquidity,
                "growth": growth,
                "flexibility": flexibility,
                "funding_gap": scen.metrics.get("funding_gap", 0),
            },
            "composite_score": comp,
        })

    eligible_items = [i for i in scored_items if i["is_eligible"]]
    ineligible_items = [i for i in scored_items if not i["is_eligible"]]
    eligible_items.sort(key=lambda item: (
        item["decision_rank"],
        0 if ("standard" in item["scenario_id"] or "Recommended Baseline" in item["scenario_name"]) else 1,
        item["strategy_id"],
        item["scenario_id"],
    ))

    ranked: list[StrategyRankingItem] = []
    for idx, item in enumerate(eligible_items, start=1):
        is_rec = (
            item["scenario_id"] == recommended_scen_id
            if recommended_scen_id
            else item["strategy_id"] == recommended_strat_id
        )
        ranked.append(StrategyRankingItem(
            rank=idx,
            strategy_id=item["strategy_id"],
            scenario_id=item["scenario_id"],
            strategy_name=item["strategy_name"],
            scenario_name=item["scenario_name"],
            composite_score=item["composite_score"],
            dimension_scores=item["dimension_scores"],
            is_recommended=is_rec,
            evidence_scores={**item["evidence_scores"], "is_alternative": item["strategy_id"] in alternative_ids},
            is_eligible=True,
            ineligible_reasons=[],
        ))

    start_rank = len(eligible_items) + 1
    for idx, item in enumerate(ineligible_items, start=start_rank):
        ranked.append(StrategyRankingItem(
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
            ineligible_reasons=item["ineligible_reasons"],
        ))

    return ranked
