from .contracts import StrategyComponent


_COMPONENTS: dict[str, StrategyComponent] = {}


def register_component(component: StrategyComponent) -> None:
    if component.component_id in _COMPONENTS:
        raise ValueError(f"Duplicate strategy component: {component.component_id}")
    _COMPONENTS[component.component_id] = component


def get_component(component_id: str) -> StrategyComponent | None:
    return _COMPONENTS.get(component_id)


def get_active_components() -> list[StrategyComponent]:
    return list(_COMPONENTS.values())
