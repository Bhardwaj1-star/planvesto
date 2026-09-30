from unittest.mock import MagicMock
import pytest
from services.multi_goal_planning_service import MultiGoalPlanningService


def test_multi_goal_planning_service_build_plan():
    mock_goal_repo = MagicMock()
    mock_strat_repo = MagicMock()
    mock_strat_service = MagicMock()
    mock_report_service = MagicMock()

    # Setup 2 mock goals
    mock_goal_repo.list_goals.return_value = [
        {"goal_id": "goal-1", "goal_name": "Retirement", "priority": "high", "flexibility": "fixed"},
        {"goal_id": "goal-2", "goal_name": "Vacation", "priority": "low", "flexibility": "flexible"},
    ]

    mock_run1 = MagicMock(strategy_run_id="run-1")
    mock_run2 = MagicMock(strategy_run_id="run-2")
    mock_strat_repo.get_latest_run.side_effect = [mock_run1, mock_run2]

    mock_report_service.build_report.side_effect = [
        {
            "goal_id": "goal-1",
            "goal_name": "Retirement",
            "goal_type": "retirement",
            "goal_calculation": {
                "required_monthly_contribution": 20000.0,
                "target_year": 2045,
                "target_month": 12,
                "today_cost": 10000000.0,
                "future_target": 25000000.0,
                "funding_gap": 15000000.0,
            },
            "recommendation": {
                "recommended_strategy_id": "progressive_de_risking",
                "feasibility_status": "feasible",
                "short_reasons": ["Long horizon"],
            },
            "strategy": {"name": "Progressive De-risking"},
        },
        {
            "goal_id": "goal-2",
            "goal_name": "Vacation",
            "goal_type": "travel",
            "goal_calculation": {
                "required_monthly_contribution": 10000.0,
                "target_year": 2028,
                "target_month": 6,
                "today_cost": 500000.0,
                "future_target": 600000.0,
                "funding_gap": 300000.0,
            },
            "recommendation": {
                "recommended_strategy_id": "debt_conservative",
                "feasibility_status": "feasible",
                "short_reasons": ["Short horizon"],
            },
            "strategy": {"name": "Conservative Debt"},
        },
    ]

    mock_strat_service._financial_context.return_value = {
        "monthly_surplus": 25000.0,
        "annual_income": 1200000.0,
    }

    service = MultiGoalPlanningService(
        goal_repo=mock_goal_repo,
        strategy_repo=mock_strat_repo,
        strategy_service=mock_strat_service,
        goal_report_service=mock_report_service,
    )

    result = service.build_multi_goal_plan("pu-123")

    assert result.competing_resources_detected is True
    assert result.total_required_contribution == 30000.0
    assert result.total_allocated_contribution == 25000.0
    assert result.monthly_gap == 5000.0
    assert result.overall_funding_status == "surplus_shortfall"

    # Goal 1 (Retirement, high priority) is fully funded
    assert result.goals[0].goal_id == "goal-1"
    assert result.goals[0].allocated_monthly_contribution == 20000.0
    assert result.goals[0].funding_status == "fully_funded"

    # Goal 2 (Vacation, low priority) gets remaining surplus (5000)
    assert result.goals[1].goal_id == "goal-2"
    assert result.goals[1].allocated_monthly_contribution == 5000.0
    assert result.goals[1].funding_status == "partially_funded"
    assert result.goals[1].feasibility_status == "constrained"
