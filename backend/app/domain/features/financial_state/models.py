"""
domain/features/financial_state/models.py
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
    category: CanonicalAssetCategoryId
    name: str
    value: Money
    as_of_date: date
    ownership_share: Rate = Rate.from_percentage("100.0")
    is_accessible: bool = True
    access_restrictions: List[str] = field(default_factory=list)
    is_committed: bool = False
    committed_goal_id: Optional[str] = None
    status: EvidenceStatus = EvidenceStatus.INVESTOR_REPORTED
    source: str = "investor_declared"

    @property
    def effective_value(self) -> Money:
        """Effective asset value belonging to investor based on ownership share."""
        share_ratio = self.ownership_share.as_decimal_ratio
        return self.value * share_ratio


@dataclass(frozen=True)
class LiabilityRecord:
    id: str
    category: CanonicalLiabilityCategoryId
    name: str
    outstanding_balance: Money
    annual_interest_rate: Rate
    monthly_payment: Money  # EMI or scheduled monthly payment
    as_of_date: date
    status: EvidenceStatus = EvidenceStatus.INVESTOR_REPORTED
    source: str = "investor_declared"


@dataclass(frozen=True)
class InsuranceRecord:
    id: str
    policy_type: CanonicalInsurancePolicyTypeId
    policy_name: str
    sum_insured: Money
    premium: Money
    premium_frequency: FlowFrequency = FlowFrequency.ANNUAL
    policy_status: str = "active"
    status: EvidenceStatus = EvidenceStatus.INVESTOR_REPORTED
    source: str = "investor_declared"


@dataclass
class FinancialStateSnapshot:
    """
    Chapter 04 Dated baseline holding an investor's validated financial facts.
    """
    investor_id: str
    as_of_date: date
    incomes: List[IncomeRecord] = field(default_factory=list)
    expenses: List[ExpenseRecord] = field(default_factory=list)
    monthly_savings_investments: List[Money] = field(default_factory=list)
    assets: List[AssetRecord] = field(default_factory=list)
    liabilities: List[LiabilityRecord] = field(default_factory=list)
    insurances: List[InsuranceRecord] = field(default_factory=list)

    def total_assets(self) -> Money:
        """Sum of all investor-owned asset effective values."""
        if not self.assets:
            return Money.zero()
        total = sum((a.effective_value.amount for a in self.assets), Decimal(0))
        return Money(amount=total)

    def total_liabilities(self) -> Money:
        """Sum of all outstanding liabilities."""
        if not self.liabilities:
            return Money.zero()
        total = sum((l.outstanding_balance.amount for l in self.liabilities), Decimal(0))
        return Money(amount=total)

    def net_worth(self) -> Money:
        """metric_net_worth = Total Assets − Total Liabilities."""
        return calculate_net_worth(self.total_assets(), self.total_liabilities())

    def get_actual_net_monthly_income(self, period: CalendarMonth) -> Money:
        """
        Total net monthly income for calendar month (excluding one-off or gross amounts).
        """
        matching = [
            inc for inc in self.incomes
            if inc.period == period and inc.is_net and inc.frequency == FlowFrequency.MONTHLY
        ]
        total = sum((inc.amount.amount for inc in matching), Decimal(0))
        return Money(amount=total)

    def get_actual_monthly_expenses(self, period: CalendarMonth) -> Money:
        """
        Total monthly expenses for calendar month (excluding own-account transfers).
        """
        matching = [
            exp for exp in self.expenses
            if exp.period == period and not exp.is_own_account_transfer
        ]
        total = sum((exp.amount.amount for exp in matching), Decimal(0))
        return Money(amount=total)

    def get_actual_monthly_savings_investments(self) -> Money:
        """Total regular monthly contributions to savings/SIPs."""
        total = sum((s.amount for s in self.monthly_savings_investments), Decimal(0))
        return Money(amount=total)

    def calculate_available_monthly_surplus(self, period: CalendarMonth) -> Money:
        """
        metric_monthly_surplus = Net Monthly Income − Expenses − Savings/Investments
        """
        net_income = self.get_actual_net_monthly_income(period)
        expenses = self.get_actual_monthly_expenses(period)
        savings = self.get_actual_monthly_savings_investments()
        return calculate_monthly_surplus(net_income, expenses, savings)
