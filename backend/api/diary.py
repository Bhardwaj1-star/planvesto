from fastapi import APIRouter, Header, HTTPException

from api.auth import authenticate_user, verify_planning_unit_ownership
from data.diary_repository import DiaryRepository
from data.strategy_repository import StrategyRepository
from schemas.diary import DiaryEntryCreateRequest, DiaryEntryUpdateRequest, FinancialDecisionCreateRequest
from services.diary_service import DiaryService

router = APIRouter(prefix="/api/diary", tags=["Investor Diary"])


def _service() -> DiaryService:
    return DiaryService(DiaryRepository(StrategyRepository().db))


def _authenticate(planning_unit_id: str, authorization: str | None) -> None:
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)


@router.get("/entries")
def list_entries(planning_unit_id: str, authorization: str | None = Header(default=None)):
    _authenticate(planning_unit_id, authorization)
    return _service().repository.list_entries(planning_unit_id)


@router.get("/entries/{entry_id}")
def get_entry(entry_id: str, planning_unit_id: str, authorization: str | None = Header(default=None)):
    _authenticate(planning_unit_id, authorization)
    entry = _service().repository.get_entry(planning_unit_id, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    return entry


@router.post("/entries")
def create_entry(request: DiaryEntryCreateRequest, authorization: str | None = Header(default=None)):
    _authenticate(request.planning_unit_id, authorization)
    return _service().create_entry(**request.model_dump())


@router.patch("/entries/{entry_id}")
def update_entry(
    entry_id: str,
    request: DiaryEntryUpdateRequest,
    planning_unit_id: str,
    authorization: str | None = Header(default=None),
):
    _authenticate(planning_unit_id, authorization)
    entry = _service().repository.get_entry(planning_unit_id, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    return _service().update_entry(planning_unit_id, entry_id, request.model_dump(exclude_unset=True))


@router.delete("/entries/{entry_id}")
def delete_entry(entry_id: str, planning_unit_id: str, authorization: str | None = Header(default=None)):
    _authenticate(planning_unit_id, authorization)
    entry = _service().repository.get_entry(planning_unit_id, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Diary entry not found")
    _service().repository.delete_entry(planning_unit_id, entry_id)
    return {"deleted": True, "entry_id": entry_id}


@router.get("/decisions")
def list_decisions(planning_unit_id: str, authorization: str | None = Header(default=None)):
    _authenticate(planning_unit_id, authorization)
    return _service().repository.list_decisions(planning_unit_id)


@router.get("/decisions/system")
def list_system_decisions(planning_unit_id: str, authorization: str | None = Header(default=None)):
    _authenticate(planning_unit_id, authorization)
    return _service().list_system_decisions(planning_unit_id)


@router.post("/decisions")
def create_decision(request: FinancialDecisionCreateRequest, authorization: str | None = Header(default=None)):
    _authenticate(request.planning_unit_id, authorization)
    return _service().create_decision(**request.model_dump())
