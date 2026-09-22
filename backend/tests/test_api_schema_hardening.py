import math

import pytest
from pydantic import ValidationError

from models.moneywheel import MoneywheelInput
from schemas.action_plan import ActionCreateRequest
from schemas.goals import GoalInput
from schemas.orchestration import PlanningOrchestrationRequest
from schemas.strategy import CustomScenarioRequest, StrategySelectRequest
from models.strategy_edit import StrategyEditRequest


def test_request_schemas_reject_unknown_fields():
    with pytest.raises(ValidationError):
        GoalInput(
            planning_unit_id="pu-1",
            goal_name="Goal",
            goal_type="General",
            today_cost=1000,
            target_month=1,
            target_year=2030,
            unexpected="should be rejected",
        )

    with pytest.raises(ValidationError):
        StrategySelectRequest(
            planning_unit_id="pu-1",
            strategy_run_id="run-1",
            selected_strategy_id="strategy-1",
            selected_scenario_id="scenario-1",
            unexpected="should be rejected",
        )


def test_financial_inputs_reject_non_finite_values():
    with pytest.raises(ValidationError):
        GoalInput(
            planning_unit_id="pu-1",
            goal_name="Goal",
            goal_type="General",
            today_cost=math.inf,
            target_month=1,
            target_year=2030,
        )

    with pytest.raises(ValidationError):
        MoneywheelInput(planning_unit_id="pu-1", total_assets=math.nan)


def test_request_collection_sizes_are_bounded():
    with pytest.raises(ValidationError):
        PlanningOrchestrationRequest(
            planning_unit_id="pu-1",
            goal_version_ids=[f"goal-{i}" for i in range(101)],
        )

    with pytest.raises(ValidationError):
        CustomScenarioRequest(
            planning_unit_id="pu-1",
            strategy_run_id="run-1",
            strategy_id="strategy-1",
            scenario_name="Custom",
            assumptions={str(i): i for i in range(51)},
        )


def test_action_and_strategy_edit_text_and_parameter_sizes_are_bounded():
    with pytest.raises(ValidationError):
        ActionCreateRequest(
            planning_unit_id="pu-1",
            strategy_version_id="version-1",
            title="x" * 201,
        )

    with pytest.raises(ValidationError):
        StrategyEditRequest(
            planning_unit_id="pu-1",
            strategy_id="strategy-1",
            parent_version=1,
            implementation_parameters={str(i): i for i in range(101)},
        )
