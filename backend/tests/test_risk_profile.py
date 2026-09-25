from engines.profile.risk import build_risk_profile


def test_risk_profile_separates_capacity_exposure_need():
    result = build_risk_profile(
        financial_state={
            "income_monthly": {"value": 100000, "available": True},
            "investable_surplus_monthly": {"value": 40000, "available": True},
            "safety_reserve_months": {"value": 6, "available": True},
            "emi_burden_monthly": {"value": 10000, "available": True},
        },
        assets=[{"value": 800000}, {"value": 200000}],
        liabilities=[{"outstanding": 300000}],
        goals=[{"time_horizon_years": 3}, {"time_horizon_years": 10}],
    )
    assert result["dimensions"]["capacity"]
    assert result["dimensions"]["exposure"]
    assert result["dimensions"]["need"]


def test_risk_profile_does_not_infer_without_evidence():
    result = build_risk_profile(financial_state=None)
    assert result["constraints"] == []
    assert result["has_sufficient_evidence"] is False


def test_asset_concentration_is_deterministic():
    result = build_risk_profile(financial_state=None, assets=[{"value": 750}, {"value": 250}])
    item = next(x for x in result["constraints"] if x["key"] == "risk_exposure_max_asset_concentration")
    assert item["value"] == 0.75
    assert item["confidence"] == 1.0
