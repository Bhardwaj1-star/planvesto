from fastapi import APIRouter, Header

from api.auth import authenticate_user, verify_planning_unit_ownership
from schemas.orchestration import PlanningOrchestrationRequest
from services.planning_orchestration_service import PlanningOrchestrationService

router = APIRouter(prefix="/api/orchestration", tags=["Planning Orchestration"])


@router.post("/context")
def build_planning_context(
    request: PlanningOrchestrationRequest,
    authorization: str | None = Header(default=None),
):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    return PlanningOrchestrationService().build_context(**request.model_dump())
