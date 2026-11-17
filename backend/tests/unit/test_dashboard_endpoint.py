"""
Unit test for Dashboard aggregation endpoint /api/dashboard.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_dashboard_endpoint():
    response = client.get("/api/dashboard?planning_unit_id=pu-test-123")
    assert response.status_code == 200
    data = response.json()

    assert data["planning_unit_id"] == "pu-test-123"
    assert "financial_state" in data
    assert "goals" in data
    assert "net_worth" in data["financial_state"]
    assert "total_assets" in data["financial_state"]
    assert "income_monthly" in data["financial_state"]
