"""
api/routers/diary.py
FastAPI router for Investor Diary endpoints.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_current_user_id
from app.api.schemas.diary import (
    DiaryEntryCreateRequest,
    DiaryEntryResponse,
    FinancialDecisionCreateRequest,
    FinancialDecisionResponse,
)

router = APIRouter(tags=["Investor Diary"])

_memory_entries: Dict[str, Dict[str, Any]] = {}
_memory_decisions: Dict[str, Dict[str, Any]] = {}


@router.get("/entries", response_model=List[DiaryEntryResponse])
@router.get("/api/diary/entries", response_model=List[DiaryEntryResponse], include_in_schema=False)
def list_entries(
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Retrieves all diary entries for a planning unit."""
    entries = [e for e in _memory_entries.values() if e.get("planning_unit_id") == planning_unit_id]
    entries.sort(key=lambda x: x.get("date", ""), reverse=True)
    return [DiaryEntryResponse(**e) for e in entries]


@router.post("/entries", response_model=DiaryEntryResponse)
@router.post("/api/diary/entries", response_model=DiaryEntryResponse, include_in_schema=False)
def create_entry(
    request: DiaryEntryCreateRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Creates a new diary entry."""
    entry_id = f"entry_{uuid.uuid4().hex[:8]}"
    now_str = datetime.now(timezone.utc).isoformat()
    entry = {
        "id": entry_id,
        "planning_unit_id": request.planning_unit_id,
        "date": request.date,
        "title": request.title,
        "content": request.content,
        "tags": request.tags,
        "prompts": [p.model_dump() for p in request.prompts],
        "follow_up_note": request.follow_up_note,
        "is_important": request.is_important,
        "created_at": now_str,
        "updated_at": now_str,
    }
    _memory_entries[entry_id] = entry
    return DiaryEntryResponse(**entry)


@router.delete("/entries/{entry_id}")
@router.delete("/api/diary/entries/{entry_id}", include_in_schema=False)
def delete_entry(
    entry_id: str,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Deletes a diary entry."""
    if entry_id in _memory_entries:
        del _memory_entries[entry_id]
    return {"deleted": True, "entry_id": entry_id}


@router.get("/decisions", response_model=List[FinancialDecisionResponse])
@router.get("/api/diary/decisions", response_model=List[FinancialDecisionResponse], include_in_schema=False)
def list_decisions(
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Retrieves confirmed investor financial decisions."""
    decisions = [d for d in _memory_decisions.values() if d.get("planning_unit_id") == planning_unit_id]
    decisions.sort(key=lambda x: x.get("date", ""), reverse=True)
    return [FinancialDecisionResponse(**d) for d in decisions]


@router.get("/decisions/system", response_model=List[FinancialDecisionResponse])
@router.get("/api/diary/decisions/system", response_model=List[FinancialDecisionResponse], include_in_schema=False)
def list_system_decisions(
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Retrieves system-generated financial milestone decisions."""
    now_str = datetime.now(timezone.utc).isoformat()
    return [
        FinancialDecisionResponse(
            id="sys_dec_1",
            planning_unit_id=planning_unit_id,
            date=datetime.now().strftime("%Y-%m-%d"),
            title="Funding Path Selected",
            summary="Selected Self Money Funding Path for primary goal.",
            category="Strategy",
            source="System",
            source_id="path_self_money",
            metrics={"expected_cagr_pct": 12.0},
            created_at=now_str,
            historical=True,
        )
    ]


@router.post("/decisions", response_model=FinancialDecisionResponse)
@router.post("/api/diary/decisions", response_model=FinancialDecisionResponse, include_in_schema=False)
def create_decision(
    request: FinancialDecisionCreateRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Creates a recorded financial decision."""
    dec_id = f"fdec_{uuid.uuid4().hex[:8]}"
    now_str = datetime.now(timezone.utc).isoformat()
    decision = {
        "id": dec_id,
        "planning_unit_id": request.planning_unit_id,
        "date": request.date,
        "title": request.title,
        "summary": request.summary,
        "category": request.category,
        "source": request.source,
        "source_id": request.source_id,
        "metrics": request.metrics,
        "notes": request.notes,
        "created_at": now_str,
        "historical": True,
    }
    _memory_decisions[dec_id] = decision
    return FinancialDecisionResponse(**decision)
