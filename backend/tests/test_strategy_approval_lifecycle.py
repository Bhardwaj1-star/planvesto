from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from models.primary_strategy_state import PrimaryStrategyState
from models.strategy import StrategyRun, StrategyRecommendation
from models.strategy_approval import SuitabilityAssessment
from models.strategy_version import StrategyVersion
from services.strategy_approval_service import StrategyApprovalService


def _run(approval_status="selected"):
    return StrategyRun(
        strategy_run_id="run-1",
        planning_unit_id="pu-1",
        goal_id="goal-1",
        defined_goal_id="dg-1",
        defined_goal_version=1,
        selected_strategy_id="strat-cap-preservation",
        selected_scenario_id="scenario-1",
        selected_strategy_version_id="sv-1",
        selected_strategy_version=1,
        selected_implementation_parameters={},
        approval_status=approval_status,
        recommendation=StrategyRecommendation(
            recommended_strategy_id="strat-cap-preservation",
            recommended_scenario_id="scenario-1",
        ),
    )


def _version():
    return StrategyVersion(
        strategy_version_id="sv-1",
        planning_unit_id="pu-1",
        strategy_id="strat-cap-preservation",
        version=1,
        library_version="1.0",
        implementation_version="1.0",
        implementation_parameters={},
    )


@patch("services.strategy_approval_service.StrategyRepository")
@patch("services.strategy_approval_service.StrategyVersionRepository")
@patch("services.strategy_approval_service.StrategyApprovalRepository")
@patch("services.strategy_approval_service.PrimaryStrategyRepository")
def test_approved_run_cannot_be_approved_again(
    MockPrimaryRepo, MockApprovalRepo, MockVersionRepo, MockStrategyRepo
):
    MockStrategyRepo.return_value.get_run_by_id.return_value = _run("approved")

    svc = StrategyApprovalService()
    with pytest.raises(HTTPException) as exc_info:
        svc.approve_selected_strategy(
            "pu-1", "run-1", SuitabilityAssessment(status="Suitable")
        )

    assert exc_info.value.status_code == 409
    assert "already approved" in exc_info.value.detail
    MockApprovalRepo.return_value.save.assert_not_called()


@patch("services.strategy_approval_service.StrategyRepository")
@patch("services.strategy_approval_service.StrategyVersionRepository")
@patch("services.strategy_approval_service.StrategyApprovalRepository")
@patch("services.strategy_approval_service.PrimaryStrategyRepository")
def test_selected_version_can_be_approved_when_lifecycle_metadata_is_stale(
    MockPrimaryRepo, MockApprovalRepo, MockVersionRepo, MockStrategyRepo
):
    MockStrategyRepo.return_value.get_run_by_id.return_value = _run("not_selected")
    MockVersionRepo.return_value.get_version.return_value = _version()
    MockApprovalRepo.return_value.save.return_value = MagicMock(approval_snapshot_id="approval-1")
    MockPrimaryRepo.return_value.get_current.return_value = None

    svc = StrategyApprovalService()
    svc.approve_selected_strategy(
        "pu-1", "run-1", SuitabilityAssessment(status="Suitable")
    )

    MockApprovalRepo.return_value.save.assert_called_once()
    MockStrategyRepo.return_value.update_approval.assert_called_once_with(
        "pu-1", "run-1", "approve"
    )


@patch("services.strategy_approval_service.StrategyRepository")
@patch("services.strategy_approval_service.StrategyVersionRepository")
@patch("services.strategy_approval_service.StrategyApprovalRepository")
@patch("services.strategy_approval_service.PrimaryStrategyRepository")
def test_replacing_primary_records_superseded_transition(
    MockPrimaryRepo, MockApprovalRepo, MockVersionRepo, MockStrategyRepo
):
    MockStrategyRepo.return_value.get_run_by_id.return_value = _run("selected")
    MockVersionRepo.return_value.get_version.return_value = _version()

    current = PrimaryStrategyState(
        planning_unit_id="pu-1",
        strategy_id="strat-old",
        strategy_version_id="sv-old",
        approval_snapshot_id="approval-old",
        previous_strategy_id=None,
        previous_strategy_version_id=None,
    )
    MockPrimaryRepo.return_value.get_current.return_value = current

    saved_snapshot = MagicMock()
    saved_snapshot.approval_snapshot_id = "approval-new"
    MockApprovalRepo.return_value.save.return_value = saved_snapshot

    svc = StrategyApprovalService()
    svc.approve_selected_strategy(
        "pu-1",
        "run-1",
        SuitabilityAssessment(status="Suitable"),
        make_primary=True,
        primary_transition_decision="archive_previous",
        pending_action_disposition="cancel",
    )

    transition = MockPrimaryRepo.return_value.set_current.call_args.args[0]
    assert transition.previous_strategy_id == "strat-old"
    assert transition.previous_strategy_version_id == "sv-old"
    assert transition.transition_metadata["previous_primary_transition"] == "superseded"
    MockPrimaryRepo.return_value.record_transition.assert_called_once_with(
        transition, "archive_previous"
    )
    MockStrategyRepo.return_value.update_approval.assert_called_once_with(
        "pu-1", "run-1", "approve"
    )
