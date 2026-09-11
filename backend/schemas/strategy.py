from typing import Any
from pydantic import BaseModel, Field
from models.strategy import InvestorPriorities
from models.strategy_approval import SuitabilityAssessment


class StrategyBuildRequest(BaseModel):
    planning_unit_id: str
    goal_id: str
    investor_priorities: InvestorPriorities | None = None


class CustomScenarioRequest(BaseModel):
    planning_unit_id: str
    strategy_run_id: str
    strategy_id: str
    scenario_name: str
    assumptions: dict[str, Any] = Field(default_factory=dict)
    funding_structure: dict[str, Any] = Field(default_factory=dict)


class PriorityWeightsRequest(BaseModel):
    planning_unit_id: str
    strategy_run_id: str
    priorities: InvestorPriorities


class StrategySelectRequest(BaseModel):
    planning_unit_id: str
    strategy_run_id: str
    selected_strategy_id: str
    selected_scenario_id: str
    selected_architecture_id: str | None = None
    selected_implementation_parameters: dict[str, Any] = Field(default_factory=dict)


class StrategyApprovalRequest(BaseModel):
    planning_unit_id: str
    strategy_run_id: str
    suitability: SuitabilityAssessment
    acknowledgement_text: str | None = None
    make_primary: bool = False
    primary_transition_decision: str | None = None
    pending_action_disposition: str | None = None
