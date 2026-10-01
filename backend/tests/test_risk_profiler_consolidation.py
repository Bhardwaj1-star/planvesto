"""Test suite for the consolidated Risk Profiler, Risk Capacity, and Behavioral Profile.

Verifies the Acceptance Criteria:
1. Canonical Risk Required + Risk Capacity + Risk Tolerance -> single authoritative Risk Profile -> Investment Engine.
2. Every risk/behavioral constraint retains:
   key + value + unit + kind + source + evidence + confidence + validity
3. Risk Required is consumed from the canonical calculation layer, not recalculated.
4. Risk Capacity is a structured assessment derived from observable financial constraints.
5. Risk Tolerance derives from BehavioralRules and observed dimensions (soft, product selection only).
6. No invented personality or risk score.
7. Investment Engine consumes the consolidated RiskProfile directly without recreating risk logic.
8. Unresolved conflicts and constraint provenance are preserved.
"""

from unittest.mock import patch
import pytest

from engines.calculation.canonical import calculate_risk_required
from engines.investment.engine import InvestmentEngine
from engines.investment.models import InvestmentEngineInput
from engines.risk_profiler.engine import RiskProfilerEngine, build_risk_profile
from engines.risk_profiler.models import RiskDimension, RiskProfile


@pytest.fixture
def sample_financial_state():
    return {
        "income_monthly": {"value": 150000.0, "available": True},
        "expenses_monthly": {"value": 80000.0, "available": True},
        "investable_surplus_monthly": {"value": 50000.0, "available": True},
        "safety_reserve_months": {"value": 6.0, "available": True},
        "emi_burden_monthly": {"value": 20000.0, "available": True},
    }


@pytest.fixture
def sample_assets():
    return [
        {"value": 1200000.0, "asset_type": "Mutual Funds"},
        {"value": 800000.0, "asset_type": "Fixed Deposits"},
    ]


@pytest.fixture
def sample_liabilities():
    return [
        {"outstanding": 500000.0, "liability_type": "Home Loan"},
    ]


@pytest.fixture
def sample_goals():
    return [
        {
            "goal_id": "g-retire",
            "future_target": 10000000.0,
            "current_funding": 2000000.0,
            "duration_years": 10.0,
            "time_horizon_years": 10.0,
        }
    ]


@pytest.fixture
def sample_behavior():
    return [
        {
            "dimension": "discipline",
            "key": "sip_adherence",
            "value": "consistent",
            "evidence": [{"type": "historical_sip", "months": 24}],
        },
        {
            "dimension": "volatility_reaction",
            "key": "market_drop_response",
            "value": "held_steady",
            "evidence": [{"event": "covid_crash_2020", "action": "no_panic_sell"}],
        },
    ]


class TestRiskProfilerConsolidation:
    """Verifies that Risk Required + Capacity + Tolerance combine into authoritative RiskProfile."""

    def test_complete_risk_profile_generation(
        self, sample_financial_state, sample_assets, sample_liabilities, sample_goals, sample_behavior
    ):
        profile = build_risk_profile(
            financial_state=sample_financial_state,
            assets=sample_assets,
            liabilities=sample_liabilities,
            goals=sample_goals,
            observed_behavior=sample_behavior,
        )

        assert isinstance(profile, RiskProfile)
        assert profile.is_complete() is True
        assert profile.status == "complete"

        # 1. Canonical Risk Required
        assert profile.risk_required.available is True
        assert profile.risk_required.source == "canonical_calculation"
        assert profile.risk_required.unit == "%"
        expected_ror = calculate_risk_required(10000000.0, 2000000.0, 10.0)
        assert profile.risk_required.value == expected_ror

        # 2. Risk Capacity
        assert profile.risk_capacity.available is True
        assert profile.risk_capacity.source == "financial_state"
        assert len(profile.risk_capacity.constraints) > 0

        # 3. Risk Tolerance
        assert profile.risk_tolerance.available is True
        assert profile.risk_tolerance.source == "observed_behavior"
        assert profile.risk_tolerance.value == 2.0  # 2 observed dimensions
        assert profile.risk_tolerance.unit == "observed_dimensions"

    def test_every_constraint_retains_required_schema(
        self, sample_financial_state, sample_assets, sample_liabilities, sample_goals, sample_behavior
    ):
        profile = build_risk_profile(
            financial_state=sample_financial_state,
            assets=sample_assets,
            liabilities=sample_liabilities,
            goals=sample_goals,
            observed_behavior=sample_behavior,
        )

        required_fields = {"key", "value", "unit", "kind", "source", "evidence", "confidence", "validity"}

        assert len(profile.constraints) > 0
        for constraint in profile.constraints:
            for field in required_fields:
                assert field in constraint, f"Constraint {constraint.get('key')} missing required field: {field}"
            # Ensure validity is a structured dictionary
            assert isinstance(constraint["validity"], dict)
            # Ensure confidence is a float
            assert isinstance(constraint["confidence"], (int, float))

    def test_risk_tolerance_does_not_invent_personality_score(self, sample_behavior):
        profile = build_risk_profile(observed_behavior=sample_behavior)

        # Behavioral constraints are soft and designated for product selection only
        assert profile.risk_tolerance.available is True
        for c in profile.risk_tolerance.constraints:
            assert c["kind"] == "soft"
            assert c["downstream_use"] == "product_selection"
            assert c["source"] == "observed_behavior"
            # Ensure value is the observed value, not an invented numerical risk score
            assert c["value"] in ("consistent", "held_steady")

    def test_partial_and_missing_profiles(self):
        # Empty input -> requires_review
        empty_profile = build_risk_profile()
        assert empty_profile.status == "requires_review"
        assert empty_profile.is_complete() is False
        assert empty_profile.risk_required.available is False
        assert empty_profile.risk_capacity.available is False
        assert empty_profile.risk_tolerance.available is False

        # Only financial state -> partial
        cap_only = build_risk_profile(financial_state={"income_monthly": {"value": 100000, "available": True}, "investable_surplus_monthly": {"value": 20000, "available": True}})
        assert cap_only.status == "partial"
        assert cap_only.risk_capacity.available is True
        assert cap_only.risk_required.available is False
        assert cap_only.risk_tolerance.available is False


class TestInvestmentEngineIntegration:
    """Verifies that InvestmentEngine consumes the consolidated RiskProfile."""

    def test_investment_engine_consumes_complete_risk_profile(
        self, sample_financial_state, sample_assets, sample_liabilities, sample_goals, sample_behavior
    ):
        risk_profile = build_risk_profile(
            financial_state=sample_financial_state,
            assets=sample_assets,
            liabilities=sample_liabilities,
            goals=sample_goals,
            observed_behavior=sample_behavior,
        )

        plan = InvestmentEngine().build(
            InvestmentEngineInput(
                risk_profile=risk_profile,
                current_portfolio={"allocation": {"equity": 0.7, "debt": 0.3}},
            )
        )

        assert plan.status == "ready"
        assert len(plan.layers) == 5
        assert plan.risk_boundary["risk_required"]["available"] is True
        assert plan.risk_boundary["risk_capacity"]["available"] is True
        assert plan.risk_boundary["risk_tolerance"]["available"] is True
        assert len(plan.constraints) == len(risk_profile.constraints)

    def test_investment_engine_handles_partial_profile_as_requires_review(self):
        # Risk tolerance missing
        risk_profile = build_risk_profile(
            risk_required_override=10.0,
            financial_state={"income_monthly": {"value": 100000, "available": True}, "investable_surplus_monthly": {"value": 20000, "available": True}},
        )

        plan = InvestmentEngine().build(
            InvestmentEngineInput(
                risk_profile=risk_profile,
            )
        )

        assert plan.status == "requires_review"
        assert plan.risk_boundary["risk_tolerance"]["available"] is False
