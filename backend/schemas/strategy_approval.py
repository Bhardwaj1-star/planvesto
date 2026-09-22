from pydantic import Field

from models.strategy_approval import SuitabilityAssessment
from models.primary_strategy import PendingActionDisposition, PrimaryTransitionDecision
from schemas.base import StrictRequestModel


class StrategyApprovalRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    strategy_run_id: str = Field(min_length=1, max_length=100)
    suitability: SuitabilityAssessment
    acknowledgement_text: str | None = Field(default=None, max_length=2000)
    make_primary: bool = False
    primary_transition_decision: PrimaryTransitionDecision | None = None
    pending_action_disposition: PendingActionDisposition | None = None


class StrategyApprovalResponse(StrictRequestModel):
    approval_snapshot_id: str | None = None
    strategy_id: str
    strategy_version_id: str
    strategy_version: int
    suitability_status: str
    is_primary: bool
    approved_at: str
