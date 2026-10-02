from types import SimpleNamespace
from unittest.mock import MagicMock

from services.goal_report_service import GoalReportService


def test_individual_goal_report_exposes_complete_goal_funding_data():
    service = GoalReportService()
    service._load = MagicMock(return_value=(
        SimpleNamespace(
            goal_id="g1",
            defined_goal_version=1,
            selected_strategy_id="strat-goal-funding",
            applicable_strategies=[],
            recommendation=SimpleNamespace(model_dump=lambda mode="json": {}),
        ),
        SimpleNamespace(
            goal_name="Vacation",
            goal_type="Travel",
            today_cost=100000.0,
            inflation_rate=0.06,
            future_target=133822.0,
            funding_gap=90000.0,
            required_monthly_contribution=1500.0,
            target_month=12,
            target_year=2031,
            duration_years=5,
            funding_status="Shortfall",
            projected_mapped_asset_value=43822.0,
            funding_return_assumption=0.08,
            feasibility_status="constrained",
            feasibility_reason="Required contribution exceeds current surplus.",
            available_monthly_surplus=1000.0,
            monthly_contribution_surplus_gap=500.0,
            funding_strategies=[
                {
                    "strategy_id": "sip",
                    "strategy_name": "SIP",
                    "status": "constrained",
                    "required_lumpsum": 0.0,
                    "required_monthly_contribution": 1500.0,
                    "starting_monthly_contribution": 1500.0,
                    "annual_step_up": 0.0,
                    "remaining_gap": 0.0,
                }
            ],
            priority="Important",
            flexibility="Flexible",
            status="Active",
            version=1,
            is_latest=True,
            mapped_assets=[],
            version_metadata={},
        ),
        {
            "annual_income": 1200000.0,
            "annual_expenses": 900000.0,
            "monthly_surplus": 25000.0,
            "assets": [],
            "liabilities": [],
            "net_worth": 500000.0,
        },
    ))
    report = service.build_report("pu-1", "run-1")

    funding = report["goal_funding"]
    assert funding["feasibility_status"] == "constrained"
    assert funding["available_monthly_surplus"] == 1000.0
    assert funding["monthly_contribution_surplus_gap"] == 500.0
    assert funding["funding_strategies"][0]["strategy_id"] == "sip"
    assert report["goal_calculation"]["funding_return_assumption"] == 0.08
    assert report["goal_context"]["priority"] == "Important"
