"""Canonical constraint policy definitions.

This is the single ownership point for constraint policy IDs, thresholds and
priority semantics.  The legacy rules.constraints module re-exports these
symbols for backward compatibility.
"""
from __future__ import annotations

PRIORITY_RANKS: dict[str, int] = {
    "critical": 0, "high": 1, "medium": 2, "low": 3,
}

RULE_EMERGENCY_RESERVE_CRITICAL = "RULE_EMERGENCY_RESERVE_CRITICAL"
WARN_EMERGENCY_RESERVE_ATTENTION = "WARN_EMERGENCY_RESERVE_ATTENTION"
RULE_DEBT_BURDEN_EXCEEDED = "RULE_DEBT_BURDEN_EXCEEDED"
WARN_DEBT_BURDEN_ATTENTION = "WARN_DEBT_BURDEN_ATTENTION"
WARN_SAVINGS_RATE_DEFICIT = "WARN_SAVINGS_RATE_DEFICIT"

EMERGENCY_RESERVE_CRITICAL_MONTHS: float = 3.0
EMERGENCY_RESERVE_HEALTHY_MONTHS: float = 6.0

DEBT_TO_INCOME_EXCELLENT_PERCENT: float = 20.0
DEBT_TO_INCOME_CRITICAL_PERCENT: float = 40.0
DEBT_TO_INCOME_HEALTHY_PERCENT: float = 30.0

SAVINGS_RATIO_HEALTHY_PERCENT: float = 20.0

from rules.goals import is_discretionary_goal, is_essential_goal

def can_discretionary_preempt_essential(
    discretionary_goal_type: str,
    essential_goal_type: str,
) -> bool:
    """Canonical constraint: discretionary goals cannot preempt essentials."""
    if is_discretionary_goal(discretionary_goal_type) and is_essential_goal(essential_goal_type):
        return False
    return True
