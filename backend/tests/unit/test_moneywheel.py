"""
Unit tests for Moneywheel (Chapter 05 & 09: Measurements & Financial Health Assessment).
"""

from datetime import date
from decimal import Decimal
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
    FlowFrequency,
)
from app.domain.features.financial_state.models import (
    IncomeRecord,
    ExpenseRecord,
    AssetRecord,
    LiabilityRecord,
    InsuranceRecord,
    FinancialStateSnapshot,
)
from app.domain.features.moneywheel import (
    ResilienceDimension,
    compute_moneywheel_measurements,
    assess_financial_health,
)


def test_moneywheel_measurements_computation():
    nov_2026 = CalendarMonth(year=2026, month=11)
    as_of = date(2026, 11, 16)

    # Income: 1,50,000 / month
    income = IncomeRecord(
        id="inc-1",
        category=CanonicalIncomeCategoryId.SALARY,
        amount=Money.from_amount("150000.00"),
        is_net=True,
        frequency=FlowFrequency.MONTHLY,
        period=nov_2026,
    )

    # Expenses: 60,000 household + 30,000 EMI
    exp1 = ExpenseRecord(
        id="exp-1",
        category=CanonicalExpenseCategoryId.FOOD_GROCERIES,
        amount=Money.from_amount("60000.00"),
        period=nov_2026,
    )
    exp_emi = ExpenseRecord(
        id="exp-2",
        category=CanonicalExpenseCategoryId.DEBT_PAYMENTS,
        amount=Money.from_amount("30000.00"),
        period=nov_2026,
        is_emi=True,
    )

    # Savings: 20,000 monthly
    savings = [Money.from_amount("20000.00")]

    # Assets:
    # 2 Lakh bank cash (liquid)
    # 8 Lakh mutual funds (financial)
    # 40 Lakh property (physical) -> Total 50 Lakh
    asset_cash = AssetRecord(
        id="ast-1",
        category=CanonicalAssetCategoryId.BANK_CASH,
        name="Savings Account",
        value=Money.from_amount("200000.00"),
        as_of_date=as_of,
    )
    asset_mf = AssetRecord(
        id="ast-2",
        category=CanonicalAssetCategoryId.MUTUAL_FUNDS,
        name="Equity Fund",
        value=Money.from_amount("800000.00"),
        as_of_date=as_of,
    )
    asset_house = AssetRecord(
        id="ast-3",
        category=CanonicalAssetCategoryId.REAL_ESTATE,
        name="Apartment",
        value=Money.from_amount("4000000.00"),
        as_of_date=as_of,
    )

    # Liabilities: 25 Lakh Home loan @ 8.5%
    loan = LiabilityRecord(
        id="lia-1",
        category=CanonicalLiabilityCategoryId.HOME_LOAN,
        name="Home Loan",
        outstanding_balance=Money.from_amount("2500000.00"),
        annual_interest_rate=Rate.from_percentage("8.5"),
        monthly_payment=Money.from_amount("30000.00"),
        as_of_date=as_of,
    )

    # Insurance: Term Life 1 Crore
    term_life = InsuranceRecord(
        id="ins-1",
        policy_type=CanonicalInsurancePolicyTypeId.TERM_LIFE,
        policy_name="Term Cover",
        sum_insured=Money.from_amount("10000000.00"),
        premium=Money.from_amount("15000.00"),
    )

    snapshot = FinancialStateSnapshot(
        investor_id="inv-123",
        as_of_date=as_of,
        incomes=[income],
        expenses=[exp1, exp_emi],
        monthly_savings_investments=savings,
        assets=[asset_cash, asset_mf, asset_house],
        liabilities=[loan],
        insurances=[term_life],
    )

    m = compute_moneywheel_measurements(snapshot, nov_2026)

    # 1. Net worth: 50L - 25L = 25 Lakh
    assert m.net_worth.amount == Decimal("2500000.00")

    # 2. Monthly cash flow:
    # 1,50,000 - 90,000 (exp) - 20,000 (savings) = 40,000 Available Surplus
    assert m.available_monthly_surplus.amount == Decimal("40000.00")

    # 3. Liquid assets: 2 Lakh -> Liquid asset ratio = 2L / 50L * 100 = 4.0%
    assert m.liquid_assets.amount == Decimal("200000.00")
    assert m.liquid_asset_ratio.percentage == Decimal("4.00")

    # 4. Financial assets: 2L + 8L = 10 Lakh -> 10L / 50L = 20.0%
    assert m.financial_assets.amount == Decimal("1000000.00")
    assert m.financial_asset_ratio.percentage == Decimal("20.00")

    # 5. Concentration: Largest is Property (40 Lakh) -> 40L / 50L = 80.0%
    assert m.portfolio_concentration.percentage == Decimal("80.00")

    # 6. Protection: Annual income = 1,50,000 * 12 = 18 Lakh.
    # Required Life Cover = (18L * 10) + 25L (liabilities) = 1.8 Cr + 25L = 2.05 Crore
    assert m.required_life_cover.amount == Decimal("20500000.00")
    assert m.existing_life_sum_assured.amount == Decimal("10000000.00")


def test_moneywheel_financial_health_assessment():
    nov_2026 = CalendarMonth(year=2026, month=11)
    as_of = date(2026, 11, 16)

    # Snapshot with:
    # 1. Low liquidity (only 50k cash vs 30L property)
    # 2. High interest personal loan @ 16.5%
    # 3. No health insurance
    income = IncomeRecord(
        id="inc-1",
        category=CanonicalIncomeCategoryId.SALARY,
        amount=Money.from_amount("100000.00"),
        is_net=True,
        frequency=FlowFrequency.MONTHLY,
        period=nov_2026,
    )
    exp = ExpenseRecord(
        id="exp-1",
        category=CanonicalExpenseCategoryId.FOOD_GROCERIES,
        amount=Money.from_amount("50000.00"),
        period=nov_2026,
    )
    asset_house = AssetRecord(
        id="ast-1",
        category=CanonicalAssetCategoryId.REAL_ESTATE,
        name="Apartment",
        value=Money.from_amount("3000000.00"),
        as_of_date=as_of,
    )
    high_loan = LiabilityRecord(
        id="lia-1",
        category=CanonicalLiabilityCategoryId.PERSONAL_LOAN,
        name="Instant Personal Loan",
        outstanding_balance=Money.from_amount("300000.00"),
        annual_interest_rate=Rate.from_percentage("16.5"),  # >14%
        monthly_payment=Money.from_amount("12000.00"),
        as_of_date=as_of,
    )

    snapshot = FinancialStateSnapshot(
        investor_id="inv-456",
        as_of_date=as_of,
        incomes=[income],
        expenses=[exp],
        assets=[asset_house],
        liabilities=[high_loan],
        insurances=[],  # No insurance
    )

    result = assess_financial_health(snapshot, nov_2026)

    assert result.investor_id == "inv-456"
    assert len(result.findings) >= 3

    dimensions = {f.dimension for f in result.findings}
    # Check that key risk dimensions were identified with structured findings
    assert ResilienceDimension.ACCESS_TO_MONEY in dimensions
    assert ResilienceDimension.DEBT_PRESSURE in dimensions
    assert ResilienceDimension.PROTECTION_GAPS in dimensions

    # Verify structured fields exist (Finding, Evidence, Impact, Uncertainty, Consideration)
    for finding in result.findings:
        assert finding.finding
        assert finding.evidence
        assert finding.impact
        assert finding.uncertainty
        assert finding.investor_consideration
