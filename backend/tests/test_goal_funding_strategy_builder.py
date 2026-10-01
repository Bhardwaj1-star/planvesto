from datetime import date

from engines.strategy.scenario import generate_baseline_scenarios
from models.defined_goal import DefinedGoal
from models.strategy import StrategyDefinition


def test_goal_funding_strategy_becomes_strategy_builder_variants():
    goal = DefinedGoal(
        goal_id="g1", planning_unit_id="pu1", goal_type="Education", goal_name="Education",
        today_cost=1000000, inflation_rate=0.06, target_month=1, target_year=2031,
        duration_years=5, future_target=1338225.58, priority="Critical", flexibility="Fixed",
        mapped_assets=[], projected_mapped_asset_value=0, funding_gap=1338225.58,
        funding_status="Shortfall", required_monthly_contribution=17800,
        funding_return_assumption=0.08, available_monthly_surplus=25000,
    )
    strategy = StrategyDefinition(
        strategy_id="strat-goal-funding", name="Goal Funding", tagline="Fund", description="Fund",
        applicable_goal_types=["Education"], implementation_parameters=[]
    )
    scenarios = generate_baseline_scenarios(strategy, goal)
    ids = {s.funding_strategy_id for s in scenarios}
    assert {"sip", "lumpsum", "lumpsum_plus_sip", "step_up_sip", "lumpsum_plus_step_up_sip"} <= ids
    assert all(s.strategy_id == "strat-goal-funding" for s in scenarios)
