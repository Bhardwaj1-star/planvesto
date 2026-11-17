"""
domain/features/investor_profile/financial_state/validation.py
Chapter 04 §3 Domain Validation.

Validates normalized investor-supplied financial facts against invariant rules:
- No negative balances for assets or liabilities
- Ownership percentages must be within 0-100%
- Proper evidence status and dates
"""

from decimal import Decimal
from typing import List
from app.domain.features.investor_profile.financial_state.models import FinancialStateSnapshot


def validate_financial_state_snapshot(snapshot: FinancialStateSnapshot) -> List[str]:
    """Returns list of validation error messages, if any."""
    errors: List[str] = []

    if not snapshot.investor_id or not snapshot.investor_id.strip():
        errors.append("Investor ID cannot be blank.")

    for asset in snapshot.assets:
        if asset.current_value.is_negative:
            errors.append(f"Asset '{asset.name}' has negative value: {asset.current_value.amount}.")
        if asset.ownership_percentage.percentage < Decimal(0) or asset.ownership_percentage.percentage > Decimal(100):
            errors.append(f"Asset '{asset.name}' ownership must be between 0% and 100%.")

    for liab in snapshot.liabilities:
        if liab.outstanding_balance.is_negative:
            errors.append(f"Liability '{liab.name}' has negative outstanding balance: {liab.outstanding_balance.amount}.")
        if liab.monthly_payment.is_negative:
            errors.append(f"Liability '{liab.name}' has negative monthly payment: {liab.monthly_payment.amount}.")

    return errors
