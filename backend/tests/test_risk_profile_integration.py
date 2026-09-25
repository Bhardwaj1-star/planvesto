from engines.profile.engine import ProfileEngine


def test_profile_engine_returns_risk_profile():
    result = ProfileEngine().build(
        financial_state={
            "income_monthly": {"value": 100000, "available": True},
            "expenses_monthly": {"value": 50000, "available": True},
            "investable_surplus_monthly": {"value": 50000, "available": True},
            "safety_reserve_months": {"value": 6, "available": True},
            "emi_burden_monthly": {"value": 10000, "available": True},
        },
        assets=[{"value": 800000}, {"value": 200000}],
        liabilities=[{"outstanding": 300000}],
        goals=[{"time_horizon_years": 3}, {"time_horizon_years": 10}],
    )
    assert set(result["risk_profile"]["dimensions"]) == {"capacity", "exposure", "need"}
    assert result["risk_profile"]["dimensions"]["capacity"]
    assert result["risk_profile"]["dimensions"]["exposure"]
    assert result["risk_profile"]["dimensions"]["need"]
