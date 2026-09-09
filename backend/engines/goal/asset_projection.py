from typing import Literal
from engines.calculation.engine import round_money

DEFAULT_ASSET_RETURNS: dict[str, float] = {
    "bank": 0.04,
    "cash": 0.04,
    "fixed deposit": 0.07,
    "fd": 0.07,
    "mutual fund": 0.12,
    "stock": 0.12,
    "equity": 0.12,
    "bond": 0.07,
    "debt": 0.07,
    "epf": 0.08,
    "ppf": 0.08,
    "provident": 0.08,
    "nps": 0.09,
    "gold": 0.08,
    "real estate": 0.09,
    "property": 0.09,
}
DEFAULT_RETURN_FALLBACK = 0.08


def get_default_expected_return(asset_name: str | None) -> float:
    if not asset_name:
        return DEFAULT_RETURN_FALLBACK
    name_clean = asset_name.strip().lower()
    for key, rate in DEFAULT_ASSET_RETURNS.items():
        if key in name_clean:
            return rate
    return DEFAULT_RETURN_FALLBACK


def get_compounding_frequency(frequency: str) -> int:
    freq = (frequency or "annual").strip().lower()
    if freq in {"monthly"}:
        return 12
    if freq in {"quarterly"}:
        return 4
    if freq in {"semi-annual", "semiannual", "half-yearly"}:
        return 2
    return 1  # default annual


def calculate_asset_projection(
    current_asset_value: float,
    allocation_type: Literal["currency", "percentage"],
    allocation_value: float,
    expected_return: float,
    return_frequency: str,
    duration_years: float,
) -> tuple[float, float, float]:
    """
    Returns (allocated_amount, allocated_percentage, projected_value)
    """
    current_val = max(0.0, float(current_asset_value))
    alloc_val = max(0.0, float(allocation_value))

    if allocation_type == "percentage":
        allocated_pct = min(100.0, alloc_val)
        allocated_amt = round_money(current_val * (allocated_pct / 100.0))
    else:  # currency
        allocated_amt = min(current_val, alloc_val)
        allocated_pct = round((allocated_amt / current_val * 100.0), 3) if current_val > 0 else 0.0

    if duration_years <= 0 or allocated_amt <= 0:
        return (allocated_amt, allocated_pct, allocated_amt)

    n = get_compounding_frequency(return_frequency)
    r = float(expected_return)
    projected = allocated_amt * ((1.0 + (r / n)) ** (n * duration_years))
    return (allocated_amt, allocated_pct, round_money(projected))
