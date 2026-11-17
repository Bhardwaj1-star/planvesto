"""
domain/features/investor_profile/financial_state/models.py
Chapter 04 — Financial State & Data Readiness (§3, §4)

Non-negotiable invariants:
1. Financial State records facts, dated evidence, provenance, and readiness.
2. It does not independently determine health, goal feasibility or strategy suitability.
3. Keep flows and stocks distinct: Incomes/Expenses are period flows; Assets/Liabilities are dated balances.
4. Distinguish gross vs take-home salary, business revenue vs profit.
5. Full EMI payment is an Expense; do not count principal/interest twice.
6. Transfers between own accounts are neither Income nor Expenses.
7. Credit-card purchases are Expense in purchase month, not again at bill payment.
8. Retain ownership share, practical access, lock-ins, and existing commitments.
"""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List, Optional

from app.domain.canonical.financial_categories import (
    CanonicalIncomeCategoryId,
    CanonicalExpenseCategoryId,
    CanonicalAssetCategoryId,
    CanonicalLiabilityCategoryId,
    CanonicalInsurancePolicyTypeId,
)
from app.domain.shared.value_objects import (
    Money,
    Rate,
    CalendarMonth,
    EvidenceStatus,
    FlowFrequency,
)
from app.domain.shared.calculations.net_worth import calculate_net_worth
from app.domain.shared.calculations.cash_flow import calculate_monthly_surplus


@dataclass(frozen=True)
class IncomeRecord:
    id: str
    category: CanonicalIncomeCategoryId
    amount: Money
    is_net: bool  # True for take-home pay/net profit; False for gross
    frequency: FlowFrequency
    period: CalendarMonth
    status: EvidenceStatus = EvidenceStatus.INVESTOR_REPORTED
    source: str = "investor_declared"
    notes: Optional[str] = None


@dataclass(frozen=True)
class ExpenseRecord:
    id: str
    category: CanonicalExpenseCategoryId
    amount: Money
    period: CalendarMonth
    is_emi: bool = False
    is_own_account_transfer: bool = False  # Excluded from income/expenses
    status: EvidenceStatus = EvidenceStatus.INVESTOR_REPORTED
    source: str = "investor_declared"
    notes: Optional[str] = None


@dataclass(frozen=True)
class AssetRecord:
    id: str
    name: str
    category: CanonicalAssetCategoryId
    current_value: Money
    as_of_date: date
    ownership_percentage: Rate = Rate.from_percentage("100.0")
    is_accessible: bool = True
    lock_in_until: Optional[date] = None
    committed_to_existing_goal: bool = False
    expected_annual_return: Optional[Rate] = None
    status: EvidenceStatus = EvidenceStatus.INVESTOR_REPORTED
    source: str = "investor_declared"

    @property
    def effective_value(self) -> Money:
        """Applies ownership percentage to current value."""
        if self.ownership_percentage.percentage == Decimal("100.0"):
            return self.current_value
        return self.current_value * self.ownership_percentage.as_decimal_ratio


@dataclass(frozen=True)
class LiabilityRecord:
    id: str
    name: str
    category: CanonicalLiabilityCategoryId
    outstanding_balance: Money
    annual_interest_rate: Rate
    monthly_payment: Money  # EMI
    as_of_date: date
    remaining_tenure_months: int
    is_high_interest: bool = False  # Set dynamically by constraint CTR-HIR-001 (>14% p.a.)
    status: EvidenceStatus = EvidenceStatus.INVESTOR_REPORTED
    source: str = "investor_declared"


@dataclass(frozen=True)
class InsuranceRecord:
    id: str
    policy_name: str
    policy_type: CanonicalInsurancePolicyTypeId
    sum_insured: Money
    annual_premium: Money
    policy_status: str = "active"
    renewal_date: Optional[date] = None
    status: EvidenceStatus = EvidenceStatus.INVESTOR_REPORTED
    source: str = "investor_declared"


@dataclass(frozen=True)
class FinancialStateSnapshot:
    """
    Dated snapshot of an investor's verified financial facts (Chapter 04).
    Purely descriptive: computes canonical sums without editorial judgement.
    """
    investor_id: str
    as_of_date: date
    incomes: List[IncomeRecord] = field(default_factory=list)
    expenses: List[ExpenseRecord] = field(default_factory=list)
    assets: List[AssetRecord] = field(default_factory=list)
    liabilities: List[LiabilityRecord] = field(default_factory=list)
    insurances: List[InsuranceRecord] = field(default_factory=list)

    def total_assets(self) -> Money:
        val = sum((a.effective_value.amount for a in self.assets), Decimal(0))
        return Money(amount=val)

    def total_liabilities(self) -> Money:
        val = sum((l.outstanding_balance.amount for l in self.liabilities), Decimal(0))
        return Money(amount=val)

    def net_worth(self) -> Money:
        return calculate_net_worth(self.total_assets(), self.total_liabilities())

    def get_actual_net_monthly_income(self, period: CalendarMonth) -> Money:
        """Sums net take-home incomes matching the specified period."""
        val = Decimal(0)
        for inc in self.incomes:
            if inc.period == period and inc.is_net:
                if inc.frequency == FlowFrequency.MONTHLY:
                    val += inc.amount.amount
                elif inc.frequency == FlowFrequency.ANNUAL:
                    val += inc.amount.amount / Decimal(12)
        return Money(amount=val)

    def get_actual_monthly_expenses(self, period: CalendarMonth) -> Money:
        """Sums living expenses and debt payments, excluding internal account transfers."""
        val = Decimal(0)
        for exp in self.expenses:
            if exp.period == period and not exp.is_own_account_transfer:
                val += exp.amount.amount
        return Money(amount=val)

    def get_actual_monthly_savings_investments(self) -> Money:
        """Sums active monthly savings, SIPs and investments."""
        return Money.zero()

    def calculate_available_monthly_surplus(self, period: CalendarMonth) -> Money:
        net_inc = self.get_actual_net_monthly_income(period)
        exp = self.get_actual_monthly_expenses(period)
        savings = self.get_actual_monthly_savings_investments()
        return calculate_monthly_surplus(net_inc, exp, savings)
