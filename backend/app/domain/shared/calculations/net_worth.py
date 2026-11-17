"""
Chapter 05 — Canonical Measurements & Formulas
metric_net_worth: Net Worth (§2 Group A, §3 Group A)

Formula:
Net Worth = Total Assets − Total Liabilities

Assumptions & Rules:
- Requires consistent valuation basis and valid asset/liability inputs.
- Pure calculation; does not mutate Financial State.
"""

from decimal import Decimal
from typing import Optional
from app.domain.shared.value_objects import Money


def calculate_net_worth(total_assets: Money, total_liabilities: Money) -> Money:
    """
    Calculate Net Worth: Total Assets − Total Liabilities.
    """
    if total_assets.currency != total_liabilities.currency:
        raise ValueError(
            f"Currency mismatch in Net Worth calculation: {total_assets.currency} vs {total_liabilities.currency}"
        )
    return total_assets - total_liabilities
