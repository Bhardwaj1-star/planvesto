"""
Unit test verifying exact contract compatibility between Frontend Moneywheel and Backend /api/moneywheel/*.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_frontend_moneywheel_contract():
    # 1. Test POST /api/moneywheel/calculate
    payload = {
        "planning_unit_id": "pu-mw-123",
        "financial_state_snapshot": {"net_worth": 500000},
    }
    calc_resp = client.post("/api/moneywheel/calculate", json=payload)
    assert calc_resp.status_code == 200
    data = calc_resp.json()
    assert "result" in data
    assert data["result"]["planning_unit_id"] == "pu-mw-123"
    assert len(data["result"]["ratios"]) == 9

    # 2. Test GET /api/moneywheel/latest/pu-mw-123
    latest_resp = client.get("/api/moneywheel/latest/pu-mw-123")
    assert latest_resp.status_code == 200
    latest_data = latest_resp.json()
    assert latest_data["planning_unit_id"] == "pu-mw-123"
    assert len(latest_data["ratios"]) == 9

    # 3. Test GET /api/moneywheel/history/pu-mw-123
    hist_resp = client.get("/api/moneywheel/history/pu-mw-123")
    assert hist_resp.status_code == 200
    hist_data = hist_resp.json()
    assert isinstance(hist_data, list)
    assert len(hist_data) >= 1
    assert len(hist_data[0]["ratios"]) == 9
