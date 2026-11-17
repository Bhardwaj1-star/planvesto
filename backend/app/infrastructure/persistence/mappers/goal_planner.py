"""
infrastructure/persistence/mappers/goal_planner.py
Bi-directional translation between Supabase/Postgres goals & defined_goals and Domain Goal entities.
"""

from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional

from app.domain.canonical.goal_taxonomy import CanonicalGoalId
from app.domain.features.goal_planner.requirement import (
    GoalInstance,
    GoalRequirementOutput,
)
from app.domain.shared.value_objects import Money, Rate


def _map_canonical_goal_id(goal_name_or_id: str) -> CanonicalGoalId:
    name_lower = str(goal_name_or_id).lower()
    for gid in CanonicalGoalId:
        if gid.value == name_lower or gid.name.lower() in name_lower:
            return gid
    if "retire" in name_lower:
        return CanonicalGoalId.RETIREMENT
    if "marri" in name_lower or "wedding" in name_lower:
        return CanonicalGoalId.MARRIAGE
    if "car" in name_lower or "vehic" in name_lower:
        return CanonicalGoalId.VEHICLE
    if "home" in name_lower or "house" in name_lower:
        return CanonicalGoalId.DREAM_HOME
    if "edu" in name_lower or "college" in name_lower or "school" in name_lower:
        return CanonicalGoalId.EDUCATION
    if "vacat" in name_lower or "travel" in name_lower:
        return CanonicalGoalId.VACATION
    if "debt" in name_lower:
        return CanonicalGoalId.DEBT_FREEDOM
    if "wealth" in name_lower:
        return CanonicalGoalId.WEALTH_CREATION
    if "fire" in name_lower:
        return CanonicalGoalId.FIRE_PASSIVE_INCOME
    return CanonicalGoalId.OTHERS


def map_db_row_to_goal_instance(
    row: Dict[str, Any],
    inflation_rate: Optional[Rate] = None,
    expected_return: Optional[Rate] = None,
) -> GoalInstance:
    """Map raw database `goals` row to domain `GoalInstance`."""
    target_date_val = row.get("target_date")
    if isinstance(target_date_val, str):
        target_date = date.fromisoformat(target_date_val)
    elif isinstance(target_date_val, date):
        target_date = target_date_val
    else:
        target_date = date.today()

    current_cost = Money(amount=Decimal(str(row.get("target_amount", row.get("today_cost", 0)))))
    canonical_id = _map_canonical_goal_id(row.get("goal_name", "goal_others"))

    created_at_val = row.get("created_at")
    if isinstance(created_at_val, str):
        created_at = date.fromisoformat(created_at_val[:10])
    elif isinstance(created_at_val, date):
        created_at = created_at_val
    else:
        created_at = date.today()

    return GoalInstance(
        id=str(row.get("goal_id", row.get("id", ""))),
        investor_id=str(row.get("planning_unit_id", "")),
        canonical_id=canonical_id,
        name=str(row.get("goal_name", "Goal")),
        target_date=target_date,
        current_cost=current_cost,
        applicable_inflation_rate=inflation_rate or Rate.from_percentage("6.0"),
        expected_annual_return=expected_return or Rate.from_percentage("10.0"),
        created_at=created_at,
        priority=int(row.get("priority", 1)) if str(row.get("priority", "")).isdigit() else 1,
        notes=row.get("notes"),
    )


def map_goal_instance_to_persistence_dict(goal: GoalInstance) -> Dict[str, Any]:
    """Convert domain `GoalInstance` to payload for inserting/updating `goals` table."""
    return {
        "goal_id": goal.id,
        "planning_unit_id": goal.investor_id,
        "goal_name": goal.name,
        "target_amount": float(goal.current_cost.amount),
        "target_date": goal.target_date.isoformat(),
        "priority": str(goal.priority),
        "flexibility": "Flexible",
    }


def map_requirement_to_defined_goal_dict(
    goal: GoalInstance,
    requirement: GoalRequirementOutput,
    version: int = 1,
    is_latest: bool = True,
) -> Dict[str, Any]:
    """Map domain `GoalRequirementOutput` to `defined_goals` persistence schema."""
    return {
        "goal_id": goal.id,
        "planning_unit_id": goal.investor_id,
        "version": version,
        "is_latest": is_latest,
        "today_cost": float(goal.current_cost.amount),
        "future_target": float(requirement.future_goal_target.amount),
        "projected_mapped_asset_value": float(requirement.projected_existing_funding.amount),
        "funding_gap": float(requirement.funding_gap.amount),
        "funding_status": "funded" if requirement.funding_gap.amount <= 0 else "gap",
        "version_metadata": {
            "inflation_rate": str(goal.applicable_inflation_rate.percentage),
            "expected_annual_return": str(goal.expected_annual_return.percentage),
            "months_horizon": requirement.months_horizon,
            "duration_years": str(requirement.duration_years),
            "required_return": str(requirement.required_return.percentage) if requirement.required_return else None,
        },
    }
