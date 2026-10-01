from datetime import date
from engines.goal.engine import GoalEngine
from schemas.goals import GoalInput


def _input(**overrides):
    payload = {
        "planning_unit_id": "pu-1",
        "goal_id": "goal-1",
        "goal_name": "Test Goal",
        "goal_type": "Travel",
        "today_cost": 100000,
        "target_month": 12,
        "target_year": 2030,
        "inflation_rate": 0.06,
        "priority": "Important",
        "flexibility": "Flexible",
        "status": "Active",
        "asset_mappings": [],
        "dynamic_details": {},
        "specialized_data": {},
    }
    payload.update(overrides)
    return GoalInput(**payload)


def test_goal_engine_builds_defined_goal():
    goal = GoalEngine().calculate_defined_goal(_input(), {})
    assert goal.goal_id == "goal-1"
    assert goal.future_target > goal.today_cost
    assert goal.duration_years > 0
    assert goal.funding_gap > 0
    assert goal.required_monthly_contribution > 0
    assert goal.funding_status == "Shortfall"


def test_goal_engine_projects_mapped_asset_into_funding_gap():
    goal = GoalEngine().calculate_defined_goal(
        _input(asset_mappings=[{
            "asset_id": "asset-1",
            "allocation_type": "currency",
            "allocation_value": 100000,
            "expected_return": 0.08,
        }]),
        {"asset-1": {"asset_id": "asset-1", "asset_name": "Equity Fund", "current_value": 100000}},
    )
    assert len(goal.mapped_assets) == 1
    assert goal.projected_mapped_asset_value > 100000
    assert goal.funding_return_assumption == 0.08


def test_goal_engine_normalizes_retirement_goal_type():
    goal = GoalEngine().calculate_defined_goal(
        _input(
            goal_name="Retirement",
            goal_type="retirement",
            today_cost=60000,
            target_month=12,
            target_year=date.today().year + 20,
            dynamic_details={"currentAge": 30, "lifeExpectancy": 85},
        ),
        {},
    )
    assert goal.future_target > 0
    assert goal.version_metadata["funding_model"] == "retirement_corpus_plus_monthly_contribution"
    assert goal.version_metadata["retirement_years"] > 0
