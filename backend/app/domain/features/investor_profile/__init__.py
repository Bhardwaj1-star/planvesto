"""
domain/features/investor_profile/__init__.py
Investor Profile top-level exports containing four sibling subfeatures:
1. financial_state
2. risk_profile
3. behavioural_profile
4. investor_preferences_needs
"""

from app.domain.features.investor_profile.financial_state import (
    IncomeRecord,
    ExpenseRecord,
    AssetRecord,
    LiabilityRecord,
    InsuranceRecord,
    FinancialStateSnapshot,
    normalize_income_to_monthly,
    validate_financial_state_snapshot,
    DataReadinessReport,
    assess_data_readiness,
)
from app.domain.features.investor_profile.risk_profile import (
    RiskCapacityBand,
    RiskToleranceBand,
    RiskProfile,
    RiskAssessmentOutcome,
    assess_risk_profile,
)
from app.domain.features.investor_profile.behavioural_profile import (
    MarketDownturnReaction,
    FinancialDecisionStyle,
    BehaviouralProfile,
    interpret_behavioural_guardrails,
)
from app.domain.features.investor_profile.investor_preferences_needs import (
    InvestorPreferences,
    validate_investor_preferences,
)

__all__ = [
    # Financial State
    "IncomeRecord",
    "ExpenseRecord",
    "AssetRecord",
    "LiabilityRecord",
    "InsuranceRecord",
    "FinancialStateSnapshot",
    "normalize_income_to_monthly",
    "validate_financial_state_snapshot",
    "DataReadinessReport",
    "assess_data_readiness",
    # Risk Profile
    "RiskCapacityBand",
    "RiskToleranceBand",
    "RiskProfile",
    "RiskAssessmentOutcome",
    "assess_risk_profile",
    # Behavioural Profile
    "MarketDownturnReaction",
    "FinancialDecisionStyle",
    "BehaviouralProfile",
    "interpret_behavioural_guardrails",
    # Preferences & Needs
    "InvestorPreferences",
    "validate_investor_preferences",
]
