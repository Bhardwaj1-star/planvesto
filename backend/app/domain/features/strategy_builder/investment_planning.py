"""
domain/features/strategy_builder/investment_planning.py
Chapter 11 — Strategy Builder Step 3: Investment Planning & Product Selection (§11.4).

Assessment of investment structure, asset allocation, and investment vehicle options
within the approved Goal Funding Strategy.
Non-negotiable invariants:
- No mandatory technique or product for every goal.
- No automatic execution or changes without explicit investor approval.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from app.domain.shared.value_objects import Money, Rate


class InvestmentVehicleType(str, Enum):
    MUTUAL_FUND_EQUITY = "mutual_fund_equity"
    MUTUAL_FUND_DEBT = "mutual_fund_debt"
    MUTUAL_FUND_HYBRID = "mutual_fund_hybrid"
    FIXED_DEPOSIT = "fixed_deposit"
    RECURRING_DEPOSIT = "recurring_deposit"
    GOVERNMENT_SAVINGS = "government_savings"
    DIRECT_EQUITY = "direct_equity"


@dataclass(frozen=True)
class AssetAllocationRecommendation:
    """Recommended portfolio allocation across asset classes for this goal horizon."""
    equity_allocation_pct: Rate
    debt_allocation_pct: Rate
    cash_allocation_pct: Rate
    rationale: str


@dataclass(frozen=True)
class InvestmentOptionAssessment:
    """Assessment of candidate investment options for meeting required contributions."""
    vehicle_type: InvestmentVehicleType
    indicative_annual_return: Rate
    risk_level: str
    liquidity_terms: str
    tax_efficiency_notes: str
    suitability_rationale: str
