"""
domain/features/action_plan/lifecycle.py
Chapter 13 — Action Plan Lifecycle & Status Transitions (§13.3).

Validates state transitions of action items.
Transitions must be explicitly confirmed by the investor.
"""

from datetime import date
from typing import Optional
from app.domain.features.action_plan.actions import ActionItem, ActionStatus


ALLOWED_TRANSITIONS = {
    ActionStatus.PENDING: {ActionStatus.IN_PROGRESS, ActionStatus.COMPLETED, ActionStatus.DEFERRED, ActionStatus.CANCELLED},
    ActionStatus.IN_PROGRESS: {ActionStatus.COMPLETED, ActionStatus.DEFERRED, ActionStatus.CANCELLED},
    ActionStatus.DEFERRED: {ActionStatus.PENDING, ActionStatus.IN_PROGRESS, ActionStatus.CANCELLED},
    ActionStatus.COMPLETED: set(),  # Terminal state
    ActionStatus.CANCELLED: {ActionStatus.PENDING},  # Can be reopened
}


def transition_action_status(
    action: ActionItem,
    new_status: ActionStatus,
    as_of_date: date,
    notes: Optional[str] = None,
) -> ActionItem:
    """
    Applies an approved state transition to an action item.
    Raises ValueError if transition is invalid.
    """
    allowed = ALLOWED_TRANSITIONS.get(action.status, set())
    if new_status not in allowed:
        raise ValueError(f"Invalid transition from {action.status.value} to {new_status.value}.")

    return ActionItem(
        action_id=action.action_id,
        investor_id=action.investor_id,
        plan_id=action.plan_id,
        action_type=action.action_type,
        title=action.title,
        description=action.description,
        target_amount=action.target_amount,
        target_date=action.target_date,
        status=new_status,
        status_updated_at=as_of_date,
        completion_notes=notes or action.completion_notes,
    )
