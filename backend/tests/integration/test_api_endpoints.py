"""
Integration tests for FastAPI endpoints:
- /api/goals/calculate and /api/goals
- /api/financial-state/build
- /api/moneywheel/calculate
- /api/goal-funding/assess
- /api/action-plan/actions
"""

from decimal import Decimal
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_goal_calculate_preview_endpoint():
    payload = {
        "planning_unit_id": "pu-test-1",
        "goal_name": "Child Education",
        "canonical_id": "goal_education",
        "today_cost": "1500000.00",
        "target_year": 2031,
        "target_month": 11,
        "inflation_rate_pct": "8.0",
        "expected_return_pct": "12.0",
        "available_monthly_surplus": "50000.00",
        "asset_mappings": [],
    }

    response = client.post("/api/goals/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["goal_name"] == "Child Education"
    assert Decimal(str(data["future_target"])) > Decimal("2000000.00")
    assert data["is_feasible_under_current_conditions"] is True
    assert Decimal(str(data["required_monthly_sip"])) < Decimal("50000.00")


def test_financial_state_build_endpoint():
    payload = {
        "planning_unit_id": "pu-test-1",
        "scope": "family",
        "target_year": 2026,
        "target_month": 11,
    }

    response = client.post("/api/financial-state/build", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["planning_unit_id"] == "pu-test-1"
    assert "data_readiness" in data
    assert "net_worth" in data


def test_moneywheel_calculate_endpoint():
    payload = {
        "planning_unit_id": "pu-test-1",
        "target_year": 2026,
        "target_month": 11,
    }

    response = client.post("/api/moneywheel/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["planning_unit_id"] == "pu-test-1"
    assert "measurements" in data
    assert "findings" in data
    assert len(data["findings"]) > 0


def test_goal_funding_assess_endpoint():
    payload = {
        "planning_unit_id": "pu-test-1",
        "goal_id": "goal-home-01",
        "target_amount": "5000000.00",
        "horizon_years": 5,
        "start_calendar_year": 2026,
        "initial_allocated_assets": "1000000.00",
        "required_monthly_sip": "45000.00",
        "expected_annual_return_pct": "10.0",
        "available_monthly_surplus": "60000.00",
        "financing_option": {
            "down_payment": "1500000.00",
            "loan_annual_interest_rate_pct": "9.0",
            "loan_tenure_months": 120,
        },
    }

    response = client.post("/api/goal-funding/assess", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["goal_id"] == "goal-home-01"
    assert "self_money_path" in data
    assert "financing_path" in data
    assert "comparison_matrix" in data
    assert Decimal(str(data["financing_path"]["monthly_emi"])) > 0
    assert "Trade-off Decision" in data["comparison_matrix"]["investor_decision_prompt"]


def test_action_plan_create_endpoint():
    payload = {
        "planning_unit_id": "pu-test-1",
        "plan_id": "plan-acc-01",
        "action_type": "start_sip",
        "title": "Start Mutual Fund SIP",
        "description": "Automate 15,000 monthly SIP",
        "target_amount": "15000.00",
        "target_date": "2026-12-01",
    }

    response = client.post("/api/action-plan/actions", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["plan_id"] == "plan-acc-01"
    assert data["action_type"] == "start_sip"
    assert data["status"] == "pending"
