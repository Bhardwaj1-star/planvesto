from typing import Literal

from engines.calculation.engine import round_money
from engines.calculation.canonical import calculate_goal_funding_gap
from rules.assumptions import DEFAULT_FUNDING_RETURN_ASSUMPTION, normalize_annual_return


def calculate_funding_gap(
    future_target: float,
    projected_mapped_asset_value: float,
) -> tuple[float, Literal["Shortfall", "On Track", "Overfunded"]]:
    """Compare the future target with eligible mapped assets at the goal date."""
    gap = calculate_goal_funding_gap(future_target, projected_mapped_asset_value)
    if gap is None:
        gap = 0.0
    if abs(gap) < 0.01:
        return (0.0, "On Track")
    if gap > 0:
        return (gap, "Shortfall")
    return (gap, "Overfunded")


def effective_monthly_rate(annual_effective_return: float) -> float:
    """Convert an effective annual return to an equivalent effective monthly rate."""
    annual = float(annual_effective_return)
    if annual <= -1.0:
        raise ValueError("Annual return must be greater than -100%")
    return (1.0 + annual) ** (1.0 / 12.0) - 1.0


def calculate_required_monthly_contribution(
    funding_gap: float,
    annual_return: float,
    duration_years: float,
) -> float:
    """Calculate the month-end SIP required to close a future-value funding gap.

    The annual return is treated as an effective annual rate and converted to
    an equivalent effective monthly rate. This is an ordinary-annuity model;
    irregular and step-up schedules require their own dated cash-flow inputs.
    """
    gap = max(0.0, float(funding_gap))
    years = max(0.0, float(duration_years))
    if gap <= 0.0 or years <= 0.0:
        return 0.0

    monthly_rate = effective_monthly_rate(annual_return)
    months = max(1, round(years * 12))
    if abs(monthly_rate) < 1e-12:
        return round_money(gap / months)

    denominator = ((1.0 + monthly_rate) ** months) - 1.0
    if denominator <= 0.0:
        raise ValueError("Return assumption produces an invalid contribution factor")

    return round_money(max(0.0, gap * monthly_rate / denominator))


def calculate_funding_return_assumption(
    mapped_assets: list[dict],
    fallback_return: float = DEFAULT_FUNDING_RETURN_ASSUMPTION,
) -> float:
    """Return the allocated-value-weighted annual return for mapped assets.

    The fallback is an explicit planning baseline, not an asset-name inference.
    """
    fallback = normalize_annual_return(fallback_return)
    if not mapped_assets:
        return fallback

    total_value = sum(max(0.0, float(item.get("allocated_amount", 0.0))) for item in mapped_assets)
    if total_value <= 0.0:
        return fallback

    weighted = sum(
        max(0.0, float(item.get("allocated_amount", 0.0)))
        * normalize_annual_return(item.get("expected_return", fallback))
        for item in mapped_assets
    )
    return weighted / total_value
