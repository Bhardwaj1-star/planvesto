from typing import Literal
from engines.calculation.engine import round_money


from engines.calculation.canonical import calculate_goal_funding_gap


def calculate_funding_gap(
    future_target: float,
    projected_mapped_asset_value: float,
) -> tuple[float, Literal["Shortfall", "On Track", "Overfunded"]]:
    """
    Target-date funding gap:
      funding_gap = future_target - projected_mapped_asset_value
      > 0 -> Shortfall
      == 0 -> On Track
      < 0 -> Overfunded
    """
    gap = calculate_goal_funding_gap(future_target, projected_mapped_asset_value)
    if gap is None:
        gap = 0.0
    if abs(gap) < 0.01:
        return (0.0, "On Track")
    if gap > 0:
        return (gap, "Shortfall")
    return (gap, "Overfunded")


def calculate_required_monthly_contribution(
    funding_gap: float,
    annual_return: float,
    duration_years: float,
) -> float:
    """
    Calculates the end-of-month contribution required to fund a positive
    target-date gap. The same nominal annual return convention used by the
    goal asset projection is converted to a monthly rate.

    A non-positive gap requires no additional contribution. If the target is
    effectively immediate, the future monthly-contribution model is not
    applicable and returns 0; the caller should surface the immediate gap.
    """
    gap = max(0.0, float(funding_gap))
    years = max(0.0, float(duration_years))
    if gap <= 0.0 or years <= 0.0:
        return 0.0

    annual = float(annual_return)
    if annual <= -1.0:
        raise ValueError("Annual return must be greater than -100%")

    months = max(1, round(years * 12))
    monthly_rate = annual / 12.0

    if abs(monthly_rate) < 1e-12:
        return round_money(gap / months)

    denominator = ((1.0 + monthly_rate) ** months) - 1.0
    if denominator <= 0.0:
        raise ValueError("Return assumption produces an invalid contribution factor")

    required = gap * monthly_rate / denominator
    return round_money(max(0.0, required))


def calculate_funding_return_assumption(
    mapped_assets: list[dict],
    fallback_return: float = 0.08,
) -> float:
    """
    Returns the weighted nominal annual return of mapped assets using their
    allocated current value as weights. Falls back explicitly when no mapped
    capital exists.
    """
    if not mapped_assets:
        return float(fallback_return)

    total_value = sum(max(0.0, float(item.get("allocated_amount", 0.0))) for item in mapped_assets)
    if total_value <= 0.0:
        return float(fallback_return)

    weighted = sum(
        max(0.0, float(item.get("allocated_amount", 0.0)))
        * float(item.get("expected_return", fallback_return))
        for item in mapped_assets
    )
    return weighted / total_value
