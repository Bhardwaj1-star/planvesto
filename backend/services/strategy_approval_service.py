from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException

from backend.data.strategy_approval_repository import StrategyApprovalRepository
from backend.data.strategy_repository import StrategyRepository
from backend.data.strategy_version_repository import StrategyVersionRepository
from backend.models.strategy_approval import StrategyApprovalSnapshot, SuitabilityAssessment


class StrategyApprovalService:
    """Approval orchestration with a rules-ready suitability boundary.

    Actual suitability rules are intentionally not implemented yet. The caller
    must provide the final SuitabilityAssessment; this prevents the approval
    layer from inventing financial suitability conclusions.
    """

    def __init__(self):
        self.strategy_repo = StrategyRepository()
        self.version_repo = StrategyVersionRepository(self.strategy_repo.db)
        self.approval_repo = StrategyApprovalRepository(self.strategy_repo.db)

    def approve_selected_strategy(
        self,
        planning_unit_id: str,
        strategy_run_id: str,
        suitability: SuitabilityAssessment,
        acknowledgement_text: str | None = None,
        make_primary: bool = False,
    ) -> StrategyApprovalSnapshot:
        run = self.strategy_repo.get_run_by_id(planning_unit_id, strategy_run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Strategy run not found")
        if not run.selected_strategy_id or not run.selected_strategy_version_id:
            raise HTTPException(status_code=400, detail="A selected Strategy Version is required before approval")

        version = self.version_repo.get_version(
            planning_unit_id, run.selected_strategy_id, run.selected_strategy_version
        )
        if not version or version.strategy_version_id != run.selected_strategy_version_id:
            raise HTTPException(status_code=409, detail="Selected Strategy Version snapshot is unavailable or inconsistent")

        acknowledgement_type = "none"
        acknowledged_at = None
        if suitability.status == "Needs Attention":
            acknowledgement_type = "needs_attention"
            acknowledged_at = datetime.now(timezone.utc).isoformat()
        elif suitability.status == "Unsuitable":
            acknowledgement_type = "unsuitable"
            acknowledged_at = datetime.now(timezone.utc).isoformat()

        if suitability.status == "Needs Attention" and not acknowledgement_text:
            raise HTTPException(status_code=400, detail="Needs Attention requires acknowledgement text")
        if suitability.status == "Unsuitable" and not acknowledgement_text:
            raise HTTPException(status_code=400, detail="Unsuitable requires acknowledgement text")

        snapshot = StrategyApprovalSnapshot(
            planning_unit_id=planning_unit_id,
            strategy_id=run.selected_strategy_id,
            strategy_version_id=version.strategy_version_id or "",
            strategy_version=version.version,
            goal_id=run.goal_id,
            defined_goal_id=run.defined_goal_id,
            defined_goal_version=run.defined_goal_version,
            strategy_snapshot={
                "strategy_id": version.strategy_id,
                "strategy_version": version.version,
                "library_version": version.library_version,
                "implementation_version": version.implementation_version,
                "implementation_parameters": version.implementation_parameters,
                "selected_scenario_id": run.selected_scenario_id,
            },
            suitability=suitability,
            acknowledgement_type=acknowledgement_type,  # type: ignore[arg-type]
            acknowledgement_text=acknowledgement_text,
            acknowledged_at=acknowledged_at,
            is_primary=make_primary,
        )
        return self.approval_repo.save(snapshot)
