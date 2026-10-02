from engines.goal.funding_strategies import build_goal_funding_strategies


def test_funding_strategies_include_core_architectures():
    result = build_goal_funding_strategies(
        funding_gap=600000,
        annual_return=0.08,
        duration_years=5,
        available_monthly_surplus=8000,
    )
    ids = {item["strategy_id"] for item in result}
    assert {
        "sip",
        "lumpsum",
        "lumpsum_plus_sip",
        "step_up_sip",
        "lumpsum_plus_step_up_sip",
    }.issubset(ids)


def test_sip_is_feasible_when_required_contribution_fits_surplus():
    result = build_goal_funding_strategies(
        funding_gap=100000,
        annual_return=0.08,
        duration_years=5,
        available_monthly_surplus=5000,
    )
    sip = next(item for item in result if item["strategy_id"] == "sip")
    assert sip["status"] == "feasible"
    assert sip["required_monthly_contribution"] <= 5000


def test_existing_assets_covering_gap_returns_no_additional_funding_need():
    result = build_goal_funding_strategies(
        funding_gap=0,
        annual_return=0.08,
        duration_years=5,
        available_monthly_surplus=5000,
    )
    assert result[0]["strategy_id"] == "existing_assets"
    assert result[0]["required_monthly_contribution"] == 0.0
