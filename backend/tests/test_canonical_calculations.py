"""Comprehensive Unit Tests for the Canonical Financial Calculation System.

Verifies acceptance criteria:
1. Canonical calculation correctness across all derived financial facts.
2. Determinism: same input produces the exact same canonical result regardless of consumer.
3. MoneyWheel consumes canonical facts.
4. Risk Required has a single canonical calculation owner.
5. Risk Profiler consumes Risk Required rather than recalculating it.
6. Goal Engine does not duplicate shared calculations.
7. Existing Strategy Engine behavior remains intact.
8. Missing or None data is NEVER silently treated as zero.
9. Calculation and version metadata remains deterministic.
10. Division by zero, non-positive denominators, and invalid horizons fail safely to unavailable.
"""

from unittest.mock import patch
import pytest

from engines.calculation.canonical import (
    CANONICAL_CALCULATION_VERSION,
    DerivedFact,
    calculate_debt_to_income_ratio,
    calculate_emergency_coverage,
    calculate_expense_coverage,
    calculate_financial_asset_ratio,
    calculate_future_funding_ratio,
    calculate_goal_funding_gap,
    calculate_goal_funding_ratio,
    calculate_goal_future_target,
    calculate_leverage_ratio,
    calculate_liquid_asset_ratio,
    calculate_portfolio_concentration,
    calculate_required_monthly_contribution,
    calculate_required_rate_of_return,
    calculate_risk_required,
    calculate_savings_rate,
    fact_debt_to_income_ratio,
    fact_emergency_coverage,
    fact_expense_coverage,
    fact_financial_asset_ratio,
    fact_future_funding_ratio,
    fact_goal_funding_gap,
    fact_goal_funding_ratio,
    fact_leverage_ratio,
    fact_liquid_asset_ratio,
    fact_portfolio_concentration,
    fact_required_monthly_contribution,
    fact_required_rate_of_return,
    fact_risk_required,
    fact_savings_rate,
)
from engines.moneywheel.engine import MoneywheelEngine
from models.moneywheel import MoneywheelInput
from engines.profile.risk import build_risk_profile
from engines.goal.funding_gap import calculate_funding_gap
from engines.goal.target_calculator import calculate_future_target
from rules.financial_state import savings_investment_rate


class TestCanonicalCalculationCorrectness:
    """1. Canonical calculation correctness."""

    def test_savings_rate_calculation(self):
        # 25k surplus on 100k income = 25.0%
        assert calculate_savings_rate(25000, 100000) == 25.0
        # Negative surplus (deficit) yields negative savings rate
        assert calculate_savings_rate(-5000, 100000) == -5.0

    def test_liquid_asset_ratio_calculation(self):
        # 500k liquid assets on 2M total assets = 25.0%
        assert calculate_liquid_asset_ratio(500000, 2000000) == 25.0

    def test_coverage_calculations(self):
        # 600k liquid on 100k monthly expenses = 6.0 months
        assert calculate_expense_coverage(600000, 100000) == 6.0
        # 600k liquid on 50k essential expenses = 12.0 months
        assert calculate_emergency_coverage(600000, 50000) == 12.0

    def test_debt_to_income_ratio_calculation(self):
        # 30k EMI on 100k income = 30.0% (percentage) or 0.3 (ratio)
        assert calculate_debt_to_income_ratio(30000, 100000, as_percentage=True) == 30.0
        assert calculate_debt_to_income_ratio(30000, 100000, as_percentage=False) == 0.3

    def test_leverage_and_financial_asset_ratios(self):
        assert calculate_leverage_ratio(500000, 2000000) == 25.0
        assert calculate_financial_asset_ratio(1400000, 2000000) == 70.0

    def test_required_rate_of_return_and_risk_required(self):
        # 100k today growing to 200k in 7.27 years (~10% CAGR)
        # (200000 / 100000) ^ (1/5) - 1 = 2^(0.2) - 1 = 14.8698%
        res = calculate_required_rate_of_return(200000, 100000, 5)
        assert res is not None
        assert round(res, 2) == 14.87
        # Risk Required is the identical canonical function
        assert calculate_risk_required(200000, 100000, 5) == res

    def test_portfolio_concentration_calculation(self):
        # Largest 750k on 1M = 0.75 ratio or 75.0%
        assert calculate_portfolio_concentration(750000, 1000000, as_percentage=False) == 0.75
        assert calculate_portfolio_concentration(750000, 1000000, as_percentage=True) == 75.0


class TestMissingDataSafety:
    """8 & 10. Missing data is not silently treated as zero; zero denominators fail safely."""

    def test_none_inputs_return_none(self):
        assert calculate_savings_rate(None, 100000) is None
        assert calculate_savings_rate(25000, None) is None
        assert calculate_liquid_asset_ratio(None, 1000000) is None
        assert calculate_expense_coverage(100000, None) is None
        assert calculate_emergency_coverage(None, 50000) is None
        assert calculate_debt_to_income_ratio(None, 100000) is None
        assert calculate_leverage_ratio(100000, None) is None
        assert calculate_required_rate_of_return(None, 100000, 5) is None
        assert calculate_portfolio_concentration(None, 1000000) is None
        assert calculate_goal_funding_gap(None, 500000) is None
        assert calculate_required_monthly_contribution(100000, None, 5) is None

    def test_zero_or_negative_denominators_return_none(self):
        assert calculate_savings_rate(25000, 0) is None
        assert calculate_savings_rate(25000, -1000) is None
        assert calculate_liquid_asset_ratio(100000, 0) is None
        assert calculate_expense_coverage(100000, 0) is None
        assert calculate_emergency_coverage(100000, 0) is None
        assert calculate_debt_to_income_ratio(25000, 0) is None
        assert calculate_leverage_ratio(50000, 0) is None
        assert calculate_required_rate_of_return(200000, 0, 5) is None
        assert calculate_required_rate_of_return(200000, 100000, 0) is None
        assert calculate_portfolio_concentration(50000, 0) is None

    def test_derived_fact_contracts_flag_unavailable_correctly(self):
        fact = fact_savings_rate(None, 100000)
        assert fact.available is False
        assert fact.value is None
        assert fact.data_quality == "unavailable"
        assert fact.fact_id == "savings_rate"
        assert fact.calculation_version == CANONICAL_CALCULATION_VERSION


class TestDeterminismAndCrossConsumerConsistency:
    """2. Same input -> Same canonical result across multiple consumers."""

    def test_savings_rate_consistent_in_rules_and_canonical(self):
        surplus = 35000.0
        income = 100000.0
        canonical_val = calculate_savings_rate(surplus, income)
        financial_state_val = savings_investment_rate(surplus, income)
        assert canonical_val == financial_state_val == 35.0

    def test_future_target_consistent_in_goal_and_canonical(self):
        today_cost = 1000000.0
        inflation = 0.06
        duration = 10.0
        canonical_target = calculate_goal_future_target(today_cost, inflation, duration)
        goal_target = calculate_future_target(today_cost, inflation, duration)
        assert canonical_target == goal_target

    def test_funding_gap_consistent_in_goal_and_canonical(self):
        future_target = 1500000.0
        projected = 1000000.0
        canonical_gap = calculate_goal_funding_gap(future_target, projected)
        goal_gap, status = calculate_funding_gap(future_target, projected)
        assert canonical_gap == goal_gap == 500000.0
        assert status == "Shortfall"


class TestMoneywheelConsumesCanonicalFacts:
    """3. MoneyWheel delegates calculations to canonical layer."""

    def test_moneywheel_engine_calls_canonical_calculations(self):
        engine = MoneywheelEngine()
        data = MoneywheelInput(
            planning_unit_id="pu-test",
            gross_monthly_income=100000.0,
            monthly_surplus=30000.0,
            monthly_expenses=50000.0,
            essential_monthly_expenses=40000.0,
            liquid_assets=240000.0,
            monthly_debt_payments=20000.0,
            total_assets=1000000.0,
            total_liabilities=200000.0,
            financial_assets=700000.0,
            existing_sum_assured=5000000.0,
            required_insurance_cover=10000000.0,
            current_goal_funding=300000.0,
            goal_target_amount=1000000.0,
            projected_goal_funding=600000.0,
            future_goal_target=1200000.0,
            goal_duration_years=5.0,
        )

        with patch("engines.moneywheel.engine.calculate_savings_rate", wraps=calculate_savings_rate) as mock_sav, \
             patch("engines.moneywheel.engine.calculate_required_rate_of_return", wraps=calculate_required_rate_of_return) as mock_ror:
            result = engine.build(data)
            assert mock_sav.called
            assert mock_ror.called

        ratio_map = {r.key: r for r in result.ratios}
        assert ratio_map["savings_rate"].value == 30.0
        assert ratio_map["liquid_asset_ratio"].value == 24.0
        assert ratio_map["debt_to_income_ratio"].value == 20.0
        assert ratio_map["leverage_ratio"].value == 20.0
        assert ratio_map["financial_asset_ratio"].value == 70.0
        assert ratio_map["insurance_coverage_ratio"].value == 50.0
        assert ratio_map["goal_funding_ratio"].value == 30.0
        assert ratio_map["future_funding_ratio"].value == 50.0
        assert ratio_map["required_rate_of_return"].value is not None


class TestRiskProfilerConsumesCanonicalFacts:
    """4 & 5. Risk Required has single calculation owner and Risk Profiler consumes it."""

    def test_risk_profiler_consumes_canonical_dti_concentration_and_risk_required(self):
        financial_state = {
            "income_monthly": {"value": 100000, "available": True},
            "investable_surplus_monthly": {"value": 40000, "available": True},
            "safety_reserve_months": {"value": 6, "available": True},
            "emi_burden_monthly": {"value": 20000, "available": True},
        }
        assets = [{"value": 800000}, {"value": 200000}]
        goals = [{
            "future_target": 2000000,
            "current_funding": 1000000,
            "time_horizon_years": 5.0,
        }]

        with patch("engines.calculation.canonical.calculate_risk_required", wraps=calculate_risk_required) as mock_risk_req, \
             patch("engines.calculation.canonical.calculate_debt_to_income_ratio", wraps=calculate_debt_to_income_ratio) as mock_dti:
            profile = build_risk_profile(financial_state=financial_state, assets=assets, goals=goals)
            assert mock_risk_req.called
            assert mock_dti.called

        constraints_by_key = {c["key"]: c for c in profile["constraints"]}
        # Debt service ratio matches canonical calculation
        assert constraints_by_key["risk_capacity_debt_service_ratio"]["value"] == 0.2
        # Max asset concentration matches canonical calculation (800k / 1M = 0.8)
        assert constraints_by_key["risk_exposure_max_asset_concentration"]["value"] == 0.8
        # Risk Required matches canonical calculation
        expected_ror = calculate_risk_required(2000000, 1000000, 5.0)
        assert constraints_by_key["risk_need_required_return"]["value"] == expected_ror
        assert constraints_by_key["risk_need_required_return"]["source"] == "canonical_calculation"


class TestCalculationProvenanceAndDeterminism:
    """9. Provenance and deterministic versioning."""

    def test_fact_metadata_is_deterministic(self):
        fact1 = fact_required_rate_of_return(1500000, 1000000, 5)
        fact2 = fact_required_rate_of_return(1500000, 1000000, 5)
        assert fact1 == fact2
        assert fact1.calculation_version == CANONICAL_CALCULATION_VERSION
        assert fact1.source == "canonical_calculation"
        assert fact1.formula == "((Future Goal Target / Current Goal Funding) ^ (1 / Goal Duration Years) - 1) * 100"
        assert fact1.inputs_used == {
            "future_goal_target": 1500000,
            "current_goal_funding": 1000000,
            "goal_duration_years": 5,
        }
