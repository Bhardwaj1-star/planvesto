from typing import Any

from models.primary_strategy_state import PrimaryStrategyState


class PrimaryStrategyRepository:
    """Current-primary pointer plus immutable transition history."""

    def __init__(self, supabase_client: Any):
        self.client = supabase_client
        self.table_name = "primary_strategy_state"
        self.history_table = "primary_strategy_transitions"

    def get_current(self, planning_unit_id: str) -> PrimaryStrategyState | None:
        response = self.client.table(self.table_name).select("*").eq("planning_unit_id", planning_unit_id).limit(1).execute()
        rows = response.data or []
        return PrimaryStrategyState.model_validate(rows[0]) if rows else None

    def set_current(self, state: PrimaryStrategyState) -> PrimaryStrategyState:
        payload = state.model_dump(mode="json")
        response = self.client.table(self.table_name).upsert(payload, on_conflict="planning_unit_id").select("*").single().execute()
        return PrimaryStrategyState.model_validate(response.data)

    def record_transition(self, state: PrimaryStrategyState, decision: str) -> None:
        self.client.table(self.history_table).insert({
            "planning_unit_id": state.planning_unit_id,
            "previous_strategy_id": state.previous_strategy_id,
            "previous_strategy_version_id": state.previous_strategy_version_id,
            "new_strategy_id": state.strategy_id,
            "new_strategy_version_id": state.strategy_version_id,
            "approval_snapshot_id": state.approval_snapshot_id,
            "transition_decision": decision,
            "pending_action_disposition": state.pending_action_disposition,
        }).execute()
