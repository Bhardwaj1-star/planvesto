from typing import Any

from models.diary import DiaryEntry, FinancialDecision


class DiaryRepository:
    """Persistent diary entries plus append-only financial decision history."""

    def __init__(self, supabase_client: Any):
        self.client = supabase_client
        self.entry_table = "diary_entries"
        self.decision_table = "financial_decision_history"

    def list_entries(self, planning_unit_id: str) -> list[DiaryEntry]:
        response = (
            self.client.table(self.entry_table)
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .order("date", desc=True)
            .order("created_at", desc=True)
            .execute()
        )
        return [DiaryEntry.model_validate(row) for row in (response.data or [])]

    def get_entry(self, planning_unit_id: str, entry_id: str) -> DiaryEntry | None:
        response = (
            self.client.table(self.entry_table)
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .eq("id", entry_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return DiaryEntry.model_validate(rows[0]) if rows else None

    def save_entry(self, entry: DiaryEntry) -> DiaryEntry:
        payload = entry.model_dump(mode="json", exclude_none=True)
        payload.pop("id", None)
        response = self.client.table(self.entry_table).insert(payload).execute()
        rows = response.data or []
        if not rows:
            raise RuntimeError("Diary entry insert returned no data")
        return DiaryEntry.model_validate(rows[0])

    def update_entry(self, planning_unit_id: str, entry_id: str, updates: dict[str, Any]) -> DiaryEntry:
        response = (
            self.client.table(self.entry_table)
            .update(updates)
            .eq("planning_unit_id", planning_unit_id)
            .eq("id", entry_id)
            .execute()
        )
        rows = response.data or []
        if not rows:
            raise RuntimeError("Diary entry update returned no data")
        return DiaryEntry.model_validate(rows[0])

    def delete_entry(self, planning_unit_id: str, entry_id: str) -> None:
        response = (
            self.client.table(self.entry_table)
            .delete()
            .eq("planning_unit_id", planning_unit_id)
            .eq("id", entry_id)
            .execute()
        )
        if not response.data:
            raise RuntimeError("Diary entry delete affected no rows")

    def list_decisions(self, planning_unit_id: str) -> list[FinancialDecision]:
        response = (
            self.client.table(self.decision_table)
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .order("date", desc=True)
            .order("created_at", desc=True)
            .execute()
        )
        return [FinancialDecision.model_validate(row) for row in (response.data or [])]

    def save_decision(self, decision: FinancialDecision) -> FinancialDecision:
        payload = decision.model_dump(mode="json", exclude_none=True)
        payload.pop("id", None)
        response = self.client.table(self.decision_table).insert(payload).execute()
        rows = response.data or []
        if not rows:
            raise RuntimeError("Financial decision insert returned no data")
        return FinancialDecision.model_validate(rows[0])
