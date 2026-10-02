"""Authoritative constraint definitions and policy thresholds."""
from __future__ import annotations

# Canonical priority ordering used across multi-goal planning.
PRIORITY_RANKS: dict[str, int] = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}

# Rule IDs
RULE_EMERGENCY_RESERVE_CRITICAL = "RULE_EMERGENCY_RESERVE_CRITICAL"
WARN_EMERGENCY_RESERVE_ATTENTION = "WARN_EMERGENCY_RESERVE_ATTENTION"
RULE_DEBT_BURDEN_EXCEEDED = "RULE_DEBT_BURDEN_EXCEEDED"
WARN_DEBT_BURDEN_ATTENTION = "WARN_DEBT_BURDEN_ATTENTION"
WARN_SAVINGS_RATE_DEFICIT = "WARN_SAVINGS_RATE_DEFICIT"

# Thresholds (aligned with canonical Moneywheel ratios)
EMERGENCY_RESERVE_CRITICAL_MONTHS: float = 3.0
EMERGENCY_RESERVE_HEALTHY_MONTHS: float = 6.0

DEBT_TO_INCOME_CRITICAL_PERCENT: float = 40.0
DEBT_TO_INCOME_HEALTHY_PERCENT: float = 30.0

SAVINGS_RATIO_HEALTHY_PERCENT: float = 20.0
