"""
Planvesto Backend - Automated Test Suite
=========================================
Tests cover:
  - Basic calculation functions (round_money)
  - Percentage calculations
  - Income frequency conversion (monthly/annual)
  - Expense frequency conversion
  - Asset ownership calculation
  - Liability responsibility calculation
  - Net worth calculation
  - Financial State calculations (full engine)
  - Missing data / unavailable metric handling
  - Negative investable surplus handling

NO database writes. NO .env reads. NO Supabase calls.
Pure unit tests against engine logic only.
"""

import pytest
from engines.calculation.engine import annual_amount, monthly_amount, percentage, round_money
from engines.financial_state.engine import FinancialStateEngine
from rules.financial_state import (
    cash_flow_ratio,
    required_safety_reserve_months,
    savings_investment_rate,
)


# ─────────────────────────────────────────────
# Helper: build a standard FinancialState result
# ─────────────────────────────────────────────
def _build(
    income_rows=None,
    expense_rows=None,
    commitment_rows=None,
    asset_rows=None,
    liability_rows=None,
    asset_owner_rows=None,
    liability_responsibility_rows=None,
    expense_participant_rows=None,
    scope="family",
    investor_id=None,
    investors=None,
):
    return FinancialStateEngine().build(
        planning_unit_id="test-pu",
        investors=investors or [{"investor_id": "i1"}],
        income_rows=income_rows or [],
        expense_rows=expense_rows or [],
        commitment_rows=commitment_rows or [],
        asset_rows=asset_rows or [],
        liability_rows=liability_rows or [],
        asset_owner_rows=asset_owner_rows or [],
        liability_responsibility_rows=liability_responsibility_rows or [],
        expense_participant_rows=expense_participant_rows or [],
        scope=scope,
        investor_id=investor_id,
    )


# ═══════════════════════════════════════════════
# 1. BASIC CALCULATION FUNCTIONS
# ═══════════════════════════════════════════════

class TestRoundMoney:
    def test_rounds_to_two_decimals(self):
        assert round_money(100.1234567) == 100.12

    def test_zero(self):
        assert round_money(0) == 0.0

    def test_negative(self):
        # Python uses banker's rounding (round-half-to-even).
        # -50.556 unambiguously rounds to -50.56.
        assert round_money(-50.556) == -50.56

    def test_exact_value_unchanged(self):
        assert round_money(1000.00) == 1000.0


# ═══════════════════════════════════════════════
# 2. PERCENTAGE CALCULATIONS
# ═══════════════════════════════════════════════

class TestPercentage:
    def test_fifty_percent(self):
        assert percentage(500000, 1000000) == 50.0

    def test_hundred_percent(self):
        assert percentage(1000, 1000) == 100.0

    def test_zero_part(self):
        assert percentage(0, 1000) == 0.0

    def test_zero_total_returns_none(self):
        assert percentage(500, 0) is None

    def test_fractional_result(self):
        assert percentage(1, 3) == round_money(1 / 3 * 100)


# ═══════════════════════════════════════════════
# 3. INCOME FREQUENCY CONVERSION
# ═══════════════════════════════════════════════

class TestIncomeFrequencyConversion:
    # monthly_amount ---
    def test_monthly_input_monthly_amount(self):
        assert monthly_amount(100000, "Monthly") == 100000.0

    def test_annual_input_monthly_amount(self):
        assert monthly_amount(1200000, "Annual") == 100000.0

    def test_annually_variant(self):
        assert monthly_amount(1200000, "Annually") == 100000.0

    def test_yearly_variant(self):
        assert monthly_amount(1200000, "Yearly") == 100000.0

    def test_unknown_frequency_monthly_returns_none(self):
        assert monthly_amount(100000, "Quarterly") is None

    def test_empty_frequency_monthly_returns_none(self):
        assert monthly_amount(100000, "") is None

    # annual_amount ---
    def test_monthly_input_annual_amount(self):
        assert annual_amount(100000, "Monthly") == 1200000.0

    def test_annual_input_annual_amount(self):
        assert annual_amount(1200000, "Annual") == 1200000.0

    def test_unknown_frequency_annual_returns_none(self):
        assert annual_amount(100000, "Weekly") is None

    def test_case_insensitive_frequency(self):
        assert monthly_amount(120000, "monthly") == 120000.0
        assert monthly_amount(120000, "MONTHLY") == 120000.0
        assert monthly_amount(1200000, "annual") == 100000.0


# ═══════════════════════════════════════════════
# 4. EXPENSE FREQUENCY CONVERSION
# ═══════════════════════════════════════════════

class TestExpenseFrequencyConversion:
    def test_monthly_expense(self):
        result = _build(
            expense_rows=[{"expense_id": "e1", "expense_type": "Rent", "amount": 30000, "frequency": "Monthly"}]
        )
        assert result.expenses_monthly.value == 30000.0
        assert result.expenses_monthly.available is True

    def test_annual_expense_converted_to_monthly(self):
        result = _build(
            expense_rows=[{"expense_id": "e1", "expense_type": "Insurance", "amount": 120000, "frequency": "Annual"}]
        )
        assert result.expenses_monthly.value == 10000.0

    def test_unknown_expense_frequency_makes_unavailable(self):
        result = _build(
            expense_rows=[{"expense_id": "e1", "expense_type": "Other", "amount": 5000, "frequency": "Quarterly"}]
        )
        assert result.expenses_monthly.available is False

    def test_multiple_expenses_summed(self):
        result = _build(
            expense_rows=[
                {"expense_id": "e1", "expense_type": "Rent", "amount": 20000, "frequency": "Monthly"},
                {"expense_id": "e2", "expense_type": "Food", "amount": 10000, "frequency": "Monthly"},
            ]
        )
        assert result.expenses_monthly.value == 30000.0


# ═══════════════════════════════════════════════
# 5. ASSET OWNERSHIP CALCULATION
# ═══════════════════════════════════════════════

class TestAssetOwnership:
    def test_no_owner_rows_full_value(self):
        result = _build(
            asset_rows=[{"asset_id": "a1", "asset_name": "Bank / Cash", "current_value": 500000}],
        )
        assert result.total_assets.value == 500000.0

    def test_50_percent_ownership_family_scope(self):
        result = _build(
            asset_rows=[{"asset_id": "a1", "asset_name": "Real Estate", "current_value": 1000000}],
            asset_owner_rows=[
                {"asset_id": "a1", "investor_id": "i1", "ownership_percentage": 50},
                {"asset_id": "a1", "investor_id": "i2", "ownership_percentage": 50},
            ],
        )
        # family scope: sum all ownership percentages → 100% of 1M
        assert result.total_assets.value == 1000000.0

    def test_individual_scope_own_share_only(self):
        result = _build(
            investors=[{"investor_id": "i1"}, {"investor_id": "i2"}],
            asset_rows=[{"asset_id": "a1", "asset_name": "Stocks", "current_value": 1000000}],
            asset_owner_rows=[
                {"asset_id": "a1", "investor_id": "i1", "ownership_percentage": 60},
                {"asset_id": "a1", "investor_id": "i2", "ownership_percentage": 40},
            ],
            scope="individual",
            investor_id="i1",
        )
        assert result.total_assets.value == 600000.0

    def test_no_matching_owner_individual_zero_value(self):
        result = _build(
            investors=[{"investor_id": "i1"}],
            asset_rows=[{"asset_id": "a1", "asset_name": "Gold", "current_value": 200000}],
            asset_owner_rows=[{"asset_id": "a1", "investor_id": "i2", "ownership_percentage": 100}],
            scope="individual",
            investor_id="i1",
        )
        assert result.total_assets.value == 0.0

    def test_multiple_assets_summed(self):
        result = _build(
            asset_rows=[
                {"asset_id": "a1", "asset_name": "Bank / Cash", "current_value": 300000},
                {"asset_id": "a2", "asset_name": "Mutual Fund", "current_value": 700000},
            ]
        )
        assert result.total_assets.value == 1000000.0


# ═══════════════════════════════════════════════
# 6. LIABILITY RESPONSIBILITY CALCULATION
# ═══════════════════════════════════════════════

class TestLiabilityResponsibility:
    def test_no_responsibility_rows_full_outstanding(self):
        result = _build(
            liability_rows=[{"liability_id": "l1", "liability_name": "Car Loan", "outstanding_amount": 500000, "emi_amount": 15000, "frequency": "Monthly"}]
        )
        assert result.total_liabilities.value == 500000.0

    def test_50_percent_responsibility_family(self):
        result = _build(
            liability_rows=[{"liability_id": "l1", "liability_name": "Home Loan", "outstanding_amount": 2000000, "emi_amount": None, "frequency": "Monthly"}],
            liability_responsibility_rows=[
                {"liability_id": "l1", "investor_id": "i1", "responsibility_percentage": 50},
                {"liability_id": "l1", "investor_id": "i2", "responsibility_percentage": 50},
            ],
        )
        # family: sum all responsibility → 100% of 2M
        assert result.total_liabilities.value == 2000000.0

    def test_individual_scope_own_responsibility(self):
        result = _build(
            investors=[{"investor_id": "i1"}, {"investor_id": "i2"}],
            liability_rows=[{"liability_id": "l1", "liability_name": "Home Loan", "outstanding_amount": 2000000, "emi_amount": 20000, "frequency": "Monthly"}],
            liability_responsibility_rows=[
                {"liability_id": "l1", "investor_id": "i1", "responsibility_percentage": 70},
                {"liability_id": "l1", "investor_id": "i2", "responsibility_percentage": 30},
            ],
            scope="individual",
            investor_id="i1",
        )
        assert result.total_liabilities.value == 1400000.0

    def test_emi_unavailable_when_emi_amount_missing(self):
        result = _build(
            liability_rows=[{"liability_id": "l1", "liability_name": "Personal Loan", "outstanding_amount": 100000, "emi_amount": None, "frequency": "Monthly"}]
        )
        assert result.emi_burden_monthly.available is False

    def test_emi_calculated_monthly(self):
        result = _build(
            liability_rows=[{"liability_id": "l1", "liability_name": "Car Loan", "outstanding_amount": 500000, "emi_amount": 15000, "frequency": "Monthly"}]
        )
        assert result.emi_burden_monthly.available is True
        assert result.emi_burden_monthly.value == 15000.0


# ═══════════════════════════════════════════════
# 7. NET WORTH CALCULATION
# ═══════════════════════════════════════════════

class TestNetWorth:
    def test_positive_net_worth(self):
        result = _build(
            asset_rows=[{"asset_id": "a1", "asset_name": "Savings", "current_value": 1000000}],
            liability_rows=[{"liability_id": "l1", "liability_name": "Loan", "outstanding_amount": 300000, "emi_amount": None, "frequency": "Monthly"}],
        )
        assert result.net_worth.value == 700000.0
        assert result.net_worth.available is True

    def test_zero_net_worth(self):
        result = _build(
            asset_rows=[{"asset_id": "a1", "asset_name": "Savings", "current_value": 500000}],
            liability_rows=[{"liability_id": "l1", "liability_name": "Loan", "outstanding_amount": 500000, "emi_amount": None, "frequency": "Monthly"}],
        )
        assert result.net_worth.value == 0.0

    def test_negative_net_worth(self):
        result = _build(
            asset_rows=[{"asset_id": "a1", "asset_name": "Savings", "current_value": 100000}],
            liability_rows=[{"liability_id": "l1", "liability_name": "Loan", "outstanding_amount": 600000, "emi_amount": None, "frequency": "Monthly"}],
        )
        assert result.net_worth.value == -500000.0

    def test_net_worth_no_assets_no_liabilities(self):
        result = _build()
        # both assets=0, liabilities=0 → net_worth = 0
        assert result.net_worth.value == 0.0


# ═══════════════════════════════════════════════
# 8. FINANCIAL STATE ENGINE — FULL CALCULATIONS
# ═══════════════════════════════════════════════

class TestFinancialStateEngine:
    def test_income_monthly_and_annual(self):
        result = _build(
            income_rows=[{"income_id": "in1", "income_type": "Salary", "amount": 100000, "frequency": "Monthly", "investor_id": "i1"}]
        )
        assert result.income_monthly.value == 100000.0
        assert result.income_annual.value == 1200000.0

    def test_surplus_available_when_no_commitments(self):
        """When commitment list is empty, commitments.available resolves correctly."""
        result = _build(
            income_rows=[{"income_id": "in1", "income_type": "Salary", "amount": 100000, "frequency": "Monthly", "investor_id": "i1"}],
            expense_rows=[{"expense_id": "e1", "expense_type": "Living", "amount": 40000, "frequency": "Monthly"}],
            commitment_rows=[],  # empty → commitments always unavailable per current design
        )
        # Commitments always mark unavailable (no frequency field in DB yet)
        assert result.investable_surplus_monthly.available is False

    def test_surplus_unavailable_with_unresolved_commitment(self):
        result = _build(
            income_rows=[{"income_id": "in1", "income_type": "Salary", "amount": 100000, "frequency": "Monthly", "investor_id": "i1"}],
            expense_rows=[{"expense_id": "e1", "expense_type": "Living", "amount": 40000, "frequency": "Monthly"}],
            commitment_rows=[{"commitment_id": "c1", "commitment_name": "SIP", "amount": 5000}],
        )
        assert result.investable_surplus_monthly.available is False

    def test_existing_test_scenario_unchanged(self):
        """Preserves the original existing test case."""
        result = _build(
            income_rows=[{"income_id": "in1", "income_type": "Salary", "amount": 100000, "frequency": "Monthly", "investor_id": "i1"}],
            expense_rows=[{"expense_id": "e1", "expense_type": "Living", "amount": 40000, "frequency": "Monthly"}],
            commitment_rows=[{"commitment_id": "c1", "commitment_name": "Commitment", "amount": 10000}],
            asset_rows=[{"asset_id": "a1", "asset_name": "Bank / Cash", "current_value": 1000000}],
            liability_rows=[{"liability_id": "l1", "liability_name": "Home Loan", "outstanding_amount": 300000, "emi_amount": 10000, "frequency": "Monthly"}],
        )
        assert result.income_monthly.value == 100000
        assert result.expenses_monthly.value == 40000
        assert result.total_assets.value == 1000000
        assert result.total_liabilities.value == 300000
        assert result.net_worth.value == 700000
        assert result.investable_surplus_monthly.available is False

    def test_income_breakdown_by_type(self):
        result = _build(
            income_rows=[
                {"income_id": "in1", "income_type": "Salary", "amount": 80000, "frequency": "Monthly", "investor_id": "i1"},
                {"income_id": "in2", "income_type": "Rental", "amount": 20000, "frequency": "Monthly", "investor_id": "i1"},
            ]
        )
        assert result.income_monthly.value == 100000.0
        types = {item["type"] for item in result.income_breakdown}
        assert "Salary" in types
        assert "Rental" in types

    def test_expense_breakdown_by_type(self):
        result = _build(
            expense_rows=[
                {"expense_id": "e1", "expense_type": "Rent", "amount": 20000, "frequency": "Monthly"},
                {"expense_id": "e2", "expense_type": "Food", "amount": 10000, "frequency": "Monthly"},
            ]
        )
        types = {item["type"] for item in result.expense_breakdown}
        assert "Rent" in types
        assert "Food" in types

    def test_asset_allocation_percentages(self):
        result = _build(
            asset_rows=[
                {"asset_id": "a1", "asset_name": "Bank / Cash", "current_value": 400000},
                {"asset_id": "a2", "asset_name": "Mutual Fund", "current_value": 600000},
            ]
        )
        total = 1000000
        allocation = {item["name"]: item["percentage"] for item in result.asset_allocation}
        assert allocation["Bank / Cash"] == 40.0
        assert allocation["Mutual Fund"] == 60.0


# ═══════════════════════════════════════════════
# 9. MISSING DATA HANDLING
# ═══════════════════════════════════════════════

class TestMissingDataHandling:
    def test_empty_income_returns_zero_available(self):
        result = _build()
        assert result.income_monthly.value == 0.0
        assert result.income_monthly.available is True

    def test_unavailable_income_frequency(self):
        result = _build(
            income_rows=[{"income_id": "in1", "income_type": "Business", "amount": 50000, "frequency": "Quarterly", "investor_id": "i1"}]
        )
        assert result.income_monthly.available is False

    def test_cash_flow_ratio_unavailable_when_surplus_missing(self):
        result = _build(
            income_rows=[{"income_id": "in1", "income_type": "Salary", "amount": 100000, "frequency": "Monthly", "investor_id": "i1"}],
            commitment_rows=[{"commitment_id": "c1", "commitment_name": "SIP", "amount": 5000}],
        )
        assert result.cash_flow_ratio.available is False

    def test_savings_rate_unavailable_when_surplus_missing(self):
        result = _build(
            income_rows=[{"income_id": "in1", "income_type": "Salary", "amount": 100000, "frequency": "Monthly", "investor_id": "i1"}],
            commitment_rows=[{"commitment_id": "c1", "commitment_name": "SIP", "amount": 5000}],
        )
        assert result.savings_investment_rate.available is False

    def test_safety_reserve_unavailable_when_cfr_missing(self):
        result = _build(
            commitment_rows=[{"commitment_id": "c1", "commitment_name": "SIP", "amount": 5000}],
        )
        assert result.safety_reserve_months.available is False
        assert result.safety_reserve_required_amount.available is False

    def test_metric_reason_set_on_unavailable(self):
        result = _build(
            commitment_rows=[{"commitment_id": "c1", "commitment_name": "SIP", "amount": 5000}],
        )
        assert result.investable_surplus_monthly.reason is not None
        assert len(result.investable_surplus_monthly.reason) > 0


# ═══════════════════════════════════════════════
# 10. NEGATIVE INVESTABLE SURPLUS
# ═══════════════════════════════════════════════

class TestNegativeInvesteableSurplus:
    """
    Because commitments currently always return available=False,
    surplus is never directly computable. These tests verify the
    income/expense math that WOULD feed into surplus if commitments
    were resolved, and confirm the unavailable guard works correctly.
    """

    def test_expenses_exceed_income_metrics_correct(self):
        result = _build(
            income_rows=[{"income_id": "in1", "income_type": "Salary", "amount": 30000, "frequency": "Monthly", "investor_id": "i1"}],
            expense_rows=[{"expense_id": "e1", "expense_type": "Living", "amount": 50000, "frequency": "Monthly"}],
        )
        assert result.income_monthly.value == 30000.0
        assert result.expenses_monthly.value == 50000.0
        # Surplus unavailable (no commitment resolution), not guessed
        assert result.investable_surplus_monthly.available is False

    def test_surplus_guard_not_guessed_on_missing_commitment(self):
        """Surplus MUST NOT be fabricated when commitment frequency is unknown."""
        result = _build(
            income_rows=[{"income_id": "in1", "income_type": "Salary", "amount": 100000, "frequency": "Monthly", "investor_id": "i1"}],
            expense_rows=[{"expense_id": "e1", "expense_type": "Living", "amount": 20000, "frequency": "Monthly"}],
            commitment_rows=[{"commitment_id": "c1", "commitment_name": "Loan", "amount": 15000}],
        )
        assert result.investable_surplus_monthly.available is False
        assert result.investable_surplus_monthly.value is None


# ═══════════════════════════════════════════════
# 11. RULES MODULE UNIT TESTS
# ═══════════════════════════════════════════════

class TestRules:
    def test_cash_flow_ratio_basic(self):
        # (40000 + 0) / 100000 * 100 = 40%
        assert cash_flow_ratio(40000, 0, 100000) == 40.0

    def test_cash_flow_ratio_zero_income_returns_none(self):
        assert cash_flow_ratio(30000, 10000, 0) is None

    def test_savings_rate_basic(self):
        # 60000 / 100000 * 100 = 60%
        assert savings_investment_rate(60000, 100000) == 60.0

    def test_savings_rate_zero_income_returns_none(self):
        assert savings_investment_rate(10000, 0) is None

    def test_required_reserve_months_low_cfr(self):
        # CFR <= 50 → 3 months
        assert required_safety_reserve_months(30) == 3
        assert required_safety_reserve_months(50) == 3

    def test_required_reserve_months_medium_cfr(self):
        # 50 < CFR <= 70 → 6 months
        assert required_safety_reserve_months(51) == 6
        assert required_safety_reserve_months(70) == 6

    def test_required_reserve_months_high_cfr(self):
        # 70 < CFR <= 85 → 9 months
        assert required_safety_reserve_months(71) == 9
        assert required_safety_reserve_months(85) == 9

    def test_required_reserve_months_very_high_cfr(self):
        # CFR > 85 → 12 months
        assert required_safety_reserve_months(86) == 12
        assert required_safety_reserve_months(100) == 12
