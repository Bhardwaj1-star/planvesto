from api.moneywheel import _canonical_result
from rules.moneywheel import CANONICAL_RATIO_KEYS


def _ratio(key: str, value: float = 10.0, unit: str = "%") -> dict:
    return {
        "key": key,
        "name": key.replace("_", " ").title(),
        "value": value,
        "unit": unit,
        "status": "healthy",
        "formula": "test",
        "explanation": f"{key} is healthy.",
        "available": True,
    }


def _snapshot(ratios: list[dict], metadata: dict | None = None) -> dict:
    return {
        "snapshot_id": "snapshot-1",
        "planning_unit_id": "pu-1",
        "overall_status": "healthy",
        "ratios": ratios,
        "rule_set_version": "2.0",
        "calculated_at": "2026-10-03T00:00:00Z",
        "metadata": metadata or {},
    }


def test_canonical_result_returns_strictly_nine_ratios():
    canonical_ratios = [_ratio(key) for key in CANONICAL_RATIO_KEYS]
    result = _canonical_result(_snapshot(canonical_ratios, {"rules": [{"key": "expense_coverage"}]}))

    assert len(result.ratios) == 9
    assert [ratio.key for ratio in result.ratios] == list(CANONICAL_RATIO_KEYS)
    assert not hasattr(result, "rules")
    assert "rules" not in result.metadata
    assert result.metadata["snapshot_id"] == "snapshot-1"


def test_missing_ratios_are_populated_as_unavailable():
    partial_ratios = [_ratio("savings_rate")]
    result = _canonical_result(_snapshot(partial_ratios))

    assert len(result.ratios) == 9
    assert result.ratios[0].key == "savings_rate"
    assert result.ratios[0].available is True
    assert result.ratios[1].key == "liquid_asset_ratio"
    assert result.ratios[1].available is False
