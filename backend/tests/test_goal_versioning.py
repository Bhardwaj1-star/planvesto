import pytest
from models.defined_goal import DefinedGoal, DefinedGoalAssetMapping
from schemas.goals import GoalInput, AssetMappingInput
from data.goal_repository import GoalRepository


class TestGoalVersioningLogic:
    def test_detects_today_cost_material_change(self):
        repo = GoalRepository()
        current = DefinedGoal(
            goal_id="g1",
            planning_unit_id="pu1",
            version=1,
            is_latest=True,
            goal_type="Child Education",
            goal_name="College",
            today_cost=500000.0,
            inflation_rate=0.06,
            target_month=6,
            target_year=2030,
            duration_years=4.5,
            future_target=650000.0,
            priority="Critical",
            flexibility="Fixed",
            funding_gap=650000.0,
            funding_status="Shortfall",
        )
        new_in = GoalInput(
            planning_unit_id="pu1",
            goal_id="g1",
            goal_name="College",
            goal_type="Child Education",
            today_cost=600000.0,  # Changed
            target_month=6,
            target_year=2030,
        )
        assert repo.has_material_change(current, new_in) is True

    def test_detects_target_date_material_change(self):
        repo = GoalRepository()
        current = DefinedGoal(
            goal_id="g1",
            planning_unit_id="pu1",
            version=1,
            is_latest=True,
            goal_type="Travel",
            goal_name="Euro Trip",
            today_cost=300000.0,
            inflation_rate=0.06,
            target_month=5,
            target_year=2028,
            duration_years=2.0,
            future_target=337000.0,
            priority="Aspirational",
            flexibility="Flexible",
            funding_gap=337000.0,
            funding_status="Shortfall",
        )
        new_in = GoalInput(
            planning_unit_id="pu1",
            goal_id="g1",
            goal_name="Euro Trip",
            goal_type="Travel",
            today_cost=300000.0,
            target_month=12,  # Changed month
            target_year=2028,
        )
        assert repo.has_material_change(current, new_in) is True

    def test_detects_mapped_asset_material_change(self):
        repo = GoalRepository()
        current = DefinedGoal(
            goal_id="g1",
            planning_unit_id="pu1",
            version=1,
            is_latest=True,
            goal_type="Home Purchase",
            goal_name="Dream House",
            today_cost=5000000.0,
            inflation_rate=0.06,
            target_month=1,
            target_year=2035,
            duration_years=9.0,
            future_target=8447395.0,
            priority="Critical",
            flexibility="Fixed",
            funding_gap=5000000.0,
            funding_status="Shortfall",
            mapped_assets=[
                DefinedGoalAssetMapping(
                    asset_id="a1",
                    allocation_type="percentage",
                    allocation_value=50.0,
                    allocated_amount=500000.0,
                    allocated_percentage=50.0,
                    expected_return=0.10,
                    projected_value=1178974.0,
                )
            ],
        )
        # Change allocation percentage from 50% to 70%
        new_in = GoalInput(
            planning_unit_id="pu1",
            goal_id="g1",
            goal_name="Dream House",
            goal_type="Home Purchase",
            today_cost=5000000.0,
            target_month=1,
            target_year=2035,
            asset_mappings=[
                AssetMappingInput(
                    asset_id="a1",
                    allocation_type="percentage",
                    allocation_value=70.0,
                )
            ],
        )
        assert repo.has_material_change(current, new_in) is True

    def test_no_material_change_when_inputs_match(self):
        repo = GoalRepository()
        current = DefinedGoal(
            goal_id="g1",
            planning_unit_id="pu1",
            version=1,
            is_latest=True,
            goal_type="Vehicle",
            goal_name="Car",
            today_cost=800000.0,
            inflation_rate=0.06,
            target_month=10,
            target_year=2028,
            duration_years=2.75,
            future_target=939000.0,
            priority="Important",
            flexibility="Flexible",
            funding_gap=939000.0,
            funding_status="Shortfall",
            mapped_assets=[
                DefinedGoalAssetMapping(
                    asset_id="a1",
                    allocation_type="currency",
                    allocation_value=200000.0,
                    allocated_amount=200000.0,
                    allocated_percentage=25.0,
                    expected_return=0.07,
                    projected_value=240000.0,
                )
            ],
        )
        same_in = GoalInput(
            planning_unit_id="pu1",
            goal_id="g1",
            goal_name="Car",
            goal_type="Vehicle",
            today_cost=800000.0,
            target_month=10,
            target_year=2028,
            asset_mappings=[
                AssetMappingInput(
                    asset_id="a1",
                    allocation_type="currency",
                    allocation_value=200000.0,
                )
            ],
        )
        assert repo.has_material_change(current, same_in) is False
