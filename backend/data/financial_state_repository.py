from typing import Any

from data.supabase import get_supabase


class FinancialStateSnapshotRepository:
    """Persistence for immutable Financial State snapshots."""

    def __init__(self):
        self.db = get_supabase()

    def save_snapshot(
        self,
        planning_unit_id: str,
        scope: str,
        investor_id: str | None,
        financial_state: dict[str, Any],
    ) -> dict[str, Any]:
        payload = {
            "planning_unit_id": planning_unit_id,
            "scope": scope,
            "investor_id": investor_id,
            "financial_state": financial_state,
        }
        result = self.db.table("financial_state_snapshots").insert(payload).execute()
        if not result.data:
            raise RuntimeError("Failed to persist Financial State snapshot")
        return result.data[0]

    def _query(self, planning_unit_id: str, scope: str, investor_id: str | None):
        query = (
            self.db.table("financial_state_snapshots")
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .eq("scope", scope)
        )
        if scope == "individual":
            query = query.eq("investor_id", investor_id)
        else:
            query = query.is_("investor_id", "null")
        return query

    def get_latest(
        self, planning_unit_id: str, scope: str, investor_id: str | None = None
    ) -> dict[str, Any] | None:
        result = (
            self._query(planning_unit_id, scope, investor_id)
            .order("calculated_at", desc=True)
            .limit(1)
            .execute()
        )
        return result.data[0] if result.data else None

    def get_history(
        self,
        planning_unit_id: str,
        scope: str,
        investor_id: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        result = (
            self._query(planning_unit_id, scope, investor_id)
            .order("calculated_at", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data or []
