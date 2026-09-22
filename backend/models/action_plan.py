from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


ActionStatus = Literal["planned", "confirmed", "completed", "cancelled"]
ActionDecision = Literal["add", "modify", "delete", "complete", "cancel"]


class ActionPlanItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action_id: str | None = None
    planning_unit_id: str = Field(min_length=1, max_length=100)
    strategy_version_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    priority: Literal["high", "medium", "low"] = "medium"
    deadline: str | None = Field(default=None, max_length=100)
    status: ActionStatus = "planned"
    planned_impact: dict[str, Any] = Field(default_factory=dict, max_length=50)
    actual_impact: dict[str, Any] = Field(default_factory=dict, max_length=50)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @model_validator(mode="after")
    def validate_required_fields(self) -> "ActionPlanItem":
        return self


class ActionImpactPreview(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: dict[str, Any] = Field(max_length=50)
    financial_state_impact: dict[str, Any] = Field(default_factory=dict, max_length=50)
    goal_impacts: list[dict[str, Any]] = Field(default_factory=list, max_length=100)
    strategy_impact: dict[str, Any] = Field(default_factory=dict, max_length=50)
    financial_health_impact: dict[str, Any] = Field(default_factory=dict, max_length=50)
    alternatives: list[dict[str, Any]] = Field(default_factory=list, max_length=50)
    cause_explanation: str | None = Field(default=None, max_length=5000)


class ActionDecisionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decision_id: str | None = None
    planning_unit_id: str = Field(min_length=1, max_length=100)
    action_id: str = Field(min_length=1, max_length=100)
    decision: ActionDecision
    before_state: dict[str, Any] = Field(default_factory=dict, max_length=50)
    after_state: dict[str, Any] = Field(default_factory=dict, max_length=50)
    impact_preview: ActionImpactPreview
    confirmed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    historical: bool = True
