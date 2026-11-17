"""
domain/features/financial_state/__init__.py
Re-exports from app.domain.features.investor_profile.financial_state
to ensure backward compatibility across all imports.
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

__all__ = [
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
]
