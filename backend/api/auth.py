"""Authentication and Authorization endpoints and dependencies.

Provides backward-compatible wrappers around app.security.
"""

from fastapi import HTTPException
from app.security.authentication import authenticate_request
from app.security.authorization import (
    verify_planning_unit_ownership,
    verify_resource_ownership,
    verify_investor_ownership,
    verify_goal_ownership,
    verify_defined_goal_ownership,
    verify_financial_snapshot_ownership,
    verify_action_ownership,
    verify_strategy_run_ownership,
    verify_strategy_version_ownership,
    verify_assets_ownership,
)

# Preserve legacy function names exactly
authenticate_user = authenticate_request

__all__ = [
    "authenticate_user",
    "verify_planning_unit_ownership",
    "verify_investor_ownership",
    "verify_goal_ownership",
    "verify_defined_goal_ownership",
    "verify_financial_snapshot_ownership",
    "verify_action_ownership",
    "verify_strategy_run_ownership",
    "verify_strategy_version_ownership",
    "verify_assets_ownership",
]
