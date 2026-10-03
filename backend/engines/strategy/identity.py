"""Canonical identity helpers for Strategy Builder architectures.

Architecture identity is based only on the owning goal and primary strategy.
Composition (supporting strategies, techniques, and solutions) is data on the
architecture, not part of its identity.
"""

from uuid import NAMESPACE_URL, uuid5


def canonical_architecture_id(goal_id: str, primary_strategy_id: str) -> str:
    """Return a deterministic, composition-independent architecture identifier."""
    if not goal_id.strip():
        raise ValueError("goal_id cannot be empty")
    if not primary_strategy_id.strip():
        raise ValueError("primary_strategy_id cannot be empty")

    identity_key = (
        f"planvesto:strategy-architecture:{goal_id.strip()}:{primary_strategy_id.strip()}"
    )
    return f"arch-{uuid5(NAMESPACE_URL, identity_key)}"
