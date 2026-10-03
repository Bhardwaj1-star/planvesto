from api.moneywheel import _canonical_result


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


def test_legacy_twelve_ratio_snapshot_is_normalized_to_current_contract():
    legacy_keys = [
        "savings_ratio",
        "expense_ratio",
        "emergency_fund_coverage",
        "current_liquidity_ratio",
        "debt_to_income_ratio",
        "leverage_ratio",
        "liquid_asset_to_total_asset",
        "solvency_ratio",
        "financial_asset_ratio",
        "insurance_gap_ratio",
        "goal_funding_ratio",
        "future_funding_ratio",
    ]

    result = _canonical_result(_snapshot([
        _ratio(key, 10.0, "months" if key == "emergency_fund_coverage" else "%")
        for key in legacy_keys
    ]))

    assert len(result.ratios) == 9
    assert [ratio.key for ratio in result.ratios] == [
        "savings_rate",
        "liquid_asset_ratio",
        "debt_to_income_ratio",
        "leverage_ratio",
        "financial_asset_ratio",
        "insurance_coverage_ratio",
        "goal_funding_ratio",
        "future_funding_ratio",
        "required_rate_of_return",
    ]
    assert len(result.rules) == 2
    assert result.rules[0].key == "expense_coverage"
    assert result.rules[0].value == 10.0
    assert result.rules[1].key == "emergency_coverage"
    assert result.rules[1].available is False
    assert result.metadata["legacy_normalization"]["applied"] is True


def test_current_snapshot_with_stored_rules_is_not_reconstructed():
    ratios = [
        _ratio("savings_rate"),
        _ratio("liquid_asset_ratio"),
        _ratio("debt_to_income_ratio"),
        _ratio("leverage_ratio"),
        _ratio("financial_asset_ratio"),
        _ratio("insurance_coverage_ratio"),
        _ratio("goal_funding_ratio"),
        _ratio("future_funding_ratio"),
        _ratio("required_rate_of_return"),
    ]
    stored_rules = [
        {
            "key": "expense_coverage",
            "name": "Expense Coverage",
            "value": 6.0,
            "unit": "months",
            "formula": "Liquid Assets / Monthly Expenses",
            "explanation": "Expense Coverage is 6.00 months.",
            "available": True,
        },
        {
            "key": "emergency_coverage",
            "name": "Emergency Coverage",
            "value": 4.0,
            "unit": "months",
            "formula": "Liquid Assets / Essential Monthly Expenses",
            "explanation": "Emergency Coverage is 4.00 months.",
            "available": True,
        },
    ]

    result = _canonical_result(_snapshot(ratios, {"rules": stored_rules}))

    assert len(result.ratios) == 9
    assert result.rules == stored_rules
    assert "legacy_normalization" not in result.metadata
