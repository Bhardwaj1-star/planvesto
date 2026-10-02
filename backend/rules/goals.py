"""Authoritative goal classification and normalization business rules."""
from __future__ import annotations

from typing import Literal

GoalPriority = Literal["critical", "high", "medium", "low"]

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

CANONICAL_GOAL_NAMES: dict[str, str] = {
    "retirement": "Retirement",
    "passive_income": "Financial Freedom / Passive Income",
    "child education": "Education",
    "marriage": "Marriage",
    "home purchase": "Dream Home",
    "vehicle": "Vehicle",
    "travel": "Vacation",
    "other": "Others",
}

# Only non-ambiguous legacy aliases remain here. Retirement and passive income
# are permanently distinct canonical goal identities.
GOAL_TYPE_ALIASES: dict[str, str] = {
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
    clean = " ".join((value or "").strip().lower().split())
    clean = clean.replace(" / ", "/").replace("/ ", "/").replace(" /", "/")
    return GOAL_TYPE_ALIASES.get(clean, clean)


def canonical_goal_name(goal_type: str | None, fallback: str | None = None) -> str:
    """Return the canonical user-facing name for a canonical goal type."""
    canonical = canonical_goal_type(goal_type)
    return CANONICAL_GOAL_NAMES.get(canonical, fallback or str(goal_type or "").strip())


def canonical_goal_priority(value: str | None) -> GoalPriority:
    """Normalize UI/storage goal-priority vocabulary to the canonical backend contract."""
    clean = " ".join((value or "").strip().lower().split())
    return GOAL_PRIORITY_ALIASES.get(clean, "medium")


def is_discretionary_goal(goal_type: str | None) -> bool:
    """Return True if goal is categorized as discretionary spending."""
    canonical = canonical_goal_type(goal_type)
    return canonical in DISCRETIONARY_GOAL_TYPES


def is_essential_goal(goal_type: str | None) -> bool:
    """Return True if goal is categorized as essential / core security."""
    canonical = canonical_goal_type(goal_type)
    return canonical in ESSENTIAL_GOAL_TYPES
