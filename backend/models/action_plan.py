from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


ActionStatus = Literal["planned", "confirmed", "completed", "cancelled"]
ActionDecision = Literal["add", "modify", "delete", "complete", "cancel"]


class ActionPlanItem(BaseModel):
    action_id: str | None = None
    planning_unit_id: str
    strategy_version_id: str
    title: str
    description: str | None = None
    priority: Literal["high", "medium", "low"] = "medium"
    deadline: str | None = None
    status: ActionStatus = "planned"
    planned_impact: dict[str, Any] = Field(default_factory=dict)
    actual_impact: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @model_validator(mode="after")
    def validate_required_fields(self) -> "ActionPlanItem":
        if not self.planning_unit_id.strip():
            raise ValueError("planning_unit_id cannot be empty")
        if not self.strategy_version_id.strip():
            raise ValueError("strategy_version_id cannot be empty")
        if not self.title.strip():
            raise ValueError("title cannot be empty")
        return self


class ActionImpactPreview(BaseModel):
    action: dict[str, Any]
    financial_state_impact: dict[str, Any] = Field(default_factory=dict)
    goal_impacts: list[dict[str, Any]] = Field(default_factory=list)
    strategy_impact: dict[str, Any] = Field(default_factory=dict)
    financial_health_impact: dict[str, Any] = Field(default_factory=dict)
    alternatives: list[dict[str, Any]] = Field(default_factory=list)
    cause_explanation: str | None = None


class ActionDecisionRecord(BaseModel):
    decision_id: str | None = None
    planning_unit_id: str
    action_id: str
    decision: ActionDecision
    before_state: dict[str, Any] = Field(default_factory=dict)
    after_state: dict[str, Any] = Field(default_factory=dict)
    impact_preview: ActionImpactPreview
    confirmed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    historical: bool = True
