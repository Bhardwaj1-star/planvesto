from unittest.mock import MagicMock
from engines.orchestration.models import GoalResolution, MultiGoalPlanResult
from services.financial_plan_service import FinancialPlanService


def test_priority_rank_orders_known_priorities():
    service = FinancialPlanService.__new__(FinancialPlanService)
    assert service._priority_rank("critical") < service._priority_rank("high") < service._priority_rank("medium") < service._priority_rank("low")
    assert service._priority_rank("unknown") > service._priority_rank("low")


def test_goal_row_uses_recommendation_when_strategy_not_selected():
    service = FinancialPlanService.__new__(FinancialPlanService)
    report = {
        "goal_id": "goal-1",
        "goal_name": "Retirement",
        "goal_type": "retirement",
        "goal_calculation": {
            "future_target": 30000000,
            "funding_gap": 5000000,
            "required_monthly_contribution": 20000,
            "target_month": 4,
            "target_year": 2051,
            "today_cost": 10000000,
            "funding_status": "underfunded",
        },
        "recommendation": {
            "recommended_strategy_id": "progressive_de_risking",
            "complete_reasoning": "Use growth early and reduce risk near retirement.",
            "short_reasons": ["Long horizon"],
            "feasibility_status": "feasible",
        },
        "selected_strategy_id": None,
        "strategy": {"name": "Progressive De-risking"},
    }
    row = service._goal_row(report)
    assert row["strategy_id"] == "progressive_de_risking"
    assert row["required_monthly_contribution"] == 20000
    assert row["target_date"] == "2051-04"


def test_build_plan_consolidates_multi_goal_results():
    mock_goal_repo = MagicMock()
    mock_strat_repo = MagicMock()
    mock_multi_service = MagicMock()

    mock_goal_repo.list_goals.return_value = [{"goal_id": "g1"}, {"goal_id": "g2"}]
    mock_strat_repo.get_latest_run.return_value = MagicMock(strategy_run_id="run-123")

    mock_multi_service.build_multi_goal_plan.return_value = MultiGoalPlanResult(
        planning_unit_id="pu-100",
        financial_state={"annual_income": 1200000.0, "annual_expenses": 600000.0, "net_worth": 3000000.0},
        total_available_surplus=50000.0,
        total_required_contribution=40000.0,
        total_allocated_contribution=40000.0,
        monthly_gap=-10000.0,
        overall_funding_status="within_surplus",
        goals=[
            GoalResolution(
                goal_id="g1",
                goal_name="Retirement",
                goal_type="retirement",
                client_priority="critical",
                resolved_priority="critical",
                required_monthly_contribution=25000.0,
                allocated_monthly_contribution=25000.0,
                funding_status="fully_funded",
                recommended_strategy_id="progressive_de_risking",
                recommended_strategy_name="Progressive De-risking",
            ),
            GoalResolution(
                goal_id="g2",
                goal_name="Child Education",
                goal_type="education",
                client_priority="high",
                resolved_priority="high",
                required_monthly_contribution=15000.0,
                allocated_monthly_contribution=15000.0,
                funding_status="fully_funded",
                recommended_strategy_id="growth_equity",
                recommended_strategy_name="Growth Equity",
            ),
        ],
        competing_resources_detected=False,
        trade_offs=[],
        action_plan=[{"sequence": 1, "action": "Fund Retirement"}, {"sequence": 2, "action": "Fund Education"}],
        planning_notes=["Clean consolidated plan."],
    )

    service = FinancialPlanService(
        goal_repo=mock_goal_repo,
        strategy_repo=mock_strat_repo,
        multi_goal_service=mock_multi_service,
    )

    plan = service.build_plan("pu-100")

    assert plan["report_type"] == "complete_financial_plan"
    assert plan["planning_unit_id"] == "pu-100"
    assert plan["goal_count"] == 2
    assert plan["consolidated_funding"]["required_monthly_contribution"] == 40000.0
    assert plan["consolidated_funding"]["allocated_monthly_contribution"] == 40000.0
    assert plan["consolidated_funding"]["funding_status"] == "within_surplus"
    assert len(plan["actions"]) == 2


def test_generate_pdf_produces_bytes():
    mock_goal_repo = MagicMock()
    mock_strat_repo = MagicMock()
    mock_multi_service = MagicMock()

    mock_goal_repo.list_goals.return_value = [{"goal_id": "g1"}]
    mock_strat_repo.get_latest_run.return_value = MagicMock(strategy_run_id="run-1")

    mock_multi_service.build_multi_goal_plan.return_value = MultiGoalPlanResult(
        planning_unit_id="pu-200",
        financial_state={"annual_income": 1000000.0, "annual_expenses": 500000.0},
        total_available_surplus=40000.0,
        total_required_contribution=20000.0,
        total_allocated_contribution=20000.0,
        monthly_gap=-20000.0,
        overall_funding_status="within_surplus",
        goals=[
            GoalResolution(
                goal_id="g1",
                goal_name="Emergency Reserve",
                goal_type="emergency_fund",
                client_priority="critical",
                resolved_priority="critical",
                required_monthly_contribution=20000.0,
                allocated_monthly_contribution=20000.0,
                funding_status="fully_funded",
            )
        ],
        action_plan=[{"sequence": 1, "action": "Fund Emergency Reserve", "monthly_contribution": 20000.0}],
        planning_notes=["Emergency reserve priority."],
    )

    service = FinancialPlanService(
        goal_repo=mock_goal_repo,
        strategy_repo=mock_strat_repo,
        multi_goal_service=mock_multi_service,
    )

    pdf_bytes = service.generate_pdf("pu-200")
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")


def test_generate_pdf_with_system_priority_override():
    mock_goal_repo = MagicMock()
    mock_strat_repo = MagicMock()
    mock_multi_service = MagicMock()

    mock_goal_repo.list_goals.return_value = [{"goal_id": "g1"}, {"goal_id": "g2"}]
    mock_strat_repo.get_latest_run.return_value = MagicMock(strategy_run_id="run-1")

    mock_multi_service.build_multi_goal_plan.return_value = MultiGoalPlanResult(
        planning_unit_id="pu-300",
        financial_state={"annual_income": 1200000.0, "annual_expenses": 600000.0},
        total_available_surplus=30000.0,
        total_required_contribution=40000.0,
        total_allocated_contribution=30000.0,
        monthly_gap=10000.0,
        overall_funding_status="surplus_shortfall",
        goals=[
            GoalResolution(
                goal_id="g1",
                goal_name="Retirement Corpus",
                goal_type="retirement",
                client_priority="medium",
                resolved_priority="high",
                required_monthly_contribution=25000.0,
                allocated_monthly_contribution=25000.0,
                funding_status="fully_funded",
                override_applied=True,
                override_reason="Prioritized to ensure baseline retirement security ahead of luxury travel.",
            ),
            GoalResolution(
                goal_id="g2",
                goal_name="Luxury Trip",
                goal_type="travel",
                client_priority="critical",
                resolved_priority="low",
                required_monthly_contribution=15000.0,
                allocated_monthly_contribution=5000.0,
                shortfall=10000.0,
                funding_status="partially_funded",
                feasibility_status="constrained",
                override_applied=True,
                override_reason="Deprioritized because discretionary travel cannot compromise retirement.",
            ),
        ],
        trade_offs=["Goal 'Luxury Trip' is partially funded (5000.00 of 15000.00/mo)."],
        action_plan=[
            {"sequence": 1, "action": "Fund Retirement", "monthly_contribution": 25000.0},
            {"sequence": 2, "action": "Partially fund Luxury Trip", "monthly_contribution": 5000.0},
        ],
        planning_notes=["One or more goals have system-resolved priorities."],
    )

    service = FinancialPlanService(
        goal_repo=mock_goal_repo,
        strategy_repo=mock_strat_repo,
        multi_goal_service=mock_multi_service,
    )

    pdf_bytes = service.generate_pdf("pu-300")
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 1000

