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

from typing import Any, Literal

ConstraintKind = Literal["hard", "soft"]
ConstraintSource = Literal[
    "financial_state", "observed_behavior", "declared_constraint", "preference"
]

SOURCE_PRIORITY: dict[str, int] = {
    "financial_state": 4,
    "observed_behavior": 3,
    "declared_constraint": 2,
    "preference": 1,
}

class ConstraintRules:
    """Canonical normalization, conflict and priority policy for constraints."""

    @staticmethod
    def normalize(item: dict[str, Any], source: ConstraintSource) -> dict[str, Any]:
        valid_from = item.get("valid_from")
        valid_until = item.get("valid_until")
        validity = item.get("validity")
        if not isinstance(validity, dict):
            validity = {"valid_from": valid_from, "valid_until": valid_until, "status": "valid"}
        else:
            valid_from = valid_from or validity.get("valid_from")
            valid_until = valid_until or validity.get("valid_until")
        confidence = item.get("confidence")
        if confidence is None:
            confidence = ConstraintRules.confidence(source, len(item.get("evidence", [])))
        return {
            "key": item["key"], "value": item["value"], "unit": item.get("unit"),
            "kind": item.get("kind", "soft"), "source": source,
            "evidence": item.get("evidence", []), "confidence": confidence,
            "validity": validity, "valid_from": valid_from, "valid_until": valid_until,
        }

    @staticmethod
    def conflicts(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        groups: dict[str, list[dict[str, Any]]] = {}
        for item in items:
            groups.setdefault(item["key"], []).append(item)
        return [
            {
                "key": key, "status": "unresolved",
                "reason": "Evidence sources provide conflicting values.",
                "sources": [item["source"] for item in group],
                "hard_constraint_present": any(item["kind"] == "hard" for item in group),
            }
            for key, group in groups.items()
            if len({repr(item["value"]) for item in group}) > 1
        ]

    @staticmethod
    def confidence(source: ConstraintSource, evidence_count: int) -> float:
        return round(min(1.0, SOURCE_PRIORITY[source] / 4.0 + (0.15 if evidence_count > 1 else 0.0)), 4)

    @staticmethod
    def validate_priorities(constraints: list[dict[str, Any]], priorities: list[dict[str, Any]]) -> list[dict[str, Any]]:
        keys = {item["key"] for item in constraints}
        seen_keys: set[str] = set()
        seen_ranks: set[int] = set()
        normalized: list[dict[str, Any]] = []
        for item in sorted(priorities, key=lambda x: x.get("rank", 0)):
            key, rank = item.get("key"), item.get("rank")
            if key not in keys or key in seen_keys or not isinstance(rank, int) or rank < 1 or rank in seen_ranks:
                raise ValueError("Invalid, duplicate constraint, or duplicate priority rank")
            seen_keys.add(key); seen_ranks.add(rank)
            normalized.append({"key": key, "rank": rank})
        return normalized
