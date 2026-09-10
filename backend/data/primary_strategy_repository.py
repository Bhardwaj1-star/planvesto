from typing import Any

from backend.models.primary_strategy_state import PrimaryStrategyState


class PrimaryStrategyRepository:
    """Mutable current-primary pointer; historical approval snapshots remain immutable."""

    def __init__(self, supabase_client: Any):
        self.client = supabase_client
        self.table_name = "primary_strategy_state"

    def get_current(self, planning_unit_id: str) -> PrimaryStrategyState | None:
        response = (
            self.client.table(self.table_name).select("*")
            .eq("planning_unit_id", planning_unit_id).limit(1).execute()
        )
        rows = response.data or []
        return PrimaryStrategyState.model_validate(rows[0]) if rows else None

    def set_current(self, state: PrimaryStrategyState) -> PrimaryStrategyState:
        payload = state.model_dump(mode="json")
        response = (
            self.client.table(self.table_name)
            .upsert(payload, on_conflict="planning_unit_id")
            .select("*").single().execute()
        )
        return PrimaryStrategyState.model_validate(response.data)
