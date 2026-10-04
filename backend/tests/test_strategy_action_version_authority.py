from types import SimpleNamespace
from unittest.mock import MagicMock

from models.strategy import StrategyArchitecture
from models.strategy_version import StrategyVersion
from services.strategy_action_generator import StrategyActionGenerator


def test_action_generation_uses_version_architecture_and_current_selection(monkeypatch):
    version = StrategyVersion(
        strategy_version_id="sv-1",
        planning_unit_id="pu-1",
        strategy_id="strat-goal-funding",
        version=1,
        library_version="1.0",
        implementation_version="1.0",
        goal_id="goal-1",
        defined_goal_id="dg-1",
        defined_goal_version=1,
        source_strategy_run_id="run-1",
        architecture=StrategyArchitecture(
            architecture_id="arch-version",
            primary_strategy_id="strat-goal-funding",
            supporting_strategy_ids=[],
            technique_ids=[],
        ),
        decision_snapshot={
            "recommendation": {"recommended_strategy_id": "strat-goal-funding"},
        },
    )
    action_repository = MagicMock()
    action_repository.is_strategy_version_approved.return_value = True
    action_repository.list_actions_for_strategy_version.return_value = []
    action_repository.save_action.side_effect = lambda action: action

    strategy_repository = MagicMock()
    strategy_repository.get_selected_strategy_version_id.return_value = "sv-1"
    version_repository = MagicMock()
    version_repository.get_by_id.return_value = version

    monkeypatch.setattr(
        "services.strategy_action_generator.StrategyRepository",
        lambda: strategy_repository,
    )
    monkeypatch.setattr(
        "services.strategy_action_generator.StrategyVersionRepository",
        lambda _client: version_repository,
    )
    monkeypatch.setattr(
        "services.strategy_action_generator.FinancialStateSnapshotRepository",
        lambda: MagicMock(),
    )

    class CurrentFinancialStateService:
        def __init__(self, **_kwargs):
            pass

        def current(self, *_args):
            return SimpleNamespace(model_dump=lambda **_kwargs: {"planning_unit_id": "pu-1"})

    monkeypatch.setattr(
        "services.strategy_action_generator.FinancialStateService",
        CurrentFinancialStateService,
    )

    actions = StrategyActionGenerator(action_repository).generate("pu-1", "sv-1")

    assert actions
    assert all(
        action.planned_impact["architecture_id"] == "arch-version"
        for action in actions
    )
    strategy_repository.get_selected_strategy_version_id.assert_called_once_with(
        "pu-1", "goal-1"
    )
    version_repository.get_by_id.assert_called_once_with("pu-1", "sv-1")


def test_action_generation_rejects_non_current_strategy_version(monkeypatch):
    version = StrategyVersion(
        strategy_version_id="sv-old",
        planning_unit_id="pu-1",
        strategy_id="strat-goal-funding",
        version=1,
        library_version="1.0",
        implementation_version="1.0",
        goal_id="goal-1",
        defined_goal_id="dg-1",
        defined_goal_version=1,
        source_strategy_run_id="run-old",
        architecture=StrategyArchitecture(
            architecture_id="arch-old",
            primary_strategy_id="strat-goal-funding",
        ),
        decision_snapshot={
            "recommendation": {"recommended_strategy_id": "strat-goal-funding"},
        },
    )
    action_repository = MagicMock()
    action_repository.is_strategy_version_approved.return_value = True
    strategy_repository = MagicMock()
    strategy_repository.get_selected_strategy_version_id.return_value = "sv-current"
    version_repository = MagicMock()
    version_repository.get_by_id.return_value = version
    monkeypatch.setattr(
        "services.strategy_action_generator.StrategyRepository",
        lambda: strategy_repository,
    )
    monkeypatch.setattr(
        "services.strategy_action_generator.StrategyVersionRepository",
        lambda _client: version_repository,
    )

    try:
        StrategyActionGenerator(action_repository).generate("pu-1", "sv-old")
    except ValueError as error:
        assert "current StrategyVersion" in str(error)
    else:
        raise AssertionError("Action generation should reject a non-current version")
