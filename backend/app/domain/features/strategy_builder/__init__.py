"""
domain/features/strategy_builder/__init__.py
Chapter 11 — Goal Funding Strategy exports.
"""

from app.domain.features.strategy_builder.funding_paths import (
    FundingPathType,
    YearlyProjectionRow,
    SelfMoneyPathResult,
    FinancingPathResult,
)
from app.domain.features.strategy_builder.asset_assessment import (
    AssetDispositionChoice,
    AssetDecision,
)
from app.domain.features.strategy_builder.financing import (
    calculate_loan_emi,
    build_financing_path,
)
from app.domain.features.strategy_builder.projections import (
    build_self_money_path,
)
from app.domain.features.strategy_builder.comparison import (
    StrategyComparisonMatrix,
    compare_funding_paths,
)
from app.domain.features.strategy_builder.investment_planning import (
    InvestmentVehicleType,
    AssetAllocationRecommendation,
    InvestmentOptionAssessment,
)
from app.domain.features.strategy_builder.payment_withdrawal import (
    WithdrawalSourceAssessment,
    GoalPaymentPlan,
)
from app.domain.features.strategy_builder.monitoring import (
    FundingStatus,
    GoalMonitoringCheckpoint,
)

__all__ = [
    "FundingPathType",
    "YearlyProjectionRow",
    "SelfMoneyPathResult",
    "FinancingPathResult",
    "AssetDispositionChoice",
    "AssetDecision",
    "calculate_loan_emi",
    "build_financing_path",
    "build_self_money_path",
    "StrategyComparisonMatrix",
    "compare_funding_paths",
    "InvestmentVehicleType",
    "AssetAllocationRecommendation",
    "InvestmentOptionAssessment",
    "WithdrawalSourceAssessment",
    "GoalPaymentPlan",
    "FundingStatus",
    "GoalMonitoringCheckpoint",
]
