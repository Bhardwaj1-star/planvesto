from engines.rules.engine import RuleEngine
from models.defined_goal import DefinedGoal


def _goal(**overrides):
    data = {
        "goal_id": "g-rule-financial-state",
        "planning_unit_id": "pu-rule-financial-state",
        "version": 1,
        "is_latest": True,
        "goal_type": "retirement",
        "goal_name": "Retirement",
        "today_cost": 5000000.0,
        "inflation_rate": 0.06,
        "target_month": 6,
        "target_year": 2041,
        "duration_years": 15.0,
        "future_target": 10000000.0,
        "priority": "High",
        "flexibility": "Fixed",
        "funding_gap": 1000000.0,
        "funding_status": "Shortfall",
    }
    data.update(overrides)
    return DefinedGoal(**data)


def _diagnostic(assessment, rule_id):
    return next(r for r in assessment.diagnostics if r.rule_id == rule_id)


def test_rule_engine_reads_metric_objects_from_financial_state():
    assessment = RuleEngine().assess(_goal(), {"investable_surplus_monthly": {"value": 25000, "available": True}})
    result = next(r for r in assessment.soft_constraints if r.rule_id == "surplus-health")
    assert result.passed is True
    assert result.evidence["investable_surplus_monthly"] == 25000


def test_negative_surplus_is_soft_constraint_not_hard_failure():
    assessment = RuleEngine().assess(_goal(), {"investable_surplus_monthly": {"value": -5000, "available": True}})
    assert assessment.eligible is True
    result = next(r for r in assessment.soft_constraints if r.rule_id == "surplus-health")
    assert result.passed is False


def test_unavailable_metric_does_not_create_false_constraint_failure():
    assessment = RuleEngine().assess(_goal(), {"investable_surplus_monthly": {"value": None, "available": False}})
    assert assessment.eligible is True
    assert any(r.rule_id == "surplus-health" for r in assessment.diagnostics)


def test_financial_health_diagnostics_use_existing_moneywheel_metrics():
    context = {
        "emergency_fund_coverage": {"value": 8.0, "available": True},
        "current_liquidity_ratio": {"value": 1.2, "available": True},
        "debt_to_income_ratio": {"value": 25.0, "available": True},
        "leverage_ratio": {"value": 25.0, "available": True},
    }
    assessment = RuleEngine().assess(_goal(), context)
    assert _diagnostic(assessment, "emergency-reserve-health").evidence["status"] == "healthy"
    assert _diagnostic(assessment, "liquidity-health").evidence["status"] == "healthy"
    assert _diagnostic(assessment, "debt-pressure-health").evidence["status"] == "healthy"
    assert _diagnostic(assessment, "leverage-health").evidence["status"] == "healthy"


def test_financial_health_diagnostics_do_not_make_missing_data_fail():
    assessment = RuleEngine().assess(_goal(), {})
    for rule_id in ("emergency-reserve-health", "liquidity-health", "debt-pressure-health", "leverage-health"):
        result = _diagnostic(assessment, rule_id)
        assert result.evidence["available"] is False
        assert result.passed is True


def test_critical_financial_health_is_diagnostic_not_hard_constraint():
    context = {
        "emergency_fund_coverage": {"value": 2.0, "available": True},
        "current_liquidity_ratio": {"value": 0.5, "available": True},
        "debt_to_income_ratio": {"value": 45.0, "available": True},
        "leverage_ratio": {"value": 60.0, "available": True},
    }
    assessment = RuleEngine().assess(_goal(), context)
    assert assessment.eligible is True
    assert all(_diagnostic(assessment, rule_id).severity == "diagnostic" for rule_id in (
        "emergency-reserve-health", "liquidity-health", "debt-pressure-health", "leverage-health"
    ))
