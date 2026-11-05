from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app
from models.summary_report import SummaryReport, GoalSummary, Observation, ActionItem


client = TestClient(app)


def test_summary_report_api_endpoints():
    with patch("api.summary_report.authenticate_user", return_value="user-1"), \
         patch("api.summary_report.verify_planning_unit_ownership", return_value=True), \
         patch("api.summary_report.SummaryReportService.generate") as mock_generate:

        fake_report = SummaryReport(
            financial_snapshot={"annual_income": 1200000.0, "net_worth": 5000000.0},
            goals=[
                GoalSummary(
                    id="g-1",
                    name="Retirement",
                    target_amount=15000000.0,
                    horizon_years=15.0,
                    current_funding=2000000.0,
                    funding_gap=13000000.0,
                    feasibility="feasible",
                    required_contribution=35000.0,
                )
            ],
            observations=[
                Observation(
                    description="Emergency buffer coverage is optimal.",
                    relevance=0.9,
                    source="MoneyWheel",
                )
            ],
            actions=[
                ActionItem(
                    description="Maintain current monthly investments.",
                    priority=0.8,
                    source="StrategyEngine",
                )
            ],
            investment_allocation={},
            risk_profile={"risk_required": {"value": 0.08, "available": True}},
            provenance={"planning_unit_id": "pu-1"},
        )
        mock_generate.return_value = fake_report

        # 1. Test JSON endpoint
        response = client.get(
            "/api/summary-report/json",
            params={"planning_unit_id": "pu-1"},
            headers={"Authorization": "Bearer test-token"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["goals"]) == 1
        assert data["goals"][0]["name"] == "Retirement"
        assert len(data["observations"]) == 1

        # 2. Test PDF endpoint
        pdf_response = client.get(
            "/api/summary-report/pdf",
            params={"planning_unit_id": "pu-1"},
            headers={"Authorization": "Bearer test-token"},
        )
        assert pdf_response.status_code == 200
        assert pdf_response.headers["content-type"] == "application/pdf"
        assert "attachment" in pdf_response.headers["content-disposition"]
        assert pdf_response.content.startswith(b"%PDF")
        assert len(pdf_response.content) > 1000
