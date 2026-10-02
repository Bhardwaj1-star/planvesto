from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


def _validate_internal_route(route: str) -> str:
    if not route.startswith("/") or route.startswith("//") or "\\" in route:
        raise ValueError("route must be an absolute path on this application")
    return route


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


class WorkflowNextAction(BaseModel):
    label: str
    route: str

    @field_validator("route")
    @classmethod
    def route_must_be_internal(cls, route: str) -> str:
        return _validate_internal_route(route)


class WorkflowMissingData(BaseModel):
    label: str
    route: str | None = None

    @field_validator("route")
    @classmethod
    def route_must_be_internal(cls, route: str | None) -> str | None:
        return _validate_internal_route(route) if route is not None else None


class WorkflowPrerequisite(BaseModel):
    key: str
    availability: ModuleAvailability
    missing_data: list[WorkflowMissingData] = Field(default_factory=list)
    next_action: WorkflowNextAction | None = None


class WorkflowBlocker(BaseModel):
    key: str
    reason: str | None = None
    missing_data: list[WorkflowMissingData] = Field(default_factory=list)
    next_action: WorkflowNextAction | None = None


class WorkflowReadiness(BaseModel):
    status: Literal["ready", "blocked"]
    process_route: str
    blockers: list[WorkflowBlocker] = Field(default_factory=list)
    next_action: WorkflowNextAction | None = None
    return_to: str

    @field_validator("process_route", "return_to")
    @classmethod
    def routes_must_be_internal(cls, route: str) -> str:
        return _validate_internal_route(route)


class PlanningOrchestrationContext(BaseModel):
    planning_context: PlanningContext
    financial_state: ModuleAvailability
    goals: ModuleAvailability
    strategy: ModuleAvailability
    moneywheel: ModuleAvailability
    action_plan: ModuleAvailability
    metadata: dict[str, Any] = Field(default_factory=dict)
