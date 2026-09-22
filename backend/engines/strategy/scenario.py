import uuid
from typing import Any
from engines.goal.funding_gap import calculate_funding_return_assumption, calculate_required_monthly_contribution
from engines.goal.target_calculator import calculate_future_target
from models.defined_goal import DefinedGoal
from models.strategy import Scenario, StrategyDefinition


def _funding_metrics(
    defined_goal: DefinedGoal,
    target: float,
    annual_return: float,
) -> dict[str, float | None]:
    gap = max(0.0, target - defined_goal.projected_mapped_asset_value)
    monthly = calculate_required_monthly_contribution(
        funding_gap=gap,
        annual_return=annual_return,
        duration_years=defined_goal.duration_years,
    )
    return {
        "target_corpus": round(target, 2),
        "funding_gap": round(gap, 2),
        "required_monthly_contribution": monthly,
        "funding_return_assumption": round(annual_return, 6),
        # This is deliberately not called a probability: no return-distribution
        # or Monte Carlo model exists in the current engine.
        "probability_of_success": None,
        "success_probability_method": "not_estimated",
    }


def generate_baseline_scenarios(
    strategy: StrategyDefinition,
    defined_goal: DefinedGoal,
) -> list[Scenario]:
    """
    Generates transparent deterministic baseline scenarios.
    No heuristic probability is presented as a statistical probability.
    """
    mapped = [m.model_dump() for m in defined_goal.mapped_assets]
    funding_return = calculate_funding_return_assumption(mapped)

    standard_metrics = {
        "safety_score": strategy.baseline_safety_score,
        "liquidity_score": strategy.baseline_liquidity_score,
        "growth_score": strategy.baseline_growth_score,
        "flexibility_score": strategy.baseline_flexibility_score,
        "funding_status_context": defined_goal.funding_status,
        **_funding_metrics(defined_goal, defined_goal.future_target, funding_return),
    }

    scenarios: list[Scenario] = [
        Scenario(
            scenario_id=f"scen-{strategy.strategy_id}-baseline-standard",
            strategy_id=strategy.strategy_id,
            scenario_type="baseline",
            scenario_name=f"{strategy.name} — Recommended Baseline",
            assumptions={
                "inflation_rate": defined_goal.inflation_rate,
                "duration_years": defined_goal.duration_years,
                "market_condition": "Normalized Base Case",
            },
            funding_structure={
                param.name: param.default_value for param in strategy.implementation_parameters
            },
            metrics=standard_metrics,
            trade_off_notes=strategy.trade_offs[0] if strategy.trade_offs else "",
            is_investor_modified=False,
        )
    ]

    stress_inflation = min(1.0, defined_goal.inflation_rate + 0.015)
    stress_target = calculate_future_target(
        today_cost=defined_goal.today_cost,
        inflation_rate=stress_inflation,
        duration_years=defined_goal.duration_years,
    )
    stress_metrics = {
        "safety_score": min(10.0, strategy.baseline_safety_score + 0.5),
        "liquidity_score": strategy.baseline_liquidity_score,
        "growth_score": max(1.0, strategy.baseline_growth_score - 1.0),
        "flexibility_score": strategy.baseline_flexibility_score,
        "funding_status_context": defined_goal.funding_status,
        **_funding_metrics(defined_goal, stress_target, funding_return),
    }

    funding_stress = {
        param.name: param.default_value for param in strategy.implementation_parameters
    }
    if "debt_allocation_pct" in funding_stress:
        funding_stress["debt_allocation_pct"] = min(100.0, funding_stress["debt_allocation_pct"] + 10.0)
    if "growth_allocation_pct" in funding_stress:
        funding_stress["growth_allocation_pct"] = max(50.0, funding_stress["growth_allocation_pct"] - 10.0)

    scenarios.append(
        Scenario(
            scenario_id=f"scen-{strategy.strategy_id}-baseline-stressed",
            strategy_id=strategy.strategy_id,
            scenario_type="baseline",
            scenario_name=f"{strategy.name} — Conservative Hedged Variant",
            assumptions={
                "inflation_rate": stress_inflation,
                "duration_years": defined_goal.duration_years,
                "market_condition": "Stressed Market (+1.5% Inflation Drag)",
            },
            funding_structure=funding_stress,
            metrics=stress_metrics,
            trade_off_notes="Stress-tested against elevated inflation; funding requirement is recalculated.",
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
    safety_mod = 0.0
    growth_mod = 0.0
    liquidity_mod = 0.0

    eq_pct = custom_funding.get("equity_allocation_pct") or custom_funding.get("growth_allocation_pct")
    if eq_pct is not None:
        growth_mod = (float(eq_pct) - 60.0) * 0.03
        safety_mod = -(float(eq_pct) - 60.0) * 0.03

    liq_pct = custom_funding.get("instant_liquidity_pct")
    if liq_pct is not None:
        liquidity_mod = (float(liq_pct) - 40.0) * 0.04

    custom_inflation = float(custom_assumptions.get("inflation_rate", defined_goal.inflation_rate))
    custom_inflation = min(1.0, max(0.0, custom_inflation))
    custom_target = calculate_future_target(
        today_cost=defined_goal.today_cost,
        inflation_rate=custom_inflation,
        duration_years=defined_goal.duration_years,
    )
    funding_return = calculate_funding_return_assumption(
        [m.model_dump() for m in defined_goal.mapped_assets]
    )

    metrics = {
        "safety_score": max(1.0, min(10.0, round(strategy.baseline_safety_score + safety_mod, 2))),
        "liquidity_score": max(1.0, min(10.0, round(strategy.baseline_liquidity_score + liquidity_mod, 2))),
        "growth_score": max(1.0, min(10.0, round(strategy.baseline_growth_score + growth_mod, 2))),
        "flexibility_score": strategy.baseline_flexibility_score,
        "funding_status_context": defined_goal.funding_status,
        **_funding_metrics(defined_goal, custom_target, funding_return),
    }

    return Scenario(
        scenario_id=f"scen-{strategy.strategy_id}-custom-{uuid.uuid4().hex[:8]}",
        strategy_id=strategy.strategy_id,
        scenario_type="custom",
        scenario_name=custom_name,
        assumptions=custom_assumptions,
        funding_structure=custom_funding,
        metrics=metrics,
        trade_off_notes="Investor-configured custom scenario with deterministic funding calculations.",
        is_investor_modified=True,
    )
