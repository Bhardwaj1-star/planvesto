from engines.profile.engine import ProfileEngine
from data.financial_state_repository import FinancialStateSnapshotRepository
from data.profile_repository import ProfileRepository
from services.financial_state_service import FinancialStateService


class ProfileService:
    MAX_VERSION_RETRIES = 3

    def __init__(self):
        self.repository = ProfileRepository()
        self.financial_repository = FinancialStateSnapshotRepository()
        self.financial_state_service = FinancialStateService(
            snapshot_repository=self.financial_repository
        )
        self.engine = ProfileEngine()

    def build(self, request):
        snapshot = self.financial_state_service.get_current_snapshot(
            request.planning_unit_id,
            "individual",
            request.investor_id,
        )
        if (
            request.financial_snapshot_id
            and request.financial_snapshot_id != snapshot.get("snapshot_id")
        ):
            raise ValueError("Financial state snapshot is stale; rebuild the profile with the current snapshot")

        financial_state = snapshot.get("financial_state") if snapshot else None
        if isinstance(financial_state, dict):
            financial_state = {
                key: value for key, value in financial_state.items()
                if key != "__snapshot_authority"
            }
        result = self.engine.build(
            financial_state=financial_state,
            declared_constraints=request.declared_constraints,
            observed_behavior=request.observed_behavior,
            preferences=request.preferences,
            constraint_priorities=request.constraint_priorities,
        )

        base_payload = {
            "planning_unit_id": request.planning_unit_id,
            "investor_id": request.investor_id,
            "engine_version": result["engine_version"],
            "profile_version": request.profile_version,
            "financial_snapshot_id": snapshot.get("snapshot_id") if snapshot else None,
            "input_snapshot": {
                "declared_constraints": request.declared_constraints,
                "observed_behavior": request.observed_behavior,
                "preferences": request.preferences,
                "constraint_priorities": request.constraint_priorities,
                "financial_snapshot_id": snapshot.get("snapshot_id") if snapshot else None,
                "financial_state": financial_state,
            },
            "profile_result": result,
        }

        for attempt in range(self.MAX_VERSION_RETRIES):
            version = self.repository.next_version(request.planning_unit_id, request.investor_id)
            payload = {**base_payload, "version": version}
            try:
                run = self.repository.create_run(payload)
                self.repository.create_constraints(run["profile_run_id"], result["constraints"])
                self.repository.create_conflicts(run["profile_run_id"], result["conflicts"])
                run["profile_result"] = result
                return run
            except Exception as exc:
                if not self.repository.is_version_conflict(exc) or attempt == self.MAX_VERSION_RETRIES - 1:
                    raise

        raise RuntimeError("Failed to allocate profile version")

    def latest(self, planning_unit_id: str, investor_id: str):
        return self.repository.get_latest(planning_unit_id, investor_id)

    def history(self, planning_unit_id: str, investor_id: str, limit: int = 20):
        return self.repository.get_history(planning_unit_id, investor_id, limit)
