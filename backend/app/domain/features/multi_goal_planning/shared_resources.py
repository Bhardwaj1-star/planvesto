"""
domain/features/multi_goal_planning/shared_resources.py
Multi-Goal Planning: Shared Resource Analysis.

Identifies resources relevant to more than one goal (surplus capacity, shared liquid assets)
and exposes potential double-allocation conflicts where evidence supports them.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional
from app.domain.shared.value_objects import Money


@dataclass(frozen=True)
class SharedResourceConflict:
    """Detected double-allocation or over-subscription of a shared asset/surplus."""
    resource_id: str
    resource_name: str
    total_available_value: Money
    total_claimed_across_goals: Money
    deficit_or_overcommit: Money
    competing_goal_ids: List[str]


def detect_surplus_oversubscription(
    available_monthly_surplus: Money,
    goal_monthly_commitments: List[tuple[str, Money]],
) -> Optional[SharedResourceConflict]:
    """Detects if combined monthly SIP requirements exceed available monthly surplus."""
    total_claimed_amount = sum((m.amount for _, m in goal_monthly_commitments), Decimal(0))
    total_claimed = Money(amount=total_claimed_amount, currency=available_monthly_surplus.currency)

    if total_claimed > available_monthly_surplus:
        deficit = total_claimed - available_monthly_surplus
        return SharedResourceConflict(
            resource_id="available_monthly_surplus",
            resource_name="Available Monthly Surplus",
            total_available_value=available_monthly_surplus,
            total_claimed_across_goals=total_claimed,
            deficit_or_overcommit=deficit,
            competing_goal_ids=[gid for gid, _ in goal_monthly_commitments],
        )
    return None
