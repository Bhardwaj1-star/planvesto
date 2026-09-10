from typing import Any

from backend.models.strategy_approval import StrategyApprovalSnapshot


class StrategyApprovalRepository:
    """Insert/read-only persistence boundary for approval snapshots."""

    def __init__(self, supabase_client: Any):
        self.client = supabase_client
        self.table_name = "strategy_approval_snapshots"

    def save(self, snapshot: StrategyApprovalSnapshot) -> StrategyApprovalSnapshot:
        payload = snapshot.model_dump(mode="json", exclude_none=True)
        response = self.client.table(self.table_name).insert(payload).execute()
        rows = response.data or []
        if not rows:
            raise RuntimeError("Strategy approval snapshot insert returned no data")
        return StrategyApprovalSnapshot.model_validate(rows[0])

    def get_latest_primary(self, planning_unit_id: str) -> StrategyApprovalSnapshot | None:
        response = (
            self.client.table(self.table_name)
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .eq("is_primary", True)
            .order("approved_at", desc=True)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return StrategyApprovalSnapshot.model_validate(rows[0]) if rows else None

    def get_history(self, planning_unit_id: str, strategy_id: str | None = None) -> list[StrategyApprovalSnapshot]:
        query = self.client.table(self.table_name).select("*").eq("planning_unit_id", planning_unit_id)
        if strategy_id:
            query = query.eq("strategy_id", strategy_id)
        response = query.order("approved_at", desc=True).execute()
        return [StrategyApprovalSnapshot.model_validate(row) for row in (response.data or [])]
