from .goal_matrix import GOAL_CASES


def test_goal_matrix_has_representative_goals():
    assert {case.name for case in GOAL_CASES} == {"retirement", "education", "home"}


def test_goal_cases_share_the_same_strategy_contract():
    required = {"goal_type", "duration_years", "flexibility", "priority", "funding_status"}
    for case in GOAL_CASES:
        assert required.issubset(case.__dict__)
        assert case.duration_years > 0
