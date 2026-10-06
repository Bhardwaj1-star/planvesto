"""Authoritative goal taxonomy and classification business rules."""
from __future__ import annotations

from typing import Literal

GoalType = Literal[
    "retirement",
    "marriage",
    "vehicle",
    "dream_home",
    "education",
    "vacation",
    "debt_freedom",
    "wealth_creation",
    "fire_passive_income",
    "others",
]
GoalPriority = Literal["critical", "high", "medium", "low"]
GoalPriorityLevel = GoalPriority

GOAL_PRIORITY_ALIASES: dict[str, GoalPriority] = {
    "critical": "critical",
    "must-have": "critical",
    "must have": "critical",
    "high": "high",
    "important": "high",
    "medium": "medium",
    "moderate": "medium",
    "aspirational": "medium",
    "low": "low",
    "nice-to-have": "low",
    "nice to have": "low",
    "discretionary": "low",
}

# Canonical goal identity. Beneficiaries, sub-purpose and other circumstances
# belong in dynamic/context details; they are never part of the goal type.
CANONICAL_GOAL_NAMES: dict[str, str] = {
    "retirement": "Retirement",
    "marriage": "Marriage",
    "vehicle": "Vehicle",
    "dream_home": "Dream Home",
    "education": "Education",
    "vacation": "Vacation",
    "debt_freedom": "Debt Freedom",
    "wealth_creation": "Wealth Creation",
    "fire_passive_income": "FIRE / Passive Income",
    "others": "Others",
}

DISCRETIONARY_GOAL_TYPES: set[str] = {
    "vehicle",
    "dream_home",
    "vacation",
    "wealth_creation",
    "others",
}

ESSENTIAL_GOAL_TYPES: set[str] = {
    "retirement",
    "marriage",
    "education",
    "debt_freedom",
    "fire_passive_income",
}

_CANONICAL_BY_LOWER: dict[str, str] = {k.lower(): k for k in CANONICAL_GOAL_NAMES}
_CANONICAL_BY_LOWER.update({v.lower(): k for k, v in CANONICAL_GOAL_NAMES.items()})

def canonical_goal_type(value: str | None) -> str:
    """Accept only canonical onboarding goal IDs or display names (case-insensitive); return canonical ID."""
    clean = str(value or "").strip().lower()
    return _CANONICAL_BY_LOWER.get(clean, "")

def canonical_goal_name(goal_type: str | None, fallback: str | None = None) -> str:
    """Return the canonical onboarding label for a canonical goal ID."""
    canonical = canonical_goal_type(goal_type)
    return CANONICAL_GOAL_NAMES.get(canonical, "")

def canonical_goal_priority(value: str | None) -> GoalPriority:
    """Normalize UI/storage goal-priority vocabulary to the canonical backend contract."""
    clean = " ".join((value or "").strip().lower().split())
    return GOAL_PRIORITY_ALIASES.get(clean, "medium")

def is_discretionary_goal(goal_type: str | None) -> bool:
    canonical = canonical_goal_type(goal_type)
    return canonical in DISCRETIONARY_GOAL_TYPES

def is_essential_goal(goal_type: str | None) -> bool:
    canonical = canonical_goal_type(goal_type)
    return canonical in ESSENTIAL_GOAL_TYPES
