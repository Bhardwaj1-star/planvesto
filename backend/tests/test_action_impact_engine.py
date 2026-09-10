from engines.action_plan.impact_engine import ActionImpactEngine


def _state(**overrides):
    base = {
        "income_monthly": {"value": 100000},
        "expenses_monthly": {"value": 40000},
        "commitments_monthly": {"value": 10000},
        "investable_surplus_monthly": {"value": 50000},
        "total_assets": {"value": 1000000},
        "total_liabilities": {"value": 300000},
        "emi_burden_monthly": {"value": 10000},
        "net_worth": {"value": 700000},
        "safety_reserve_months": {"value": 6},
    }
    base.update(overrides)
    return base


def test_compare_returns_actual_minus_projected_variance():
    result = ActionImpactEngine().compare(
        _state(investable_surplus_monthly={"value": 50000}),
        _state(investable_surplus_monthly={"value": 45000}),
    )
    row = next(r for r in result["projected_vs_actual"] if r["metric"] == "investable_surplus_monthly")
    assert row["variance"] == -5000


def test_compare_skips_missing_values():
    result = ActionImpactEngine().compare(
        _state(total_assets={"value": None}),
        _state(total_assets={"value": 1000000}),
    )
    assert not any(r["metric"] == "total_assets" for r in result["projected_vs_actual"])


def test_cause_is_not_invented():
    result = ActionImpactEngine().compare(_state(), _state())
    assert result["cause"]["status"] == "not_determined"
    assert result["material_variances"] == []
