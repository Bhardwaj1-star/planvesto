"""Backward-compatible imports; canonical models live under investor_profile.financial_state."""
from app.domain.features.investor_profile.financial_state.models import (
    IncomeRecord, ExpenseRecord, AssetRecord,
    LiabilityRecord, InsuranceRecord, FinancialStateSnapshot,
)

__all__ = [
    "IncomeRecord", "ExpenseRecord", "AssetRecord",
    "LiabilityRecord", "InsuranceRecord", "FinancialStateSnapshot",
]
