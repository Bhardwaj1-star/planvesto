from typing import Any

from pydantic import Field
from models.action_plan import ActionImpactPreview
from schemas.base import StrictRequestModel


class ActionCreateRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    strategy_version_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    priority: str = Field(default="medium", min_length=1, max_length=20)
    deadline: str | None = Field(default=None, max_length=100)
    planned_impact: dict[str, Any] = Field(default_factory=dict, max_length=50)


class ActionDecisionRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    action_id: str = Field(min_length=1, max_length=100)
    decision: str = Field(min_length=1, max_length=30)
    impact_preview: ActionImpactPreview
    after_state: dict[str, Any] = Field(default_factory=dict, max_length=50)


class ActionCompletionRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    action_id: str = Field(min_length=1, max_length=100)
    actual_state: dict[str, Any] = Field(max_length=100)
    completion_preview: ActionImpactPreview

class ActionDecisionResponse(StrictRequestModel):
    decision_id: str | None = None
    action_id: str
    decision: str
    confirmed_at: str
    historical: bool
