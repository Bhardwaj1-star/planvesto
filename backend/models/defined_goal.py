from typing import Any, Literal
from pydantic import BaseModel, Field, model_validator
from models.orchestration import WorkflowReadiness


class DefinedGoalAssetMapping(BaseModel):
    mapping_id: str | None = None
    defined_goal_id: str | None = None
    asset_id: str
    asset_name: str | None = None
    allocation_type: Literal["currency", "percentage"]
    allocation_value: float
    allocated_amount: float
    allocated_percentage: float
    expected_return: float
    return_frequency: str = "annual"
    projected_value: float
    created_at: str | None = None


class DefinedGoal(BaseModel):
    defined_goal_id: str | None = None
    goal_id: str
    planning_unit_id: str
    investor_id: str | None = None
    version: int = 1
    is_latest: bool = True
    goal_type: str
    goal_name: str
    today_cost: float
    inflation_rate: float
    inflation_source: str = "default"
    target_month: int
    target_year: int
    duration_years: float
    future_target: float
    priority: str
    flexibility: str
    status: str = "Active"
    mapped_assets: list[DefinedGoalAssetMapping] = Field(default_factory=list)
    projected_mapped_asset_value: float = 0.0
    funding_gap: float
    funding_status: Literal["Shortfall", "On Track", "Overfunded"]
    required_monthly_contribution: float = 0.0
    funding_return_assumption: float = 0.08
    feasibility_status: Literal["feasible", "constrained", "infeasible", "unknown"] = "unknown"
    workflow_readiness: WorkflowReadiness | None = None
    available_monthly_surplus: float | None = None
    monthly_contribution_surplus_gap: float | None = None
    feasibility_reason: str | None = None
    funding_strategies: list[dict[str, Any]] = Field(default_factory=list)
    version_metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = None

    @model_validator(mode="before")
    @classmethod
    def hydrate_workflow_readiness(cls, value):
        if isinstance(value, dict) and "workflow_readiness" not in value:
            metadata = value.get("version_metadata") or {}
            if isinstance(metadata, dict) and metadata.get("workflow_readiness"):
                return {**value, "workflow_readiness": metadata["workflow_readiness"]}
        return value


class DefinedGoalVersionSummary(BaseModel):
    defined_goal_id: str
    goal_id: str
    version: int
    is_latest: bool
    today_cost: float
    future_target: float
    projected_mapped_asset_value: float
    funding_gap: float
    funding_status: str
    feasibility_status: str = "unknown"
    feasibility_reason: str | None = None
    created_at: str
