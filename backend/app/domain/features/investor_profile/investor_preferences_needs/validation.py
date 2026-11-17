"""
domain/features/investor_profile/investor_preferences_needs/validation.py
Validation of preference/need inputs against the approved feature contract.

Does not override hard constraints or authorize a transaction.
"""

from typing import List
from app.domain.features.investor_profile.investor_preferences_needs.preferences import (
    InvestorPreferences,
)


def validate_investor_preferences(preferences: InvestorPreferences) -> List[str]:
    """Validates investor preferences against business invariants."""
    errors: List[str] = []

    if not preferences.investor_id or not preferences.investor_id.strip():
        errors.append("Investor ID cannot be blank.")

    if preferences.liquidity_buffer_months < 0:
        errors.append("Liquidity buffer months cannot be negative.")

    if preferences.minimum_emergency_reserve_target and preferences.minimum_emergency_reserve_target.is_negative:
        errors.append("Emergency reserve target cannot be negative.")

    return errors
