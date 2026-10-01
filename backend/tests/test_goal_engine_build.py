from datetime import date

from engines.goal.engine import GoalEngine
from schemas.goals import GoalInput


GOAL_TYPES = [
    "Vacation",
    "Home Purchase",
    "Retirement / Financial Freedom",
    "Child Education",
    "Marriage",
    "Vehicle",
]


def _input(goal_type: str, **overrides):
    payload = {
        "planning_unit_id": "pu-1",
        "goal_id": f"goal-{goal_type.lower().replace(' ', '-')}",
        "goal_name": goal_type,
        "goal_type": goal_type,
        "today_cost": 100000,
        "target_month": 12,
        "target_year": date.today().year + 5,
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


def test_all_planned_goal_types_use_the_same_generic_engine():
    for goal_type in GOAL_TYPES:
        goal = GoalEngine().calculate_defined_goal(_input(goal_type), {})
        assert goal.goal_type == goal_type
        assert goal.future_target > goal.today_cost
        assert goal.duration_years > 0
        assert goal.funding_gap > 0
        assert goal.required_monthly_contribution > 0
        assert goal.version_metadata["funding_model"] == "target_gap_plus_monthly_contribution"


def test_goal_engine_projects_mapped_asset_into_funding_gap():
    goal = GoalEngine().calculate_defined_goal(
        _input(
            "Home Purchase",
            asset_mappings=[
                {
                    "asset_id": "asset-1",
                    "allocation_type": "currency",
                    "allocation_value": 100000,
                    "expected_return": 0.08,
                }
            ],
        ),
        {"asset-1": {"asset_id": "asset-1", "asset_name": "Equity Fund", "current_value": 100000}},
    )
    assert len(goal.mapped_assets) == 1
    assert goal.projected_mapped_asset_value > 100000
    assert goal.funding_return_assumption == 0.08
