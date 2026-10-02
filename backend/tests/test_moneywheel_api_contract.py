from api.moneywheel import _canonical_result


def _row():
    return {
        "snapshot_id": "mw-123",
        "planning_unit_id": "pu-1",
        "overall_status": "healthy",
        "ratios": [
            {
                "key": f"ratio-{i}",
                "name": f"Ratio {i}",
                "value": 1.0,
                "unit": "x",
                "status": "healthy",
                "formula": "1",
                "explanation": "test",
                "available": True,
            }
            for i in range(9)
        ],
        "rule_set_version": "1.3",
        "calculated_at": "2026-10-02T00:00:00Z",
        "metadata": {
            "source": "test",
            "rules": [
                {
                    "key": "rule-1",
                    "name": "Rule 1",
                    "value": 1.0,
                    "unit": "x",
                    "formula": "1",
                    "explanation": "test",
                    "available": True,
                },
                {
                    "key": "rule-2",
                    "name": "Rule 2",
                    "value": 1.0,
                    "unit": "x",
                    "formula": "1",
                    "explanation": "test",
                    "available": True,
                },
            ],
        },
    }


def test_canonical_result_matches_frontend_moneywheel_contract():
    result = _canonical_result(_row())

    assert result.planning_unit_id == "pu-1"
    assert len(result.ratios) == 9
    assert len(result.rules) == 2
    assert result.metadata["snapshot_id"] == "mw-123"
    assert result.metadata["source"] == "test"
    assert "rules" not in result.metadata
