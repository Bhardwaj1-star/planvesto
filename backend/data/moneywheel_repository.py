from typing import Any

from data.supabase import get_supabase
from models.moneywheel import MoneywheelResult


class MoneywheelRepository:
    """Append-only Moneywheel snapshots."""

    def __init__(self, supabase_client: Any | None = None):
        self.client = supabase_client or get_supabase()
        self.table = "moneywheel_snapshots"

    def save_snapshot(self, result: MoneywheelResult, financial_state_snapshot: dict[str, Any]) -> MoneywheelResult:
        payload = {
            "planning_unit_id": result.planning_unit_id,
            "rule_set_version": result.rule_set_version,
            "overall_status": result.overall_status,
            "ratios": [r.model_dump(mode="json") for r in result.ratios],
            "financial_state_snapshot": financial_state_snapshot,
            "calculated_at": result.calculated_at,
            "metadata": result.metadata,
        }
        response = self.client.table(self.table).insert(payload).select("*").execute()
        rows = response.data
        if not rows:
            raise RuntimeError("Moneywheel snapshot insert returned no data")
        row = rows[0] if isinstance(rows, list) else rows
        result.metadata["snapshot_id"] = row["snapshot_id"]
        return result

    def get_latest(self, planning_unit_id: str) -> dict[str, Any] | None:
        response = (
            self.client.table(self.table).select("*")
            .eq("planning_unit_id", planning_unit_id)
            .order("calculated_at", desc=True).limit(1).execute()
        )
        rows = response.data or []
        return rows[0] if rows else None

    def get_history(self, planning_unit_id: str, limit: int = 50) -> list[dict[str, Any]]:
        response = (
            self.client.table(self.table).select("*")
            .eq("planning_unit_id", planning_unit_id)
            .order("calculated_at", desc=True).limit(limit).execute()
        )
        return response.data or []
