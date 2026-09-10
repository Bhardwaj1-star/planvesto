from typing import Any

from backend.library.strategies.registry import get_strategy_by_id
from backend.models.strategy import StrategyDefinition
from backend.models.strategy_version import StrategyVersion
from backend.data.strategy_version_repository import StrategyVersionRepository


class StrategyVersionService:
    """Creates validated immutable strategy versions."""

    def __init__(self, repository: StrategyVersionRepository):
        self.repository = repository

    def validate_parameters(
        self,
        strategy: StrategyDefinition,
        parameters: dict[str, Any],
        parent_parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        definitions = {param.name: param for param in strategy.implementation_parameters}
        unknown = set(parameters) - set(definitions)
        if unknown:
            raise ValueError(f"Unknown implementation parameters: {sorted(unknown)}")

        base = dict(parent_parameters or {})
        validated: dict[str, Any] = {}
        for name, definition in definitions.items():
            if name in parameters:
                value = parameters[name]
                if parent_parameters is not None and value != base.get(name) and not definition.editable:
                    raise ValueError(f"Implementation parameter is not editable: {name}")
            elif name in base:
                value = base[name]
            else:
                value = definition.default_value

            self._validate_value(definition, value)
            validated[name] = value

        return validated

    @staticmethod
    def _validate_value(definition: Any, value: Any) -> None:
        if definition.param_type == "choice":
            if value not in definition.choices:
                raise ValueError(f"Invalid choice for {definition.name}: {value}")
            return

        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"Invalid numeric value for {definition.name}")

        if definition.param_type == "integer" and float(value) != int(value):
            raise ValueError(f"Integer value required for {definition.name}")
        if definition.min_value is not None and value < definition.min_value:
            raise ValueError(f"Value below minimum for {definition.name}")
        if definition.max_value is not None and value > definition.max_value:
            raise ValueError(f"Value above maximum for {definition.name}")

    def create_version(
        self,
        planning_unit_id: str,
        strategy_id: str,
        parameters: dict[str, Any] | None = None,
        parent_version: int | None = None,
        source: str = "library",
        status: str = "draft",
    ) -> StrategyVersion:
        strategy = get_strategy_by_id(strategy_id)
        if strategy is None:
            raise ValueError(f"Unknown strategy: {strategy_id}")

        parent_parameters: dict[str, Any] | None = None
        if parent_version is not None:
            parent = self.repository.get_version(planning_unit_id, strategy_id, parent_version)
            if parent is None:
                raise ValueError(f"Parent strategy version not found: {parent_version}")
            parent_parameters = parent.implementation_parameters

        if source == "investor_edit" and parent_version is None:
            raise ValueError("investor_edit versions require parent_version")
        if source not in {"library", "investor_edit"}:
            raise ValueError(f"Invalid strategy version source: {source}")

        latest = self.repository.get_latest_version(planning_unit_id, strategy_id)
        next_version = (latest.version + 1) if latest else 1
        validated = self.validate_parameters(strategy, parameters or {}, parent_parameters)

        return self.repository.save_version(
            StrategyVersion(
                planning_unit_id=planning_unit_id,
                strategy_id=strategy_id,
                version=next_version,
                parent_version=parent_version,
                source=source,  # type: ignore[arg-type]
                library_version=strategy.library_version,
                implementation_version=strategy.implementation_version,
                implementation_parameters=validated,
                status=status,  # type: ignore[arg-type]
            )
        )
