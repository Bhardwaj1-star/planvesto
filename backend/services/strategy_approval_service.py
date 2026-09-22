from datetime import datetime, timezone

from fastapi import HTTPException

from data.strategy_approval_repository import StrategyApprovalRepository
from data.strategy_repository import StrategyRepository
from data.strategy_version_repository import StrategyVersionRepository
from data.primary_strategy_repository import PrimaryStrategyRepository
from models.strategy_approval import StrategyApprovalSnapshot, SuitabilityAssessment
from models.primary_strategy_state import PrimaryStrategyState


class StrategyApprovalService:
    """Approval orchestration with a rules-ready suitability boundary and primary lifecycle."""

    def __init__(self):
        self.strategy_repo = StrategyRepository()
        self.version_repo = StrategyVersionRepository(self.strategy_repo.db)
        self.approval_repo = StrategyApprovalRepository(self.strategy_repo.db)
        self.primary_repo = PrimaryStrategyRepository(self.strategy_repo.db)

    def approve_selected_strategy(
        self, planning_unit_id: str, strategy_run_id: str,
        suitability: SuitabilityAssessment, acknowledgement_text: str | None = None,
        make_primary: bool = False, primary_transition_decision: str | None = None,
        pending_action_disposition: str | None = None,
    ) -> StrategyApprovalSnapshot:
        run = self.strategy_repo.get_run_by_id(planning_unit_id, strategy_run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Strategy run not found")

        has_selected_version = bool(
            run.selected_strategy_id
            and run.selected_strategy_version_id
            and run.selected_strategy_version is not None
        )

        # The selected Strategy Version is the source of truth for whether this
        # run is ready for approval. approval_status is lifecycle metadata and
        # may be stale on older runs.
        if run.approval_status == "approved":
            raise HTTPException(status_code=409, detail="Strategy Version is already approved")
        if run.approval_status in {"rejected", "superseded"}:
            raise HTTPException(status_code=409, detail="Strategy run is no longer eligible for approval")
        if not has_selected_version:
            raise HTTPException(status_code=400, detail="A selected Strategy Version is required before approval")

        version = self.version_repo.get_version(planning_unit_id, run.selected_strategy_id, run.selected_strategy_version)
        if not version or version.strategy_version_id != run.selected_strategy_version_id:
            raise HTTPException(status_code=409, detail="Selected Strategy Version snapshot is unavailable or inconsistent")

        acknowledgement_type = "none"
        acknowledged_at = None
        if suitability.status == "Needs Attention":
            acknowledgement_type, acknowledged_at = "needs_attention", datetime.now(timezone.utc).isoformat()
        elif suitability.status == "Unsuitable":
            acknowledgement_type, acknowledged_at = "unsuitable", datetime.now(timezone.utc).isoformat()
        if suitability.status in {"Needs Attention", "Unsuitable"} and not acknowledgement_text:
            raise HTTPException(status_code=400, detail=f"{suitability.status} requires acknowledgement text")

        current = self.primary_repo.get_current(planning_unit_id)
        replacing_primary = bool(make_primary and current and current.strategy_version_id != version.strategy_version_id)
        if replacing_primary and primary_transition_decision is None:
            raise HTTPException(status_code=409, detail="Existing Primary Strategy requires an explicit transition decision")
        if replacing_primary and primary_transition_decision not in {"archive_previous", "keep_previous_approved"}:
            raise HTTPException(status_code=400, detail="Invalid primary transition decision")
        if replacing_primary and pending_action_disposition is None:
            raise HTTPException(status_code=409, detail="Pending implementation action disposition is required when replacing a Primary Strategy")
        if pending_action_disposition not in {None, "retain_for_reassessment", "cancel"}:
            raise HTTPException(status_code=400, detail="Invalid pending action disposition")

        saved = self.approval_repo.save(StrategyApprovalSnapshot(
            planning_unit_id=planning_unit_id, strategy_id=run.selected_strategy_id,
            strategy_version_id=version.strategy_version_id or "", strategy_version=version.version,
            goal_id=run.goal_id, defined_goal_id=run.defined_goal_id, defined_goal_version=run.defined_goal_version,
            strategy_snapshot={"strategy_id": version.strategy_id, "strategy_version": version.version,
                               "library_version": version.library_version, "implementation_version": version.implementation_version,
                               "implementation_parameters": version.implementation_parameters, "selected_scenario_id": run.selected_scenario_id},
            suitability=suitability, acknowledgement_type=acknowledgement_type,
            acknowledgement_text=acknowledgement_text, acknowledged_at=acknowledged_at, is_primary=make_primary,
        ))

        if make_primary:
            decision = primary_transition_decision or "set_initial_primary"
            transition = PrimaryStrategyState(
                planning_unit_id=planning_unit_id, strategy_id=version.strategy_id,
                strategy_version_id=version.strategy_version_id or "", approval_snapshot_id=saved.approval_snapshot_id or "",
                previous_strategy_id=current.strategy_id if replacing_primary else None,
                previous_strategy_version_id=current.strategy_version_id if replacing_primary else None,
                pending_action_disposition=pending_action_disposition,
                transition_metadata={"decision": decision, "previous_primary_transition":
                                     "superseded" if replacing_primary else "none"},
            )
            self.primary_repo.set_current(transition)
            self.primary_repo.record_transition(transition, decision)

        self.strategy_repo.update_approval(planning_unit_id, strategy_run_id, "approve")
        return saved
