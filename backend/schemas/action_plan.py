from typing import Any

from pydantic import BaseModel, Field

from models.action_plan import ActionImpactPreview


class ActionCreateRequest(BaseModel):
    planning_unit_id: str
    strategy_version_id: str
    title: str
    description: str | None = None
    priority: str = "medium"
    deadline: str | None = None
    planned_impact: dict[str, Any] = Field(default_factory=dict)


class ActionDecisionRequest(BaseModel):
    planning_unit_id: str
    action_id: str
    decision: str
    impact_preview: ActionImpactPreview
    after_state: dict[str, Any] = Field(default_factory=dict)


class ActionDecisionResponse(BaseModel):
    decision_id: str | None = None
    action_id: str
    decision: str
    confirmed_at: str
    historical: bool
