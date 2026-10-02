"""Backward-compatible Strategy Library catalog interface.

Canonical strategy definitions live in canonical.py. This module preserves
existing imports while making the canonical registry the source of truth.
"""

from library.strategies.canonical import (
    CANONICAL_STRATEGIES,
    get_canonical_strategy,
    get_canonical_strategies,
)

STRATEGY_CATALOG = CANONICAL_STRATEGIES


def get_all_strategies():
    return get_canonical_strategies()
