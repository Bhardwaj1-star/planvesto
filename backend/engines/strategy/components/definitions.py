"""Backward-compatible component definitions interface.

Canonical component definitions live in library.strategies.components.
"""

from library.strategies.components import CANONICAL_COMPONENTS
from .registry import get_active_components, register_component

COMPONENT_DEFINITIONS = CANONICAL_COMPONENTS


def register_default_components() -> None:
    existing = {component.component_id for component in get_active_components()}
    for component in COMPONENT_DEFINITIONS:
        if component.component_id not in existing:
            register_component(component)
