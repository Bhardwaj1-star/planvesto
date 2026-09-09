import uuid
from typing import Any
from models.defined_goal import DefinedGoal
from models.strategy import Scenario, StrategyDefinition


def generate_baseline_scenarios(
    strategy: StrategyDefinition,
    defined_goal: DefinedGoal,
) -> list[Scenario]:
    """
    Generates system baseline scenarios for an applicable strategy.
    Scenario = assumptions + funding structure.
    Original baseline scenarios remain immutable.
    """
    scenarios: list[Scenario] = []

    # Baseline 1: Standard Balanced Execution
    assumptions_std = {
        "inflation_rate": defined_goal.inflation_rate,
        "duration_years": defined_goal.duration_years,
        "market_condition": "Normalized Base Case",
    }
    funding_std = {
        param.name: param.default_value for param in strategy.implementation_parameters
    }
    metrics_std = {
        "safety_score": strategy.baseline_safety_score,
        "liquidity_score": strategy.baseline_liquidity_score,
        "growth_score": strategy.baseline_growth_score,
        "flexibility_score": strategy.baseline_flexibility_score,
        "probability_of_success": min(95.0, round(75.0 + (strategy.baseline_safety_score * 2.0), 1)),
        "funding_status_context": defined_goal.funding_status,
        "target_corpus": defined_goal.future_target,
    }

    scenarios.append(
        Scenario(
            scenario_id=f"scen-{strategy.strategy_id}-baseline-standard",
            strategy_id=strategy.strategy_id,
            scenario_type="baseline",
            scenario_name=f"{strategy.name} — Recommended Baseline",
            assumptions=assumptions_std,
            funding_structure=funding_std,
            metrics=metrics_std,
            trade_off_notes=strategy.trade_offs[0] if strategy.trade_offs else "",
            is_investor_modified=False,
        )
    )

    # Baseline 2: Conservative / Stress-Tested Execution
    assumptions_stress = {
        "inflation_rate": round(defined_goal.inflation_rate + 0.015, 4),
        "duration_years": defined_goal.duration_years,
        "market_condition": "Stressed Market (+1.5% Inflation Drag)",
    }
    funding_stress = dict(funding_std)
    # Slightly adjust parameters conservatively if present
    if "debt_allocation_pct" in funding_stress:
        funding_stress["debt_allocation_pct"] = min(100.0, funding_stress["debt_allocation_pct"] + 10.0)
    if "growth_allocation_pct" in funding_stress:
        funding_stress["growth_allocation_pct"] = max(50.0, funding_stress["growth_allocation_pct"] - 10.0)

    metrics_stress = {
        "safety_score": min(10.0, strategy.baseline_safety_score + 0.5),
        "liquidity_score": strategy.baseline_liquidity_score,
        "growth_score": max(1.0, strategy.baseline_growth_score - 1.0),
        "flexibility_score": strategy.baseline_flexibility_score,
        "probability_of_success": min(92.0, round(70.0 + (strategy.baseline_safety_score * 2.0), 1)),
        "funding_status_context": defined_goal.funding_status,
        "target_corpus": defined_goal.future_target,
    }

    scenarios.append(
        Scenario(
            scenario_id=f"scen-{strategy.strategy_id}-baseline-stressed",
            strategy_id=strategy.strategy_id,
            scenario_type="baseline",
            scenario_name=f"{strategy.name} — Conservative Hedged Variant",
            assumptions=assumptions_stress,
            funding_structure=funding_stress,
            metrics=metrics_stress,
            trade_off_notes="Stress-tested against elevated inflation and conservative growth assumptions.",
            is_investor_modified=False,
        )
    )

    return scenarios


def create_custom_scenario(
    strategy: StrategyDefinition,
    defined_goal: DefinedGoal,
    custom_name: str,
    custom_assumptions: dict[str, Any],
    custom_funding: dict[str, Any],
) -> Scenario:
    """
    Creates an investor-customized scenario that participates in the comparison
    while keeping baseline scenarios pristine.
    """
    # Recalculate metrics based on custom inputs
    safety_mod = 0.0
    growth_mod = 0.0
    liquidity_mod = 0.0

    eq_pct = custom_funding.get("equity_allocation_pct") or custom_funding.get("growth_allocation_pct")
    if eq_pct is not None:
        # Higher equity raises growth, lowers safety
        growth_mod = (float(eq_pct) - 60.0) * 0.03
        safety_mod = -(float(eq_pct) - 60.0) * 0.03

    liq_pct = custom_funding.get("instant_liquidity_pct")
    if liq_pct is not None:
        liquidity_mod = (float(liq_pct) - 40.0) * 0.04

    metrics = {
        "safety_score": max(1.0, min(10.0, round(strategy.baseline_safety_score + safety_mod, 2))),
        "liquidity_score": max(1.0, min(10.0, round(strategy.baseline_liquidity_score + liquidity_mod, 2))),
        "growth_score": max(1.0, min(10.0, round(strategy.baseline_growth_score + growth_mod, 2))),
        "flexibility_score": strategy.baseline_flexibility_score,
        "probability_of_success": min(95.0, round(75.0 + ((strategy.baseline_safety_score + safety_mod) * 2.0), 1)),
        "funding_status_context": defined_goal.funding_status,
        "target_corpus": defined_goal.future_target,
    }

    return Scenario(
        scenario_id=f"scen-{strategy.strategy_id}-custom-{uuid.uuid4().hex[:8]}",
        strategy_id=strategy.strategy_id,
        scenario_type="custom",
        scenario_name=custom_name,
        assumptions=custom_assumptions,
        funding_structure=custom_funding,
        metrics=metrics,
        trade_off_notes="Investor-configured custom scenario reflecting specific user parameters.",
        is_investor_modified=True,
    )
