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
    from engines.calculation.canonical import calculate_goal_future_target
    val = calculate_goal_future_target(today_cost, inflation_rate, duration_years)
    return val if val is not None else 0.0


def calculate_retirement_corpus(
    current_monthly_expense: float,
    inflation_rate: float,
    years_to_retirement: float,
    current_age: float,
    life_expectancy: float,
    retirement_return: float,
) -> tuple[float, float, float]:
    """Calculate the retirement corpus required at the retirement date.

    The monthly lifestyle expense is inflated to the retirement date. The
    resulting annual retirement expense is then valued as a finite growing
    annuity over the post-retirement period. Retirement return is the nominal
    annual portfolio return assumption during retirement.

    Returns: (retirement_age, retirement_years, required_corpus).
    """
    monthly = float(current_monthly_expense)
    years = max(0.0, float(years_to_retirement))
    age = float(current_age)
    life = float(life_expectancy)
    ret = float(retirement_return)

    if monthly <= 0:
        raise ValueError("Current monthly retirement expense must be greater than zero")
    if age < 0 or age >= 150:
        raise ValueError("Current age must be between 0 and 149")
    if life <= age or life >= 150:
        raise ValueError("Life expectancy must be greater than current age and below 150")
    if ret <= -1.0:
        raise ValueError("Retirement return must be greater than -100%")

    retirement_age = age + years
    retirement_years = life - retirement_age
    if retirement_years <= 0:
        raise ValueError("Retirement target must occur before life expectancy")

    first_year_expense = monthly * 12.0 * ((1.0 + float(inflation_rate)) ** years)
    n = max(1, round(retirement_years))
    growth = float(inflation_rate)
    discount = ret

    if abs(discount - growth) < 1e-12:
        corpus = first_year_expense * n / (1.0 + discount)
    else:
        corpus = (first_year_expense / (discount - growth)) * (
            1.0 - ((1.0 + growth) / (1.0 + discount)) ** n
        )

    return round(retirement_age, 3), round(retirement_years, 3), round_money(max(0.0, corpus))
