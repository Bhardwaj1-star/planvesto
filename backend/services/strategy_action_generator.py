from data.financial_state_repository import FinancialStateSnapshotRepository
from data.strategy_repository import StrategyRepository
from data.strategy_version_repository import StrategyVersionRepository
from library.strategies.registry import get_strategy_by_id
from library.strategies.techniques import get_technique_by_id
from models.action_plan import ActionPlanItem
from rules.action_plan import build_action_specs
from services.financial_state_service import FinancialStateService


class StrategyActionGenerator:
    """Materialises an approved Strategy Version into deterministic implementation actions."""

    def __init__(self, action_repository):
        self.action_repository = action_repository
        self.strategy_repository = StrategyRepository()
        self.version_repository = StrategyVersionRepository(self.strategy_repository.db)
        self.snapshot_repository = FinancialStateSnapshotRepository()

    def generate(self, planning_unit_id: str, strategy_version_id: str) -> list[ActionPlanItem]:
        if not self.action_repository.is_strategy_version_approved(planning_unit_id, strategy_version_id):
            raise ValueError("Actions can only be generated for an approved Strategy Version")

        version = self.version_repository.get_by_id(planning_unit_id, strategy_version_id)
        if version is None:
            raise ValueError("Strategy Version not found")
        strategy = get_strategy_by_id(version.strategy_id)
        if strategy is None:
            raise ValueError(f"Strategy is not available in the active Strategy Library: {version.strategy_id}")

        run = self.strategy_repository.get_run_by_strategy_version_id(planning_unit_id, strategy_version_id)
        architecture = run.selected_architecture if run else None
        strategy_ids = [strategy.strategy_id]
        technique_ids = list(strategy.technique_ids)
        if architecture:
            strategy_ids = [architecture.primary_strategy_id, *architecture.supporting_strategy_ids]
            technique_ids = list(dict.fromkeys([*architecture.technique_ids, *technique_ids]))

        definitions = [get_strategy_by_id(strategy_id) for strategy_id in strategy_ids]
        definitions = [item for item in definitions if item is not None]
        techniques = [get_technique_by_id(technique_id) for technique_id in technique_ids]
        techniques = [item for item in techniques if item is not None]

        baseline = self.snapshot_repository.get_latest(planning_unit_id, "family")
        if baseline and baseline.get("financial_state"):
            financial_state = baseline["financial_state"]
        else:
            financial_state = FinancialStateService().build(planning_unit_id, "family").model_dump(mode="json")

        existing = self.action_repository.list_actions_for_strategy_version(planning_unit_id, strategy_version_id)
        existing_keys = {
            str((item.planned_impact or {}).get("generation_key"))
            for item in existing
            if (item.planned_impact or {}).get("generation_key")
        }

        primary = definitions[0] if definitions else strategy
        specs = build_action_specs(
            primary_strategy=primary,
            supporting_strategies=definitions[1:],
            techniques=techniques,
        )

        generated: list[ActionPlanItem] = []
        for index, (title, description, priority) in enumerate(specs, start=1):
            generation_key = f"{strategy_version_id}:strategy-action:{index}:{title}"
            if generation_key in existing_keys:
                continue
            generated.append(self.action_repository.save_action(ActionPlanItem(
                planning_unit_id=planning_unit_id,
                strategy_version_id=strategy_version_id,
                title=title,
                description=description,
                priority=priority,  # type: ignore[arg-type]
                planned_impact={
                    "generation_key": generation_key,
                    "generated": True,
                    "strategy_id": version.strategy_id,
                    "strategy_version_id": strategy_version_id,
                    "implementation_parameters": version.implementation_parameters,
                    "architecture_id": architecture.architecture_id if architecture else None,
                    "financial_state": financial_state,
                },
            )))
        return generated
