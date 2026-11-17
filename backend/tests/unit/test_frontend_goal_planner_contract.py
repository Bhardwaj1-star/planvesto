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
    assert isinstance(data.get("mapped_assets"), list)
    assert isinstance(data.get("version_metadata"), dict)
    assert data["goal_type"] == "retirement"
    assert data["funding_status"] in ("Shortfall", "On Track", "Overfunded")
    assert float(data["future_target"]) > 600000
    assert data.get("feasibility_status") == "unknown"
    assert data.get("available_monthly_surplus") is None


def test_goal_feasibility_surplus_is_calculated_from_backend_financial_state(monkeypatch):
    import app.api.routers.goal_planner as goal_planner_router

    monkeypatch.setattr(
        goal_planner_router._profile_repo,
        "get_latest_financial_state_snapshot",
        lambda planning_unit_id, scope="family": {
            "financial_state": {
                "income_monthly": {"value": 120000, "available": True},
                "expenses_monthly": {"value": 65000, "available": True},
                "monthly_savings_investments": {"value": 15000, "available": True},
            }
        },
    )
    payload = {
        "planning_unit_id": "pu-12345",
        "goal_name": "Education",
        "goal_type": "education",
        "today_cost": 600000,
        "target_month": 1,
        "target_year": 2032,
        "inflation_rate": 0.06,
        "expected_return_pct": 10,
        "asset_mappings": [],
        "available_monthly_surplus": 999999,
    }

    response = client.post("/api/goals/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert float(data["available_monthly_surplus"]) == 40000
    assert data["feasibility_source"] == "income_monthly - expenses_monthly - monthly_savings_investments"
    assert data["feasibility_status"] == "feasible"
