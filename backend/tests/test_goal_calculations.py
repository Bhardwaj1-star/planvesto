from datetime import date
import pytest
from engines.goal.target_calculator import (
    calculate_duration,
    calculate_future_target,
    calculate_retirement_corpus,
    DEFAULT_INFLATION_RATE,
)
from engines.goal.asset_projection import (
    calculate_asset_projection,
    get_default_expected_return,
    get_compounding_frequency,
)
from engines.goal.funding_gap import (
    calculate_funding_gap,
    calculate_funding_return_assumption,
    calculate_required_monthly_contribution,
)
from engines.goal.engine import GoalEngine
from schemas.goals import GoalInput, AssetMappingInput
from pydantic import ValidationError


class TestTargetCalculator:
    def test_duration_calculation(self):
        ref = date(2026, 1, 1)
        dur = calculate_duration(target_month=1, target_year=2031, reference_date=ref)
        assert dur == 5.0

    def test_duration_past_date_returns_zero(self):
        ref = date(2026, 1, 1)
        dur = calculate_duration(target_month=1, target_year=2020, reference_date=ref)
        assert dur == 0.0

    def test_future_target_with_inflation(self):
        future = calculate_future_target(100000.0, 0.06, 5.0)
        assert future == 133822.56

    def test_future_target_zero_cost(self):
        assert calculate_future_target(0.0, 0.06, 5.0) == 0.0

    def test_retirement_corpus_uses_post_retirement_horizon(self):
        retirement_age, retirement_years, corpus = calculate_retirement_corpus(
            current_monthly_expense=100000.0,
            inflation_rate=0.06,
            years_to_retirement=14.0,
            current_age=30.0,
            life_expectancy=80.0,
            retirement_return=0.08,
        )
        assert retirement_age == 44.0
        assert retirement_years == 36.0
        assert corpus == 66440975.63

    def test_retirement_corpus_rejects_invalid_lifespan(self):
        with pytest.raises(ValueError):
            calculate_retirement_corpus(100000, 0.06, 14, 70, 75, 0.08)


class TestAssetProjection:
    def test_percentage_allocation(self):
        amt, pct, proj = calculate_asset_projection(
            current_asset_value=1000000.0,
            allocation_type="percentage",
            allocation_value=50.0,
            expected_return=0.12,
            return_frequency="annual",
            duration_years=5.0,
        )
        assert amt == 500000.0
        assert pct == 50.0
        assert proj == 881170.84

    def test_currency_allocation(self):
        amt, pct, proj = calculate_asset_projection(
            current_asset_value=1000000.0,
            allocation_type="currency",
            allocation_value=200000.0,
            expected_return=0.10,
            return_frequency="annual",
            duration_years=3.0,
        )
        assert amt == 200000.0
        assert pct == 20.0
        assert proj == 266200.0

    def test_compounding_frequency_monthly(self):
        amt, pct, proj = calculate_asset_projection(
            current_asset_value=100000.0,
            allocation_type="percentage",
            allocation_value=100.0,
            expected_return=0.12,
            return_frequency="monthly",
            duration_years=1.0,
        )
        assert proj == 112682.50

    def test_multiple_goals_can_share_asset(self):
        amt1, pct1, _ = calculate_asset_projection(1000000, "percentage", 30.0, 0.1, "annual", 5)
        amt2, pct2, _ = calculate_asset_projection(1000000, "percentage", 40.0, 0.1, "annual", 5)
        assert amt1 + amt2 == 700000.0

    def test_missing_expected_return_uses_default(self):
        assert get_default_expected_return("HDFC Equity Mutual Funds") == 0.12
        assert get_default_expected_return("Savings Bank Account") == 0.04
        assert get_default_expected_return("Unknown Exotic Asset") == 0.08


class TestFundingGap:
    def test_shortfall(self):
        gap, status = calculate_funding_gap(500000.0, 300000.0)
        assert gap == 200000.0
        assert status == "Shortfall"

    def test_on_track(self):
        gap, status = calculate_funding_gap(500000.0, 500000.0)
        assert gap == 0.0
        assert status == "On Track"

    def test_overfunded(self):
        gap, status = calculate_funding_gap(500000.0, 650000.0)
        assert gap == -150000.0
        assert status == "Overfunded"

    def test_required_monthly_contribution_zero_return(self):
        assert calculate_required_monthly_contribution(120000.0, 0.0, 1.0) == 10000.0

    def test_required_monthly_contribution_with_return(self):
        result = calculate_required_monthly_contribution(120000.0, 0.12, 1.0)
        assert result == 9461.85

    def test_required_monthly_contribution_ignores_surplus(self):
        assert calculate_required_monthly_contribution(-1000.0, 0.12, 5.0) == 0.0

    def test_weighted_funding_return(self):
        result = calculate_funding_return_assumption(
            [
                {"allocated_amount": 300000, "expected_return": 0.10},
                {"allocated_amount": 100000, "expected_return": 0.20},
            ]
        )
        assert result == 0.125


class TestGoalEngineFull:
    def test_complete_goal_calculation(self):
        engine = GoalEngine()
        ref = date(2026, 1, 1)
        inp = GoalInput(
            planning_unit_id="pu-123",
            goal_id="goal-1",
            goal_name="Higher Education",
            goal_type="Child Education",
            today_cost=1000000.0,
            target_month=1,
            target_year=2031,
            inflation_rate=0.06,
            priority="Critical",
            flexibility="Fixed",
            asset_mappings=[
                AssetMappingInput(
                    asset_id="a1",
                    allocation_type="percentage",
                    allocation_value=50.0,
                    expected_return=0.12,
                )
            ],
        )
        assets = {"a1": {"asset_name": "Equity Mutual Fund", "current_value": 800000.0}}
        defined = engine.calculate_defined_goal(inp, assets, version=1, reference_date=ref)

        assert defined.duration_years == 5.0
        assert defined.future_target == 1338225.58
        assert defined.mapped_assets[0].allocated_amount == 400000.0
        assert defined.mapped_assets[0].projected_value == 704936.67
        assert defined.projected_mapped_asset_value == 704936.67
        assert defined.funding_gap == 633288.91
        assert defined.funding_status == "Shortfall"
        assert defined.funding_return_assumption == 0.12
        assert defined.required_monthly_contribution == 7754.27

    def test_retirement_goal_uses_corpus_not_annual_expense(self):
        engine = GoalEngine()
        ref = date(2026, 1, 1)
        inp = GoalInput(
            planning_unit_id="pu-123",
            goal_id="retirement-1",
            goal_name="Retirement",
            goal_type="Retirement",
            today_cost=1200000.0,
            target_month=1,
            target_year=2040,
            inflation_rate=0.06,
            priority="Critical",
            flexibility="Flexible",
            asset_mappings=[],
            dynamic_details={"currentAge": "30", "lifeExpectancy": "80"},
        )
        defined = engine.calculate_defined_goal(inp, {}, version=1, reference_date=ref)

        assert defined.duration_years == 14.0
        assert defined.future_target == 66440975.63
        assert defined.version_metadata["retirement_age"] == 44.0
        assert defined.version_metadata["retirement_years"] == 36.0
        assert defined.funding_return_assumption == 0.08
        assert defined.funding_gap == 66440975.63


class TestFinancialInputValidation:
    def test_percentage_allocation_over_100_is_rejected(self):
        with pytest.raises(ValidationError):
            AssetMappingInput(asset_id="a1", allocation_type="percentage", allocation_value=101)

    def test_expected_return_bounds_are_rejected(self):
        with pytest.raises(ValidationError):
            AssetMappingInput(asset_id="a1", allocation_type="percentage", allocation_value=50, expected_return=1.01)
        with pytest.raises(ValidationError):
            AssetMappingInput(asset_id="a1", allocation_type="percentage", allocation_value=50, expected_return=-1.0)

    def test_invalid_goal_month_and_inflation_are_rejected(self):
        with pytest.raises(ValidationError):
            GoalInput(planning_unit_id="pu", goal_name="Goal", goal_type="General", today_cost=1000, target_month=13, target_year=2030)
        with pytest.raises(ValidationError):
            GoalInput(planning_unit_id="pu", goal_name="Goal", goal_type="General", today_cost=1000, target_month=1, target_year=2030, inflation_rate=1.01)
