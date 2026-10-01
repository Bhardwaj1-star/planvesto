from typing import Any
import time

from data.supabase import get_supabase
from models.moneywheel import MoneywheelResult


class MoneywheelRepository:
    """Append-only Moneywheel snapshots."""

    def __init__(self, supabase_client: Any | None = None):
        self.client = supabase_client or get_supabase()
        self.table = "moneywheel_snapshots"

    @staticmethod
    def _execute(query: Any, retries: int = 3) -> Any:
        """Retry transient HTTP disconnects from Supabase without changing business logic."""
        for attempt in range(retries):
            try:
                return query.execute()
            except Exception as exc:
                transient = exc.__class__.__name__ in {
                    "RemoteProtocolError",
                    "ConnectError",
                    "ReadTimeout",
                    "WriteTimeout",
                }
                if not transient or attempt == retries - 1:
                    raise
                time.sleep(0.5 * (2**attempt))
        raise RuntimeError("Supabase request failed after retries")

    def save_snapshot(self, result: MoneywheelResult, financial_state_snapshot: dict[str, Any]) -> MoneywheelResult:
        payload = {
            "planning_unit_id": result.planning_unit_id,
            "rule_set_version": result.rule_set_version,
            "overall_status": result.overall_status,
            "ratios": [r.model_dump(mode="json") for r in result.ratios],
            "financial_state_snapshot": financial_state_snapshot,
            "calculated_at": result.calculated_at,
            "metadata": {**result.metadata, "rules": [rule.model_dump(mode="json") for rule in result.rules]},
        }
        response = self._execute(self.client.table(self.table).insert(payload).select("*"))
        rows = response.data
        if not rows:
            raise RuntimeError("Moneywheel snapshot insert returned no data")
        row = rows[0] if isinstance(rows, list) else rows
        result.metadata["snapshot_id"] = row["snapshot_id"]
        return result

    def get_latest(self, planning_unit_id: str) -> dict[str, Any] | None:
        response = self._execute(
            self.client.table(self.table).select("*")
            .eq("planning_unit_id", planning_unit_id)
            .order("calculated_at", desc=True).limit(1)
        )
        rows = response.data or []
        return rows[0] if rows else None

    def get_history(self, planning_unit_id: str, limit: int = 50) -> list[dict[str, Any]]:
        response = self._execute(
            self.client.table(self.table).select("*")
            .eq("planning_unit_id", planning_unit_id)
            .order("calculated_at", desc=True).limit(limit)
        )
        rows = response.data or []
        return rows
