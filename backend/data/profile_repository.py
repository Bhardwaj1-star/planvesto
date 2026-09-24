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

    def create_dimensions(self, profile_run_id: str, dimensions: dict[str, dict[str, Any]]) -> None:
        rows = []
        for key, dimension in dimensions.items():
            rows.append({
                "profile_run_id": profile_run_id,
                "dimension_key": key,
                "score": dimension["score"],
                "band": dimension["band"],
                "confidence": dimension["confidence"],
                "components": dimension.get("components", {}),
                "explanations": dimension.get("explanations", []),
            })
        if rows:
            result = self.db.table("profile_dimensions").insert(rows).execute()
            if len(result.data or []) != len(rows):
                raise RuntimeError("Failed to persist profile dimensions")

    def get_latest(self, planning_unit_id: str, investor_id: str) -> dict[str, Any] | None:
        result = (self.db.table("profile_runs").select("*, profile_dimensions(*)")
            .eq("planning_unit_id", planning_unit_id).eq("investor_id", investor_id)
            .order("version", desc=True).limit(1).execute())
        return result.data[0] if result.data else None

    def get_history(self, planning_unit_id: str, investor_id: str, limit: int = 20) -> list[dict[str, Any]]:
        result = (self.db.table("profile_runs").select("*, profile_dimensions(*)")
            .eq("planning_unit_id", planning_unit_id).eq("investor_id", investor_id)
            .order("version", desc=True).limit(limit).execute())
        return result.data or []
