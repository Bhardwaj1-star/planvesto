from __future__ import annotations

from datetime import date
from math import isclose
from typing import Any


def _years_between(start: date, end: date) -> float:
    return max(0.0, (end - start).days / 365.25)


def calculate_retirement_corpus(
    *,
    current_monthly_expense: float,
    current_age: float,
    retirement_age: float,
    life_expectancy: float,
    inflation_rate: float,
    post_retirement_return: float,
    reference_date: date,
) -> tuple[float, dict[str, Any]]:
    if current_monthly_expense <= 0:
        raise ValueError("Retirement monthly expense must be greater than zero")
    if retirement_age <= current_age:
        raise ValueError("Retirement age must be greater than current age")
    if life_expectancy <= retirement_age:
        raise ValueError("Life expectancy must be greater than retirement age")
    years_to_retirement = retirement_age - current_age
    retirement_years = life_expectancy - retirement_age
    annual_expense_today = current_monthly_expense * 12
    first_year_expense = annual_expense_today * ((1 + inflation_rate) ** years_to_retirement)

    r = post_retirement_return
    g = inflation_rate
    if isclose(r, g, abs_tol=1e-12):
        corpus = first_year_expense * retirement_years / (1 + r)
    else:
        corpus = (first_year_expense / (r - g)) * (
            1 - ((1 + g) / (1 + r)) ** retirement_years
        )

    retirement_year = reference_date.year + int(years_to_retirement)
    retirement_month = reference_date.month
    return round(max(0.0, corpus), 2), {
        "calculation": "growing_annuity_retirement_corpus",
        "current_monthly_expense": current_monthly_expense,
        "current_age": current_age,
        "retirement_age": retirement_age,
        "life_expectancy": life_expectancy,
        "years_to_retirement": years_to_retirement,
        "retirement_years": retirement_years,
        "first_year_retirement_expense": round(first_year_expense, 2),
        "retirement_target_year": retirement_year,
        "retirement_target_month": retirement_month,
    }


def calculate_education_target(
    *,
    current_education_cost: float,
    child_current_age: float,
    education_start_age: float,
    inflation_rate: float,
) -> tuple[float, float]:
    if current_education_cost <= 0:
        raise ValueError("Education current cost must be greater than zero")
    if education_start_age <= child_current_age:
        raise ValueError("Education start age must be greater than child's current age")
    years = education_start_age - child_current_age
    target = current_education_cost * ((1 + inflation_rate) ** years)
    return round(target, 2), years


def calculate_travel_schedule(
    *,
    first_trip_cost: float,
    first_trip_date: date,
    repeat_every_years: float,
    number_of_trips: int,
    inflation_rate: float,
    reference_date: date,
) -> tuple[float, float, list[dict[str, Any]]]:
    if first_trip_cost <= 0:
        raise ValueError("Travel cost must be greater than zero")
    if repeat_every_years <= 0:
        raise ValueError("Travel repeat interval must be greater than zero")
    if number_of_trips < 1:
        raise ValueError("Travel must contain at least one trip")

    schedule: list[dict[str, Any]] = []
    total = 0.0
    first_years = _years_between(reference_date, first_trip_date)
    for i in range(number_of_trips):
        years_from_now = first_years + (i * repeat_every_years)
        cost = first_trip_cost * ((1 + inflation_rate) ** years_from_now)
        total += cost
        schedule.append({
            "trip_number": i + 1,
            "years_from_now": round(years_from_now, 4),
            "future_cost": round(cost, 2),
        })
    return round(total, 2), max(0.0, first_years), schedule
