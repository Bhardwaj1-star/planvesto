"""Authoritative goal taxonomy and classification business rules."""
from __future__ import annotations

from typing import Literal

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
    "emergency_fund": "Emergency Fund",
    "debt_freedom": "Debt Freedom",
    "education": "Education",
    "marriage": "Marriage",
    "home": "Home",
    "home_improvement": "Home Improvement",
    "vehicle": "Vehicle",
    "travel": "Travel & Experiences",
    "retirement": "Retirement",
    "financial_independence": "Financial Independence",
    "family_care": "Family Care",
    "healthcare": "Healthcare",
    "business": "Business & Entrepreneurship",
    "lifestyle": "Lifestyle",
    "wealth_creation": "Wealth Creation",
    "legacy_giving": "Legacy & Giving",
    "other": "Other",
}

# Legacy UI/storage labels normalize into the canonical identities above.
# Existing persisted values remain readable; no database migration is required.
GOAL_TYPE_ALIASES: dict[str, str] = {
    "emergency fund": "emergency_fund",
    "emergency": "emergency_fund",
    "contingency": "emergency_fund",
    "debt repayment": "debt_freedom",
    "debt_repayment": "debt_freedom",
    "debt freedom": "debt_freedom",
    "education": "education",
    "child education": "education",
    "children education": "education",
    "child's education": "education",
    "childrens education": "education",
    "marriage": "marriage",
    "child marriage": "marriage",
    "child_marriage": "marriage",
    "children marriage": "marriage",
    "dream home": "home",
    "home purchase": "home",
    "home_purchase": "home",
    "home": "home",
    "home improvement": "home_improvement",
    "renovation": "home_improvement",
    "car": "vehicle",
    "vehicle": "vehicle",
    "vacation": "travel",
    "travel": "travel",
    "travel & experiences": "travel",
    "passive income": "financial_independence",
    "passive_income": "financial_independence",
    "financial freedom": "financial_independence",
    "financial freedom/passive income": "financial_independence",
    "financial freedom / passive income": "financial_independence",
    "financial independence": "financial_independence",
    "business": "business",
    "business & entrepreneurship": "business",
    "entrepreneurship": "business",
    "family care": "family_care",
    "parents care": "family_care",
    "healthcare": "healthcare",
    "health care": "healthcare",
    "lifestyle": "lifestyle",
    "wealth creation": "wealth_creation",
    "legacy & giving": "legacy_giving",
    "legacy and giving": "legacy_giving",
    "philanthropy": "legacy_giving",
    "charity": "legacy_giving",
    "giving": "legacy_giving",
    "others": "other",
    "other": "other",
}

DISCRETIONARY_GOAL_TYPES: set[str] = {
    "home",
    "home_improvement",
    "vehicle",
    "travel",
    "lifestyle",
    "wealth_creation",
    "legacy_giving",
    "other",
}

ESSENTIAL_GOAL_TYPES: set[str] = {
    "emergency_fund",
    "debt_freedom",
    "education",
    "retirement",
    "financial_independence",
    "family_care",
    "healthcare",
}

def canonical_goal_type(value: str | None) -> str:
    """Normalize legacy/UI goal labels to one canonical goal identity."""
    clean = " ".join((value or "").strip().lower().split())
    clean = clean.replace(" / ", "/").replace("/ ", "/").replace(" /", "/")
    if clean.startswith("retirement/"):
        return "retirement"
    return GOAL_TYPE_ALIASES.get(clean, clean)

def canonical_goal_name(goal_type: str | None, fallback: str | None = None) -> str:
    """Preserve a real goal name while replacing legacy/type-label names with the canonical label."""
    canonical = canonical_goal_type(goal_type)
    supplied = " ".join((fallback or "").strip().split())
    if supplied:
        supplied_key = supplied.lower().replace(" / ", "/").replace("/ ", "/").replace(" /", "/")
        canonical_labels = {name.lower(): key for key, name in CANONICAL_GOAL_NAMES.items()}
        if supplied_key not in GOAL_TYPE_ALIASES and supplied_key not in canonical_labels and not supplied_key.startswith("retirement/"):
            return supplied
    return CANONICAL_GOAL_NAMES.get(canonical, str(goal_type or "").strip())

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
