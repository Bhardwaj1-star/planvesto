from typing import Any

from models.action_plan import ActionDecisionRecord, ActionPlanItem


class ActionPlanRepository:
    """Current Action Plan plus append-only decision history."""

    def __init__(self, supabase_client: Any):
        self.client = supabase_client
        self.action_table = "action_plan_items"
        self.history_table = "action_decision_history"

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
