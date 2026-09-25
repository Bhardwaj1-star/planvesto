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
        existing_sum_assured=8000000,
        required_insurance_cover=10000000,
    )
    values.update(overrides)
    return MoneywheelInput(**values)


def test_all_ten_ratios_are_returned():
    result = MoneywheelEngine().build(_input())
    assert len(result.ratios) == 10
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
    assert statuses["debt_to_income_ratio"] == "healthy"


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


def test_insurance_coverage_ratio_is_calculated():
    result = MoneywheelEngine().build(_input(existing_sum_assured=8000000, required_insurance_cover=10000000))
    ratio = next(r for r in result.ratios if r.key == "insurance_gap_ratio")
    assert ratio.value == 80.0
    assert ratio.status == "excellent"
    assert ratio.available is True


def test_insurance_ratio_is_unavailable_without_cover_inputs():
    result = MoneywheelEngine().build(_input(existing_sum_assured=None, required_insurance_cover=None))
    ratio = next(r for r in result.ratios if r.key == "insurance_gap_ratio")
    assert ratio.value is None
    assert ratio.status == "unavailable"
    assert ratio.available is False


def test_moneywheel_repository_save_snapshot():
    from unittest.mock import MagicMock
    from data.moneywheel_repository import MoneywheelRepository

    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_client.table.return_value = mock_table
    mock_table.insert.return_value.select.return_value.execute.return_value.data = [
        {"snapshot_id": "snap-test-123"}
    ]

    repo = MoneywheelRepository(mock_client)
    result = MoneywheelEngine().build(_input())
    saved = repo.save_snapshot(result, {"sample": "state"})

    assert saved.metadata.get("snapshot_id") == "snap-test-123"
    mock_table.insert.assert_called_once()
    mock_table.insert.return_value.select.assert_called_once_with("*")


def test_post_moneywheel_calculate_uses_server_financial_state():
    from unittest.mock import MagicMock, patch
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)
    fake_result = MoneywheelEngine().build(_input())
    fake_service = MagicMock()
    fake_service.calculate_from_financial_state.return_value = fake_result
    fake_state = MagicMock()

    with patch("api.moneywheel.authenticate_user", return_value="user-123"), \
         patch("api.moneywheel.verify_planning_unit_ownership", return_value=True), \
         patch("api.moneywheel.FinancialStateService") as mock_state_service, \
         patch("api.moneywheel._service", return_value=fake_service):
        mock_state_service.return_value.build.return_value = fake_state
        response = client.post(
            "/api/moneywheel/calculate",
            headers={"Authorization": "Bearer test-token"},
            json={
                "planning_unit_id": "pu-1",
                "financial_state_snapshot": {"net_worth": {"value": 999999999}},
            },
        )

    assert response.status_code == 200
    mock_state_service.return_value.build.assert_called_once_with("pu-1", "family")
    fake_service.calculate_from_financial_state.assert_called_once_with(fake_state)


def test_post_moneywheel_calculate_success():
    from unittest.mock import patch, MagicMock
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)
    fake_result = MoneywheelEngine().build(_input())
    fake_service = MagicMock()
    fake_service.calculate_from_financial_state.return_value = fake_result
    fake_state = MagicMock()

    with patch("api.moneywheel.authenticate_user", return_value="user-123"), \
         patch("api.moneywheel.verify_planning_unit_ownership", return_value=True), \
         patch("api.moneywheel.FinancialStateService") as mock_state_service, \
         patch("api.moneywheel._service", return_value=fake_service):
        mock_state_service.return_value.build.return_value = fake_state

        response = client.post(
            "/api/moneywheel/calculate",
            headers={"Authorization": "Bearer test-token"},
            json={
                "planning_unit_id": "pu-1",
                "gross_monthly_income": 100000,
                "savings": 30000,
                "essential_monthly_expenses": 35000,
                "monthly_expenses": 50000,
                "liquid_assets": 500000,
                "short_term_liabilities": 250000,
                "monthly_debt_payments": 20000,
                "total_assets": 2000000,
                "total_liabilities": 400000,
                "financial_assets": 1500000,
                "existing_sum_assured": 8000000,
                "required_insurance_cover": 10000000,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert len(data["result"]["ratios"]) == 10
        assert data["result"]["metadata"]
