from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_basket_report_api_endpoints():
    with patch("api.basket_report.authenticate_user", return_value="user-1"), \
         patch("api.basket_report.verify_planning_unit_ownership", return_value=True), \
         patch("api.basket_report.BasketReportService") as mock_service_class:

        mock_instance = MagicMock()
        mock_instance.build_report.return_value = {
            "report_type": "goal_basket_report",
            "basket": {"name": "Test Basket", "goal_count": 2},
            "summary": {"combined_future_target": 1000000.0},
        }
        mock_instance.generate_pdf.return_value = b"%PDF-1.4 test basket pdf"
        mock_service_class.return_value = mock_instance

        # Test JSON endpoint
        response = client.post(
            "/api/basket-report",
            params={"planning_unit_id": "pu-1", "basket_name": "Test Basket"},
            json=["goal-1", "goal-2"],
            headers={"Authorization": "Bearer test-token"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["report_type"] == "goal_basket_report"
        assert data["basket"]["name"] == "Test Basket"

        # Test PDF endpoint
        pdf_response = client.post(
            "/api/basket-report/pdf",
            params={"planning_unit_id": "pu-1", "basket_name": "Test Basket"},
            json=["goal-1", "goal-2"],
            headers={"Authorization": "Bearer test-token"},
        )
        assert pdf_response.status_code == 200
        assert pdf_response.headers["content-type"] == "application/pdf"
        assert "attachment" in pdf_response.headers["content-disposition"]
        assert pdf_response.content.startswith(b"%PDF")
