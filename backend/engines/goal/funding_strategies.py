from typing import Any

from engines.calculation.engine import round_money


# Goal Feasibility funding methods are owned by Goal Planner. They are not
# Strategy Library entries and do not imply an investor-selected strategy.
_METHODS = {
    "existing_assets": ("Existing mapped assets", "existing_assets", "Uses the goal assets already mapped and projected in Chapter 10."),
    "sip": ("SIP", "recurring_contribution", "Funds the remaining requirement through recurring monthly contributions."),
    "lumpsum": ("Lump Sum", "upfront_capital", "Funds the remaining requirement through an upfront contribution."),
    "lumpsum_plus_sip": ("Lump Sum + SIP", "combined_funding", "Combines an upfront amount with recurring monthly contributions."),
    "step_up_sip": ("Step-Up SIP", "recurring_contribution", "Increases the monthly contribution on the supplied annual step-up schedule."),
    "lumpsum_plus_step_up_sip": ("Lump Sum + Step-Up SIP", "combined_funding", "Combines upfront capital with a stepped recurring contribution."),
}


def _method(method_id: str) -> dict[str, str]:
    name, method_type, description = _METHODS[method_id]
    return {"method_id": method_id, "method_name": name, "method_type": method_type, "description": description}


def _finalize(options: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for option in options:
        option["constraints"] = [] if option["status"] == "feasible" else [option["reason"]]
    return options


def _future_value_growing_monthly(monthly: float, step_up: float, annual_return: float, years: float) -> float:
    months = max(0, round(float(years) * 12))
    if months <= 0 or monthly <= 0:
        return 0.0
    monthly_rate = float(annual_return) / 12.0
    total = 0.0
    for month in range(months):
        contribution = monthly * ((1.0 + max(0.0, step_up)) ** (month // 12))
        total += contribution * ((1.0 + monthly_rate) ** (months - month - 1))
    return total


def _solve_step_up(target: float, starting_monthly: float, annual_return: float, years: float) -> float | None:
    if target <= 0:
        return 0.0
    if starting_monthly <= 0 or years <= 0:
        return None
    if _future_value_growing_monthly(starting_monthly, 1.0, annual_return, years) < target:
        return None
    low, high = 0.0, 1.0
    for _ in range(60):
        mid = (low + high) / 2.0
        if _future_value_growing_monthly(starting_monthly, mid, annual_return, years) >= target:
            high = mid
        else:
            low = mid
    return high


def build_goal_funding_options(
    funding_gap: float,
    annual_return: float,
    duration_years: float,
    available_monthly_surplus: float | None,
) -> list[dict[str, Any]]:
    """Evaluate Chapter 10 funding methods; never selects or recommends a path."""
    gap = max(0.0, float(funding_gap))
    years = max(0.0, float(duration_years))
    surplus = max(0.0, float(available_monthly_surplus or 0.0))
    if gap <= 0:
        return _finalize([{
            **_method("existing_assets"), "status": "feasible",
            "required_lumpsum": 0.0, "required_monthly_contribution": 0.0,
            "starting_monthly_contribution": 0.0, "annual_step_up": 0.0,
            "remaining_gap": 0.0,
            "reason": "Existing mapped assets already cover the target-date requirement.",
        }])
    if years <= 0:
        return _finalize([{
            **_method("lumpsum"), "status": "requires_upfront_capital",
            "required_lumpsum": round_money(gap), "required_monthly_contribution": 0.0,
            "starting_monthly_contribution": 0.0, "annual_step_up": 0.0,
            "remaining_gap": 0.0,
            "reason": "The target date is immediate; a future monthly contribution is not applicable.",
        }])

    monthly_rate = float(annual_return) / 12.0
    months = max(1, round(years * 12))
    annuity_factor = float(months) if abs(monthly_rate) < 1e-12 else ((1 + monthly_rate) ** months - 1) / monthly_rate
    required_sip = gap / annuity_factor
    required_lumpsum = gap / ((1.0 + float(annual_return)) ** years)
    sip_future = _future_value_growing_monthly(surplus, 0.0, annual_return, years)
    sip_fits = required_sip <= surplus + 0.01

    options = [
        {**_method("sip"), "status": "feasible" if sip_fits else "constrained",
         "required_lumpsum": 0.0, "required_monthly_contribution": round_money(required_sip),
         "starting_monthly_contribution": round_money(required_sip), "annual_step_up": 0.0,
         "remaining_gap": round_money(max(0.0, gap - sip_future)),
         "reason": "Required SIP fits current monthly surplus." if sip_fits else "Required SIP exceeds current monthly surplus."},
        {**_method("lumpsum"), "status": "requires_upfront_capital",
         "required_lumpsum": round_money(required_lumpsum), "required_monthly_contribution": 0.0,
         "starting_monthly_contribution": 0.0, "annual_step_up": 0.0, "remaining_gap": 0.0,
         "reason": "Funds the remaining goal gap upfront today."},
    ]

    residual = max(0.0, gap - sip_future)
    mixed_lumpsum = residual / ((1.0 + float(annual_return)) ** years)
    options.append({**_method("lumpsum_plus_sip"), "status": "feasible" if residual <= 0.01 else "requires_upfront_capital",
        "required_lumpsum": round_money(mixed_lumpsum), "required_monthly_contribution": round_money(surplus),
        "starting_monthly_contribution": round_money(surplus), "annual_step_up": 0.0,
        "remaining_gap": round_money(residual),
        "reason": "Combines available monthly surplus with the upfront amount shown."})

    step_up = _solve_step_up(gap, surplus, annual_return, years)
    step_up_value = _future_value_growing_monthly(surplus, step_up if step_up is not None else 1.0, annual_return, years)
    step_residual = max(0.0, gap - step_up_value)
    step_lumpsum = step_residual / ((1.0 + float(annual_return)) ** years)
    options.append({**_method("step_up_sip"), "status": "feasible" if step_up is not None else "constrained",
        "required_lumpsum": 0.0, "required_monthly_contribution": round_money(required_sip),
        "starting_monthly_contribution": round_money(min(required_sip, surplus)) if surplus > 0 else 0.0,
        "annual_step_up": round(step_up, 6) if step_up is not None else None,
        "remaining_gap": 0.0 if step_up is not None else round_money(gap),
        "reason": "Starts within current surplus and increases contributions annually." if step_up is not None else "A 100% annual step-up from current surplus does not close the gap within the horizon."})
    options.append({**_method("lumpsum_plus_step_up_sip"), "status": "feasible" if step_up is not None else "requires_upfront_capital",
        "required_lumpsum": round_money(step_lumpsum), "required_monthly_contribution": round_money(required_sip),
        "starting_monthly_contribution": round_money(surplus), "annual_step_up": round(step_up, 6) if step_up is not None else 1.0,
        "remaining_gap": round_money(step_residual),
        "reason": "Combines an upfront amount with a stepped recurring contribution."})
    return _finalize(options)
