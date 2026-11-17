"""
domain/features/moneywheel/assessment.py
Chapter 05 & Chapter 09 — Moneywheel Canonical Measurements.

Non-negotiable invariants:
1. Do not invent a combined health score, universal severity label, or pass/fail result.
2. Present evidence and interpretation separately so the investor understands why.
3. Keep factual measurements distinct from qualitative diagnostic findings.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List, Optional

from app.domain.canonical.financial_categories import CanonicalAssetCategoryId
from app.domain.shared.value_objects import (
    Money,
    Rate,
    CalendarMonth,
)
from app.domain.shared.calculations import (
    DebtItem,
    calculate_savings_rate,
    calculate_debt_to_income_ratio,
    calculate_leverage_ratio,
    calculate_liquid_asset_ratio,
    calculate_financial_asset_ratio,
    calculate_portfolio_concentration,
    calculate_weighted_debt_rate,
)
from app.domain.features.investor_profile.financial_state.models import FinancialStateSnapshot
from app.domain.features.moneywheel.findings import AssessmentFinding
from app.domain.features.moneywheel.protection import (
    calculate_required_life_cover,
    evaluate_existing_life_insurance,
    evaluate_life_coverage_ratio,
    evaluate_health_insurance,
)


@dataclass(frozen=True)
class MoneywheelMeasurements:
    """Canonical measurements and ratios calculated from Financial State (Chapter 05)."""
    as_of_date: date

    # Group A: Basic Position
    net_worth: Money

    # Group B: Monthly Cash Flow
    net_monthly_income: Money
    monthly_expenses: Money
    monthly_savings_investments: Money
    available_monthly_surplus: Money
    savings_rate: Optional[Rate]

    # Group C: Debt & Assets
    monthly_debt_payments: Money
    total_liabilities: Money
    total_assets: Money
    liquid_assets: Money
    financial_assets: Money
    largest_single_asset: Money

    debt_to_income_ratio: Optional[Rate]
    leverage_ratio: Optional[Rate]
    liquid_asset_ratio: Optional[Rate]
    financial_asset_ratio: Optional[Rate]
    portfolio_concentration: Optional[Rate]
    weighted_debt_rate: Optional[Rate]

    # Chapter 09 §4.1: Protection Coverage
    gross_annual_income: Money
    required_life_cover: Money
    existing_life_sum_assured: Money
    life_insurance_coverage_ratio: Optional[Rate]
    has_active_health_insurance: bool
    total_health_sum_insured: Money


@dataclass(frozen=True)
class MoneywheelAssessmentResult:
    """Complete Moneywheel output containing measurements and explainable findings."""
    investor_id: str
    evaluation_date: date
    measurements: MoneywheelMeasurements
    findings: List[AssessmentFinding]


def compute_moneywheel_measurements(
    snapshot: FinancialStateSnapshot,
    period: CalendarMonth,
) -> MoneywheelMeasurements:
    """
    Sub-feature 1: Computes all Chapter 05 canonical measurements from Financial State.
    """
    # 1. Assets & Net Worth
    total_assets = snapshot.total_assets()
    total_liabilities = snapshot.total_liabilities()
    net_worth = snapshot.net_worth()

    # Liquid Assets (Bank/Cash and unencumbered accessible liquid holdings)
    liquid_categories = {
        CanonicalAssetCategoryId.BANK_CASH,
        CanonicalAssetCategoryId.FIXED_DEPOSITS,
    }
    liquid_sum = sum(
        (a.effective_value.amount for a in snapshot.assets if a.category in liquid_categories and a.is_accessible),
        Decimal(0),
    )
    liquid_assets = Money(amount=liquid_sum)

    # Financial Assets (excluding real estate, physical vehicle, personal physical assets)
    physical_categories = {
        CanonicalAssetCategoryId.REAL_ESTATE,
        CanonicalAssetCategoryId.VEHICLE,
        CanonicalAssetCategoryId.GOLD,
    }
    financial_sum = sum(
        (a.effective_value.amount for a in snapshot.assets if a.category not in physical_categories),
        Decimal(0),
    )
    financial_assets = Money(amount=financial_sum)

    # Largest single asset
    largest_asset_val = max(
        (a.effective_value.amount for a in snapshot.assets),
        default=Decimal(0),
    )
    largest_single_asset = Money(amount=largest_asset_val)

    # 2. Monthly Cash Flow
    net_income = snapshot.get_actual_net_monthly_income(period)
    expenses = snapshot.get_actual_monthly_expenses(period)
    savings = snapshot.get_actual_monthly_savings_investments()
    surplus = snapshot.calculate_available_monthly_surplus(period)
    savings_rate = calculate_savings_rate(savings, net_income)

    # 3. Debt & Ratios
    monthly_debt_payments_sum = sum((l.monthly_payment.amount for l in snapshot.liabilities), Decimal(0))
    monthly_debt_payments = Money(amount=monthly_debt_payments_sum)

    dti = calculate_debt_to_income_ratio(monthly_debt_payments, net_income)
    leverage = calculate_leverage_ratio(total_liabilities, total_assets)
    liq_ratio = calculate_liquid_asset_ratio(liquid_assets, total_assets)
    fin_ratio = calculate_financial_asset_ratio(financial_assets, total_assets)
    concentration = calculate_portfolio_concentration(largest_single_asset, total_assets)

    debt_items = [
        DebtItem(outstanding_principal=l.outstanding_balance, annual_interest_rate=l.annual_interest_rate)
        for l in snapshot.liabilities
    ]
    weighted_debt_rate = calculate_weighted_debt_rate(debt_items)

    # 4. Protection (Chapter 09 §4.1)
    annual_income = net_income * 12
    required_life_cover = calculate_required_life_cover(annual_income, total_liabilities)
    existing_life_cover = evaluate_existing_life_insurance(snapshot.insurances)
    life_coverage_ratio = evaluate_life_coverage_ratio(existing_life_cover, required_life_cover)
    has_health, total_health_cover = evaluate_health_insurance(snapshot.insurances)

    return MoneywheelMeasurements(
        as_of_date=snapshot.as_of_date,
        net_worth=net_worth,
        net_monthly_income=net_income,
        monthly_expenses=expenses,
        monthly_savings_investments=savings,
        available_monthly_surplus=surplus,
        savings_rate=savings_rate,
        monthly_debt_payments=monthly_debt_payments,
        total_liabilities=total_liabilities,
        total_assets=total_assets,
        liquid_assets=liquid_assets,
        financial_assets=financial_assets,
        largest_single_asset=largest_single_asset,
        debt_to_income_ratio=dti,
        leverage_ratio=leverage,
        liquid_asset_ratio=liq_ratio,
        financial_asset_ratio=fin_ratio,
        portfolio_concentration=concentration,
        weighted_debt_rate=weighted_debt_rate,
        gross_annual_income=annual_income,
        required_life_cover=required_life_cover,
        existing_life_sum_assured=existing_life_cover,
        life_insurance_coverage_ratio=life_coverage_ratio,
        has_active_health_insurance=has_health,
        total_health_sum_insured=total_health_cover,
    )
