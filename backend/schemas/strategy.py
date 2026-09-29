from typing import Any

from pydantic import Field
from models.strategy import InvestorPriorities
from schemas.base import StrictRequestModel


class StrategyBuildRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    goal_id: str = Field(min_length=1, max_length=100)
    investor_priorities: InvestorPriorities | None = None


class CustomScenarioRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    strategy_run_id: str = Field(min_length=1, max_length=100)
    strategy_id: str = Field(min_length=1, max_length=100)
    scenario_name: str = Field(min_length=1, max_length=100)
    assumptions: dict[str, Any] = Field(default_factory=dict, max_length=50)
    funding_structure: dict[str, Any] = Field(default_factory=dict, max_length=50)


class PriorityWeightsRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    strategy_run_id: str = Field(min_length=1, max_length=100)
    priorities: InvestorPriorities


class StrategySelectRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    strategy_run_id: str = Field(min_length=1, max_length=100)
    selected_strategy_id: str = Field(min_length=1, max_length=100)
    selected_scenario_id: str = Field(min_length=1, max_length=100)
    selected_architecture_id: str | None = Field(default=None, min_length=1, max_length=100)
    selected_implementation_parameters: dict[str, Any] = Field(default_factory=dict, max_length=100)
