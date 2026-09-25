from datetime import date

import pytest

from engines.goal.specialized import calculate_education, calculate_retirement, calculate_travel


def test_retirement_derives_required_corpus():
    result = calculate_retirement({
        "current_monthly_expense": 100000,
        "current_age": 40,
        "retirement_age": 60,
        "life_expectancy": 85,
        "inflation_rate": 0.06,
        "post_retirement_return": 0.08,
    }, date(2026, 9, 25))
    assert result["future_target"] > result["today_cost"]
    assert result["target_year"] == 2046


def test_education_uses_dependent_dob():
    result = calculate_education({
        "current_cost": 2000000,
        "education_start_age": 18,
        "education_inflation_rate": 0.08,
        "dependent_date_of_birth": "2016-09-25",
    }, date(2026, 9, 25))
    assert result["dependent_current_age"] == pytest.approx(10.0, abs=0.01)
    assert result["years_to_start"] == pytest.approx(8.0, abs=0.01)
    assert result["future_target"] > 2000000


def test_travel_sums_recurring_inflated_trips():
    result = calculate_travel({
        "current_trip_cost": 100000,
        "repeat_every_years": 3,
        "number_of_trips": 3,
        "travel_inflation_rate": 0.06,
    }, date(2026, 9, 25))
    assert len(result["future_trip_costs"]) == 3
    assert result["future_target"] == pytest.approx(sum(result["future_trip_costs"]))
    assert result["target_year"] == 2029
