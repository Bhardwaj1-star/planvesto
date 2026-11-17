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


def test_goal_feasibility_uses_canonical_surplus_and_does_not_overstate_overall_feasibility(monkeypatch):
    import app.api.routers.goal_planner as goal_planner_router
    from decimal import Decimal

    monkeypatch.setattr(
        goal_planner_router,
        "_financial_feasibility_context",
        lambda planning_unit_id, goal_id=None, user_id="": {
            "available_monthly_surplus": Decimal("50000"),
            "existing_goal_sip": Decimal("5000"),
            "source": "financial_state.investable_surplus_monthly",
        },
    )
    defined = {
        "goal_id": "goal-1",
        "goal_name": "Education",
        "goal_type": "education",
        "today_cost": Decimal("600000"),
        "target_month": 1,
        "target_year": 2032,
        "inflation_rate": Decimal("6"),
        "mapped_assets": [],
        "version_metadata": {"funding_return_assumption_pct": "10"},
    }

    result = goal_planner_router._apply_current_feasibility(defined, "pu-1", "user-1")

    assert result["feasibility_source"] == "financial_state.investable_surplus_monthly"
    assert result["fund_feasibility_case"] == "case_1_affordable"
    # Case 1 passes when surplus covers the additional required SIP and no blocking constraint exists.
    assert result["feasibility_status"] == "feasible"
    assert result["is_feasible_under_current_conditions"] is True
    assert result["fund_feasibility_case"] == "case_1_affordable"
    assert result["feasibility_status"] == "feasible"
    assert result["is_feasible_under_current_conditions"] is True
    assert result["surplus_gap"] == 0
    assert "funding_strategies" not in result


def test_goal_feasibility_is_unknown_when_canonical_surplus_is_unavailable(monkeypatch):
    import app.api.routers.goal_planner as goal_planner_router

    monkeypatch.setattr(
        goal_planner_router,
        "_financial_feasibility_context",
        lambda planning_unit_id, goal_id=None, user_id="": {
            "available_monthly_surplus": None,
            "existing_goal_sip": 0,
            "source": None,
        },
    )
    defined = {
        "goal_id": "goal-2", "goal_name": "Retirement", "goal_type": "retirement",
        "today_cost": 1000000, "target_month": 1, "target_year": 2035,
        "inflation_rate": 6, "mapped_assets": [], "version_metadata": {},
    }
    result = goal_planner_router._apply_current_feasibility(defined, "pu-1", "user-1")
    assert result["feasibility_status"] == "unknown"
    assert result["is_feasible_under_current_conditions"] is False
    assert "funding_strategies" not in result
