import pytest

from engines.suitability.engine import SuitabilityEngine


def test_suitability_engine_preserves_framework_status_and_version():
    result = SuitabilityEngine().assess(
        "Needs Attention",
        [{"component": "risk", "status": "needs_attention"}],
    )
    assert result.status == "Needs Attention"
    assert result.diagnostics[0]["component"] == "risk"
    assert result.rule_set_version == "framework-1.0"


def test_suitability_engine_rejects_unknown_status():
    with pytest.raises(ValueError):
        SuitabilityEngine().assess("Unknown")
