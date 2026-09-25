"""Calculators for Goal Planner goal types that cannot use a simple target amount."""

from __future__ import annotations

from datetime import date
from math import pow
from typing import Any


def _require(details: dict[str, Any], key: str) -> float:
    value = details.get(key)
    if value is None or float(value) < 0:
        raise ValueError(f"goal_details.{key} is required and must be non-negative")
    return float(value)


def _age_on(dob: date, on_date: date) -> float:
    return max(0.0, (on_date - dob).days / 365.2425)


def _parse_date(value: Any) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def calculate_retirement(details: dict[str, Any], reference_date: date) -> dict[str, Any]:
    current_monthly_expense = _require(details, "current_monthly_expense")
    current_age = _require(details, "current_age")
    retirement_age = _require(details, "retirement_age")
    life_expectancy = _require(details, "life_expectancy")
    inflation = float(details.get("inflation_rate", 0.06))
    post_retirement_return = float(details.get("post_retirement_return", 0.08))

    if retirement_age <= current_age:
        raise ValueError("retirement_age must be greater than current_age")
    if life_expectancy <= retirement_age:
        raise ValueError("life_expectancy must be greater than retirement_age")
    if not 0 <= inflation <= 1 or not 0 <= post_retirement_return < 1:
        raise ValueError("Invalid retirement inflation/return assumption")

    years_to_retirement = retirement_age - current_age
    retirement_monthly_expense = current_monthly_expense * pow(1 + inflation, years_to_retirement)
    retirement_annual_expense = retirement_monthly_expense * 12
    retirement_years = life_expectancy - retirement_age
    real_return = (1 + post_retirement_return) / (1 + inflation) - 1

    if abs(real_return) < 1e-9:
        corpus = retirement_annual_expense * retirement_years
    else:
        corpus = retirement_annual_expense * (1 - pow(1 + real_return, -retirement_years)) / real_return

    target_date = date(reference_date.year + int(years_to_retirement), reference_date.month, 1)
    return {
        "today_cost": current_monthly_expense * 12,
        "future_target": max(0.0, corpus),
        "target_month": target_date.month,
        "target_year": target_date.year,
        "inflation_rate": inflation,
        "calculation": "retirement_corpus_real_return_annuity",
        "years_to_retirement": years_to_retirement,
        "retirement_monthly_expense": retirement_monthly_expense,
        "retirement_annual_expense": retirement_annual_expense,
        "retirement_years": retirement_years,
        "real_return": real_return,
    }


def calculate_education(details: dict[str, Any], reference_date: date) -> dict[str, Any]:
    current_cost = _require(details, "current_cost")
    start_age = _require(details, "education_start_age")
    education_inflation = float(details.get("education_inflation_rate", 0.08))
    dependent_dob = _parse_date(details["dependent_date_of_birth"])
    current_age = _age_on(dependent_dob, reference_date)

    if start_age < current_age:
        raise ValueError("education_start_age cannot be below the dependent's current age")
    years_to_start = start_age - current_age
    future_target = current_cost * pow(1 + education_inflation, years_to_start)
    target_date = date(reference_date.year + int(years_to_start), reference_date.month, 1)

    return {
        "today_cost": current_cost,
        "future_target": future_target,
        "target_month": target_date.month,
        "target_year": target_date.year,
        "inflation_rate": education_inflation,
        "calculation": "education_cost_inflation",
        "dependent_current_age": current_age,
        "years_to_start": years_to_start,
    }


def calculate_travel(details: dict[str, Any], reference_date: date) -> dict[str, Any]:
    trip_cost = _require(details, "current_trip_cost")
    interval_years = _require(details, "repeat_every_years")
    occurrences = int(_require(details, "number_of_trips"))
    inflation = float(details.get("travel_inflation_rate", 0.06))

    if interval_years <= 0 or occurrences <= 0:
        raise ValueError("repeat_every_years and number_of_trips must be positive")
    if not 0 <= inflation <= 1:
        raise ValueError("Invalid travel inflation assumption")

    future_costs = [trip_cost * pow(1 + inflation, interval_years * i) for i in range(1, occurrences + 1)]
    first_years = interval_years
    target_date = date(reference_date.year + int(first_years), reference_date.month, 1)

    return {
        "today_cost": trip_cost,
        "future_target": sum(future_costs),
        "target_month": target_date.month,
        "target_year": target_date.year,
        "inflation_rate": inflation,
        "calculation": "recurring_travel_inflated_sum",
        "number_of_trips": occurrences,
        "repeat_every_years": interval_years,
        "future_trip_costs": future_costs,
    }


def resolve_specialized_goal(goal_type: str, details: dict[str, Any], reference_date: date) -> dict[str, Any] | None:
    if goal_type == "Retirement":
        return calculate_retirement(details, reference_date)
    if goal_type == "Child Education":
        return calculate_education(details, reference_date)
    if goal_type == "Travel":
        return calculate_travel(details, reference_date)
    return None
