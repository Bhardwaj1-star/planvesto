from engines.strategy.scenario import generate_what_if_scenarios
from models.strategy import StrategyDefinition


class Goal:
    today_cost = 1000000
    inflation_rate = 0.06
    future_target = 1700000
    projected_mapped_asset_value = 500000
    funding_gap = 1200000
    duration_years = 5
    required_monthly_contribution = 15000
    funding_return_assumption = 0.08
    funding_status = "Shortfall"
    mapped_assets = []
    available_monthly_surplus = 30000


def test_generated_what_ifs_cover_core_decision_dimensions():
    strategy = StrategyDefinition(
        strategy_id="strat-goal-funding",
        name="Goal Funding",
        tagline="Fund the goal",
        description="Funding architecture",
        applicable_goal_types=["Dream Home"],
        strategic_objective="Fund the defined goal.",
    )
    scenarios = generate_what_if_scenarios(strategy, Goal())
    names = {s.scenario_name for s in scenarios}
    assert "What-if: Monthly contribution +10%" in names
    assert "What-if: Goal date +1 year(s)" in names
    assert "What-if: Target reduced by 10%" in names
    assert "What-if: Annual contribution step-up 10%" in names
    assert all(s.scenario_type == "custom" for s in scenarios)
    assert all(s.is_investor_modified is False for s in scenarios)


def test_what_ifs_do_not_change_strategy_selection_inputs():
    strategy = StrategyDefinition(
        strategy_id="strat-goal-funding",
        name="Goal Funding",
        tagline="Fund the goal",
        description="Funding architecture",
        applicable_goal_types=["Dream Home"],
    )
    scenarios = generate_what_if_scenarios(strategy, Goal())
    assert scenarios
    assert all(s.strategy_id == "strat-goal-funding" for s in scenarios)
