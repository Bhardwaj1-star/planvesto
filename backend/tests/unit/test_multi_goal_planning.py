"""
Unit tests for Multi-Goal Planning (Goal Coordination, Shared Resources & Conflict Detection).
"""

from decimal import Decimal
from app.domain.shared.value_objects import Money
from app.domain.features.multi_goal_planning import (
    SharedResourceConflict,
    detect_surplus_oversubscription,
)


def test_detect_surplus_oversubscription_conflict():
    surplus = Money.from_amount("50000.00")
    commitments = [
        ("goal-retire", Money.from_amount("30000.00")),
        ("goal-child-edu", Money.from_amount("25000.00")),
        ("goal-vacation", Money.from_amount("10000.00")),
    ]
    # Total commitments = 65,000 > Surplus 50,000 -> Deficit of 15,000

    conflict = detect_surplus_oversubscription(surplus, commitments)
    assert conflict is not None
    assert conflict.resource_id == "available_monthly_surplus"
    assert conflict.deficit_or_overcommit.amount == Decimal("15000.00")
    assert "goal-retire" in conflict.competing_goal_ids
    assert "goal-child-edu" in conflict.competing_goal_ids


def test_no_conflict_when_commitments_within_surplus():
    surplus = Money.from_amount("70000.00")
    commitments = [
        ("goal-retire", Money.from_amount("30000.00")),
        ("goal-child-edu", Money.from_amount("25000.00")),
    ]
    conflict = detect_surplus_oversubscription(surplus, commitments)
    assert conflict is None
