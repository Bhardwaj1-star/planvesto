from typing import Literal

from pydantic import BaseModel


PendingActionDisposition = Literal["retain_for_reassessment", "cancel"]
PrimaryTransitionDecision = Literal["archive_previous", "keep_previous_approved"]


class PrimaryStrategyTransition(BaseModel):
    planning_unit_id: str
    new_strategy_id: str
    new_strategy_version_id: str
    previous_strategy_id: str | None = None
    previous_strategy_version_id: str | None = None
    previous_primary_archived: bool = False
    pending_action_disposition: PendingActionDisposition | None = None
    decision: PrimaryTransitionDecision = "archive_previous"
