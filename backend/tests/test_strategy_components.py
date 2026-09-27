from engines.strategy.components.contracts import StrategyComponent
from engines.strategy.components.definitions import COMPONENT_DEFINITIONS, register_default_components
from engines.strategy.components.registry import get_active_components, get_component
from engines.strategy.applicability import filter_applicable_strategies
from models.defined_goal import DefinedGoal


def _goal(goal_type="Child Education", funding_status="Shortfall", duration_years=6.0):
    return DefinedGoal(
        goal_id="component-test-goal",
        planning_unit_id="component-test-unit",
        version=1,
        is_latest=True,
        goal_type=goal_type,
        goal_name="Component Test Goal",
        today_cost=1000000.0,
        inflation_rate=0.06,
        target_month=6,
        target_year=2032,
        duration_years=duration_years,
        future_target=1418519.0,
        priority="Critical",
        flexibility="Fixed",
        funding_gap=500000.0,
        funding_status=funding_status,
    )


def test_default_components_are_registered_and_have_unique_ids():
    register_default_components()
    components = get_active_components()
    ids = [component.component_id for component in components]
    assert ids
    assert len(ids) == len(set(ids))
    assert {"component-funding", "component-debt", "component-credit"}.issubset(ids)


def test_component_activation_uses_metadata_rules_and_unknown_data_is_not_invented():
    register_default_components()
    debt = get_component("component-debt")
    assert debt is not None
    assert debt.is_preferred({"total_liabilities": 500000, "emi_burden_monthly": {"value": 12000, "available": True}})
    assert not debt.is_preferred({"total_liabilities": 500000})
    assert not debt.is_preferred({"total_liabilities": 500000, "emi_burden_monthly": {"available": False}})


def test_component_combination_respects_declared_role_conflicts():
    left = StrategyComponent("a", "preservation", conflicts_with_roles=("growth",))
    right = StrategyComponent("b", "growth")
    assert left.can_combine_with(right) is False
    assert right.can_combine_with(left) is False


def test_component_inactivity_does_not_remove_parent_strategy_from_eligibility():
    strategies = filter_applicable_strategies(
        defined_goal=_goal(),
        financial_context={"total_liabilities": 500000},
    )
    ids = {strategy.strategy_id for strategy in strategies}
    assert "strat-debt-reduction" in ids


def test_component_definitions_cover_strategy_component_ids():
    defined_ids = {component.component_id for component in COMPONENT_DEFINITIONS}
    from library.strategies.registry import get_active_strategies
    referenced_ids = {
        component_id
        for strategy in get_active_strategies()
        for component_id in strategy.component_ids
    }
    assert referenced_ids <= defined_ids
