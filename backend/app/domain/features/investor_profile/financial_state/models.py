"""
Canonical Chapter 04 Financial State domain model.

This is the single source of truth for investor financial facts and derived
cash-flow/net-worth measurements. Persistence and API layers translate to and
from these domain records; downstream features consume this snapshot.
"""
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List, Optional

from app.domain.canonical.financial_categories import (
    CanonicalIncomeCategoryId, CanonicalExpenseCategoryId,
    CanonicalAssetCategoryId, CanonicalLiabilityCategoryId,
    CanonicalInsurancePolicyTypeId,
)
from app.domain.shared.value_objects import (
    Money, Rate, CalendarMonth, EvidenceStatus, FlowFrequency,
)
from app.domain.shared.calculations.net_worth import calculate_net_worth
from app.domain.shared.calculations.cash_flow import calculate_monthly_surplus


@dataclass(frozen=True)
class IncomeRecord:
    id: str
    category: CanonicalIncomeCategoryId
    amount: Money
    is_net: bool
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
    is_own_account_transfer: bool = False
    status: EvidenceStatus = EvidenceStatus.INVESTOR_REPORTED
    source: str = "investor_declared"
    notes: Optional[str] = None


@dataclass(frozen=True)
class AssetRecord:
    """Dated asset fact; legacy field names are exposed as read-only aliases."""
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
    expected_annual_return: Optional[Rate] = None
    lock_in_until: Optional[date] = None

    @property
    def effective_value(self) -> Money:
        return self.value * self.ownership_share.as_decimal_ratio

    @property
    def current_value(self) -> Money:
        return self.value

    @property
    def ownership_percentage(self) -> Rate:
        return self.ownership_share

    @property
    def committed_to_existing_goal(self) -> bool:
        return self.is_committed


@dataclass(frozen=True)
class LiabilityRecord:
    id: str
    category: CanonicalLiabilityCategoryId
    name: str
    outstanding_balance: Money
    annual_interest_rate: Rate
    monthly_payment: Money
    as_of_date: date
    remaining_tenure_months: int = 0
    is_high_interest: bool = False
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

    @property
    def annual_premium(self) -> Money:
        if self.premium_frequency == FlowFrequency.MONTHLY:
            return self.premium * 12
        if self.premium_frequency == FlowFrequency.QUARTERLY:
            return self.premium * 4
        if self.premium_frequency == FlowFrequency.SEMI_ANNUAL:
            return self.premium * 2
        return self.premium


@dataclass
class FinancialStateSnapshot:
    """Validated, dated baseline of an investor's financial facts."""
    investor_id: str
    as_of_date: date
    incomes: List[IncomeRecord] = field(default_factory=list)
    expenses: List[ExpenseRecord] = field(default_factory=list)
    monthly_savings_investments: List[Money] = field(default_factory=list)
    assets: List[AssetRecord] = field(default_factory=list)
    liabilities: List[LiabilityRecord] = field(default_factory=list)
    insurances: List[InsuranceRecord] = field(default_factory=list)

    def total_assets(self) -> Money:
        total = sum((asset.effective_value.amount for asset in self.assets), Decimal("0"))
        currency = self.assets[0].value.currency if self.assets else Money.zero().currency
        return Money(amount=total, currency=currency)

    def total_liabilities(self) -> Money:
        total = sum((item.outstanding_balance.amount for item in self.liabilities), Decimal("0"))
        currency = self.liabilities[0].outstanding_balance.currency if self.liabilities else Money.zero().currency
        return Money(amount=total, currency=currency)

    def net_worth(self) -> Money:
        return calculate_net_worth(self.total_assets(), self.total_liabilities())

    def get_actual_net_monthly_income(self, period: CalendarMonth) -> Money:
        """Sum net income after normalizing its declared frequency to monthly."""
        from app.domain.features.investor_profile.financial_state.normalization import normalize_income_to_monthly

        total = Decimal("0")
        currency = Money.zero().currency
        for income in self.incomes:
            if income.period == period and income.is_net:
                monthly = normalize_income_to_monthly(income)
                total += monthly.amount
                currency = monthly.currency
        return Money(amount=total, currency=currency)

    def get_actual_monthly_expenses(self, period: CalendarMonth) -> Money:
        """Sum monthly expenses, excluding transfers between own accounts."""
        matching = [
            item for item in self.expenses
            if item.period == period and not item.is_own_account_transfer
        ]
        total = sum((item.amount.amount for item in matching), Decimal("0"))
        currency = matching[0].amount.currency if matching else Money.zero().currency
        return Money(amount=total, currency=currency)

    def get_actual_monthly_savings_investments(self) -> Money:
        """Sum recurring monthly savings and investment contributions."""
        total = sum((item.amount for item in self.monthly_savings_investments), Decimal("0"))
        currency = self.monthly_savings_investments[0].currency if self.monthly_savings_investments else Money.zero().currency
        return Money(amount=total, currency=currency)

    def calculate_available_monthly_surplus(self, period: CalendarMonth) -> Money:
        """Net monthly income less expenses and existing savings/investments."""
        return calculate_monthly_surplus(
            self.get_actual_net_monthly_income(period),
            self.get_actual_monthly_expenses(period),
            self.get_actual_monthly_savings_investments(),
        )
