"""
api/schemas/action_plan.py
Transport schemas for Action Plan endpoints.
"""

from decimal import Decimal
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class ActionCreateRequest(BaseModel):
    planning_unit_id: str
    plan_id: Optional[str] = None
    strategy_version_id: Optional[str] = None
    action_type: Optional[str] = "start_sip"
    title: str
    description: Optional[str] = None
    priority: Optional[Literal["high", "medium", "low"]] = "medium"
    deadline: Optional[str] = None
    target_amount: Optional[Decimal] = None
    target_date: Optional[str] = None
    planned_impact: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ActionPlanItemSchema(BaseModel):
    action_id: Optional[str] = None
    planning_unit_id: str
    strategy_version_id: Optional[str] = "sv_default"
    plan_id: Optional[str] = None
    action_type: Optional[str] = "start_sip"
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    deadline: Optional[str] = None
    status: str = "planned"
    planned_impact: Dict[str, Any] = Field(default_factory=dict)
    actual_impact: Dict[str, Any] = Field(default_factory=dict)
    created_at: str


class ActionStatusUpdateRequest(BaseModel):
    planning_unit_id: str
    new_status: str
    notes: Optional[str] = None


class ActionCompletionRequest(BaseModel):
    planning_unit_id: str
    action_id: str
    actual_state: Dict[str, Any] = Field(default_factory=dict)
    completion_preview: Dict[str, Any] = Field(default_factory=dict)


class ActionDecisionInput(BaseModel):
    planning_unit_id: str
    action_id: str
    decision: Literal["add", "modify", "delete", "complete", "cancel"]
    impact_preview: Dict[str, Any] = Field(default_factory=dict)
    after_state: Dict[str, Any] = Field(default_factory=dict)


class ActionDecisionResponse(BaseModel):
    decision_id: Optional[str] = None
    action_id: str
    decision: str
    confirmed_at: str
    historical: bool = True


class ActionDecisionRecord(BaseModel):
    decision_id: Optional[str] = None
    planning_unit_id: str
    action_id: str
    decision: str
    before_state: Dict[str, Any] = Field(default_factory=dict)
    after_state: Dict[str, Any] = Field(default_factory=dict)
    impact_preview: Dict[str, Any] = Field(default_factory=dict)
    confirmed_at: str
    historical: bool = True


class ActionItemResponse(BaseModel):
    action_id: str
    investor_id: str
    plan_id: str
    action_type: str
    title: str
    description: str
    target_amount: Optional[Decimal] = None
    target_date: Optional[str] = None
    status: str
    status_updated_at: Optional[str] = None
    completion_notes: Optional[str] = None
