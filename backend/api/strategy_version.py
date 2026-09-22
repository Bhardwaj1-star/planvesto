from fastapi import APIRouter, Header, HTTPException, Query

from api.auth import authenticate_user, verify_planning_unit_ownership, verify_strategy_version_ownership
from data.strategy_repository import StrategyRepository
from data.strategy_version_repository import StrategyVersionRepository
from models.strategy_version import StrategyVersion

router = APIRouter(prefix="/api/strategy", tags=["Strategy Versioning"])


def _repository() -> StrategyVersionRepository:
    strategy_repo = StrategyRepository()
    return StrategyVersionRepository(strategy_repo.db)


@router.get("/versions/{strategy_id}", response_model=list[StrategyVersion])
def get_strategy_version_history(strategy_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return _repository().get_history(planning_unit_id, strategy_id)


@router.get("/versions/by-id/{strategy_version_id}", response_model=StrategyVersion)
def get_strategy_version_by_id(strategy_version_id: str, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    result = _repository().get_by_id(planning_unit_id, strategy_version_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Strategy Version not found")
    return result


@router.get("/versions/{strategy_id}/{version}", response_model=StrategyVersion)
def get_strategy_version(strategy_id: str, version: int, planning_unit_id: str = Query(...), authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    result = _repository().get_version(planning_unit_id, strategy_id, version)
    if result is None:
        raise HTTPException(status_code=404, detail="Strategy Version not found")
    return result
