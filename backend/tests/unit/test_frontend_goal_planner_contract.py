"""
Unit test verifying exact contract compatibility between Frontend Goal Planner and Backend /api/goals/calculate.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_frontend_exact_calculate_payload():
    frontend_payload = {
        "planning_unit_id": "pu-12345",
        "goal_id": None,
        "goal_name": "Retirement Corpus",
        "goal_type": "retirement",
        "today_cost": 600000,
        "target_month": 1,
        "target_year": 2030,
        "inflation_rate": 0.06,
        "priority": "high",
        "flexibility": "Flexible",
        "status": "Active",
        "asset_mappings": [
            {
                "asset_id": "asset-abc",
                "allocation_type": "percentage",
                "allocation_value": 100,
                "expected_return": 0.10,
                "return_frequency": "annual",
            }
        ],
        "dynamic_details": {
            "lifeExpectancy": "85",
            "desiredLifestyleMonthlyExpense": "50000",
        },
    }

    response = client.post("/api/goals/calculate", json=frontend_payload)
    assert response.status_code == 200
    data = response.json()

    # Verify all fields frontend expects in previewResult:
    assert "duration_years" in data
    assert "future_target" in data
    assert "projected_mapped_asset_value" in data
    assert "funding_gap" in data
    assert "funding_status" in data
    assert "required_monthly_contribution" in data
    assert data["goal_type"] == "retirement"
    assert data["funding_status"] in ("Shortfall", "On Track", "Overfunded")
    assert float(data["future_target"]) > 600000
