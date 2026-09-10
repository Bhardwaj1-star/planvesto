from engines.moneywheel.engine import MoneywheelEngine
from models.moneywheel import MoneywheelInput


def _input(**overrides):
    values = dict(
        planning_unit_id="pu-1",
        gross_monthly_income=100000,
        savings=30000,
        essential_monthly_expenses=35000,
        monthly_expenses=50000,
        liquid_assets=500000,
        short_term_liabilities=250000,
        monthly_debt_payments=20000,
        total_assets=2000000,
        total_liabilities=400000,
        financial_assets=1500000,
    )
    values.update(overrides)
    return MoneywheelInput(**values)


def test_all_nine_ratios_are_returned():
    result = MoneywheelEngine().build(_input())
    assert len(result.ratios) == 9
    assert all(r.available for r in result.ratios)


def test_zero_is_a_valid_ratio_value():
    result = MoneywheelEngine().build(_input(savings=0))
    ratio = next(r for r in result.ratios if r.key == "savings_ratio")
    assert ratio.value == 0
    assert ratio.status == "critical"
    assert ratio.available is True


def test_excellent_status_is_supported():
    result = MoneywheelEngine().build(_input())
    statuses = {r.key: r.status for r in result.ratios}
    assert statuses["savings_ratio"] == "excellent"
    assert statuses["debt_to_income_ratio"] == "excellent"


def test_missing_input_is_not_treated_as_zero():
    result = MoneywheelEngine().build(_input(liquid_assets=None))
    for key in ("emergency_fund_coverage", "current_liquidity_ratio", "liquid_asset_to_total_asset"):
        ratio = next(r for r in result.ratios if r.key == key)
        assert ratio.value is None
        assert ratio.status == "unavailable"
        assert ratio.available is False


def test_solvency_is_one_minus_leverage():
    result = MoneywheelEngine().build(_input(total_assets=1000000, total_liabilities=300000))
    leverage = next(r for r in result.ratios if r.key == "leverage_ratio")
    solvency = next(r for r in result.ratios if r.key == "solvency_ratio")
    assert leverage.value == 30.0
    assert solvency.value == 70.0
