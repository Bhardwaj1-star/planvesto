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
