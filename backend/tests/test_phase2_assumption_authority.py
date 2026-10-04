from engines.goal.funding_gap import calculate_funding_return_assumption
from rules.assumptions import DEFAULT_FUNDING_RETURN_ASSUMPTION, normalize_annual_return
from services.basket_report_service import BasketReportService
from services.financial_plan_service import FinancialPlanService


def test_default_funding_return_assumption_is_canonical():
    assert DEFAULT_FUNDING_RETURN_ASSUMPTION == 0.08
    assert normalize_annual_return(None) == DEFAULT_FUNDING_RETURN_ASSUMPTION
    assert calculate_funding_return_assumption([]) == DEFAULT_FUNDING_RETURN_ASSUMPTION


def test_mapped_asset_return_is_weighted_by_allocated_value():
    result = calculate_funding_return_assumption([
        {"allocated_amount": 100000, "expected_return": 0.06},
        {"allocated_amount": 300000, "expected_return": 0.10},
    ])
    assert result == 0.09


def test_complete_plan_trajectory_uses_financial_assets_not_net_worth_percentage():
    trajectory = FinancialPlanService._build_family_cash_flow_trajectory(
        [{
            "goal_name": "Education",
            "target_date": "2030-06",
            "future_target": 100000,
            "projected_mapped_asset_value": 0,
            "funding_return_assumption": 0.08,
        }],
        total_monthly_allocated=1000,
        financial_state={"financial_assets": 500000, "net_worth": 2000000},
    )
    assert trajectory[0]["opening_balance"] == 500000.0


def test_basket_trajectory_uses_goal_assumptions():
    goals = [
        {
            "goal_name": "Education",
            "duration_years": 5,
            "future_target": 100000,
            "projected_mapped_asset_value": 100000,
            "required_monthly_contribution": 1000,
            "funding_return_assumption": 0.06,
        },
        {
            "goal_name": "Retirement",
            "duration_years": 10,
            "future_target": 200000,
            "projected_mapped_asset_value": 300000,
            "required_monthly_contribution": 2000,
            "funding_return_assumption": 0.10,
        },
    ]
    trajectory = BasketReportService._build_combined_cash_flow_trajectory(goals)
    # Weighted by mapped capital: (100k*6% + 300k*10%) / 400k = 9%.
    expected_growth = (400000 + (3000 * 12) / 2) * 0.09
    assert trajectory[0]["growth"] == round(expected_growth, 2)
