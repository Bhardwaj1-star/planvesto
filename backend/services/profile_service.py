from engines.profile.engine import ProfileEngine
from data.financial_state_repository import FinancialStateSnapshotRepository
from data.profile_repository import ProfileRepository


class ProfileService:
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
            risk_tolerance_answers=request.risk_tolerance_answers,
            behavioral_answers=request.behavioral_answers,
            identity_answers=request.identity_answers,
        )
        version = self.repository.next_version(request.planning_unit_id, request.investor_id)
        payload = {
            "planning_unit_id": request.planning_unit_id,
            "investor_id": request.investor_id,
            "version": version,
            "engine_version": result["engine_version"],
            "questionnaire_version": request.questionnaire_version,
            "financial_snapshot_id": snapshot.get("snapshot_id") if snapshot else None,
            "completeness": result["completeness"],
            "input_snapshot": {
                "risk_tolerance_answers": request.risk_tolerance_answers,
                "behavioral_answers": request.behavioral_answers,
                "identity_answers": request.identity_answers,
                "financial_snapshot_id": snapshot.get("snapshot_id") if snapshot else None,
                "financial_state": financial_state,
            },
        }
        run = self.repository.create_run(payload)
        dimensions = {k: v for k, v in result.items() if k in {"risk_capacity", "risk_tolerance", "behavioral_profile", "investor_identity"}}
        self.repository.create_dimensions(run["profile_run_id"], dimensions)
        run["profile_dimensions"] = [dict(v, dimension_key=k) for k, v in dimensions.items()]
        return run

    def latest(self, planning_unit_id: str, investor_id: str):
        return self.repository.get_latest(planning_unit_id, investor_id)

    def history(self, planning_unit_id: str, investor_id: str, limit: int = 20):
        return self.repository.get_history(planning_unit_id, investor_id, limit)
