"""Authoritative goal classification and normalization business rules."""
from __future__ import annotations

from typing import Literal

GoalPriority = Literal["critical", "high", "medium", "low"]

GOAL_TYPE_ALIASES: dict[str, str] = {
    "retirement/financial freedom": "retirement",
    "financial freedom/passive income": "passive_income",
    "financial freedom": "passive_income",
    "education": "child education",
    "child education": "child education",
    "marriage": "marriage",
    "dream home": "home purchase",
    "home": "home purchase",
    "car": "vehicle",
    "vacation": "travel",
    "others": "other",
    "passive income": "passive_income",
    "debt repayment": "other",
    "philanthropy": "other",
}

DISCRETIONARY_GOAL_TYPES: set[str] = {
    "vacation",
    "travel",
    "car",
    "vehicle",
    "luxury",
    "others",
    "other",
    "passive_income",
}

ESSENTIAL_GOAL_TYPES: set[str] = {
    "emergency_fund",
    "emergency",
    "contingency",
    "debt_repayment",
    "retirement",
}


def canonical_goal_type(value: str | None) -> str:
    """Normalize goal type strings without changing their business meaning."""
    clean = (value or "").strip().lower()
    clean = clean.replace(" / ", "/")
    return GOAL_TYPE_ALIASES.get(clean, clean)


def is_discretionary_goal(goal_type: str | None) -> bool:
    """Return True if goal is categorized as discretionary spending."""
    canonical = canonical_goal_type(goal_type)
    return canonical in DISCRETIONARY_GOAL_TYPES


def is_essential_goal(goal_type: str | None) -> bool:
    """Return True if goal is categorized as essential / core security."""
    canonical = canonical_goal_type(goal_type)
    return canonical in ESSENTIAL_GOAL_TYPES
