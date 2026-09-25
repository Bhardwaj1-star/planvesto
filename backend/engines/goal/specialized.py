from __future__ import annotations

from datetime import date
from math import pow
from typing import Any


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


def calculate_specialized_target(goal_type: str, data: dict[str, Any], reference_date: date) -> dict[str, Any]:
    kind = goal_type.strip().lower()

    if kind == "retirement":
        current_age = _positive(data, "current_age")
        retirement_age = _positive(data, "retirement_age")
        life_expectancy = _positive(data, "life_expectancy")
        monthly_expense = _positive(data, "current_monthly_expense")
        expense_inflation = float(data.get("expense_inflation_rate", 0.06))
        post_retirement_return = float(data.get("post_retirement_return_rate", 0.08))
        years_to_retirement = _years_to_age(current_age, retirement_age)
        retirement_years = life_expectancy - retirement_age
        if years_to_retirement <= 0:
            raise ValueError("Retirement age must be greater than current age")
        if retirement_years <= 0:
            raise ValueError("Life expectancy must be greater than retirement age")
        annual_expense_at_retirement = monthly_expense * 12 * pow(1 + expense_inflation, years_to_retirement)
        real_return = (1 + post_retirement_return) / (1 + expense_inflation) - 1
        if abs(real_return) < 1e-9:
            corpus = annual_expense_at_retirement * retirement_years
        else:
            corpus = annual_expense_at_retirement * (1 - pow(1 + real_return, -retirement_years)) / real_return
        return {
            "today_cost": monthly_expense * 12,
            "future_target": corpus,
            "duration_years": years_to_retirement,
            "target_age": retirement_age,
            "retirement_years": retirement_years,
            "annual_expense_at_retirement": annual_expense_at_retirement,
            "current_age": current_age,
            "retirement_age": retirement_age,
            "life_expectancy": life_expectancy,
            "current_monthly_expense": monthly_expense,
            "post_retirement_return_rate": post_retirement_return,
        }

    if kind in {"child education", "education"}:
        current_cost = _positive(data, "current_education_cost")
        child_age = float(data.get("child_age", 0) or 0)
        education_start_age = _positive(data, "education_start_age")
        duration = _positive(data, "education_duration_years")
        education_inflation = float(data.get("education_inflation_rate", 0.08))
        years = _years_to_age(child_age, education_start_age)
        first_year_cost = current_cost * pow(1 + education_inflation, years)
        total_cost = sum(first_year_cost * pow(1 + education_inflation, year) for year in range(int(duration)))
        return {
            "today_cost": current_cost,
            "future_target": total_cost,
            "duration_years": years,
            "education_start_age": education_start_age,
            "child_age": child_age,
            "education_duration_years": duration,
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
            "future_target": total,
            "duration_years": first_trip_years,
            "travel_total_cost": total,
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
        "future_target": current_cost * pow(1 + inflation, years),
        "duration_years": years,
        "current_cost": current_cost,
        "years_to_goal": years,
        "inflation_rate": inflation,
    }
