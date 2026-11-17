"""
infrastructure/persistence/mappers/action_plan.py
Bi-directional translation for Action Plan items between DB records and Domain entities.
"""

from datetime import date
from decimal import Decimal
from typing import Any, Dict, Optional
from app.domain.features.action_plan.actions import ActionItem, ActionStatus, ActionType
from app.domain.shared.value_objects import Money


def _map_action_type(type_str: str) -> ActionType:
    t_lower = str(type_str).lower()
    for item in ActionType:
        if item.value == t_lower or item.name.lower() == t_lower:
            return item
    return ActionType.START_SIP


def _map_action_status(status_str: str) -> ActionStatus:
    s_lower = str(status_str).lower()
    for item in ActionStatus:
        if item.value == s_lower or item.name.lower() == s_lower:
            return item
    return ActionStatus.PENDING


def map_db_row_to_action_item(row: Dict[str, Any]) -> ActionItem:
    """Map database `action_plan_items` row to Domain ActionItem."""
    target_amt = None
    if row.get("target_amount") is not None:
        target_amt = Money(amount=Decimal(str(row["target_amount"])))

    target_dt = None
    if row.get("target_date"):
        target_dt = date.fromisoformat(str(row["target_date"])[:10])

    status_updated = None
    if row.get("status_updated_at"):
        status_updated = date.fromisoformat(str(row["status_updated_at"])[:10])

    return ActionItem(
        action_id=str(row.get("action_id", row.get("id", ""))),
        investor_id=str(row.get("planning_unit_id", "")),
        plan_id=str(row.get("plan_id", row.get("strategy_version_id", ""))),
        action_type=_map_action_type(row.get("action_type", "start_sip")),
        title=str(row.get("title", row.get("action_name", "Action"))),
        description=str(row.get("description", "")),
        target_amount=target_amt,
        target_date=target_dt,
        status=_map_action_status(row.get("status", "pending")),
        status_updated_at=status_updated,
        completion_notes=row.get("completion_notes"),
    )


def map_action_item_to_dict(item: ActionItem) -> Dict[str, Any]:
    """Convert Domain ActionItem to dictionary for database insertion or update."""
    return {
        "action_id": item.action_id,
        "planning_unit_id": item.investor_id,
        "plan_id": item.plan_id,
        "action_type": item.action_type.value,
        "title": item.title,
        "description": item.description,
        "target_amount": float(item.target_amount.amount) if item.target_amount else None,
        "target_date": item.target_date.isoformat() if item.target_date else None,
        "status": item.status.value,
        "status_updated_at": item.status_updated_at.isoformat() if item.status_updated_at else None,
        "completion_notes": item.completion_notes,
    }
