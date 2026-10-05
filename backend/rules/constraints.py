"""Backward-compatible facade for the canonical constraint policy.

Constraint policy is owned by engines.constraints.policy.  New code must
import from that module; this facade exists only for legacy callers.
"""
from engines.constraints.policy import (
    PRIORITY_RANKS,
    RULE_EMERGENCY_RESERVE_CRITICAL,
    WARN_EMERGENCY_RESERVE_ATTENTION,
    RULE_DEBT_BURDEN_EXCEEDED,
    WARN_DEBT_BURDEN_ATTENTION,
    WARN_SAVINGS_RATE_DEFICIT,
    RULE_GOAL_POSITIVE_HORIZON,
    RULE_GOAL_POSITIVE_TARGET,
    EMERGENCY_RESERVE_CRITICAL_MONTHS,
    EMERGENCY_RESERVE_HEALTHY_MONTHS,
    DEBT_TO_INCOME_EXCELLENT_PERCENT,
    DEBT_TO_INCOME_CRITICAL_PERCENT,
    DEBT_TO_INCOME_HEALTHY_PERCENT,
    SAVINGS_RATIO_HEALTHY_PERCENT,
)

__all__ = [name for name in globals() if name.isupper()]
