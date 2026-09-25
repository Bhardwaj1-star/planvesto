from engines.profile.engine import ProfileEngine
from data.financial_state_repository import FinancialStateSnapshotRepository
from data.profile_repository import ProfileRepository


class ProfileService:
    MAX_VERSION_RETRIES = 3

    def __init__(self):
        self.repository = ProfileRepository()
        self.financial_repository = FinancialStateSnapshotRepository()
        self.engine = ProfileEngine()

    def build(self, request):
        snapshot = None
        if request.financial_snapshot_id:
            from data.supabase import get_supabase
            result = (get_supabase().table("financial_state_snapshots").select("*")
                      .eq("snapshot_id", request.financial_snapshot_id)
                      .eq("planning_unit_id", request.planning_unit_id).maybe_single().execute())
            snapshot = result.data if result and result.data else None
            if snapshot is None:
                raise ValueError("Financial state snapshot not found")
        else:
            snapshot = self.financial_repository.get_latest(
                request.planning_unit_id, "individual", request.investor_id
            ) or self.financial_repository.get_latest(request.planning_unit_id, "family")

        financial_state = snapshot.get("financial_state") if snapshot else None
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
