from services.goal_report_service import GoalReportService


def test_individual_goal_pdf_is_generated_from_complete_goal_report_contract(monkeypatch):
    service = GoalReportService()
    service.build_report = lambda planning_unit_id, strategy_run_id=None, strategy_version_id=None: {
        "goal_name": "My Vacation",
        "goal_type": "Travel",
        "goal_details": {},
        "mapped_assets": [],
        "strategy_run_id": strategy_run_id,
        "strategy": {
            "name": "Goal Funding",
            "objective": "Fund the vacation goal",
            "trade_offs": ["Higher contribution may reduce discretionary surplus."],
        },
        "recommendation": {
            "short_reasons": ["Funding fits the selected plan."],
            "complete_reasoning": "The selected funding path is based on the current goal gap and available surplus.",
        },
        "selected_strategy_id": "strat-goal-funding",
        "goal_calculation": {
            "today_cost": 100000.0,
            "inflation_rate": 0.06,
            "future_target": 133822.0,
            "funding_gap": 90000.0,
            "required_monthly_contribution": 1500.0,
            "target_month": 12,
            "target_year": 2031,
            "duration_years": 5,
            "funding_status": "Shortfall",
            "projected_mapped_asset_value": 43822.0,
            "funding_return_assumption": 0.08,
        },
        "goal_funding": {
            "feasibility_status": "constrained",
            "feasibility_reason": "Required contribution exceeds current surplus.",
            "available_monthly_surplus": 1000.0,
            "monthly_contribution_surplus_gap": 500.0,
            "required_monthly_contribution": 1500.0,
            "funding_gap": 90000.0,
            "funding_status": "Shortfall",
            "funding_return_assumption": 0.08,
            "funding_strategies": [
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
        },
        "goal_context": {
            "priority": "Important",
            "flexibility": "Flexible",
            "status": "Active",
        },
        "financial_state": {
            "annual_income": 1200000.0,
            "annual_expenses": 900000.0,
            "monthly_surplus": 25000.0,
            "assets": [],
            "liabilities": [],
            "net_worth": 500000.0,
        },
    }

    pdf = service.generate_pdf("pu-1", "run-1")

    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1000
