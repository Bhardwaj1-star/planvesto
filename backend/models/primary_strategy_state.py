from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class PrimaryStrategyState(BaseModel):
    planning_unit_id: str
    strategy_id: str
    strategy_version_id: str
    approval_snapshot_id: str
    status: str = "primary"
    previous_strategy_id: str | None = None
    previous_strategy_version_id: str | None = None
    pending_action_disposition: str | None = None
    transition_metadata: dict[str, Any] = Field(default_factory=dict)
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
