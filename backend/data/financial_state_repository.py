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
        authority: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        stored_state = dict(financial_state)
        if authority is not None:
            stored_state["__snapshot_authority"] = authority
        payload = {
            "planning_unit_id": planning_unit_id,
            "scope": scope,
            "investor_id": investor_id,
            "financial_state": stored_state,
        }
        result = self.db.table("financial_state_snapshots").insert(payload).execute()
        if not result.data:
            raise RuntimeError("Failed to persist Financial State snapshot")
        return result.data[0]

    def get_by_id(self, planning_unit_id: str, snapshot_id: str) -> dict[str, Any] | None:
        result = (
            self.db.table("financial_state_snapshots")
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .eq("snapshot_id", snapshot_id)
            .limit(1)
            .execute()
        )
        return result.data[0] if result.data else None

    def has_completed_action_lineage(
        self,
        planning_unit_id: str,
        action_id: str,
        snapshot_id: str,
        strategy_version_id: str,
    ) -> bool:
        result = (
            self.db.table("action_plan_items")
            .select("status, strategy_version_id, actual_impact")
            .eq("planning_unit_id", planning_unit_id)
            .eq("action_id", action_id)
            .limit(1)
            .execute()
        )
        rows = result.data or []
        if not rows or rows[0].get("status") != "completed":
            return False
        impact = rows[0].get("actual_impact") or {}
        return (
            rows[0].get("strategy_version_id") == strategy_version_id
            and impact.get("strategy_version_id") == strategy_version_id
            and impact.get("financial_state_snapshot_id") == snapshot_id
        )

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
        rows = result.data or []
        for row in rows:
            stored_state = dict(row.get("financial_state") or {})
            authority = stored_state.pop("__snapshot_authority", None)
            row["financial_state"] = stored_state
            if authority is not None:
                row["authority"] = authority
        return rows
