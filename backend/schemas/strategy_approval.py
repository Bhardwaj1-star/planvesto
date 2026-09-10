from pydantic import BaseModel, Field

from models.strategy_approval import SuitabilityAssessment


class StrategyApprovalRequest(BaseModel):
    planning_unit_id: str
    strategy_run_id: str
    suitability: SuitabilityAssessment
    acknowledgement_text: str | None = None
    make_primary: bool = False


class StrategyApprovalResponse(BaseModel):
    approval_snapshot_id: str | None = None
    strategy_id: str
    strategy_version_id: str
    strategy_version: int
    suitability_status: str
    is_primary: bool
    approved_at: str
