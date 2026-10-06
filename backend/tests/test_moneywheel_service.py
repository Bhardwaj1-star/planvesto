from unittest.mock import MagicMock
import pytest

from models.financial_state import FinancialState, Metric
from models.moneywheel import MoneywheelInput
from services.moneywheel_service import MoneywheelService


def _make_metric(val):
    return Metric(value=val, available=val is not None)


def _make_financial_state(**overrides):
    base = dict(
        scope="family",
        planning_unit_id="pu-test-1",
        income_monthly=_make_metric(100000),
        income_annual=_make_metric(1200000),
        expenses_monthly=_make_metric(50000),
        expenses_annual=_make_metric(600000),
        investable_surplus_monthly=_make_metric(50000),
        investable_surplus_annual=_make_metric(600000),
        total_assets=_make_metric(2000000),
        total_liabilities=_make_metric(200000),
        emi_burden_monthly=_make_metric(10000),
        total_insurance_sum_assured=_make_metric(10000000),
        insurance_breakdown=[{"policy_type": "Term Life", "sum_assured": 10000000}],
    )
    base.update(overrides)
    return FinancialState(**base)


def test_moneywheel_ratios_consume_canonical_financial_state_values():
    """Verifies MoneyWheel consumes canonical FinancialState facts without re-deriving them."""

    mock_snap_repo = MagicMock()
    mock_snap_repo.save_snapshot.side_effect = lambda res, snap: res

    mock_data_repo = MagicMock()

    mock_goal_repo = MagicMock()
    mock_goal_repo.list_goals.return_value = []

    service = MoneywheelService(
        repository=mock_snap_repo,
        data_repository=mock_data_repo,
        goal_repository=mock_goal_repo,
    )

    state = _make_financial_state(
        total_assets=_make_metric(2000000),
        total_liabilities=_make_metric(200000),
        expenses_monthly=_make_metric(50000),
        essential_monthly_expenses=_make_metric(50000),
        liquid_assets=_make_metric(400000),
        financial_assets=_make_metric(600000),
        total_insurance_sum_assured=_make_metric(10000000),
        insurance_breakdown=[{"policy_type": "Term Life", "sum_assured": 10000000}],
    )

    result = service.calculate_from_financial_state(state)
    assert len(result.ratios) == 9
    assert not hasattr(result, "rules")
    ratio_map = {r.key: r for r in result.ratios}

    # Liquid asset ratio:
    # total_assets = 2,000,000
    # liquid_asset_ratio = 400k / 2M * 100 = 20.0%
    liquid_to_total = ratio_map["liquid_asset_ratio"]
    assert liquid_to_total.value == 20.0
    assert liquid_to_total.status == "healthy"
    assert liquid_to_total.available is True

    # financial_assets = 600k comes directly from canonical FinancialState.
    # financial_asset_ratio = 600k / 2M * 100 = 30.0%
    fin_asset_ratio = ratio_map["financial_asset_ratio"]
    assert fin_asset_ratio.value == 30.0
    assert fin_asset_ratio.status == "attention"
    assert fin_asset_ratio.available is True

    # Insurance coverage ratio:
    # annual_income = 1,200,000; total_liabilities = 200,000 => required = 10 * 1.2M + 200k = 12.2M
    # existing_sum_assured = 10,000,000
    # insurance_coverage_ratio = 10M / 12.2M * 100 = ~81.97%
    ins_ratio = ratio_map["insurance_coverage_ratio"]
    assert ins_ratio.available is True
    assert round(ins_ratio.value, 2) == 81.97
    assert ins_ratio.status == "excellent"

    # Data repository get_insurance_policies was NOT called (Finding 1 resolved)
    mock_data_repo.get_insurance_policies.assert_not_called()
