import pytest
from pydantic import ValidationError

from library.strategies.registry import get_active_strategies, get_strategy_by_id, validate_strategy_library
from models.strategy import StrategyDefinition, StrategyImplementationParamDef


def test_active_strategy_library_has_unique_ids():
    strategies = get_active_strategies()
    ids = [strategy.strategy_id for strategy in strategies]
    assert strategies
    assert len(ids) == len(set(ids))


def test_strategy_lookup_returns_active_strategy():
    strategy = get_strategy_by_id("strat-cap-preservation")
    assert strategy is not None
    assert strategy.active is True


def test_strategy_library_version_is_validated():
    strategy = get_strategy_by_id("strat-cap-preservation")
    assert strategy is not None
    validate_strategy_library([strategy])


def test_duplicate_implementation_parameters_are_rejected():
    with pytest.raises(ValidationError):
        StrategyDefinition(
            strategy_id="duplicate-param-test",
            name="Test",
            tagline="Test",
            description="Test",
            implementation_parameters=[
                StrategyImplementationParamDef(
                    name="allocation",
                    label="Allocation",
                    param_type="percentage",
                    description="Test",
                    default_value=50,
                    min_value=0,
                    max_value=100,
                ),
                StrategyImplementationParamDef(
                    name="allocation",
                    label="Allocation 2",
                    param_type="percentage",
                    description="Test",
                    default_value=50,
                    min_value=0,
                    max_value=100,
                ),
            ],
        )


def test_non_editable_parameter_is_supported():
    param = StrategyImplementationParamDef(
        name="fixed_rule",
        label="Fixed Rule",
        param_type="integer",
        description="System-controlled rule.",
        default_value=1,
        min_value=1,
        max_value=1,
        editable=False,
    )
    assert param.editable is False


def test_invalid_percentage_bounds_are_rejected():
    with pytest.raises(ValidationError):
        StrategyImplementationParamDef(
            name="allocation",
            label="Allocation",
            param_type="percentage",
            description="Test",
            default_value=50,
            min_value=0,
            max_value=120,
        )
