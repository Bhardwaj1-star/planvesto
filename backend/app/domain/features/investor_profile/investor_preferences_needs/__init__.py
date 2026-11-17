"""
domain/features/investor_profile/investor_preferences_needs/__init__.py
Investor preferences & needs subfeature exports.
"""

from app.domain.features.investor_profile.investor_preferences_needs.preferences import (
    InvestorPreferences,
)
from app.domain.features.investor_profile.investor_preferences_needs.validation import (
    validate_investor_preferences,
)

__all__ = [
    "InvestorPreferences",
    "validate_investor_preferences",
]
