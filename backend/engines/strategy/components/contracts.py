from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class StrategyComponent:
    """Generic reusable strategic building block."""

    component_id: str
    role: str
    description: str = ""
    required_inputs: tuple[str, ...] = ()
    output_keys: tuple[str, ...] = ()
    compatible_roles: tuple[str, ...] = ()
    conflicts_with_roles: tuple[str, ...] = ()
    implementation_parameters: tuple[str, ...] = ()
    activation_rules: tuple[tuple[str, str, Any], ...] = ()

    def can_combine_with(self, other: "StrategyComponent") -> bool:
        if other.role in self.conflicts_with_roles:
            return False
        if self.role in other.conflicts_with_roles:
            return False
        return True

    def is_preferred(self, context: dict[str, Any]) -> bool:
        return all(_matches(context.get(key), operator, expected) for key, operator, expected in self.activation_rules)


@dataclass
class StrategyPlan:
    """Normalized intermediate contract consumed by later strategy stages."""
    goal_id: str
    primary_component_ids: list[str] = field(default_factory=list)
    supporting_component_ids: list[str] = field(default_factory=list)
    technique_ids: list[str] = field(default_factory=list)
    rationale: list[str] = field(default_factory=list)
    trade_offs: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    implementation: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


def _matches(actual: Any, operator: str, expected: Any) -> bool:
    if operator == "eq": return actual == expected
    if operator == "neq": return actual != expected
    if operator == "gte": return actual is not None and actual >= expected
    if operator == "lte": return actual is not None and actual <= expected
    if operator == "gt": return actual is not None and actual > expected
    if operator == "lt": return actual is not None and actual < expected
    if operator == "in": return actual in expected
    return False
