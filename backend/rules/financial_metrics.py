"""Authoritative classifications for financial metrics and budget items."""
from __future__ import annotations

SHORT_TERM_LIABILITY_TYPES: set[str] = {
    "Credit Card",
    "Personal Loan",
    "Consumer Loan",
    "Other",
}

ESSENTIAL_EXPENSE_TYPES: set[str] = {
    "Housing",
    "Utilities",
    "Groceries",
    "Healthcare",
    "Insurance",
    "Education",
    "Debt Payments",
}


def is_short_term_liability(liability_type: str | None) -> bool:
    """Check if liability type is classified as short-term."""
    return str(liability_type or "Other") in SHORT_TERM_LIABILITY_TYPES


def is_essential_expense(expense_type: str | None) -> bool:
    """Check if expense type is classified as essential need expense."""
    return str(expense_type or "Other") in ESSENTIAL_EXPENSE_TYPES
