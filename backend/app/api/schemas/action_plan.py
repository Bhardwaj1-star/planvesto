"""
api/schemas/action_plan.py
Transport schemas for Action Plan endpoints.
"""

from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class ActionCreateRequest(BaseModel):
    planning_unit_id: str
    plan_id: str
    action_type: str
    title: str
    description: str
    target_amount: Optional[Decimal] = None
    target_date: Optional[str] = None


class ActionStatusUpdateRequest(BaseModel):
    planning_unit_id: str
    new_status: str
    notes: Optional[str] = None


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
