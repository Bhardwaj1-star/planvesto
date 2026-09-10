from typing import Any

from data.financial_state_repository import FinancialStateSnapshotRepository
from models.orchestration import ModuleAvailability, PlanningContext, PlanningOrchestrationContext


class PlanningOrchestrationService:
    """Builds the shared context used to connect Planvesto planning modules.

    This layer coordinates references and availability only. It does not invent
    financial classifications, suitability rules, strategy rankings, or a
    Moneywheel aggregate status.
    """

    def __init__(self, financial_state_repository: Any | None = None):
        self.financial_state_repository = financial_state_repository or FinancialStateSnapshotRepository()

    def build_context(
        self,
        planning_unit_id: str,
        scope: str = "family",
        investor_id: str | None = None,
        goal_version_ids: list[str] | None = None,
        strategy_version_id: str | None = None,
    ) -> PlanningOrchestrationContext:
        snapshot = self.financial_state_repository.get_latest(
            planning_unit_id=planning_unit_id,
            scope=scope,
            investor_id=investor_id,
        )

        financial_state_available = snapshot is not None
        reason = None if financial_state_available else "No Financial State snapshot exists for this planning context"

        return PlanningOrchestrationContext(
            planning_context=PlanningContext(
                planning_unit_id=planning_unit_id,
                scope=scope,
                investor_id=investor_id,
                financial_state_snapshot_id=(snapshot.get("snapshot_id") if snapshot else None),
                goal_version_ids=goal_version_ids or [],
                strategy_version_id=strategy_version_id,
            ),
            financial_state=ModuleAvailability(available=financial_state_available, reason=reason),
            goals=ModuleAvailability(
                available=bool(goal_version_ids),
                reason=None if goal_version_ids else "No goal versions supplied in the planning context",
            ),
            strategy=ModuleAvailability(
                available=strategy_version_id is not None,
                reason=None if strategy_version_id else "No strategy version supplied in the planning context",
            ),
            moneywheel=ModuleAvailability(
                available=financial_state_available,
                reason=(None if financial_state_available else "Moneywheel requires a Financial State snapshot")
            ),
            action_plan=ModuleAvailability(
                available=strategy_version_id is not None,
                reason=None if strategy_version_id else "Action Plan requires a strategy version reference",
            ),
            metadata={"orchestration_version": "1.0"},
        )
