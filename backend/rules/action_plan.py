"""Authoritative action-plan generation rules and item specifications."""
from __future__ import annotations

from typing import Any


def build_action_specs(
    primary_strategy: Any,
    supporting_strategies: list[Any],
    techniques: list[Any],
) -> list[tuple[str, str, str]]:
    """Build deterministic action plan item specifications (title, description, priority).

    Rule:
    - Primary strategy generates a 'high' priority action describing execution of the core mechanism.
    - Each supporting strategy generates a 'medium' priority action describing its component objective.
    - Each implementation technique generates a 'medium' priority action describing its purpose.
    """
    specs: list[tuple[str, str, str]] = []

    if primary_strategy is not None:
        specs.append((
            f"Implement {primary_strategy.name}",
            f"Execute the approved {primary_strategy.name} strategy architecture for this goal. Core mechanism: {primary_strategy.core_mechanism}",
            "high",
        ))

    for supporting in supporting_strategies:
        specs.append((
            f"Implement supporting strategy: {supporting.name}",
            f"Apply the supporting {supporting.name} component defined by the approved strategy architecture. Strategic objective: {supporting.strategic_objective}",
            "medium",
        ))

    for technique in techniques:
        specs.append((
            f"Apply {technique.name}",
            f"Apply this implementation technique as part of the approved strategy: {technique.description} Purpose: {technique.purpose}",
            "medium",
        ))

    return specs
