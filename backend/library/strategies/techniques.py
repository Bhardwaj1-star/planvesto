"""Backward-compatible technique catalog interface.

Canonical technique definitions live in techniques_canonical.py.
"""

from library.strategies.techniques_canonical import (
    CANONICAL_TECHNIQUES,
    get_canonical_technique,
    get_canonical_techniques,
)

TECHNIQUE_CATALOG = CANONICAL_TECHNIQUES


def get_all_techniques():
    return get_canonical_techniques()


def get_technique_by_id(technique_id: str):
    return get_canonical_technique(technique_id)
