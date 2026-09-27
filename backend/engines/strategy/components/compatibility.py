from __future__ import annotations

from itertools import combinations
from .definitions import register_default_components
from .registry import get_component


# Explicit compatibility policy. Unknown pairs are treated as compatible only
# when neither component declares a conflict; this keeps the library extensible.
CONFLICTING_COMPONENTS: set[frozenset[str]] = {
    frozenset(("component-credit", "component-preservation")),
}


def are_compatible(component_ids: tuple[str, ...]) -> bool:
    register_default_components()
    for left, right in combinations(component_ids, 2):
        if frozenset((left, right)) in CONFLICTING_COMPONENTS:
            return False
        left_component = get_component(left)
        right_component = get_component(right)
        if left_component is None or right_component is None:
            return False
        if not left_component.can_combine_with(right_component):
            return False
    return True


def incompatible_pairs(component_ids: tuple[str, ...]) -> list[tuple[str, str]]:
    register_default_components()
    result: list[tuple[str, str]] = []
    for left, right in combinations(component_ids, 2):
        if not are_compatible((left, right)):
            result.append((left, right))
    return result
