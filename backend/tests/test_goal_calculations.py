from datetime import date
import pytest
from engines.goal.target_calculator import (
    calculate_duration,
    calculate_future_target,
    DEFAULT_INFLATION_RATE,
)
from engines.goal.asset_projection import (
    calculate_asset_projection,
    get_default_expected_return,
    get_compounding_frequency,
)
from engines.goal.funding_gap import calculate_funding_gap
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
        # 100,000 at 6% for 5 years = 100000 * 1.06^5 = 133822.56
        future = calculate_future_target(100000.0, 0.06, 5.0)
        assert future == 133822.56

    def test_future_target_zero_cost(self):
        assert calculate_future_target(0.0, 0.06, 5.0) == 0.0


class TestAssetProjection:
    def test_percentage_allocation(self):
        # Current value 1,000,000; 50% allocated; 12% expected return; 5 years annual compounding
        # 500,000 * (1.12)^5 = 500,000 * 1.76234168 = 881170.84
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
        # Current value 1,000,000; Rs 200,000 allocated; 10% expected return; 3 years
        # 200,000 * (1.10)^3 = 200,000 * 1.331 = 266200.0
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
        # 100,000 at 12% monthly compounding for 1 year
        # 100,000 * (1 + 0.01)^12 = 112682.50
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
        # Asset total 10L
        # Goal 1 takes 30% = 3L
        amt1, pct1, _ = calculate_asset_projection(1000000, "percentage", 30.0, 0.1, "annual", 5)
        # Goal 2 takes 40% = 4L
        amt2, pct2, _ = calculate_asset_projection(1000000, "percentage", 40.0, 0.1, "annual", 5)
        assert amt1 + amt2 == 700000.0

    def test_missing_expected_return_uses_default(self):
        ret_mf = get_default_expected_return("HDFC Equity Mutual Funds")
        assert ret_mf == 0.12
        ret_bank = get_default_expected_return("Savings Bank Account")
        assert ret_bank == 0.04
        ret_fallback = get_default_expected_return("Unknown Exotic Asset")
        assert ret_fallback == 0.08


class TestFundingGap:
    def test_shortfall(self):
        gap, status = calculate_funding_gap(future_target=500000.0, projected_mapped_asset_value=300000.0)
        assert gap == 200000.0
        assert status == "Shortfall"

    def test_on_track(self):
        gap, status = calculate_funding_gap(future_target=500000.0, projected_mapped_asset_value=500000.0)
        assert gap == 0.0
        assert status == "On Track"

    def test_overfunded(self):
        gap, status = calculate_funding_gap(future_target=500000.0, projected_mapped_asset_value=650000.0)
        assert gap == -150000.0
        assert status == "Overfunded"


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
        assets = {
            "a1": {"asset_name": "Equity Mutual Fund", "current_value": 800000.0}
        }
        defined = engine.calculate_defined_goal(inp, assets, version=1, reference_date=ref)

        assert defined.duration_years == 5.0
        assert defined.future_target == 1338225.58
        assert len(defined.mapped_assets) == 1
        # 400,000 * 1.12^5 = 704936.67
        assert defined.mapped_assets[0].allocated_amount == 400000.0
        assert defined.mapped_assets[0].projected_value == 704936.67
        assert defined.projected_mapped_asset_value == 704936.67
        assert defined.funding_gap == 633288.91
        assert defined.funding_status == "Shortfall"


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
