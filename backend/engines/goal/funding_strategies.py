from typing import Any

from engines.calculation.engine import round_money


def _future_value_lumpsum(amount: float, annual_return: float, years: float) -> float:
    return max(0.0, float(amount)) * ((1.0 + float(annual_return)) ** max(0.0, float(years)))


def _future_value_growing_monthly(
    monthly_contribution: float,
    annual_step_up: float,
    annual_return: float,
    years: float,
) -> float:
    """Future value of a monthly contribution growing once per year."""
    months = max(0, round(float(years) * 12))
    if months <= 0 or monthly_contribution <= 0:
        return 0.0

    monthly_rate = float(annual_return) / 12.0
    growth = max(0.0, float(annual_step_up))
    total = 0.0
    for month in range(months):
        contribution = monthly_contribution * ((1.0 + growth) ** (month // 12))
        periods = months - month - 1
        total += contribution * ((1.0 + monthly_rate) ** periods)
    return total


def _solve_step_up_for_target(
    target: float,
    starting_monthly: float,
    annual_return: float,
    years: float,
    max_step_up: float = 1.0,
) -> float | None:
    if target <= 0:
        return 0.0
    if starting_monthly <= 0 or years <= 0:
        return None
    if _future_value_growing_monthly(starting_monthly, max_step_up, annual_return, years) < target:
        return None

    low, high = 0.0, max_step_up
    for _ in range(60):
        mid = (low + high) / 2.0
        if _future_value_growing_monthly(starting_monthly, mid, annual_return, years) >= target:
            high = mid
        else:
            low = mid
    return high


def build_goal_funding_strategies(
    funding_gap: float,
    annual_return: float,
    duration_years: float,
    available_monthly_surplus: float | None,
) -> list[dict[str, Any]]:
    """Build deterministic funding architectures for the Goal Feasibility layer.

    Existing mapped assets are already reflected in funding_gap. These strategies
    describe the additional funding required from this point onward.
    """
    gap = max(0.0, float(funding_gap))
    years = max(0.0, float(duration_years))
    surplus = max(0.0, float(available_monthly_surplus or 0.0))
    result: list[dict[str, Any]] = []

    if gap <= 0:
        return [{
            "strategy_id": "existing_assets",
            "strategy_name": "Existing Assets",
            "strategy_type": "existing_asset_funding",
            "status": "feasible",
            "required_lumpsum": 0.0,
            "required_monthly_contribution": 0.0,
            "starting_monthly_contribution": 0.0,
            "annual_step_up": 0.0,
            "remaining_gap": 0.0,
            "reason": "Existing mapped assets already cover the target-date funding requirement.",
        }]

    if years <= 0:
        lumpsum = round_money(gap)
        return [{
            "strategy_id": "lumpsum",
            "strategy_name": "Lumpsum",
            "strategy_type": "lumpsum",
            "status": "requires_upfront_capital",
            "required_lumpsum": lumpsum,
            "required_monthly_contribution": 0.0,
            "starting_monthly_contribution": 0.0,
            "annual_step_up": 0.0,
            "remaining_gap": 0.0,
            "reason": "The target date is immediate, so a future monthly contribution is not applicable.",
        }]

    monthly_rate = float(annual_return) / 12.0
    if abs(monthly_rate) < 1e-12:
        annuity_factor = years * 12.0
    else:
        months = max(1, round(years * 12))
        annuity_factor = ((1.0 + monthly_rate) ** months - 1.0) / monthly_rate

    required_sip = gap / annuity_factor
    required_lumpsum = gap / ((1.0 + float(annual_return)) ** years)
    sip_fit = required_sip <= surplus + 0.01

    result.append({
        "strategy_id": "sip",
        "strategy_name": "SIP",
        "strategy_type": "sip",
        "status": "feasible" if sip_fit else "constrained",
        "required_lumpsum": 0.0,
        "required_monthly_contribution": round_money(required_sip),
        "starting_monthly_contribution": round_money(required_sip),
        "annual_step_up": 0.0,
        "remaining_gap": 0.0,
        "reason": "Required SIP fits current monthly surplus." if sip_fit else "Required SIP exceeds current monthly surplus.",
    })

    result.append({
        "strategy_id": "lumpsum",
        "strategy_name": "Lumpsum",
        "strategy_type": "lumpsum",
        "status": "feasible" if required_lumpsum <= 0 else "requires_upfront_capital",
        "required_lumpsum": round_money(required_lumpsum),
        "required_monthly_contribution": 0.0,
        "starting_monthly_contribution": 0.0,
        "annual_step_up": 0.0,
        "remaining_gap": 0.0,
        "reason": "Fund the remaining goal gap upfront today.",
    })

    # Lumpsum + SIP: use all currently available surplus for the recurring leg.
    sip_future = _future_value_growing_monthly(surplus, 0.0, annual_return, years)
    residual_after_sip = max(0.0, gap - sip_future)
    mixed_lumpsum = residual_after_sip / ((1.0 + float(annual_return)) ** years)
    result.append({
        "strategy_id": "lumpsum_plus_sip",
        "strategy_name": "Lumpsum + SIP",
        "strategy_type": "hybrid_funding",
        "status": "feasible" if residual_after_sip <= 0.01 else "requires_upfront_capital",
        "required_lumpsum": round_money(mixed_lumpsum),
        "required_monthly_contribution": round_money(surplus),
        "starting_monthly_contribution": round_money(surplus),
        "annual_step_up": 0.0,
        "remaining_gap": round_money(residual_after_sip),
        "reason": "Uses the available monthly surplus first and funds the remaining gap upfront." if residual_after_sip > 0.01 else "Available monthly surplus is sufficient when combined with the upfront amount shown.",
    })

    step_up = _solve_step_up_for_target(gap, surplus, annual_return, years)
    result.append({
        "strategy_id": "step_up_sip",
        "strategy_name": "Step-up SIP",
        "strategy_type": "step_up_sip",
        "status": "feasible" if step_up is not None else "constrained",
        "required_lumpsum": 0.0,
        "required_monthly_contribution": round_money(required_sip),
        "starting_monthly_contribution": round_money(min(required_sip, surplus)) if surplus > 0 else 0.0,
        "annual_step_up": round(step_up, 6) if step_up is not None else None,
        "remaining_gap": 0.0 if step_up is not None else round_money(gap),
        "reason": "Starts within current surplus and increases the contribution annually." if step_up is not None else "Even a 100% annual step-up from the current surplus does not close the gap within the goal horizon.",
    })

    return result
