import pytest

from engines.profile.behavioral import BehavioralRules
from engines.profile.engine import ProfileEngine


def observation(dimension, key="test_constraint", value="observed", evidence=None):
    return {
        "dimension": dimension,
        "key": key,
        "value": value,
        "evidence": evidence or [{"event": "historical_action", "count": 3}],
    }


def test_all_behavior_dimensions_without_evidence_are_unknown():
    result = BehavioralRules.resolve([])
    assert set(result["dimensions"]) == {
        "decision_consistency",
        "volatility_reaction",
        "discipline",
        "intervention_tendency",
        "loss_uncertainty_response",
    }
    assert all(item["status"] == "insufficient_evidence" for item in result["dimensions"].values())


def test_observed_behavior_requires_supported_dimension_and_evidence():
    with pytest.raises(ValueError):
        BehavioralRules.normalize({"dimension": "risk_tolerance", "key": "x", "value": "high", "evidence": [1]})
    with pytest.raises(ValueError):
        BehavioralRules.normalize({"dimension": "discipline", "key": "x", "value": "high", "evidence": []})


def test_behavioral_constraint_is_marked_for_product_selection_only():
    item = BehavioralRules.normalize(observation("intervention_tendency"))
    assert item["source"] == "observed_behavior"
    assert item["downstream_use"] == "product_selection"


def test_profile_engine_exposes_behavioral_profile_without_scoring_personality():
    result = ProfileEngine().build(
        financial_state=None,
        observed_behavior=[observation("discipline", key="contribution_consistency", value="consistent")],
    )
    assert result["behavioral_profile"]["dimensions"]["discipline"]["status"] == "observed"
    assert result["behavioral_profile"]["dimensions"]["volatility_reaction"]["status"] == "insufficient_evidence"
    item = result["constraints"][0]
    assert item["dimension"] == "discipline"
    assert item["downstream_use"] == "product_selection"
