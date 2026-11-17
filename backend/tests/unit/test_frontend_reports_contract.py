"""
tests/unit/test_frontend_reports_contract.py
Verifies Reports endpoints (basket report, summary report, pdf rendering).
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_basket_report_and_pdf():
    """Verify basket report json and pdf download."""
    planning_unit_id = "test_pu_reports"
    payload = {
        "planning_unit_id": planning_unit_id,
        "goal_ids": ["goal_1", "goal_2"],
        "basket_name": "Family Future Basket",
    }

    # JSON report
    resp = client.post("/api/basket-report", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["basket_name"] == "Family Future Basket"
    assert data["consolidated_status"] == "feasible"

    # PDF report
    pdf_resp = client.post("/api/basket-report/pdf", json=payload)
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"
    assert pdf_resp.content.startswith(b"%PDF")


def test_summary_report_pdf():
    """Verify investor summary report pdf download."""
    planning_unit_id = "test_pu_reports"
    pdf_resp = client.get(f"/api/summary-report/pdf?planning_unit_id={planning_unit_id}")
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"
    assert pdf_resp.content.startswith(b"%PDF")


def test_financial_plan_and_retirement_reports():
    """Verify complete financial plan and retirement reports endpoints."""
    planning_unit_id = "test_pu_reports"

    # 1. Financial plan JSON
    plan_resp = client.get(f"/api/strategy/financial-plan?planning_unit_id={planning_unit_id}")
    assert plan_resp.status_code == 200
    assert "summary" in plan_resp.json()

    # 2. Financial plan PDF
    plan_pdf = client.get(f"/api/strategy/financial-plan.pdf?planning_unit_id={planning_unit_id}")
    assert plan_pdf.status_code == 200
    assert plan_pdf.headers["content-type"] == "application/pdf"
    assert plan_pdf.content.startswith(b"%PDF")

    # 3. Retirement report JSON & PDF
    ret_resp = client.get(f"/api/strategy/runs/srun_test/retirement-report?planning_unit_id={planning_unit_id}")
    assert ret_resp.status_code == 200

    ret_pdf = client.get(f"/api/strategy/runs/srun_test/retirement-report.pdf?planning_unit_id={planning_unit_id}")
    assert ret_pdf.status_code == 200
    assert ret_pdf.headers["content-type"] == "application/pdf"
