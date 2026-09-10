from datetime import datetime, timezone
from typing import Any

from models.diary import DiaryEntry, FinancialDecision
from data.diary_repository import DiaryRepository


class DiaryService:
    """Owns diary persistence semantics; financial decisions are append-only."""

    def __init__(self, repository: DiaryRepository):
        self.repository = repository

    def create_entry(self, **data: Any) -> DiaryEntry:
        return self.repository.save_entry(DiaryEntry(**data))

    def update_entry(self, planning_unit_id: str, entry_id: str, updates: dict[str, Any]) -> DiaryEntry:
        updates = {key: value for key, value in updates.items() if value is not None}
        updates["updated_at"] = datetime.now(timezone.utc).isoformat()
        return self.repository.update_entry(planning_unit_id, entry_id, updates)

    def create_decision(self, **data: Any) -> FinancialDecision:
        return self.repository.save_decision(FinancialDecision(**data))
