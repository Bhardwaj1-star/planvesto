from typing import Any

from models.action_plan import ActionDecisionRecord, ActionPlanItem


class ActionPlanRepository:
    """Current Action Plan plus append-only decision history."""

    def __init__(self, supabase_client: Any):
        self.client = supabase_client
        self.action_table = "action_plan_items"
        self.history_table = "action_decision_history"

    def is_strategy_version_approved(self, planning_unit_id: str, strategy_version_id: str) -> bool:
        response = (
            self.client.table("strategy_approval_snapshots")
            .select("approval_snapshot_id")
            .eq("planning_unit_id", planning_unit_id)
            .eq("strategy_version_id", strategy_version_id)
            .limit(1)
            .execute()
        )
        return bool(response.data)

    def save_action(self, action: ActionPlanItem) -> ActionPlanItem:
        payload = action.model_dump(mode="json", exclude_none=True)
        response = self.client.table(self.action_table).insert(payload).execute()
        rows = response.data or []
        if not rows:
            raise RuntimeError("Action Plan insert returned no data")
        return ActionPlanItem.model_validate(rows[0])

    def get_action(self, planning_unit_id: str, action_id: str) -> ActionPlanItem | None:
        response = self.client.table(self.action_table).select("*").eq(
            "planning_unit_id", planning_unit_id
        ).eq("action_id", action_id).limit(1).execute()
        rows = response.data or []
        return ActionPlanItem.model_validate(rows[0]) if rows else None

    def list_actions(self, planning_unit_id: str) -> list[ActionPlanItem]:
        response = (
            self.client.table(self.action_table)
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .order("created_at", desc=True)
            .execute()
        )
        return [ActionPlanItem.model_validate(row) for row in (response.data or [])]

    def update_action(self, planning_unit_id: str, action_id: str, updates: dict[str, Any]) -> ActionPlanItem:
        response = (
            self.client.table(self.action_table)
            .update(updates)
            .eq("planning_unit_id", planning_unit_id)
            .eq("action_id", action_id)
            .execute()
        )
        rows = response.data or []
        if not rows:
            raise RuntimeError("Action Plan update returned no data")
        return ActionPlanItem.model_validate(rows[0])

    def delete_action(self, planning_unit_id: str, action_id: str) -> None:
        response = (
            self.client.table(self.action_table)
            .delete()
            .eq("planning_unit_id", planning_unit_id)
            .eq("action_id", action_id)
            .execute()
        )
        if not response.data:
            raise RuntimeError("Action Plan delete affected no rows")

    def record_decision(self, record: ActionDecisionRecord) -> ActionDecisionRecord:
        payload = record.model_dump(mode="json", exclude_none=True)
        response = self.client.table(self.history_table).insert(payload).execute()
        rows = response.data or []
        if not rows:
            raise RuntimeError("Action decision insert returned no data")
        return ActionDecisionRecord.model_validate(rows[0])

    def list_decision_history(self, planning_unit_id: str, action_id: str | None = None) -> list[ActionDecisionRecord]:
        query = (
            self.client.table(self.history_table)
            .select("*")
            .eq("planning_unit_id", planning_unit_id)
            .order("confirmed_at", desc=True)
        )
        if action_id:
            query = query.eq("action_id", action_id)
        response = query.execute()
        return [ActionDecisionRecord.model_validate(row) for row in (response.data or [])]
