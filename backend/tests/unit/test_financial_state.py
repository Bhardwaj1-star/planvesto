"""
Unit tests for Chapter 04 Financial State models and aggregations.
"""

from datetime import date
from decimal import Decimal
from app.domain.canonical.financial_categories import (
    CanonicalIncomeCategoryId,
    CanonicalExpenseCategoryId,
    CanonicalAssetCategoryId,
    CanonicalLiabilityCategoryId,
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
    FinancialStateSnapshot,
)


def test_financial_state_snapshot_aggregations():
    nov_2026 = CalendarMonth(year=2026, month=11)
    as_of = date(2026, 11, 16)

    # 1. Income: Salary 1,20,000 net take-home
    income = IncomeRecord(
        id="inc-1",
        category=CanonicalIncomeCategoryId.SALARY,
        amount=Money.from_amount("120000.00"),
        is_net=True,
        frequency=FlowFrequency.MONTHLY,
        period=nov_2026,
    )

    # 2. Expenses: 40,000 household + 25,000 Home Loan EMI
    exp1 = ExpenseRecord(
        id="exp-1",
        category=CanonicalExpenseCategoryId.FOOD_GROCERIES,
        amount=Money.from_amount("40000.00"),
        period=nov_2026,
    )
    exp_emi = ExpenseRecord(
        id="exp-2",
        category=CanonicalExpenseCategoryId.DEBT_PAYMENTS,
        amount=Money.from_amount("25000.00"),
        period=nov_2026,
        is_emi=True,
    )
    # Own-account transfer of 10,000 (must be ignored in expense sum)
    exp_transfer = ExpenseRecord(
        id="exp-3",
        category=CanonicalExpenseCategoryId.OTHER,
        amount=Money.from_amount("10000.00"),
        period=nov_2026,
        is_own_account_transfer=True,
    )

    # 3. Existing savings: 15,000 monthly SIP
    existing_savings = [Money.from_amount("15000.00")]

    # 4. Assets:
    # Mutual fund 10 Lakh (100% owned)
    # Real estate 50 Lakh (50% joint ownership share -> 25 Lakh effective)
    asset_mf = AssetRecord(
        id="ast-1",
        category=CanonicalAssetCategoryId.MUTUAL_FUNDS,
        name="Equity Index Fund",
        value=Money.from_amount("1000000.00"),
        as_of_date=as_of,
    )
    asset_house = AssetRecord(
        id="ast-2",
        category=CanonicalAssetCategoryId.REAL_ESTATE,
        name="Apartment",
        value=Money.from_amount("5000000.00"),
        as_of_date=as_of,
        ownership_share=Rate.from_percentage("50.0"),
    )

    # 5. Liabilities: Home loan 20 Lakh
    liability = LiabilityRecord(
        id="lia-1",
        category=CanonicalLiabilityCategoryId.HOME_LOAN,
        name="Home Loan",
        outstanding_balance=Money.from_amount("2000000.00"),
        annual_interest_rate=Rate.from_percentage("8.5"),
        monthly_payment=Money.from_amount("25000.00"),
        as_of_date=as_of,
    )

    snapshot = FinancialStateSnapshot(
        investor_id="inv-123",
        as_of_date=as_of,
        incomes=[income],
        expenses=[exp1, exp_emi, exp_transfer],
        monthly_savings_investments=existing_savings,
        assets=[asset_mf, asset_house],
        liabilities=[liability],
    )

    # Total assets: 10 Lakh + 25 Lakh (50% of 50 Lakh) = 35 Lakh
    assert snapshot.total_assets().amount == Decimal("3500000.00")

    # Total liabilities: 20 Lakh
    assert snapshot.total_liabilities().amount == Decimal("2000000.00")

    # Net worth: 35 Lakh - 20 Lakh = 15 Lakh
    assert snapshot.net_worth().amount == Decimal("1500000.00")

    # Monthly cash flow:
    # Net income = 1,20,000
    # Expenses = 40,000 + 25,000 = 65,000 (Transfer excluded)
    # Savings = 15,000
    # Available surplus = 1,20,000 - 65,000 - 15,000 = 40,000
    assert snapshot.get_actual_net_monthly_income(nov_2026).amount == Decimal("120000.00")
    assert snapshot.get_actual_monthly_expenses(nov_2026).amount == Decimal("65000.00")
    assert snapshot.get_actual_monthly_savings_investments().amount == Decimal("15000.00")
    assert snapshot.calculate_available_monthly_surplus(nov_2026).amount == Decimal("40000.00")
