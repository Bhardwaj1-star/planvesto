from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_routes_registered():
    paths = app.openapi()["paths"]
    assert "/api/strategy/financial-plan/build" in paths
    assert "/api/strategy/financial-plan" in paths
    assert "/api/strategy/financial-plan.pdf" in paths


def test_financial_plan_unauthenticated_returns_401():
    r = client.get("/api/strategy/financial-plan?planning_unit_id=pu-1")
    assert r.status_code == 401

    r_post = client.post("/api/strategy/financial-plan/build", json={"planning_unit_id": "pu-1"})
    assert r_post.status_code == 401

    r_pdf = client.get("/api/strategy/financial-plan.pdf?planning_unit_id=pu-1")
    assert r_pdf.status_code == 401


@patch("api.strategy.verify_planning_unit_ownership")
@patch("api.strategy.authenticate_user")
@patch("api.strategy.FinancialPlanService.build_plan")
def test_financial_plan_build_success(mock_build, mock_auth, mock_verify):
    mock_auth.return_value = "user-1"
    mock_verify.return_value = True
    mock_build.return_value = {
        "report_type": "complete_financial_plan",
        "planning_unit_id": "pu-1",
        "goals": [],
        "consolidated_funding": {"required_monthly_contribution": 0.0},
    }

    headers = {"Authorization": "Bearer mock-token"}
    payload = {"planning_unit_id": "pu-1"}
    r = client.post("/api/strategy/financial-plan/build", json=payload, headers=headers)

    assert r.status_code == 200
    assert r.json()["report_type"] == "complete_financial_plan"
    mock_auth.assert_called_once()
    mock_verify.assert_called_once_with("pu-1", "user-1")


@patch("api.strategy.verify_planning_unit_ownership")
@patch("api.strategy.authenticate_user")
@patch("api.strategy.FinancialPlanService.build_plan")
def test_financial_plan_get_success(mock_build, mock_auth, mock_verify):
    mock_auth.return_value = "user-1"
    mock_verify.return_value = True
    mock_build.return_value = {
        "report_type": "complete_financial_plan",
        "planning_unit_id": "pu-1",
        "goals": [],
    }

    headers = {"Authorization": "Bearer mock-token"}
    r = client.get("/api/strategy/financial-plan?planning_unit_id=pu-1", headers=headers)

    assert r.status_code == 200
    assert r.json()["planning_unit_id"] == "pu-1"


@patch("api.strategy.verify_planning_unit_ownership")
@patch("api.strategy.authenticate_user")
@patch("api.strategy.FinancialPlanService.generate_pdf")
def test_financial_plan_download_pdf_success(mock_pdf, mock_auth, mock_verify):
    mock_auth.return_value = "user-1"
    mock_verify.return_value = True
    mock_pdf.return_value = b"%PDF-1.4 mock pdf data"

    headers = {"Authorization": "Bearer mock-token"}
    r = client.get("/api/strategy/financial-plan.pdf?planning_unit_id=pu-1", headers=headers)

    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert "complete-financial-plan-pu-1.pdf" in r.headers["content-disposition"]
    assert r.content.startswith(b"%PDF-1.4")
