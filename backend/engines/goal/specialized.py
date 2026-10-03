from __future__ import annotations

from datetime import date
from math import isclose, pow
from typing import Any


def _years_between(start: date, end: date) -> float:
    return max(0.0, (end - start).days / 365.25)


def _positive(data: dict[str, Any], key: str) -> float:
    value = float(data.get(key, 0) or 0)
    if value <= 0:
        raise ValueError(f"{key} must be greater than 0")
    return value


def _years_to_age(current_age: float, target_age: float) -> float:
    years = target_age - current_age
    if years < 0:
        raise ValueError("Target age cannot be less than current age")
    return years


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


def calculate_specialized_target(goal_type: str, data: dict[str, Any], reference_date: date | None = None) -> dict[str, Any]:
    ref = reference_date or date.today()
    kind = goal_type.strip().lower()

    if kind == "retirement":
        current_age = _positive(data, "current_age")
        retirement_age = _positive(data, "retirement_age")
        life_expectancy = _positive(data, "life_expectancy")
        monthly_expense = _positive(data, "current_monthly_expense")
        expense_inflation = float(data.get("expense_inflation_rate", 0.06))
        post_retirement_return = float(data.get("post_retirement_return_rate", 0.08))
        corpus, meta = calculate_retirement_corpus(
            current_monthly_expense=monthly_expense,
            current_age=current_age,
            retirement_age=retirement_age,
            life_expectancy=life_expectancy,
            inflation_rate=expense_inflation,
            post_retirement_return=post_retirement_return,
            reference_date=ref,
        )
        return {
            "today_cost": monthly_expense * 12,
            "future_target": corpus,
            "duration_years": meta["years_to_retirement"],
            "target_age": retirement_age,
            "retirement_years": meta["retirement_years"],
            "annual_expense_at_retirement": meta["first_year_retirement_expense"],
            "current_age": current_age,
            "retirement_age": retirement_age,
            "life_expectancy": life_expectancy,
            "current_monthly_expense": monthly_expense,
            "post_retirement_return_rate": post_retirement_return,
            **meta,
        }

    if kind == "education":
        current_cost = _positive(data, "current_education_cost")
        child_age = float(data.get("child_age", 0) or 0)
        education_start_age = _positive(data, "education_start_age")
        education_inflation = float(data.get("education_inflation_rate", 0.08))
        target, years = calculate_education_target(
            current_education_cost=current_cost,
            child_current_age=child_age,
            education_start_age=education_start_age,
            inflation_rate=education_inflation,
        )
        return {
            "today_cost": current_cost,
            "future_target": target,
            "duration_years": years,
            "education_start_age": education_start_age,
            "child_age": child_age,
            "current_education_cost": current_cost,
            "education_inflation_rate": education_inflation,
            "dependent_id": data.get("dependent_id"),
        }

    if kind == "travel":
        trip_cost = _positive(data, "current_trip_cost")
        trips = int(data.get("number_of_trips", 1) or 1)
        interval = _positive(data, "repeat_every_years")
        first_trip_years = _positive(data, "years_to_first_trip")
        travel_inflation = float(data.get("travel_inflation_rate", 0.06))
        if trips < 1:
            raise ValueError("number_of_trips must be at least 1")
        total = sum(trip_cost * pow(1 + travel_inflation, first_trip_years + (i * interval)) for i in range(trips))
        return {
            "today_cost": trip_cost,
            "future_target": round(total, 2),
            "duration_years": first_trip_years,
            "travel_total_cost": round(total, 2),
            "number_of_trips": trips,
            "repeat_every_years": interval,
            "years_to_first_trip": first_trip_years,
            "current_trip_cost": trip_cost,
            "travel_inflation_rate": travel_inflation,
        }

    current_cost = _positive(data, "current_cost")
    years = float(data.get("years_to_goal", 0) or 0)
    if years <= 0:
        raise ValueError("years_to_goal must be greater than 0")
    inflation = float(data.get("inflation_rate", 0.06))
    return {
        "today_cost": current_cost,
        "future_target": round(current_cost * pow(1 + inflation, years), 2),
        "duration_years": years,
        "current_cost": current_cost,
        "years_to_goal": years,
        "inflation_rate": inflation,
    }
