import pytest
from engines.profile.engine import ProfileEngine, _band


def financial_state(**overrides):
    base = {
        "investable_surplus_monthly": {"value": 50000, "available": True},
        "safety_reserve_months": {"value": 6, "available": True},
        "emi_burden_monthly": {"value": 10000, "available": True},
        "net_worth": {"value": 2000000, "available": True},
    }
    base.update(overrides)
    return base


def answers(value):
    return {"loss_reaction": value, "volatility_comfort": value, "capital_stability": value, "investment_experience": value, "time_horizon_comfort": value}


def test_scoring_is_deterministic():
    engine = ProfileEngine()
    kwargs = dict(
        financial_state=financial_state(),
        risk_tolerance_answers=answers(3),
        behavioral_answers={"loss_reaction": 2, "decision_discipline": 3},
        identity_answers={"goal_orientation": 4, "planning_orientation": 3},
    )
    assert engine.build(**kwargs) == engine.build(**kwargs)


def test_risk_tolerance_is_separate_from_capacity():
    engine = ProfileEngine()
    result = engine.build(
        financial_state=financial_state(),
        risk_tolerance_answers=answers(0),
        behavioral_answers={},
        identity_answers={},
    )
    assert result["risk_tolerance"]["score"] == 0
    assert result["risk_capacity"]["score"] > 0


def test_missing_financial_state_does_not_infer_capacity():
    result = ProfileEngine().build(
        financial_state=None,
        risk_tolerance_answers=answers(4),
        behavioral_answers={},
        identity_answers={},
    )
    assert result["risk_capacity"]["score"] == 0
    assert result["risk_capacity"]["confidence"] == 0
    assert "cannot be established" in result["risk_capacity"]["explanations"][0]


def test_answer_validation_boundary_is_owned_by_schema_but_engine_is_deterministic():
    result = ProfileEngine().build(
        financial_state=financial_state(),
        risk_tolerance_answers={"loss_reaction": 4},
        behavioral_answers={"decision_discipline": 0},
        identity_answers={"goal_orientation": 4},
    )
    assert 0 <= result["risk_tolerance"]["score"] <= 100
    assert 0 <= result["behavioral_profile"]["score"] <= 100
    assert 0 <= result["investor_identity"]["score"] <= 100


def test_band_boundaries():
    assert _band(0) == "low"
    assert _band(24.999) == "low"
    assert _band(25) == "moderate-low"
    assert _band(50) == "moderate-high"
    assert _band(75) == "high"
