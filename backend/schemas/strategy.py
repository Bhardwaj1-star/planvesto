from typing import Any

from pydantic import Field
from models.strategy import InvestorPriorities
from schemas.base import StrictRequestModel


class StrategyBuildRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    goal_id: str = Field(min_length=1, max_length=100)
    investor_priorities: InvestorPriorities | None = None


class FinancialPlanBuildRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
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


class GoalDecisionReport(StrictRequestModel):
    """Canonical typed contract for the Goal Decision Report."""
    model_config = {"extra": "ignore"}

    report_type: str = "goal_decision_report"
    report_version: str = "1.0"
    goal: dict[str, Any]
    financial_state: dict[str, Any]
    goal_calculation: dict[str, Any]
    feasibility: dict[str, Any]
    strategy: dict[str, Any]
    decision: dict[str, Any]
    provenance: dict[str, Any]
    funding_solutions: list[dict[str, Any]] = Field(default_factory=list)
    alternatives: list[dict[str, Any]] = Field(default_factory=list)
    scenarios: list[dict[str, Any]] = Field(default_factory=list)
    what_if_analysis: list[dict[str, Any]] = Field(default_factory=list)
    trade_off_analysis: list[dict[str, Any]] = Field(default_factory=list)
    technique_execution: list[dict[str, Any]] = Field(default_factory=list)
    assumptions: dict[str, Any] = Field(default_factory=dict)
    cash_flow_trajectory: list[dict[str, Any]] = Field(default_factory=list)
    contribution_rules: list[str] = Field(default_factory=list)
    product_architecture: list[dict[str, Any]] = Field(default_factory=list)
    action_plan_timeline: list[dict[str, Any]] = Field(default_factory=list)
    contingency_matrix: list[dict[str, Any]] = Field(default_factory=list)
    mapped_assets: list[dict[str, Any]] = Field(default_factory=list)
    investor_priorities: dict[str, Any] = Field(default_factory=dict)
    goal_funding: dict[str, Any] | None = None
    goal_context: dict[str, Any] | None = None

