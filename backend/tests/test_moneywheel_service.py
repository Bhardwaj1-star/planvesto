from unittest.mock import MagicMock
import pytest

from models.financial_state import FinancialState, Metric
from models.moneywheel import MoneywheelInput
from services.moneywheel_service import MoneywheelService


MOCK_ASSET_TYPE_MASTER = [
    {"code": "BANK_CASH", "name": "Bank / Cash", "category": "Cash & Bank", "is_liquid": True, "is_financial": True, "is_investment": False, "is_active": True},
    {"code": "FIXED_DEPOSIT", "name": "Fixed Deposits", "category": "Debt / Fixed Income", "is_liquid": False, "is_financial": True, "is_investment": True, "is_active": True},
    {"code": "MUTUAL_FUNDS", "name": "Mutual Funds", "category": "Market Linked", "is_liquid": True, "is_financial": True, "is_investment": True, "is_active": True},
    {"code": "STOCKS_EQUITY", "name": "Stocks / Equity", "category": "Equity", "is_liquid": True, "is_financial": True, "is_investment": True, "is_active": True},
    {"code": "BONDS_DEBT", "name": "Bonds / Debt", "category": "Debt / Fixed Income", "is_liquid": False, "is_financial": True, "is_investment": True, "is_active": True},
    {"code": "EPF_PPF", "name": "EPF / PPF", "category": "Retirement", "is_liquid": False, "is_financial": True, "is_investment": True, "is_active": True},
    {"code": "NPS", "name": "NPS", "category": "Retirement", "is_liquid": False, "is_financial": True, "is_investment": True, "is_active": True},
    {"code": "GOLD", "name": "Gold", "category": "Commodities", "is_liquid": False, "is_financial": True, "is_investment": True, "is_active": True},
    {"code": "REAL_ESTATE", "name": "Real Estate", "category": "Property", "is_liquid": False, "is_financial": False, "is_investment": True, "is_active": True},
    {"code": "VEHICLE", "name": "Vehicle", "category": "Personal Use", "is_liquid": False, "is_financial": False, "is_investment": False, "is_active": True},
    {"code": "BUSINESS", "name": "Business Ownership", "category": "Business", "is_liquid": False, "is_financial": False, "is_investment": True, "is_active": True},
    {"code": "OTHER", "name": "Other", "category": "Other", "is_liquid": False, "is_financial": False, "is_investment": False, "is_active": True},
]


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
        cash_flow_ratio=_make_metric(0.5),
        savings_investment_rate=_make_metric(0.5),
        total_assets=_make_metric(2000000),
        total_liabilities=_make_metric(200000),
        emi_burden_monthly=_make_metric(10000),
        net_worth=_make_metric(1800000),
        safety_reserve_months=_make_metric(6),
        safety_reserve_required_amount=_make_metric(300000),
    )
    base.update(overrides)
    return FinancialState(**base)


def test_moneywheel_ratios_consume_canonical_financial_state_values():
    """Verifies MoneyWheel consumes canonical FinancialState facts without re-deriving them."""

    mock_snap_repo = MagicMock()
    mock_snap_repo.save_snapshot.side_effect = lambda res, snap: res

    mock_data_repo = MagicMock()
    mock_data_repo.get_active_asset_types.return_value = MOCK_ASSET_TYPE_MASTER
    mock_data_repo.get_liabilities.return_value = [{"liability_type": "Credit Card", "outstanding_amount": 200000}]
    mock_data_repo.get_insurance_policies.return_value = []

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
    )

    result = service.calculate_from_financial_state(state)
    ratio_map = {r.key: r for r in result.ratios}
    rule_map = {r.key: r for r in result.rules}

    # Liquidity & Resilience comes directly from canonical FinancialState fields:
    # liquid_assets = 400k; essential_monthly_expenses = 50k => 8.0 months
    emergency_fund = rule_map.get("emergency_coverage") or ratio_map.get("emergency_fund_coverage")
    assert emergency_fund is not None
    assert emergency_fund.value == 8.0
    assert emergency_fund.available is True

    # Investment Structure:
    # total_assets = 2,000,000
    # liquid_asset_ratio = 400k / 2M * 100 = 20.0%
    liquid_to_total = ratio_map.get("liquid_asset_ratio") or ratio_map.get("liquid_asset_to_total_asset")
    assert liquid_to_total is not None
    assert liquid_to_total.value == 20.0
    assert liquid_to_total.status == "healthy"
    assert liquid_to_total.available is True

    # financial_assets = 600k comes directly from canonical FinancialState.
    # financial_asset_ratio = 600k / 2M * 100 = 30.0%
    fin_asset_ratio = ratio_map["financial_asset_ratio"]
    assert fin_asset_ratio.value == 30.0
    assert fin_asset_ratio.status == "attention"
    assert fin_asset_ratio.available is True

    # Metadata exposes unmapped types as empty list when all mapped
    assert result.metadata.get("unmapped_asset_types") == []


