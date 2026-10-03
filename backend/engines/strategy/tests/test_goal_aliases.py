from rules.goals import canonical_goal_type
from .goal_matrix import expected_goal_aliases


def test_supported_goal_aliases_are_canonical():
    for raw_name, canonical in expected_goal_aliases().items():
        assert canonical_goal_type(raw_name) == canonical


def test_user_facing_goal_names_are_canonicalized():
    assert _canonical_goal_type("Education") == "education"
    assert _canonical_goal_type("Dream Home") == "home"
