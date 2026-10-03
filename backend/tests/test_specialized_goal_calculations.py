from datetime import date

import pytest

from engines.goal.specialized import calculate_specialized_target


def test_retirement_calculates_required_corpus():
    result = calculate_specialized_target(
        "Retirement",
        {
            "current_age": 35,
            "retirement_age": 60,
            "life_expectancy": 85,
            "current_monthly_expense": 100000,
            "expense_inflation_rate": 0.06,
            "post_retirement_return_rate": 0.08,
        },
        date(2026, 1, 1),
    )
    assert result["duration_years"] == 25
    assert result["retirement_years"] == 25
    assert result["future_target"] > 0


def test_education_uses_child_age_and_start_age():
    result = calculate_specialized_target(
        "Education",
        {
            "child_age": 8,
            "education_start_age": 18,
            "current_education_cost": 2000000,
            "education_inflation_rate": 0.08,
        },
        date(2026, 1, 1),
    )
    assert result["duration_years"] == 10
    assert result["future_target"] == pytest.approx(4317852.86, rel=1e-6)


def test_travel_accumulates_repeated_trips_with_inflation():
    result = calculate_specialized_target(
        "Travel",
        {
            "current_trip_cost": 100000,
            "years_to_first_trip": 2,
            "repeat_every_years": 2,
            "number_of_trips": 3,
            "travel_inflation_rate": 0.06,
        },
        date(2026, 1, 1),
    )
    assert result["duration_years"] == 2
    assert result["number_of_trips"] == 3
    assert result["future_target"] == pytest.approx(380459.61, rel=1e-6)


def test_invalid_retirement_horizon_is_rejected():
    with pytest.raises(ValueError):
        calculate_specialized_target(
            "Retirement",
            {
                "current_age": 60,
                "retirement_age": 60,
                "life_expectancy": 85,
                "current_monthly_expense": 100000,
            },
            date(2026, 1, 1),
        )
