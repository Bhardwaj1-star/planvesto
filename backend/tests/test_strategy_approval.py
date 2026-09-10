import pytest

from models.strategy_approval import StrategyApprovalSnapshot, SuitabilityAssessment


def test_suitable_requires_no_acknowledgement():
    snapshot = StrategyApprovalSnapshot(
        planning_unit_id="pu-1",
        strategy_id="strat-1",
        strategy_version_id="version-1",
        strategy_version=1,
        goal_id="goal-1",
        defined_goal_id="defined-1",
        defined_goal_version=1,
        strategy_snapshot={"implementation_parameters": {"allocation": 60}},
        suitability=SuitabilityAssessment(status="Suitable"),
    )
    assert snapshot.acknowledgement_type == "none"


def test_needs_attention_requires_acknowledgement():
    with pytest.raises(ValueError, match="Needs Attention requires"):
        StrategyApprovalSnapshot(
            planning_unit_id="pu-1",
            strategy_id="strat-1",
            strategy_version_id="version-1",
            strategy_version=1,
            goal_id="goal-1",
            defined_goal_id="defined-1",
            defined_goal_version=1,
            strategy_snapshot={},
            suitability=SuitabilityAssessment(status="Needs Attention"),
        )


def test_unsuitable_requires_full_acknowledgement():
    with pytest.raises(ValueError, match="Unsuitable requires"):
        StrategyApprovalSnapshot(
            planning_unit_id="pu-1",
            strategy_id="strat-1",
            strategy_version_id="version-1",
            strategy_version=1,
            goal_id="goal-1",
            defined_goal_id="defined-1",
            defined_goal_version=1,
            strategy_snapshot={},
            suitability=SuitabilityAssessment(status="Unsuitable"),
        )


def test_acknowledged_needs_attention_snapshot_is_valid():
    snapshot = StrategyApprovalSnapshot(
        planning_unit_id="pu-1",
        strategy_id="strat-1",
        strategy_version_id="version-1",
        strategy_version=1,
        goal_id="goal-1",
        defined_goal_id="defined-1",
        defined_goal_version=1,
        strategy_snapshot={},
        suitability=SuitabilityAssessment(status="Needs Attention"),
        acknowledgement_type="needs_attention",
        acknowledgement_text="I reviewed the identified conditions and want to proceed.",
        acknowledged_at="2026-09-10T00:00:00+00:00",
    )
    assert snapshot.acknowledgement_type == "needs_attention"
