from types import SimpleNamespace
from unittest.mock import MagicMock

from services.financial_plan_service import FinancialPlanService
from engines.orchestration.models import GoalResolution, MultiGoalPlanResult


def test_complete_financial_plan_contains_goal_calculation_and_funding_options():
    goal_repo = MagicMock()
    multi_goal = MagicMock()

    defined_goal = SimpleNamespace(
        today_cost=100000.0,
        future_target=133822.0,
        funding_gap=90000.0,
        projected_mapped_asset_value=43822.0,
        available_monthly_surplus=25000.0,
        funding_strategies=[{"strategy_id": "sip", "status": "feasible"}],
    )
    goal_repo.get_latest_defined_goal.return_value = defined_goal

    multi_goal.build_multi_goal_plan.return_value = MultiGoalPlanResult(
        planning_unit_id="pu-1",
        total_available_surplus=25000.0,
        total_required_contribution=12000.0,
        total_allocated_contribution=12000.0,
        overall_funding_status="within_surplus",
        goals=[
            GoalResolution(
                goal_id="g1",
                goal_name="Vacation",
                goal_type="Travel",
                client_priority="medium",
                resolved_priority="medium",
                target_date="2031-12",
                required_monthly_contribution=12000.0,
                allocated_monthly_contribution=12000.0,
                funding_status="fully_funded",
                feasibility_status="feasible",
                recommended_strategy_id="strat-goal-funding",
                recommended_strategy_name="Goal Funding",
            )
        ],
    )

    strat_repo = MagicMock()
    strat_repo.get_latest_run.return_value = None
    service = FinancialPlanService(
        goal_repo=goal_repo,
        strategy_repo=strat_repo,
        multi_goal_service=multi_goal,
    )
    result = service.build_plan("pu-1")

    row = result["goals"][0]
    assert row["today_cost"] == 100000.0
    assert row["future_target"] == 133822.0
    assert row["funding_gap"] == 90000.0
    assert row["projected_mapped_asset_value"] == 43822.0
    assert row["available_monthly_surplus"] == 25000.0
    assert row["funding_strategies"] == [{"strategy_id": "sip", "status": "feasible"}]


def test_goal_plan_summary_preserves_strategy_and_funding_data():
    goal_repo = MagicMock()
    multi_goal = MagicMock()
    strategy_repo = MagicMock()

    goal_repo.get_latest_defined_goal.return_value = SimpleNamespace(
        today_cost=100000.0,
        future_target=133822.0,
        funding_gap=90000.0,
        projected_mapped_asset_value=43822.0,
        available_monthly_surplus=25000.0,
        funding_strategies=[{"strategy_id": "sip", "status": "feasible"}],
    )
    strategy_repo.get_latest_run.return_value = SimpleNamespace(strategy_run_id="run-1")
    multi_goal.build_multi_goal_plan.return_value = MultiGoalPlanResult(
        planning_unit_id="pu-1",
        total_available_surplus=25000.0,
        total_required_contribution=12000.0,
        total_allocated_contribution=12000.0,
        overall_funding_status="within_surplus",
        goals=[GoalResolution(
            goal_id="g1", goal_name="Vacation", goal_type="Travel",
            client_priority="medium", resolved_priority="medium",
            target_date="2031-12", required_monthly_contribution=12000.0,
            allocated_monthly_contribution=12000.0,
            funding_status="fully_funded", feasibility_status="feasible",
            recommended_strategy_id="strat-goal-funding",
            recommended_strategy_name="Goal Funding",
        )],
    )

    service = FinancialPlanService(
        goal_repo=goal_repo,
        strategy_repo=strategy_repo,
        multi_goal_service=multi_goal,
    )
    result = service.build_plan("pu-1")
    plan = result["goal_plans"][0]

    assert plan["strategy_run_id"] == "run-1"
    assert plan["strategy_id"] == "strat-goal-funding"
    assert plan["funding_gap"] == 90000.0
    assert plan["funding_strategies"] == [{"strategy_id": "sip", "status": "feasible"}]
