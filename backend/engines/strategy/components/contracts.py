from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class StrategyComponent:
    """Generic reusable strategic building block.

    Components are goal-agnostic. A goal-specific strategy is composed from
    applicable components rather than implemented as a separate engine.
    """

    component_id: str
    role: str
    description: str = ""
    required_inputs: tuple[str, ...] = ()
    output_keys: tuple[str, ...] = ()
    compatible_roles: tuple[str, ...] = ()
    conflicts_with_roles: tuple[str, ...] = ()
    implementation_parameters: tuple[str, ...] = ()

    def can_combine_with(self, other: "StrategyComponent") -> bool:
        if other.role in self.conflicts_with_roles:
            return False
        if self.role in other.conflicts_with_roles:
            return False
        return True


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
