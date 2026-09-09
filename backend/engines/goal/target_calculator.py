from datetime import date
from engines.calculation.engine import round_money

DEFAULT_INFLATION_RATE = 0.06


def calculate_duration(
    target_month: int,
    target_year: int,
    reference_date: date | None = None,
) -> float:
    if reference_date is None:
        reference_date = date.today()
    total_months = (target_year - reference_date.year) * 12 + (target_month - reference_date.month)
    if total_months < 0:
        return 0.0
    return round(total_months / 12.0, 3)


def calculate_future_target(
    today_cost: float,
    inflation_rate: float,
    duration_years: float,
) -> float:
    if today_cost <= 0:
        return 0.0
    val = today_cost * ((1.0 + inflation_rate) ** duration_years)
    return round_money(val)
