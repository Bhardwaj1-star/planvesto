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

    def list_system_decisions(self, planning_unit_id: str) -> list[FinancialDecision]:
        """Read authoritative module histories without duplicating or mutating them."""
        client = self.repository.client
        decisions: list[FinancialDecision] = []

        action_rows = client.table("action_decision_history").select("*").eq("planning_unit_id", planning_unit_id).order("confirmed_at", desc=True).execute().data or []
        actions = {r["action_id"]: r for r in (client.table("action_plan_items").select("action_id,title,strategy_version_id").eq("planning_unit_id", planning_unit_id).execute().data or [])}
        for row in action_rows:
            action = actions.get(row.get("action_id"), {})
            timestamp = row.get("confirmed_at") or row.get("created_at") or datetime.now(timezone.utc).isoformat()
            decisions.append(FinancialDecision(
                id=f"action:{row.get('decision_id') or row.get('action_id')}:{timestamp}",
                planning_unit_id=planning_unit_id,
                date=timestamp,
                title=f"Action: {action.get('title') or row.get('action_id')}",
                summary=f"Action decision recorded: {row.get('decision')}",
                category="Strategy",
                source="action_plan",
                source_id=row.get("decision_id") or row.get("action_id"),
                metrics={"decision": row.get("decision"), "before_state": row.get("before_state") or {}, "after_state": row.get("after_state") or {}, "impact_preview": row.get("impact_preview") or {}, "strategy_version_id": action.get("strategy_version_id")},
                historical=True,
            ))

        approval_rows = client.table("strategy_approval_snapshots").select("*").eq("planning_unit_id", planning_unit_id).order("approved_at", desc=True).execute().data or []
        for row in approval_rows:
            suitability = row.get("suitability") or {}
            timestamp = row.get("approved_at") or datetime.now(timezone.utc).isoformat()
            decisions.append(FinancialDecision(
                id=f"approval:{row.get('approval_snapshot_id') or timestamp}",
                planning_unit_id=planning_unit_id,
                date=timestamp,
                title="Strategy Version approved",
                summary=f"Strategy {row.get('strategy_id')} version {row.get('strategy_version')} approved with suitability: {suitability.get('status', 'not recorded')}.",
                category="Strategy",
                source="strategy_approval",
                source_id=row.get("approval_snapshot_id"),
                metrics={"strategy_id": row.get("strategy_id"), "strategy_version_id": row.get("strategy_version_id"), "strategy_version": row.get("strategy_version"), "goal_id": row.get("goal_id"), "suitability": suitability, "is_primary": bool(row.get("is_primary"))},
                notes=row.get("acknowledgement_text"),
                historical=True,
            ))

        transition_rows = client.table("primary_strategy_transitions").select("*").eq("planning_unit_id", planning_unit_id).order("created_at", desc=True).execute().data or []
        for row in transition_rows:
            timestamp = row.get("created_at") or datetime.now(timezone.utc).isoformat()
            decisions.append(FinancialDecision(
                id=f"primary:{row.get('transition_id') or timestamp}",
                planning_unit_id=planning_unit_id,
                date=timestamp,
                title="Primary Strategy changed",
                summary=f"Primary Strategy transition recorded: {row.get('transition_decision')}.",
                category="Strategy",
                source="primary_strategy",
                source_id=row.get("transition_id"),
                metrics={"previous_strategy_id": row.get("previous_strategy_id"), "previous_strategy_version_id": row.get("previous_strategy_version_id"), "new_strategy_id": row.get("new_strategy_id"), "new_strategy_version_id": row.get("new_strategy_version_id"), "approval_snapshot_id": row.get("approval_snapshot_id"), "pending_action_disposition": row.get("pending_action_disposition")},
                historical=True,
            ))

        return sorted(decisions, key=lambda item: (item.date, item.created_at), reverse=True)
