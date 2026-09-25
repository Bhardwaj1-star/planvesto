from engines.profile.strategy_context import to_strategy_context


def test_strategy_context_is_read_only_projection():
    profile = {
        "profile_run_id": "run-1",
        "version": 3,
        "engine_version": "profile-engine-v4",
        "constraints": [{
            "key": "liquidity_priority", "value": "high", "unit": None,
            "kind": "soft", "confidence": 0.5, "priority_rank": 1,
            "source": "declared_constraint", "evidence": ["private detail"],
        }],
        "priorities": [{"key": "liquidity_priority", "rank": 1}],
        "conflicts": [],
    }
    context = to_strategy_context(profile)
    assert context["profile_run_id"] == "run-1"
    assert context["constraints"][0]["key"] == "liquidity_priority"
    assert "evidence" not in context["constraints"][0]
    assert context["priorities"] == [{"key": "liquidity_priority", "rank": 1}]


def test_missing_profile_sections_are_safe():
    context = to_strategy_context({})
    assert context == {
        "profile_run_id": None,
        "profile_version": None,
        "engine_version": None,
        "constraints": [],
        "priorities": [],
        "conflicts": [],
    }
