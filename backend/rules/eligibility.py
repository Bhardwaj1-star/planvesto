"""Authoritative eligibility status and fit definitions for Strategy Builder."""
from __future__ import annotations

from enum import Enum


class EligibilityStatus(str, Enum):
    PASS = "pass"
    CONDITIONAL = "conditional"
    FAIL = "fail"


ELIGIBILITY_FITS: tuple[str, ...] = (
    "cashflow_fit",
    "liquidity_fit",
    "debt_fit",
    "asset_resource_fit",
    "risk_capacity_fit",
    "goal_constraint_fit",
    "multi_goal_conflict_fit",
    "implementation_fit",
)
