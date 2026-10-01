import uuid
from typing import Any

from engines.goal.funding_gap import (
    calculate_funding_return_assumption,
    calculate_required_monthly_contribution,
)
from engines.goal.target_calculator import calculate_future_target
from engines.goal.funding_strategies import build_goal_funding_strategies
from models.defined_goal import DefinedGoal
from models.strategy import Scenario, StrategyDefinition


def _future_value_monthly_contribution(
    monthly_contribution: float,
    annual_return: float,
    duration_years: float,
) -> float:
    months = max(0, round(float(duration_years) * 12))
    if months == 0 or monthly_contribution <= 0:
        return 0.0
    monthly_rate = float(annual_return) / 12.0
    if abs(monthly_rate) < 1e-12:
        return round(monthly_contribution * months, 2)
    factor = ((1.0 + monthly_rate) ** months - 1.0) / monthly_rate
    return round(monthly_contribution * factor, 2)


def _future_value_lumpsum(
    lumpsum: float,
    annual_return: float,
    duration_years: float,
) -> float:
    if lumpsum <= 0 or duration_years <= 0:
        return 0.0
    return round(lumpsum * ((1.0 + annual_return) ** duration_years), 2)


def _future_value_step_up(
    starting_monthly: float,
    annual_step_up: float,
    annual_return: float,
    duration_years: float,
) -> float:
    years = max(0, round(float(duration_years)))
    if years <= 0 or starting_monthly <= 0:
        return 0.0
    total = 0.0
    for year in range(years):
        monthly = starting_monthly * ((1.0 + annual_step_up) ** year)
        total += _future_value_monthly_contribution(
            monthly,
            annual_return,
            1.0,
        ) * ((1.0 + annual_return) ** (years - year - 1))
    return round(total, 2)


def _funding_metrics(
    defined_goal: DefinedGoal,
    target: float,
    annual_return: float,
    duration_years: float | None = None,
    additional_monthly_contribution: float = 0.0,
    additional_lumpsum: float = 0.0,
    annual_step_up: float = 0.0,
    base_resources: float | None = None,
) -> dict[str, float | None | str]:
    years = defined_goal.duration_years if duration_years is None else max(0.0, duration_years)
    base_resources = (
        max(0.0, float(defined_goal.projected_mapped_asset_value))
        if base_resources is None
        else max(0.0, float(base_resources))
    )
    base_contribution = max(0.0, float(defined_goal.required_monthly_contribution or 0.0))

    contribution_fv = _future_value_monthly_contribution(
        base_contribution + max(0.0, additional_monthly_contribution),
        annual_return,
        years,
    )
    step_up_fv = (
        _future_value_step_up(
            base_contribution + max(0.0, additional_monthly_contribution),
            annual_step_up,
            annual_return,
            years,
        )
        if annual_step_up > 0
        else 0.0
    )
    lumpsum_fv = _future_value_lumpsum(additional_lumpsum, annual_return, years)

    # Existing mapped resources are already projected by Goal Engine. To avoid
    # double-counting them, only incremental contributions/lumpsum are added here.
    # Required contribution is not part of projected mapped assets. Therefore
    # the scenario's full contribution stream is incremental funding.
    incremental_funding = max(
        0.0,
        contribution_fv if annual_step_up <= 0 else step_up_fv,
    )
    projected_total = base_resources + incremental_funding + lumpsum_fv
    remaining_gap = round(float(target) - projected_total, 2)
    return {
        "target_corpus": round(float(target), 2),
        "projected_total_resources": round(projected_total, 2),
        "funding_gap": max(0.0, remaining_gap),
        "remaining_gap": remaining_gap,
        "required_monthly_contribution": calculate_required_monthly_contribution(
            max(0.0, float(target) - base_resources),
            annual_return,
            years,
        ),
        "additional_monthly_contribution": round(max(0.0, additional_monthly_contribution), 2),
        "additional_lumpsum": round(max(0.0, additional_lumpsum), 2),
        "annual_step_up": round(max(0.0, annual_step_up), 6),
        "duration_years": round(years, 2),
        "funding_return_assumption": round(annual_return, 6),
        "probability_of_success": None,
        "success_probability_method": "not_estimated",
    }


def generate_baseline_scenarios(
    strategy: StrategyDefinition,
    defined_goal: DefinedGoal,
) -> list[Scenario]:
    """Generate transparent deterministic baseline scenarios."""
    mapped = [m.model_dump() for m in defined_goal.mapped_assets]
    funding_return = calculate_funding_return_assumption(mapped)

    if strategy.strategy_id == "strat-goal-funding":
        variants = build_goal_funding_strategies(
            funding_gap=defined_goal.funding_gap,
            annual_return=funding_return,
            duration_years=defined_goal.duration_years,
            available_monthly_surplus=defined_goal.available_monthly_surplus,
        )
        return [
            Scenario(
                scenario_id=f"scen-{strategy.strategy_id}-{variant['strategy_id']}",
                strategy_id=strategy.strategy_id,
                funding_strategy_id=variant["strategy_id"],
                scenario_type="baseline",
                scenario_name=f"{strategy.name} — {variant['strategy_name']}",
                assumptions={
                    "inflation_rate": defined_goal.inflation_rate,
                    "duration_years": defined_goal.duration_years,
                    "market_condition": "Normalized Base Case",
                },
                funding_structure=variant,
                metrics={
                    "safety_score": strategy.baseline_safety_score,
                    "liquidity_score": strategy.baseline_liquidity_score,
                    "growth_score": strategy.baseline_growth_score,
                    "flexibility_score": strategy.baseline_flexibility_score,
                    "funding_status_context": defined_goal.funding_status,
                    "funding_strategy_status": variant.get("status"),
                    "funding_gap": variant.get("remaining_gap", defined_goal.funding_gap),
                    "required_monthly_contribution": variant.get("required_monthly_contribution", 0.0),
                    "required_lumpsum": variant.get("required_lumpsum", 0.0),
                    "starting_monthly_contribution": variant.get("starting_monthly_contribution", 0.0),
                    "annual_step_up": variant.get("annual_step_up", 0.0),
                    "funding_return_assumption": round(funding_return, 6),
                    "probability_of_success": None,
                    "success_probability_method": "not_estimated",
                },
                trade_off_notes=variant.get("reason", ""),
                is_investor_modified=False,
            )
            for variant in variants
        ]

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
            funding_structure={
                param.name: param.default_value for param in strategy.implementation_parameters
            },
            metrics={
                "safety_score": min(10.0, strategy.baseline_safety_score + 0.5),
                "liquidity_score": strategy.baseline_liquidity_score,
                "growth_score": max(1.0, strategy.baseline_growth_score - 1.0),
                "flexibility_score": strategy.baseline_flexibility_score,
                "funding_status_context": defined_goal.funding_status,
                **_funding_metrics(defined_goal, stress_target, funding_return),
            },
            trade_off_notes="Stress-tested against elevated inflation; funding requirement is recalculated.",
            is_investor_modified=False,
        )
    )
    return scenarios


def generate_what_if_scenarios(
    strategy: StrategyDefinition,
    defined_goal: DefinedGoal,
) -> list[Scenario]:
    """Generate transparent sensitivity scenarios for decision reports.

    These are exploratory what-ifs, not recommendations. Each scenario changes
    one planning variable at a time and records the resulting deterministic
    funding consequence.
    """
    mapped = [m.model_dump() for m in defined_goal.mapped_assets]
    funding_return = calculate_funding_return_assumption(mapped)
    base_target = float(defined_goal.future_target)
    base_years = float(defined_goal.duration_years)

    scenarios: list[Scenario] = []

    # 1. Contribution sensitivity.
    for pct in (0.10, 0.25, 0.50):
        extra = max(0.0, float(defined_goal.required_monthly_contribution or 0.0)) * pct
        metrics = _funding_metrics(
            defined_goal,
            base_target,
            funding_return,
            additional_monthly_contribution=extra,
        )
        scenarios.append(
            Scenario(
                scenario_id=f"scen-{strategy.strategy_id}-whatif-contribution-{int(pct*100)}",
                strategy_id=strategy.strategy_id,
                scenario_type="custom",
                scenario_name=f"What-if: Monthly contribution +{int(pct*100)}%",
                assumptions={"duration_years": base_years, "change_type": "monthly_contribution"},
                funding_structure={"additional_monthly_contribution": extra},
                metrics=metrics,
                trade_off_notes="Higher current cash-flow commitment in exchange for a lower remaining funding gap.",
                is_investor_modified=False,
            )
        )

    # 2. Goal-date sensitivity. Existing mapped assets are reprojected to the
    # new horizon rather than reusing the original target-date projection.
    current_mapped_value = sum(
        max(0.0, float(item.get("allocated_amount", 0.0)))
        for item in mapped
    )
    def projected_mapped_at(years: float) -> float:
        if current_mapped_value <= 0:
            return 0.0
        projected = 0.0
        for item in mapped:
            amount = max(0.0, float(item.get("allocated_amount", 0.0)))
            expected = float(item.get("expected_return", funding_return))
            projected += amount * ((1.0 + expected) ** years)
        return round(projected, 2)

    # 2. Goal-date sensitivity.
    for extra_years in (1.0, 3.0):
        years = base_years + extra_years
        target = calculate_future_target(
            today_cost=defined_goal.today_cost,
            inflation_rate=defined_goal.inflation_rate,
            duration_years=years,
        )
        metrics = _funding_metrics(
            defined_goal,
            target,
            funding_return,
            duration_years=years,
            base_resources=projected_mapped_at(years),
        )
        scenarios.append(
            Scenario(
                scenario_id=f"scen-{strategy.strategy_id}-whatif-date-plus-{int(extra_years)}",
                strategy_id=strategy.strategy_id,
                scenario_type="custom",
                scenario_name=f"What-if: Goal date +{int(extra_years)} year(s)",
                assumptions={
                    "duration_years": years,
                    "change_type": "goal_horizon",
                    "inflation_rate": defined_goal.inflation_rate,
                },
                funding_structure={"additional_years": extra_years},
                metrics=metrics,
                trade_off_notes="Extending the horizon changes both the inflation-adjusted target and the time available to fund it.",
                is_investor_modified=False,
            )
        )

    # 3. Target sensitivity.
    for reduction in (0.10, 0.20):
        target = base_target * (1.0 - reduction)
        metrics = _funding_metrics(
            defined_goal,
            target,
            funding_return,
            duration_years=base_years,
        )
        scenarios.append(
            Scenario(
                scenario_id=f"scen-{strategy.strategy_id}-whatif-target-minus-{int(reduction*100)}",
                strategy_id=strategy.strategy_id,
                scenario_type="custom",
                scenario_name=f"What-if: Target reduced by {int(reduction*100)}%",
                assumptions={"duration_years": base_years, "change_type": "target_amount"},
                funding_structure={"target_reduction_pct": reduction},
                metrics=metrics,
                trade_off_notes="Lower target reduces the funding requirement but changes the defined goal outcome.",
                is_investor_modified=False,
            )
        )

    # 4. Step-up sensitivity.
    for step_up in (0.10, 0.20):
        metrics = _funding_metrics(
            defined_goal,
            base_target,
            funding_return,
            duration_years=base_years,
            annual_step_up=step_up,
        )
        scenarios.append(
            Scenario(
                scenario_id=f"scen-{strategy.strategy_id}-whatif-stepup-{int(step_up*100)}",
                strategy_id=strategy.strategy_id,
                scenario_type="custom",
                scenario_name=f"What-if: Annual contribution step-up {int(step_up*100)}%",
                assumptions={"duration_years": base_years, "change_type": "annual_step_up"},
                funding_structure={"annual_step_up": step_up},
                metrics=metrics,
                trade_off_notes="Starts with the current contribution requirement and increases it annually; future cash-flow burden rises over time.",
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
