from fastapi import APIRouter, Header

from api.auth import authenticate_user, verify_planning_unit_ownership
from schemas.strategy_approval import StrategyApprovalRequest, StrategyApprovalResponse
from services.strategy_approval_service import StrategyApprovalService


router = APIRouter(prefix="/api/strategy", tags=["Strategy Approval"])


@router.post("/approve", response_model=StrategyApprovalResponse)
def approve_strategy(
    request: StrategyApprovalRequest,
    authorization: str | None = Header(default=None),
):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    snapshot = StrategyApprovalService().approve_selected_strategy(
        planning_unit_id=request.planning_unit_id,
        strategy_run_id=request.strategy_run_id,
        suitability=request.suitability,
        acknowledgement_text=request.acknowledgement_text,
        make_primary=request.make_primary,
        primary_transition_decision=request.primary_transition_decision,
        pending_action_disposition=request.pending_action_disposition,
    )
    return StrategyApprovalResponse(
        approval_snapshot_id=snapshot.approval_snapshot_id,
        strategy_id=snapshot.strategy_id,
        strategy_version_id=snapshot.strategy_version_id,
        strategy_version=snapshot.strategy_version,
        suitability_status=snapshot.suitability.status,
        is_primary=snapshot.is_primary,
        approved_at=snapshot.approved_at,
    )
