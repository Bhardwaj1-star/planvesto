"""Tests for the centralized canonical constraints layer.

Covers:
  - CanonicalConstraint model
  - ConstraintSet typed accessors
  - Adapter functions (RuleResult, RatioResult, RiskProfiler, Strategy)
  - ConstraintAggregator
  - Conflict detection
  - Backward compatibility with existing ConstraintCheckResult
"""
import pytest
from engines.constraints.models import (
    CanonicalConstraint,
    ConstraintCheckResult,
    ConstraintConflict,
    ConstraintSet,
    FinancialRatioResult,
    RatioConstraintAssessment,
)
from engines.constraints.adapters import (
    adapt_constraint_check,
    adapt_ratio_assessment,
    adapt_ratio_result,
    adapt_risk_constraint,
    adapt_risk_profile_constraints,
    adapt_rule_result,
    adapt_rule_assessment,
    adapt_strategy_constraints,
    build_constraint_set,
)
from engines.constraints.aggregator import ConstraintAggregator


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_canonical_constraints():
    return [
        CanonicalConstraint(
            constraint_id="c1", rule_id="RULE_A", domain="financial_ratio",
            source="moneywheel", source_engine="Evaluator",
            severity="hard", role="hard_constraint", kind="hard",
            passed=False, message="Hard failure", value=42.0, unit="%",
        ),
        CanonicalConstraint(
            constraint_id="c2", rule_id="RULE_B", domain="goal_diagnostic",
            source="rule_engine", source_engine="RuleEngine",
            severity="warning", role="recommendation_only", kind="soft",
            passed=True, message="Soft warning",
        ),
        CanonicalConstraint(
            constraint_id="c3", rule_id="RULE_C", domain="risk_capacity",
            source="financial_state", source_engine="RiskProfilerEngine",
            severity="info", role="explanatory_evidence", kind="diagnostic",
            passed=True, message="Info observation",
        ),
    ]


# ---------------------------------------------------------------------------
# CanonicalConstraint model tests
# ---------------------------------------------------------------------------

class TestCanonicalConstraint:
    def test_creation(self):
        c = CanonicalConstraint(
            constraint_id="test-1", rule_id="TEST_RULE",
            domain="financial_ratio", source="test", source_engine="TestEngine",
            severity="hard",
        )
        assert c.constraint_id == "test-1"
        assert c.severity == "hard"
        assert c.passed is True  # default
        assert c.confidence == 1.0

    def test_default_validity(self):
        c = CanonicalConstraint(
            constraint_id="t", rule_id="r", domain="declared",
            source="s", source_engine="e", severity="info",
        )
        assert c.validity["status"] == "valid"


# ---------------------------------------------------------------------------
# ConstraintSet accessor tests
# ---------------------------------------------------------------------------

class TestConstraintSet:
    def test_hard_constraints(self, sample_canonical_constraints):
        cs = ConstraintSet(constraints=sample_canonical_constraints)
        hard = cs.hard_constraints
        assert len(hard) == 1
        assert hard[0].constraint_id == "c1"

    def test_warnings(self, sample_canonical_constraints):
        cs = ConstraintSet(constraints=sample_canonical_constraints)
        assert len(cs.warnings) == 1
        assert cs.warnings[0].constraint_id == "c2"

    def test_info(self, sample_canonical_constraints):
        cs = ConstraintSet(constraints=sample_canonical_constraints)
        assert len(cs.info) == 1
        assert cs.info[0].constraint_id == "c3"

    def test_failed(self, sample_canonical_constraints):
        cs = ConstraintSet(constraints=sample_canonical_constraints)
        assert len(cs.failed) == 1

    def test_has_hard_failures(self, sample_canonical_constraints):
        cs = ConstraintSet(constraints=sample_canonical_constraints)
        assert cs.has_hard_failures is True

    def test_no_hard_failures_when_all_pass(self):
        cs = ConstraintSet(constraints=[
            CanonicalConstraint(
                constraint_id="x", rule_id="r", domain="declared",
                source="s", source_engine="e", severity="hard", passed=True,
            ),
        ])
        assert cs.has_hard_failures is False

    def test_by_domain(self, sample_canonical_constraints):
        cs = ConstraintSet(constraints=sample_canonical_constraints)
        assert len(cs.by_domain("financial_ratio")) == 1
        assert len(cs.by_domain("risk_capacity")) == 1

    def test_by_goal(self):
        cs = ConstraintSet(constraints=[
            CanonicalConstraint(
                constraint_id="a", rule_id="r", domain="declared",
                source="s", source_engine="e", severity="info", goal_id="g1",
            ),
            CanonicalConstraint(
                constraint_id="b", rule_id="r2", domain="declared",
                source="s", source_engine="e", severity="info", goal_id="g2",
            ),
        ])
        assert len(cs.by_goal("g1")) == 1

    def test_suggested_overrides(self):
        cs = ConstraintSet(constraints=[
            CanonicalConstraint(
                constraint_id="o", rule_id="r", domain="declared",
                source="s", source_engine="e", severity="hard",
                goal_id="g1", suggested_override_priority="low",
                override_reason="test reason",
            ),
        ])
        overrides = cs.suggested_overrides()
        assert "g1" in overrides
        assert overrides["g1"]["resolved_priority"] == "low"


# ---------------------------------------------------------------------------
# Adapter tests
# ---------------------------------------------------------------------------

class TestAdapters:
    def test_adapt_ratio_result(self):
        ratio = FinancialRatioResult(
            ratio_key="savings_ratio", name="Savings Ratio",
            value=25.0, unit="%", status="healthy",
            evidence={"monthly_surplus": 50000},
        )
        c = adapt_ratio_result(ratio)
        assert c.domain == "financial_ratio"
        assert c.source_engine == "FinancialRatioConstraintEvaluator"
        assert c.value == 25.0
        assert c.severity == "info"  # healthy -> info
        assert c.passed is True

    def test_adapt_ratio_result_critical(self):
        ratio = FinancialRatioResult(
            ratio_key="debt_to_income_ratio", name="DTI",
            value=55.0, unit="%", status="critical",
        )
        c = adapt_ratio_result(ratio)
        assert c.severity == "hard"
        assert c.passed is False

    def test_adapt_constraint_check(self):
        check = ConstraintCheckResult(
            rule_id="RULE_DEBT_BURDEN_EXCEEDED",
            goal_id="g1",
            severity="hard",
            passed=False,
            message="DTI too high",
            suggested_override_priority="low",
            override_reason="System override",
        )
        c = adapt_constraint_check(check)
        assert c.severity == "hard"
        assert c.goal_id == "g1"
        assert c.suggested_override_priority == "low"
        assert c.role == "hard_constraint"

    def test_adapt_risk_constraint(self):
        item = {
            "key": "risk_capacity_surplus",
            "value": 30000,
            "unit": "INR/month",
            "kind": "hard",
            "source": "financial_state",
            "evidence": [{"field": "investable_surplus_monthly", "value": 30000}],
            "confidence": 1.0,
            "validity": {"status": "valid"},
        }
        c = adapt_risk_constraint(item, index=0)
        assert c.domain == "risk_capacity"
        assert c.source_engine == "RiskProfilerEngine"
        assert c.severity == "hard"
        assert c.value == 30000

    def test_adapt_strategy_constraints(self):
        msgs = ["Missing inputs: X", "Diagnostic: Y is critical"]
        result = adapt_strategy_constraints(msgs, strategy_id="strat-1")
        assert len(result) == 2
        assert result[0].domain == "strategy"
        assert result[0].source_engine == "StrategyEngine"

    def test_adapt_risk_profile_constraints_list(self):
        items = [
            {"key": "risk_need_required_return", "value": 12.5, "unit": "%", "kind": "hard", "source": "canonical_calculation", "evidence": [], "confidence": 1.0, "validity": {}},
            {"key": "risk_capacity_reserve", "value": 6.0, "unit": "months", "kind": "hard", "source": "financial_state", "evidence": [], "confidence": 1.0, "validity": {}},
        ]
        result = adapt_risk_profile_constraints(items)
        assert len(result) == 2
        domains = {c.domain for c in result}
        assert "risk_required" in domains
        assert "risk_capacity" in domains


# ---------------------------------------------------------------------------
# Conflict detection tests
# ---------------------------------------------------------------------------

class TestConflictDetection:
    def test_no_conflict_same_values(self):
        cs = build_constraint_set([
            CanonicalConstraint(
                constraint_id="a", rule_id="SAME_RULE", domain="declared",
                source="s1", source_engine="e", severity="info", value=10.0,
            ),
            CanonicalConstraint(
                constraint_id="b", rule_id="SAME_RULE", domain="declared",
                source="s2", source_engine="e", severity="info", value=10.0,
            ),
        ])
        assert len(cs.conflicts) == 0

    def test_conflict_different_values(self):
        cs = build_constraint_set([
            CanonicalConstraint(
                constraint_id="a", rule_id="CONFLICT_RULE", domain="declared",
                source="s1", source_engine="e", severity="hard", value=10.0,
            ),
            CanonicalConstraint(
                constraint_id="b", rule_id="CONFLICT_RULE", domain="declared",
                source="s2", source_engine="e", severity="info", value=20.0,
            ),
        ])
        assert len(cs.conflicts) == 1
        assert cs.conflicts[0].key == "CONFLICT_RULE"
        assert cs.conflicts[0].hard_constraint_present is True
        # Both constraints preserved
        assert len(cs.constraints) == 2


# ---------------------------------------------------------------------------
# Aggregator tests
# ---------------------------------------------------------------------------

class TestConstraintAggregator:
    def test_aggregator_empty(self):
        agg = ConstraintAggregator()
        cs = agg.aggregate()
        assert isinstance(cs, ConstraintSet)
        assert len(cs.constraints) == 0

    def test_aggregator_with_risk_constraints(self):
        agg = ConstraintAggregator()
        risk_constraints = [
            {"key": "risk_capacity_surplus", "value": 25000, "unit": "INR/month", "kind": "hard", "source": "financial_state", "evidence": [], "confidence": 1.0, "validity": {}},
        ]
        cs = agg.aggregate(risk_profile_constraints=risk_constraints)
        assert len(cs.constraints) == 1
        assert cs.constraints[0].domain == "risk_capacity"

    def test_aggregator_with_strategy_constraints(self):
        agg = ConstraintAggregator()
        cs = agg.aggregate(
            strategy_constraints=["Missing inputs: X"],
            strategy_id="strat-1",
        )
        assert len(cs.constraints) == 1
        assert cs.constraints[0].domain == "strategy"

    def test_aggregator_provenance(self):
        agg = ConstraintAggregator()
        cs = agg.aggregate(planning_unit_id="PU-123")
        assert cs.provenance["planning_unit_id"] == "PU-123"


# ---------------------------------------------------------------------------
# Backward compatibility tests
# ---------------------------------------------------------------------------

class TestBackwardCompatibility:
    def test_legacy_models_still_importable(self):
        """Ensure existing imports from engines.constraints continue to work."""
        from engines.constraints import (
            ConstraintCheckResult,
            FinancialRatioResult,
            RatioConstraintAssessment,
            ConstraintSeverity,
            RatioStatus,
            FinancialRatioConstraintEvaluator,
        )
        # Legacy model should still be constructable
        check = ConstraintCheckResult(
            rule_id="LEGACY_RULE", severity="hard", passed=False, message="test",
        )
        assert check.rule_id == "LEGACY_RULE"

    def test_legacy_evaluator_still_works(self):
        """The existing FinancialRatioConstraintEvaluator should work unchanged."""
        from engines.constraints.evaluator import FinancialRatioConstraintEvaluator
        evaluator = FinancialRatioConstraintEvaluator()
        ratios = evaluator.evaluate_ratios({
            "monthly_income": 100000, "monthly_expenses": 50000,
            "monthly_surplus": 50000, "liquid_assets": 350000,
            "monthly_debt_payments": 25000, "total_assets": 1000000,
            "total_liabilities": 250000,
        })
        assert len(ratios) >= 4
        ratio_keys = {r.ratio_key for r in ratios}
        assert "savings_ratio" in ratio_keys
