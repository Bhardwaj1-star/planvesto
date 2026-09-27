from .goal_matrix import GOAL_CASES


def test_strategy_engine_contract_is_goal_agnostic():
    """The matrix defines the minimum context every goal must provide.

    This deliberately tests the contract rather than hard-coding a winning
    strategy for any goal. Strategy selection remains data-driven by the
    engine/library.
    """
    for case in GOAL_CASES:
        assert case.goal_type
        assert case.duration_years > 0
        assert case.flexibility in {"Flexible", "Fixed"}
        assert case.priority in {"High", "Medium", "Low"}
        assert case.funding_status in {"Shortfall", "On Track", "Overfunded"}
