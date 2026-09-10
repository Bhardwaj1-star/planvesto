from pydantic import BaseModel

from models.strategy_approval import SuitabilityAssessment
from models.primary_strategy import PendingActionDisposition, PrimaryTransitionDecision


class StrategyApprovalRequest(BaseModel):
    planning_unit_id: str
    strategy_run_id: str
    suitability: SuitabilityAssessment
    acknowledgement_text: str | None = None
    make_primary: bool = False
    primary_transition_decision: PrimaryTransitionDecision | None = None
    pending_action_disposition: PendingActionDisposition | None = None


class StrategyApprovalResponse(BaseModel):
    approval_snapshot_id: str | None = None
    strategy_id: str
    strategy_version_id: str
    strategy_version: int
    suitability_status: str
    is_primary: bool
    approved_at: str
