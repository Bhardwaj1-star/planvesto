from library.strategies.solution_matrix import (
    CANONICAL_STRATEGY_SOLUTIONS,
    get_strategy_solutions,
)


def test_goal_funding_exposes_all_canonical_variants():
    solutions = get_strategy_solutions("strat-goal-funding")
    assert {s.variant_id for s in solutions} == {
        "existing_assets",
        "sip",
        "lumpsum",
        "lumpsum_plus_sip",
        "step_up_sip",
        "lumpsum_plus_step_up_sip",
    }


def test_progressive_de_risking_exposes_library_techniques():
    solutions = get_strategy_solutions("strat-progressive-de-risking")
    assert {s.technique_ids[0] for s in solutions} == {
        "tech-glide-path",
        "tech-bucketing",
        "tech-cashflow-matching",
    }


def test_solution_goal_scope_matches_strategy_library():
    for solution in CANONICAL_STRATEGY_SOLUTIONS:
        assert solution.goal_types
        assert solution.strategy_id
