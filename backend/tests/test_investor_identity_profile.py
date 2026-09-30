import pytest
from engines.profile.identity import build_identity_profile, DIMENSIONS
from engines.profile.engine import ProfileEngine


def test_identity_profile_empty_evidence():
    result = build_identity_profile(evidence=[])
    assert set(result["dimensions"].keys()) == set(DIMENSIONS)
    assert all(not val for val in result["dimensions"].values())
    assert len(result["unsupported_dimensions"]) == len(DIMENSIONS)


def test_identity_profile_with_evidence():
    evidence = [
        {"dimension": "financial_role", "value": "primary_earner", "evidence": ["tax_return"], "confidence": 0.95},
        {"dimension": "decision_authority", "value": "sole", "evidence": ["survey"], "confidence": 0.8},
    ]
    result = build_identity_profile(evidence=evidence)
    assert len(result["dimensions"]["financial_role"]) == 1
    assert result["dimensions"]["financial_role"][0]["value"] == "primary_earner"
    assert result["evidence_sufficient"]["financial_role"] is True
    assert result["evidence_sufficient"]["responsibility_load"] is False


def test_profile_engine_integrates_identity_profile():
    result = ProfileEngine().build(
        financial_state=None,
        identity_evidence=[{"dimension": "financial_role", "value": "joint", "evidence": ["joint_account"]}],
    )
    assert "identity_profile" in result
    assert result["identity_profile"]["evidence_sufficient"]["financial_role"] is True
