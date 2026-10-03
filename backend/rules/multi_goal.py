"""Authoritative multi-goal allocation, trade-off, and priority hierarchy rules."""
from __future__ import annotations

from typing import Any, Literal
from rules.goals import GoalPriority, is_discretionary_goal, is_essential_goal

# Canonical multi-goal status vocabularies. Allocation and orchestration share these.
FundingStatusType = Literal[
    "fully_funded", "partially_funded", "unfunded",
    "within_surplus", "surplus_shortfall", "requires_review",
]
FeasibilityStatusType = Literal["feasible", "constrained", "infeasible"]

# Priority Ranks: lower number = higher priority
PRIORITY_RANK_MAP: dict[str, int] = {
    "critical": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
}


def get_priority_rank(priority: str | None) -> int:
    """Return numeric priority rank for ordering (1 = Critical, 4 = Low)."""
    clean = str(priority or "medium").strip().lower()
    return PRIORITY_RANK_MAP.get(clean, 3)


def is_higher_priority(priority_a: str | None, priority_b: str | None) -> bool:
    """Check if priority_a has strictly higher precedence than priority_b."""
    return get_priority_rank(priority_a) < get_priority_rank(priority_b)


def can_discretionary_preempt_essential(
    discretionary_goal_type: str,
    essential_goal_type: str,
) -> bool:
    """Rule: Discretionary commitments must never preempt essential or safety reserve funding."""
    if is_discretionary_goal(discretionary_goal_type) and is_essential_goal(essential_goal_type):
        return False
    return True
