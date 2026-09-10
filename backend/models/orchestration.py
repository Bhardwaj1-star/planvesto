from typing import Any, Literal

from pydantic import BaseModel, Field


class PlanningContext(BaseModel):
    planning_unit_id: str
    scope: Literal["family", "individual"]
    investor_id: str | None = None
    financial_state_snapshot_id: str | None = None
    goal_version_ids: list[str] = Field(default_factory=list)
    strategy_version_id: str | None = None


class ModuleAvailability(BaseModel):
    available: bool
    reason: str | None = None


class PlanningOrchestrationContext(BaseModel):
    planning_context: PlanningContext
    financial_state: ModuleAvailability
    goals: ModuleAvailability
    strategy: ModuleAvailability
    moneywheel: ModuleAvailability
    action_plan: ModuleAvailability
    metadata: dict[str, Any] = Field(default_factory=dict)
