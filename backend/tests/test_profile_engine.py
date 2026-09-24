from engines.profile.engine import ProfileEngine
from engines.profile.constraints import ConstraintRules


def financial_state(**overrides):
    base = {
        "income_monthly": {"value": 100000, "available": True},
        "expenses_monthly": {"value": 50000, "available": True},
        "investable_surplus_monthly": {"value": 50000, "available": True},
        "safety_reserve_months": {"value": 6, "available": True},
        "emi_burden_monthly": {"value": 10000, "available": True},
    }
    base.update(overrides)
    return base


def test_resolution_is_deterministic():
    engine = ProfileEngine()
    kwargs = {
        "financial_state": financial_state(),
        "declared_constraints": [{"key": "max_loss_amount", "value": 100000, "kind": "hard"}],
        "observed_behavior": [{"key": "plan_deviation", "value": "low"}],
        "preferences": [{"key": "liquidity_priority", "value": "high"}],
    }
    assert engine.build(**kwargs) == engine.build(**kwargs)


def test_financial_facts_create_hard_constraints_with_evidence():
    result = ProfileEngine().build(financial_state=financial_state())
    assert all(item["kind"] == "hard" for item in result["constraints"])
    assert all(item["source"] == "financial_state" for item in result["constraints"])
    assert all(item["evidence"] for item in result["constraints"])


def test_missing_financial_state_does_not_infer_constraints():
    result = ProfileEngine().build(financial_state=None)
    assert result["constraints"] == []
    assert result["conflicts"] == []


def test_conflicting_evidence_is_unresolved():
    result = ProfileEngine().build(
        financial_state=None,
        declared_constraints=[{"key": "liquidity_priority", "value": "high"}],
        preferences=[{"key": "liquidity_priority", "value": "low"}],
    )
    assert len(result["conflicts"]) == 1
    assert result["conflicts"][0]["status"] == "unresolved"


def test_source_priority_confidence():
    assert ConstraintRules.confidence("financial_state", 1) == 1.0
    assert ConstraintRules.confidence("observed_behavior", 1) == 0.75
    assert ConstraintRules.confidence("declared_constraint", 1) == 0.5
    assert ConstraintRules.confidence("preference", 1) == 0.25
    assert ConstraintRules.confidence("observed_behavior", 2) == 0.9
