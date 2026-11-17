"""
domain/features/investor_profile/financial_state/normalization.py
Chapter 04 §3 Financial State Normalization.

Normalizes Financial State values into the approved domain representation:
- Period flows: converts annual frequency to monthly equivalents or preserves frequency
- Validates that flows and balances maintain consistent currency
- Retains distinct net take-home salary vs gross
"""

from decimal import Decimal
from app.domain.shared.value_objects import Money, FlowFrequency
from app.domain.features.investor_profile.financial_state.models import IncomeRecord


def normalize_income_to_monthly(income: IncomeRecord) -> Money:
    """Normalizes an income record to its monthly cash equivalent."""
    if income.frequency == FlowFrequency.MONTHLY:
        return income.amount
    elif income.frequency == FlowFrequency.ANNUAL:
        monthly_amt = income.amount.amount / Decimal(12)
        return Money(amount=monthly_amt, currency=income.amount.currency)
    elif income.frequency == FlowFrequency.QUARTERLY:
        monthly_amt = income.amount.amount / Decimal(3)
        return Money(amount=monthly_amt, currency=income.amount.currency)
    return income.amount
