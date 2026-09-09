from typing import Literal
from engines.calculation.engine import round_money


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
    gap = round_money(future_target - projected_mapped_asset_value)
    if abs(gap) < 0.01:
        return (0.0, "On Track")
    if gap > 0:
        return (gap, "Shortfall")
    return (gap, "Overfunded")
