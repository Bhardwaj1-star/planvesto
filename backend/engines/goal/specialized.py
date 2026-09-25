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
    if years <= 0:
        raise ValueError("Target age must be greater than current age")
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
        }

    if kind in {"child education", "education"}:
        current_cost = _positive(data, "current_education_cost")
        child_age = _positive(data, "child_age")
        education_start_age = _positive(data, "education_start_age")
        education_inflation = float(data.get("education_inflation_rate", 0.08))
        years = _years_to_age(child_age, education_start_age)
        future_cost = current_cost * pow(1 + education_inflation, years)
        return {
            "today_cost": current_cost,
            "future_target": future_cost,
            "duration_years": years,
            "education_start_age": education_start_age,
            "child_age": child_age,
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
        }

    # Generic specialized one-time goals: use today's cost and the common inflation model.
    current_cost = _positive(data, "current_cost")
    years = _positive(data, "years_to_goal")
    inflation = float(data.get("inflation_rate", 0.06))
    return {
        "today_cost": current_cost,
        "future_target": current_cost * pow(1 + inflation, years),
        "duration_years": years,
    }
