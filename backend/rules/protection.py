"""Authoritative protection and insurance business rules."""
from __future__ import annotations

# Benchmark: 10 years of gross income plus outstanding debt liabilities
INCOME_REPLACEMENT_YEARS: float = 10.0

LIFE_INSURANCE_TYPES: set[str] = {
    "term insurance",
    "term",
    "endowment",
    "whole life",
    "ulip",
    "money back",
}

HEALTH_INSURANCE_TYPES: set[str] = {
    "health insurance",
    "health",
}


def calculate_required_insurance_cover(annual_income: float, total_liabilities: float) -> float:
    """Calculate baseline required insurance cover.

    Rule: 10 years of gross annual income plus total outstanding liabilities.
    Existing assets are intentionally not netted off so insurance remains a pure protection signal.
    """
    return (max(0.0, annual_income) * INCOME_REPLACEMENT_YEARS) + max(0.0, total_liabilities)


def is_life_insurance(policy_type: str | None) -> bool:
    """Check if policy type qualifies as life insurance cover."""
    clean = str(policy_type or "").strip().lower()
    return clean in LIFE_INSURANCE_TYPES


def is_health_insurance(policy_type: str | None) -> bool:
    """Check if policy type qualifies as health insurance cover."""
    clean = str(policy_type or "").strip().lower()
    return clean in HEALTH_INSURANCE_TYPES
