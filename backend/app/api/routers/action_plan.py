"""
api/routers/action_plan.py
FastAPI router for Action Plan endpoints.
"""

from datetime import date
from decimal import Decimal
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_current_user_id
from app.api.schemas.action_plan import (
    ActionCreateRequest,
    ActionStatusUpdateRequest,
    ActionItemResponse,
)
from app.domain.shared.value_objects import Money
from app.domain.features.action_plan import (
    ActionType,
    ActionStatus,
    ActionItem,
    transition_action_status,
)

router = APIRouter(tags=["Action Plan"])


@router.post("/actions", response_model=ActionItemResponse)
@router.post("/api/action-plan/actions", response_model=ActionItemResponse, include_in_schema=False)
def create_action_item(
    request: ActionCreateRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Creates a new action item derived from an accepted plan."""
    action_id = f"act_{uuid.uuid4().hex[:8]}"

    # Resolve ActionType
    resolved_type = ActionType.START_SIP
    for t in ActionType:
        if t.value == request.action_type:
            resolved_type = t
            break

    target_amt = Money.from_amount(request.target_amount) if request.target_amount else None
    target_dt = date.fromisoformat(request.target_date) if request.target_date else None

    action = ActionItem(
        action_id=action_id,
        investor_id=user_id,
        plan_id=request.plan_id,
        action_type=resolved_type,
        title=request.title,
        description=request.description,
        target_amount=target_amt,
        target_date=target_dt,
        status=ActionStatus.PENDING,
        status_updated_at=date.today(),
    )

    return ActionItemResponse(
        action_id=action.action_id,
        investor_id=action.investor_id,
        plan_id=action.plan_id,
        action_type=action.action_type.value,
        title=action.title,
        description=action.description,
        target_amount=action.target_amount.amount if action.target_amount else None,
        target_date=action.target_date.isoformat() if action.target_date else None,
        status=action.status.value,
        status_updated_at=action.status_updated_at.isoformat() if action.status_updated_at else None,
        completion_notes=action.completion_notes,
    )
