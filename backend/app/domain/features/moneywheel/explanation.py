"""
domain/features/moneywheel/explanation.py
Chapter 09 Domain Explanation Helpers.

Helper functions to generate transparent, explainable finding texts for each dimension.
"""

from decimal import Decimal
from typing import Optional
from app.domain.shared.value_objects import Money, Rate


def explain_liquidity_status(liquid_assets: Money, liquid_ratio: Optional[Rate]) -> str:
    """Returns clear descriptive text for liquidity reserve status."""
    ratio_str = f"{liquid_ratio.percentage:.1f}%" if liquid_ratio else "N/A"
    return f"Liquid assets stand at {liquid_assets.amount} ({ratio_str} of total assets)."


def explain_cash_flow_status(income: Money, expenses: Money, commitments: Money, surplus: Money) -> str:
    """Returns clear descriptive text for monthly surplus / deficit."""
    if surplus.is_negative:
        return (
            f"Expenses ({expenses.amount}) and commitments ({commitments.amount}) "
            f"exceed income ({income.amount}) by {abs(surplus.amount)}."
        )
    return f"Available surplus is {surplus.amount} after meeting monthly expenses and ongoing savings."
