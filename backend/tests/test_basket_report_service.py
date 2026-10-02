from unittest.mock import MagicMock
from services.basket_report_service import BasketReportService


def test_basket_report_service_build_report_and_generate_pdf():
    service = BasketReportService()

    # Mock repositories
    service.strategy_repo = MagicMock()
    service.goal_report_service = MagicMock()

    mock_run_g1 = MagicMock(strategy_run_id="run-g1")
    mock_run_g2 = MagicMock(strategy_run_id="run-g2")

    def mock_get_latest_run(pu_id, goal_id):
        if goal_id == "g1":
            return mock_run_g1
        elif goal_id == "g2":
            return mock_run_g2
        return None

    service.strategy_repo.get_latest_run.side_effect = mock_get_latest_run

    mock_report_g1 = {
        "report_type": "goal_decision_report",
        "goal": {
            "id": "g1",
            "name": "Higher Education",
            "type": "Education",
            "priority": "High",
            "duration_years": 4,
            "target_year": 2030,
            "target_month": 6,
        },
        "goal_calculation": {
            "future_target": 2500000.0,
            "today_cost": 1800000.0,
            "funding_gap": 1500000.0,
            "required_monthly_contribution": 25000.0,
            "projected_mapped_asset_value": 1000000.0,
            "funding_status": "Shortfall",
            "priority": "High",
        },
        "strategy": {
            "selected_strategy_name": "Progressive De-risking",
            "rationale": "Protect capital as maturity approaches.",
            "trade_offs": ["Lower equity allocation in final 2 years."],
        },
        "provenance": {"strategy_run_id": "run-g1"},
    }

    mock_report_g2 = {
        "report_type": "goal_decision_report",
        "goal": {
            "id": "g2",
            "name": "Family Vacation",
            "type": "Vacation",
            "priority": "Medium",
            "duration_years": 2,
            "target_year": 2028,
            "target_month": 12,
        },
        "goal_calculation": {
            "future_target": 500000.0,
            "today_cost": 400000.0,
            "funding_gap": 300000.0,
            "required_monthly_contribution": 12000.0,
            "projected_mapped_asset_value": 200000.0,
            "funding_status": "Shortfall",
            "priority": "Medium",
        },
        "strategy": {
            "selected_strategy_name": "Goal Funding",
            "rationale": "Systematic savings into liquid and short-duration debt.",
            "trade_offs": ["Zero equity exposure."],
        },
        "provenance": {"strategy_run_id": "run-g2"},
    }

    def mock_build_report(pu_id, run_id):
        if run_id == "run-g1":
            return mock_report_g1
        elif run_id == "run-g2":
            return mock_report_g2
        raise ValueError("Unknown run")

    service.goal_report_service.build_report.side_effect = mock_build_report

    report = service.build_report("pu-1", "Education & Vacation Basket", ["g1", "g2"])

    assert report["report_type"] == "goal_basket_report"
    assert report["basket"]["name"] == "Education & Vacation Basket"
    assert report["basket"]["goal_count"] == 2
    assert report["summary"]["combined_future_target"] == 3000000.0
    assert report["summary"]["combined_funding_gap"] == 1800000.0
    assert report["summary"]["combined_required_monthly_contribution"] == 37000.0
    assert len(report["priority_ladder"]) == 2
    assert len(report["combined_cash_flow_trajectory"]) > 0
    assert len(report["product_architecture"]) == 3
    assert len(report["action_plan_timeline"]) >= 4
    assert len(report["contingency_matrix"]) == 3

    pdf = service.generate_pdf("pu-1", "Education & Vacation Basket", ["g1", "g2"])
    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1000
