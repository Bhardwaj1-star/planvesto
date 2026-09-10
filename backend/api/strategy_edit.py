from fastapi import APIRouter, Header

from api.auth import authenticate_user, verify_planning_unit_ownership
from data.strategy_repository import StrategyRepository
from data.strategy_version_repository import StrategyVersionRepository
from models.strategy_edit import StrategyEditRequest, StrategyEditResult
from services.strategy_edit_service import StrategyEditService

router = APIRouter(prefix="/api/strategy", tags=["Strategy Builder"])


@router.post("/edit", response_model=StrategyEditResult)
def edit_strategy(
    request: StrategyEditRequest,
    authorization: str | None = Header(default=None),
):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    repo = StrategyRepository()
    version_repo = StrategyVersionRepository(repo.db)
    return StrategyEditService(version_repo).edit_strategy(request)
