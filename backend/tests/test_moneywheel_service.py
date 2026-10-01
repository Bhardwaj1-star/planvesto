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


def test_bank_cash_is_liquid_and_financial():
    rows = [{"asset_type": "Bank / Cash", "current_value": 100000}]
    liquid = MoneywheelService._sum_assets(rows, "is_liquid", MOCK_ASSET_TYPE_MASTER)
    financial = MoneywheelService._sum_assets(rows, "is_financial", MOCK_ASSET_TYPE_MASTER)
    investment = MoneywheelService._sum_assets(rows, "is_investment", MOCK_ASSET_TYPE_MASTER)

    assert liquid == 100000
    assert financial == 100000
    assert investment == 0  # Cash is not investment


def test_mutual_funds_is_liquid_financial_and_investment():
    rows = [{"asset_type": "Mutual Funds", "current_value": 200000}]
    liquid = MoneywheelService._sum_assets(rows, "is_liquid", MOCK_ASSET_TYPE_MASTER)
    financial = MoneywheelService._sum_assets(rows, "is_financial", MOCK_ASSET_TYPE_MASTER)
    investment = MoneywheelService._sum_assets(rows, "is_investment", MOCK_ASSET_TYPE_MASTER)

    assert liquid == 200000
    assert financial == 200000
    assert investment == 200000


def test_stocks_equity_is_liquid_financial_and_investment():
    rows = [{"asset_type": "Stocks / Equity", "current_value": 300000}]
    liquid = MoneywheelService._sum_assets(rows, "is_liquid", MOCK_ASSET_TYPE_MASTER)
    financial = MoneywheelService._sum_assets(rows, "is_financial", MOCK_ASSET_TYPE_MASTER)
    investment = MoneywheelService._sum_assets(rows, "is_investment", MOCK_ASSET_TYPE_MASTER)

    assert liquid == 300000
    assert financial == 300000
    assert investment == 300000


def test_fixed_deposits_is_financial_and_investment_not_liquid():
    rows = [{"asset_type": "Fixed Deposits", "current_value": 150000}]
    liquid = MoneywheelService._sum_assets(rows, "is_liquid", MOCK_ASSET_TYPE_MASTER)
    financial = MoneywheelService._sum_assets(rows, "is_financial", MOCK_ASSET_TYPE_MASTER)
    investment = MoneywheelService._sum_assets(rows, "is_investment", MOCK_ASSET_TYPE_MASTER)

    assert liquid == 0
    assert financial == 150000
    assert investment == 150000


def test_real_estate_is_investment_not_financial_or_liquid():
    rows = [{"asset_type": "Real Estate", "current_value": 2500000}]
    liquid = MoneywheelService._sum_assets(rows, "is_liquid", MOCK_ASSET_TYPE_MASTER)
    financial = MoneywheelService._sum_assets(rows, "is_financial", MOCK_ASSET_TYPE_MASTER)
    investment = MoneywheelService._sum_assets(rows, "is_investment", MOCK_ASSET_TYPE_MASTER)

    assert liquid == 0
    assert financial == 0
    assert investment == 2500000


def test_matching_is_case_insensitive_and_trims_whitespace():
    rows = [
        {"asset_type": "  bank / cash  ", "current_value": 50000},
        {"asset_type": "MUTUAL FUNDS", "current_value": 75000},
        {"asset_type": "  stocks / equity  ", "current_value": 100000},
        {"asset_type": "fixed deposits  ", "current_value": 25000},
        {"asset_type": "  REAL ESTATE  ", "current_value": 500000},
    ]
    # Liquid: bank/cash (50k) + mutual funds (75k) + stocks (100k) = 225k
    liquid = MoneywheelService._sum_assets(rows, "is_liquid", MOCK_ASSET_TYPE_MASTER)
    assert liquid == 225000

    # Financial: bank/cash (50k) + mutual funds (75k) + stocks (100k) + fixed deposits (25k) = 250k
    financial = MoneywheelService._sum_assets(rows, "is_financial", MOCK_ASSET_TYPE_MASTER)
    assert financial == 250000

    # Investment: mutual funds (75k) + stocks (100k) + fixed deposits (25k) + real estate (500k) = 700k
    investment = MoneywheelService._sum_assets(rows, "is_investment", MOCK_ASSET_TYPE_MASTER)
    assert investment == 700000


def test_encoded_asset_name_resolution():
    rows = [
        {"asset_name": "Mutual Funds - hdfc flexi cap", "current_value": 50000},
        {"asset_name": "Bank / Cash - salary account", "current_value": 20000},
        {"asset_name": "Insurance - LIC jeevan anand", "current_value": 80000},
    ]
    unmapped = set()
    liquid = MoneywheelService._sum_assets(rows, "is_liquid", MOCK_ASSET_TYPE_MASTER, unmapped)
    assert liquid == 70000  # 50k + 20k
    assert "Insurance" in unmapped


def test_unknown_asset_type_is_excluded_and_tracked():
    rows = [
        {"asset_type": "Cryptocurrency", "current_value": 100000},
        {"asset_type": "Antiques", "current_value": 50000},
        {"asset_type": "Mutual Funds", "current_value": 200000},
    ]
    unmapped = set()
    liquid = MoneywheelService._sum_assets(rows, "is_liquid", MOCK_ASSET_TYPE_MASTER, unmapped)
    financial = MoneywheelService._sum_assets(rows, "is_financial", MOCK_ASSET_TYPE_MASTER, unmapped)

    assert liquid == 200000
    assert financial == 200000
    assert unmapped == {"Cryptocurrency", "Antiques"}


def test_empty_assets_returns_zero():
    liquid = MoneywheelService._sum_assets([], "is_liquid", MOCK_ASSET_TYPE_MASTER)
    financial = MoneywheelService._sum_assets([], "is_financial", MOCK_ASSET_TYPE_MASTER)
    assert liquid == 0.0
    assert financial == 0.0


def test_moneywheel_ratios_receive_calculated_values_instead_of_zero():
    """Verifies that Liquidity & Resilience and Investment Structure ratios
    receive non-zero calculated values from active asset types instead of hard-coded zero.
    """
    mock_snap_repo = MagicMock()
    mock_snap_repo.save_snapshot.side_effect = lambda res, snap: res

    mock_data_repo = MagicMock()
    mock_data_repo.get_active_asset_types.return_value = MOCK_ASSET_TYPE_MASTER
    mock_data_repo.get_expenses.return_value = [{"expense_type": "Housing", "amount": 50000, "frequency": "Monthly"}]
    mock_data_repo.get_liabilities.return_value = [{"liability_type": "Credit Card", "outstanding_amount": 200000}]
    mock_data_repo.get_insurance_policies.return_value = []
    mock_data_repo.get_assets.return_value = [
        {"asset_type": "Bank / Cash", "current_value": 100000},
        {"asset_type": "Mutual Funds", "current_value": 300000},
        {"asset_type": "Fixed Deposits", "current_value": 200000},
        {"asset_type": "Real Estate", "current_value": 1400000},
    ]

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
    )

    result = service.calculate_from_financial_state(state)
    ratio_map = {r.key: r for r in result.ratios}
    rule_map = {r.key: r for r in result.rules}

    # Liquidity & Resilience:
    # liquid_assets = 100k + 300k = 400k
    # emergency_coverage = 400k / 50k = 8.0 months
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

    # financial_assets = 100k + 300k + 200k = 600k
    # financial_asset_ratio = 600k / 2M * 100 = 30.0%
    fin_asset_ratio = ratio_map["financial_asset_ratio"]
    assert fin_asset_ratio.value == 30.0
    assert fin_asset_ratio.status == "attention"
    assert fin_asset_ratio.available is True

    # Metadata exposes unmapped types as empty list when all mapped
    assert result.metadata.get("unmapped_asset_types") == []


def test_moneywheel_exposes_unmapped_asset_types_in_metadata():
    mock_snap_repo = MagicMock()
    mock_snap_repo.save_snapshot.side_effect = lambda res, snap: res

    mock_data_repo = MagicMock()
    mock_data_repo.get_active_asset_types.return_value = MOCK_ASSET_TYPE_MASTER
    mock_data_repo.get_expenses.return_value = []
    mock_data_repo.get_liabilities.return_value = []
    mock_data_repo.get_insurance_policies.return_value = []
    mock_data_repo.get_assets.return_value = [
        {"asset_type": "Mutual Funds", "current_value": 50000},
        {"asset_type": "Unknown Precious Metal", "current_value": 30000},
        {"asset_name": "Insurance - LIC Jeevan", "current_value": 20000},
    ]

    mock_goal_repo = MagicMock()
    mock_goal_repo.list_goals.return_value = []

    service = MoneywheelService(
        repository=mock_snap_repo,
        data_repository=mock_data_repo,
        goal_repository=mock_goal_repo,
    )

    state = _make_financial_state()
    result = service.calculate_from_financial_state(state)

    unmapped = result.metadata.get("unmapped_asset_types")
    assert unmapped is not None
    assert "Unknown Precious Metal" in unmapped
    assert "Insurance" in unmapped
