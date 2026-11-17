"""Investor/record ownership checks and permission enforcement before protected operations."""

from typing import List, Sequence
from fastapi import HTTPException
from app.infrastructure.persistence.database import get_db_client
from app.core.exceptions import AuthorizationError


def verify_planning_unit_ownership(planning_unit_id: str, user_id: str) -> None:
    """Verify that a planning unit is owned by the authenticated user."""
    client = get_db_client()
    result = (
        client.table("planning_units")
        .select("planning_unit_id")
        .eq("planning_unit_id", planning_unit_id)
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )
    if not result or not result.data:
        raise HTTPException(status_code=403, detail="Planning unit does not belong to authenticated user")


def verify_resource_ownership(
    table: str,
    id_column: str,
    resource_id: str,
    planning_unit_id: str,
    user_id: str,
    detail: str = "Resource does not belong to planning unit",
) -> None:
    """Verify resource belongs to user's planning unit."""
    verify_planning_unit_ownership(planning_unit_id, user_id)
    client = get_db_client()
    result = (
        client.table(table)
        .select(id_column)
        .eq(id_column, resource_id)
        .eq("planning_unit_id", planning_unit_id)
        .maybe_single()
        .execute()
    )
    if not result or not result.data:
        raise HTTPException(status_code=403, detail=detail)


def verify_investor_ownership(planning_unit_id: str, investor_id: str, user_id: str) -> None:
    verify_resource_ownership(
        "investors", "investor_id", investor_id, planning_unit_id, user_id, "Investor does not belong to planning unit"
    )


def verify_goal_ownership(planning_unit_id: str, goal_id: str, user_id: str) -> None:
    verify_resource_ownership(
        "goals", "goal_id", goal_id, planning_unit_id, user_id, "Goal does not belong to planning unit"
    )


def verify_defined_goal_ownership(planning_unit_id: str, defined_goal_id: str, user_id: str) -> None:
    verify_resource_ownership(
        "defined_goals",
        "defined_goal_id",
        defined_goal_id,
        planning_unit_id,
        user_id,
        "Defined goal does not belong to planning unit",
    )


def verify_financial_snapshot_ownership(planning_unit_id: str, snapshot_id: str, user_id: str) -> None:
    verify_resource_ownership(
        "financial_state_snapshots",
        "snapshot_id",
        snapshot_id,
        planning_unit_id,
        user_id,
        "Financial state snapshot does not belong to planning unit",
    )


def verify_action_ownership(planning_unit_id: str, action_id: str, user_id: str) -> None:
    verify_resource_ownership(
        "action_plan_items",
        "action_id",
        action_id,
        planning_unit_id,
        user_id,
        "Action does not belong to planning unit",
    )


def verify_strategy_run_ownership(planning_unit_id: str, strategy_run_id: str, user_id: str) -> None:
    verify_resource_ownership(
        "strategy_runs",
        "strategy_run_id",
        strategy_run_id,
        planning_unit_id,
        user_id,
        "Strategy run does not belong to planning unit",
    )


def verify_strategy_version_ownership(planning_unit_id: str, strategy_version_id: str, user_id: str) -> None:
    verify_resource_ownership(
        "strategy_versions",
        "strategy_version_id",
        strategy_version_id,
        planning_unit_id,
        user_id,
        "Strategy version does not belong to planning unit",
    )


def verify_assets_ownership(planning_unit_id: str, asset_ids: Sequence[str], user_id: str) -> None:
    """Verify that all listed assets belong to the user's planning unit."""
    verify_planning_unit_ownership(planning_unit_id, user_id)
    unique_ids = list(dict.fromkeys(asset_ids))
    if not unique_ids:
        return
    client = get_db_client()
    result = (
        client.table("assets")
        .select("asset_id")
        .eq("planning_unit_id", planning_unit_id)
        .in_("asset_id", unique_ids)
        .execute()
    )
    found = {row["asset_id"] for row in (result.data or [])}
    if found != set(unique_ids):
        raise HTTPException(status_code=403, detail="One or more assets do not belong to planning unit")
