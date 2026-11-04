from typing import Any

from engines.calculation.engine import round_money
from engines.goal.funding_gap import effective_monthly_rate


# These are Goal Planner funding methods, not Strategy Builder paths.
_METHODS = {
    "existing_assets": ("Existing mapped assets", "existing_assets", "Uses eligible assets mapped to this goal."),
    "sip": ("SIP", "recurring_contribution", "Funds the remaining future-value gap through month-end contributions."),
    "lumpsum": ("Lump Sum", "upfront_capital", "Funds the remaining future-value gap through upfront capital."),
    "lumpsum_plus_sip": ("Lump Sum + SIP", "combined_funding", "Combines an upfront amount with a recurring contribution."),
    "step_up_sip": ("Step-Up SIP", "recurring_contribution", "Requires an explicit dated step-up contribution schedule."),
    "lumpsum_plus_step_up_sip": ("Lump Sum + Step-Up SIP", "combined_funding", "Requires an explicit dated step-up contribution schedule."),
}


def _method(method_id: str) -> dict[str, str]:
    name, method_type, description = _METHODS[method_id]
    return {"method_id": method_id, "method_name": name, "method_type": method_type, "description": description}


def _finalize(options: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for option in options:
        option["constraints"] = [] if option["status"] == "feasible" else [option["reason"]]
    return options


def _future_value_monthly(monthly: float, annual_return: float, months: int) -> float:
    if monthly <= 0 or months <= 0:
        return 0.0
    monthly_rate = effective_monthly_rate(annual_return)
    if abs(monthly_rate) < 1e-12:
        return monthly * months
    return monthly * (((1.0 + monthly_rate) ** months - 1.0) / monthly_rate)


def build_goal_funding_options(
    funding_gap: float,
    annual_return: float,
    duration_years: float,
    available_monthly_surplus: float | None,
) -> list[dict[str, Any]]:
    """Evaluate supported Goal Planner methods without selecting one for the investor."""
    gap = max(0.0, float(funding_gap))
    years = max(0.0, float(duration_years))
    surplus = float(available_monthly_surplus or 0.0)
    months = max(0, round(years * 12))

    if gap <= 0:
        return _finalize([{
            **_method("existing_assets"),
            "status": "feasible",
            "required_lumpsum": 0.0,
            "required_monthly_contribution": 0.0,
            "starting_monthly_contribution": 0.0,
            "annual_step_up": None,
            "remaining_gap": 0.0,
            "reason": "Eligible mapped assets already cover the target-date requirement.",
        }])

    if months <= 0:
        return _finalize([{
            **_method("lumpsum"),
            "status": "requires_upfront_capital",
            "required_lumpsum": round_money(gap),
            "required_monthly_contribution": 0.0,
            "starting_monthly_contribution": 0.0,
            "annual_step_up": None,
            "remaining_gap": 0.0,
            "reason": "The target date is immediate; a future monthly contribution is not applicable.",
        }])

    monthly_rate = effective_monthly_rate(annual_return)
    factor = months if abs(monthly_rate) < 1e-12 else (((1.0 + monthly_rate) ** months - 1.0) / monthly_rate)
    required_sip = gap / factor
    required_lumpsum = gap / ((1.0 + float(annual_return)) ** years)
    sip_future = _future_value_monthly(max(0.0, surplus), annual_return, months)
    sip_fits = required_sip <= max(0.0, surplus) + 0.01
    residual = max(0.0, gap - sip_future)
    mixed_lumpsum = residual / ((1.0 + float(annual_return)) ** years)

    options = [
        {
            **_method("sip"),
            "status": "feasible" if sip_fits else "constrained",
            "required_lumpsum": 0.0,
            "required_monthly_contribution": round_money(required_sip),
            "starting_monthly_contribution": round_money(required_sip),
            "annual_step_up": None,
            "remaining_gap": round_money(residual),
            "reason": "Required SIP fits the uncommitted Available Monthly Surplus." if sip_fits else "Required SIP exceeds the uncommitted Available Monthly Surplus.",
        },
        {
            **_method("lumpsum"),
            "status": "requires_upfront_capital",
            "required_lumpsum": round_money(required_lumpsum),
            "required_monthly_contribution": 0.0,
            "starting_monthly_contribution": 0.0,
            "annual_step_up": None,
            "remaining_gap": 0.0,
            "reason": "Illustrative upfront capital required today; availability and suitability must be assessed separately.",
        },
        {
            **_method("lumpsum_plus_sip"),
            "status": "requires_upfront_capital" if residual > 0.01 else "feasible",
            "required_lumpsum": round_money(mixed_lumpsum),
            "required_monthly_contribution": round_money(max(0.0, surplus)),
            "starting_monthly_contribution": round_money(max(0.0, surplus)),
            "annual_step_up": None,
            "remaining_gap": round_money(residual),
            "reason": "Illustrative combination using the non-negative uncommitted monthly surplus; upfront capital must be independently verified.",
        },
        {
            **_method("step_up_sip"),
            "status": "not_assessed",
            "required_lumpsum": None,
            "required_monthly_contribution": None,
            "starting_monthly_contribution": None,
            "annual_step_up": None,
            "remaining_gap": round_money(gap),
            "reason": "An investor-approved dated contribution and step-up schedule is required; no arbitrary step-up rate is assumed.",
        },
        {
            **_method("lumpsum_plus_step_up_sip"),
            "status": "not_assessed",
            "required_lumpsum": None,
            "required_monthly_contribution": None,
            "starting_monthly_contribution": None,
            "annual_step_up": None,
            "remaining_gap": round_money(gap),
            "reason": "An investor-approved dated contribution and step-up schedule is required before this combination can be calculated.",
        },
    ]
    return _finalize(options)
