from unittest.mock import MagicMock

from engines.strategy.identity import canonical_architecture_id
from models.strategy import (
    Scenario,
    StrategyArchitecture,
    StrategyDefinition,
    StrategyRecommendation,
    StrategyRun,
)
from schemas.strategy import StrategySelectRequest
from services.strategy_service import StrategyService


def test_canonical_architecture_id_is_stable_and_composition_independent():
    goal_id = "18aa89c7-5372-4f5c-896c-a1edc1dc0ffd"
    primary = "strat-goal-funding"

    architecture_id = canonical_architecture_id(goal_id, primary)
    same_id_with_different_support = canonical_architecture_id(goal_id, primary)
    different_primary_id = canonical_architecture_id(goal_id, "strat-progressive-de-risking")

    assert architecture_id == same_id_with_different_support
    assert architecture_id != different_primary_id
    assert architecture_id.startswith("arch-")
    assert len(architecture_id) <= 100

    request = StrategySelectRequest(
        planning_unit_id="pu-1",
        strategy_run_id="run-1",
        selected_strategy_id=primary,
        selected_scenario_id="scenario-1",
        selected_architecture_id=architecture_id,
    )
    assert request.selected_architecture_id == architecture_id


def test_legacy_architecture_ids_are_normalized_without_schema_changes():
    goal_id = "18aa89c7-5372-4f5c-896c-a1edc1dc0ffd"
    primary = "strat-goal-funding"
    legacy_id = (
        f"arch-{goal_id}-{primary}-"
        "strat-progressive-de-risking-strat-capital-preservation-"
        "strat-debt-reduction-strat-credit-utilisation"
    )

    strategy = StrategyDefinition(
        strategy_id=primary,
        name="Goal Funding",
        tagline="Fund the goal",
        description="Direct goal funding strategy",
    )
    scenario = Scenario(
        scenario_id="scenario-1",
        strategy_id=primary,
        scenario_name="Baseline",
    )
    legacy_architecture = StrategyArchitecture(
        architecture_id=legacy_id,
        primary_strategy_id=primary,
        supporting_strategy_ids=[
            "strat-progressive-de-risking",
            "strat-capital-preservation",
            "strat-debt-reduction",
            "strat-credit-utilisation",
        ],
    )
    recommendation = StrategyRecommendation(
        recommended_strategy_id=primary,
        recommended_scenario_id=scenario.scenario_id,
        architecture=legacy_architecture,
        alternative_architecture_ids=[legacy_id],
    )
    run = StrategyRun(
        strategy_run_id="run-1",
        planning_unit_id="pu-1",
        goal_id=goal_id,
        defined_goal_id="dg-1",
        defined_goal_version=1,
        applicable_strategies=[strategy],
        scenarios=[scenario],
        recommendation=recommendation,
        architectures=[legacy_architecture],
        selected_strategy_id=primary,
        selected_scenario_id=scenario.scenario_id,
        selected_architecture=legacy_architecture,
    )

    service = StrategyService.__new__(StrategyService)
    service.strat_repo = MagicMock()
    service.goal_repo = MagicMock()

    normalized = service._ensure_run_architectures(run)
    expected_id = canonical_architecture_id(goal_id, primary)

    assert normalized.architectures[0].architecture_id == expected_id
    assert normalized.selected_architecture is not None
    assert normalized.selected_architecture.architecture_id == expected_id
    assert normalized.recommendation.architecture is not None
    assert normalized.recommendation.architecture.architecture_id == expected_id
    assert normalized.recommendation.alternative_architecture_ids == []
    service.strat_repo.update_architectures.assert_called_once()


def test_canonical_architecture_id_rejects_empty_identity_parts():
    try:
        canonical_architecture_id("", "strat-goal-funding")
    except ValueError as exc:
        assert "goal_id" in str(exc)
    else:
        raise AssertionError("Expected empty goal_id to be rejected")

    try:
        canonical_architecture_id("goal-1", "")
    except ValueError as exc:
        assert "primary_strategy_id" in str(exc)
    else:
        raise AssertionError("Expected empty primary_strategy_id to be rejected")
