from typing import Any
from data.supabase import get_supabase


class ProfileRepository:
    def __init__(self):
        self.db = get_supabase()

    def next_version(self, planning_unit_id: str, investor_id: str) -> int:
        result = (self.db.table("profile_runs").select("version")
            .eq("planning_unit_id", planning_unit_id).eq("investor_id", investor_id)
            .order("version", desc=True).limit(1).execute())
        return int(result.data[0]["version"]) + 1 if result.data else 1

    def create_run(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = self.db.table("profile_runs").insert(payload).execute()
        if not result.data:
            raise RuntimeError("Failed to persist investor profile")
        return result.data[0]

    @staticmethod
    def is_version_conflict(exc: Exception) -> bool:
        code = getattr(exc, "code", None)
        message = str(exc)
        return code == "23505" or "profile_runs" in message and "version" in message

    def create_constraints(self, profile_run_id: str, constraints: list[dict[str, Any]]) -> None:
        rows = [{"profile_run_id": profile_run_id, **item} for item in constraints]
        if rows:
            result = self.db.table("profile_constraints").insert(rows).execute()
            if len(result.data or []) != len(rows):
                raise RuntimeError("Failed to persist profile constraints")

    def create_conflicts(self, profile_run_id: str, conflicts: list[dict[str, Any]]) -> None:
        rows = [{"profile_run_id": profile_run_id, **item} for item in conflicts]
        if rows:
            result = self.db.table("profile_conflicts").insert(rows).execute()
            if len(result.data or []) != len(rows):
                raise RuntimeError("Failed to persist profile conflicts")

    def get_latest(self, planning_unit_id: str, investor_id: str) -> dict[str, Any] | None:
        result = (self.db.table("profile_runs")
            .select("*, profile_constraints(*), profile_conflicts(*)")
            .eq("planning_unit_id", planning_unit_id).eq("investor_id", investor_id)
            .order("version", desc=True).limit(1).execute())
        return result.data[0] if result.data else None

    def get_history(self, planning_unit_id: str, investor_id: str, limit: int = 20) -> list[dict[str, Any]]:
        result = (self.db.table("profile_runs")
            .select("*, profile_constraints(*), profile_conflicts(*)")
            .eq("planning_unit_id", planning_unit_id).eq("investor_id", investor_id)
            .order("version", desc=True).limit(limit).execute())
        return result.data or []
