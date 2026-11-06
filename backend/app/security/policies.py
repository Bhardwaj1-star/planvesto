"""Reusable access-control policies and composition of authorization checks."""

from typing import Sequence
from app.security.authorization import (
    verify_planning_unit_ownership,
    verify_investor_ownership,
    verify_goal_ownership,
    verify_action_ownership,
    verify_assets_ownership,
)


class AccessControlPolicy:
    """Enforces high-level access-control rules on domain operations."""

    @staticmethod
    def ensure_can_access_planning_unit(planning_unit_id: str, user_id: str) -> None:
        verify_planning_unit_ownership(planning_unit_id, user_id)

    @staticmethod
    def ensure_can_modify_goal(planning_unit_id: str, goal_id: str, user_id: str) -> None:
        verify_goal_ownership(planning_unit_id, goal_id, user_id)

    @staticmethod
    def ensure_can_modify_assets(planning_unit_id: str, asset_ids: Sequence[str], user_id: str) -> None:
        verify_assets_ownership(planning_unit_id, asset_ids, user_id)

    @staticmethod
    def ensure_can_complete_action(planning_unit_id: str, action_id: str, user_id: str) -> None:
        verify_action_ownership(planning_unit_id, action_id, user_id)
