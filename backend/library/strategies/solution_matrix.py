"""Canonical Strategy Solution Matrix.

Strategy = responsibility / architecture.
Solution = concrete implementation path inside that strategy.
Goal applicability = where that responsibility may participate.

The matrix reuses canonical strategy, variant and technique IDs. It does not
calculate investor-specific values; runtime engines remain responsible for that.
"""

from dataclasses import dataclass

from library.strategies.canonical import get_canonical_strategy
from library.strategies.variants import get_canonical_strategy_variants
from library.strategies.techniques_canonical import get_canonical_technique
from rules.goals import canonical_goal_type


@dataclass(frozen=True)
class StrategySolutionDefinition:
    solution_id: str
    strategy_id: str
    name: str
    responsibility: str
    goal_types: tuple[str, ...]
    technique_ids: tuple[str, ...] = ()
    variant_id: str | None = None
    role: str = "primary"
    description: str = ""
    version: str = "1.0"


def _goal_funding_solutions() -> list[StrategySolutionDefinition]:
    strategy_id = "strat-goal-funding"
    strategy = get_canonical_strategy(strategy_id)
    assert strategy is not None

    return [
        StrategySolutionDefinition(
            solution_id=f"solution-{strategy_id}-{variant.variant_id}",
            strategy_id=strategy_id,
            name=variant.name,
            responsibility=strategy.strategic_objective,
            goal_types=tuple(strategy.applicable_goal_types),
            variant_id=variant.variant_id,
            role="primary",
            description=variant.description,
        )
        for variant in get_canonical_strategy_variants(strategy_id)
    ]


def _technique_solutions(strategy_id: str) -> list[StrategySolutionDefinition]:
    strategy = get_canonical_strategy(strategy_id)
    assert strategy is not None

    solutions = []
    for technique_id in strategy.technique_ids:
        technique = get_canonical_technique(technique_id)
        if technique is None:
            raise ValueError(
                f"Strategy {strategy_id} references unknown canonical technique: {technique_id}"
            )
        solutions.append(
            StrategySolutionDefinition(
                solution_id=f"solution-{strategy_id}-{technique_id}",
                strategy_id=strategy_id,
                name=technique.name,
                responsibility=strategy.strategic_objective,
                goal_types=tuple(strategy.applicable_goal_types),
                technique_ids=(technique_id,),
                role="supporting",
                description=technique.description,
            )
        )
    return solutions


CANONICAL_STRATEGY_SOLUTIONS: tuple[StrategySolutionDefinition, ...] = tuple(
    _goal_funding_solutions()
    + _technique_solutions("strat-progressive-de-risking")
    + _technique_solutions("strat-capital-preservation")
    + _technique_solutions("strat-debt-reduction")
    + _technique_solutions("strat-credit-utilisation")
)


def get_strategy_solutions(
    strategy_id: str | None = None,
    goal_type: str | None = None,
) -> list[StrategySolutionDefinition]:
    solutions = list(CANONICAL_STRATEGY_SOLUTIONS)
    if strategy_id is not None:
        solutions = [s for s in solutions if s.strategy_id == strategy_id]
    if goal_type is not None:
        canonical = canonical_goal_type(goal_type)
        solutions = [
            s for s in solutions
            if canonical in {canonical_goal_type(value) for value in s.goal_types}
        ]
    return solutions


def get_strategy_solution(solution_id: str) -> StrategySolutionDefinition | None:
    return next((s for s in CANONICAL_STRATEGY_SOLUTIONS if s.solution_id == solution_id), None)


def validate_strategy_solution_matrix() -> None:
    ids = [s.solution_id for s in CANONICAL_STRATEGY_SOLUTIONS]
    if len(ids) != len(set(ids)):
        raise ValueError("Canonical Strategy Solution Matrix contains duplicate solution_id values")

    for solution in CANONICAL_STRATEGY_SOLUTIONS:
        if get_canonical_strategy(solution.strategy_id) is None:
            raise ValueError(f"Unknown strategy: {solution.strategy_id}")
        if not solution.goal_types:
            raise ValueError(f"Solution {solution.solution_id} has no applicable goal types")
        if solution.variant_id is not None:
            variant = next(
                (
                    v for v in get_canonical_strategy_variants(solution.strategy_id)
                    if v.variant_id == solution.variant_id
                ),
                None,
            )
            if variant is None:
                raise ValueError(f"Solution {solution.solution_id} references an invalid variant")
        for technique_id in solution.technique_ids:
            if get_canonical_technique(technique_id) is None:
                raise ValueError(
                    f"Solution {solution.solution_id} references an unknown technique"
                )


validate_strategy_solution_matrix()
