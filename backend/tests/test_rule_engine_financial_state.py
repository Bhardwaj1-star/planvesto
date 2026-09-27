from engines.rules.engine import RuleEngine
from models.defined_goal import DefinedGoal


def _goal(**overrides):
    data = {"goal_type": "retirement", "name": "Retirement", "priority": "High", "flexibility": "Fixed", "duration_years": 15, "future_target": 10000000, "funding_status": "Shortfall"}
    data.update(overrides)
    return DefinedGoal(**data)


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
