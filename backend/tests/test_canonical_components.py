from library.strategies.components import (
    CANONICAL_COMPONENTS,
    get_canonical_component,
    get_canonical_components,
    validate_component_registry,
)
from engines.strategy.components.definitions import COMPONENT_DEFINITIONS
from engines.strategy.components.registry import get_active_components


def test_canonical_component_registry_has_unique_ids():
    ids = [c.component_id for c in CANONICAL_COMPONENTS]
    assert ids
    assert len(ids) == len(set(ids))
    validate_component_registry()


def test_component_definitions_are_canonical():
    assert COMPONENT_DEFINITIONS is CANONICAL_COMPONENTS
    assert get_canonical_components() == list(CANONICAL_COMPONENTS)


def test_canonical_component_lookup():
    component = get_canonical_component("component-funding")
    assert component is not None
    assert component.role == "funding"


def test_runtime_component_registration_uses_canonical_definitions():
    from engines.strategy.components.definitions import register_default_components
    register_default_components()
    active = {c.component_id: c for c in get_active_components()}
    assert set(active) >= {c.component_id for c in CANONICAL_COMPONENTS}
    assert active["component-funding"] is CANONICAL_COMPONENTS[0]
