from engines.profile.engine import ProfileEngine


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


def test_financial_facts_create_hard_constraints():
    result = ProfileEngine().build(financial_state=financial_state())
    keys = {item["key"] for item in result["constraints"]}
    assert "monthly_investable_surplus" in keys
    assert "safety_reserve_months" in keys
    assert all(item["kind"] == "hard" for item in result["constraints"])


def test_missing_financial_state_does_not_infer_constraints():
    result = ProfileEngine().build(financial_state=None)
    assert result["constraints"] == []
    assert result["conflicts"] == []


def test_conflicting_evidence_is_preserved():
    result = ProfileEngine().build(
        financial_state=None,
        declared_constraints=[{"key": "liquidity_priority", "value": "high"}],
        preferences=[{"key": "liquidity_priority", "value": "low"}],
    )
    assert len(result["conflicts"]) == 1
    assert result["conflicts"][0]["status"] == "unresolved"


def test_evidence_source_changes_confidence():
    result = ProfileEngine().build(
        financial_state=None,
        declared_constraints=[{"key": "max_loss_amount", "value": 100000}],
        observed_behavior=[{"key": "plan_deviation", "value": "low"}],
    )
    assert result["constraints"][0]["confidence"] == 0.5
    assert result["constraints"][1]["confidence"] == 0.75
