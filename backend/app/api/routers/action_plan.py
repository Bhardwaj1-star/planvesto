"""
api/routers/action_plan.py
FastAPI router for Action Plan endpoints.
Chapter 13 — Explicit Investor Acceptance & Action Implementation.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_current_user_id
from app.api.schemas.action_plan import (
    ActionCreateRequest,
    ActionPlanItemSchema,
    ActionCompletionRequest,
    ActionDecisionInput,
    ActionDecisionResponse,
    ActionDecisionRecord,
)
from app.infrastructure.persistence.repositories.action_plan import ActionPlanRepository

router = APIRouter(tags=["Action Plan"])

_action_repo = ActionPlanRepository()
_decision_history: List[Dict[str, Any]] = []


@router.get("/actions", response_model=List[ActionPlanItemSchema])
@router.get("/api/action-plan/actions", response_model=List[ActionPlanItemSchema], include_in_schema=False)
def list_actions(
    planning_unit_id: str = Query(...),
    strategy_version_id: Optional[str] = Query(default=None),
    user_id: str = Depends(get_current_user_id),
):
    """Lists active actions for a planning unit, optionally filtered by strategy version."""
    actions = _action_repo.list_actions(planning_unit_id)
    if strategy_version_id:
        actions = [a for a in actions if a.get("strategy_version_id") == strategy_version_id]
    return [
        ActionPlanItemSchema(
            action_id=a.get("action_id"),
            planning_unit_id=a.get("planning_unit_id", planning_unit_id),
            strategy_version_id=a.get("strategy_version_id", strategy_version_id or "sv_default"),
            title=a.get("title", ""),
            description=a.get("description"),
            priority=a.get("priority", "medium"),
            deadline=a.get("deadline"),
            status=a.get("status", "planned"),
            planned_impact=a.get("planned_impact", {}),
            actual_impact=a.get("actual_impact", {}),
            created_at=a.get("created_at", datetime.now(timezone.utc).isoformat()),
        )
        for a in actions
    ]


@router.post("/actions/generate", response_model=List[ActionPlanItemSchema])
@router.post("/api/action-plan/actions/generate", response_model=List[ActionPlanItemSchema], include_in_schema=False)
def generate_actions(
    planning_unit_id: str = Query(...),
    strategy_version_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Generates standard milestone actions for an accepted strategy version."""
    now_str = datetime.now(timezone.utc).isoformat()
    defaults = [
        {
            "action_id": f"act_{uuid.uuid4().hex[:8]}",
            "planning_unit_id": planning_unit_id,
            "strategy_version_id": strategy_version_id,
            "title": "Set up Systematic Investment Plan (SIP)",
            "description": "Establish automated monthly contribution for goal funding.",
            "priority": "high",
            "deadline": "Month 1",
            "status": "planned",
            "planned_impact": {"monthly_contribution_increase": 15000},
            "actual_impact": {},
            "created_at": now_str,
        },
        {
            "action_id": f"act_{uuid.uuid4().hex[:8]}",
            "planning_unit_id": planning_unit_id,
            "strategy_version_id": strategy_version_id,
            "title": "Maintain Emergency Reserve",
            "description": "Verify 6 months essential expenses in liquid instrument before aggressive equity allocation.",
            "priority": "high",
            "deadline": "Month 2",
            "status": "planned",
            "planned_impact": {"reserve_corpus": 300000},
            "actual_impact": {},
            "created_at": now_str,
        },
        {
            "action_id": f"act_{uuid.uuid4().hex[:8]}",
            "planning_unit_id": planning_unit_id,
            "strategy_version_id": strategy_version_id,
            "title": "Annual Portfolio Rebalancing",
            "description": "Review equity-debt asset allocation drift and adjust contributions.",
            "priority": "medium",
            "deadline": "Year 1",
            "status": "planned",
            "planned_impact": {"target_equity_pct": 70, "target_debt_pct": 30},
            "actual_impact": {},
            "created_at": now_str,
        },
    ]

    results = []
    for d in defaults:
        _action_repo.save_action(d)
        results.append(ActionPlanItemSchema(**d))
    return results


@router.get("/actions/{action_id}", response_model=ActionPlanItemSchema)
@router.get("/api/action-plan/actions/{action_id}", response_model=ActionPlanItemSchema, include_in_schema=False)
def get_action(
    action_id: str,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Retrieves an action by ID."""
    act = _action_repo.get_action(planning_unit_id, action_id)
    if not act:
        raise HTTPException(status_code=404, detail="Action not found")
    return ActionPlanItemSchema(
        action_id=act.get("action_id"),
        planning_unit_id=act.get("planning_unit_id", planning_unit_id),
        strategy_version_id=act.get("strategy_version_id", "sv_default"),
        title=act.get("title", ""),
        description=act.get("description"),
        priority=act.get("priority", "medium"),
        deadline=act.get("deadline"),
        status=act.get("status", "planned"),
        planned_impact=act.get("planned_impact", {}),
        actual_impact=act.get("actual_impact", {}),
        created_at=act.get("created_at", datetime.now(timezone.utc).isoformat()),
    )


@router.post("/actions", response_model=ActionPlanItemSchema)
@router.post("/api/action-plan/actions", response_model=ActionPlanItemSchema, include_in_schema=False)
def create_action(
    request: ActionCreateRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Creates a custom action item."""
    action_id = f"act_{uuid.uuid4().hex[:8]}"
    now_str = datetime.now(timezone.utc).isoformat()
    payload = {
        "action_id": action_id,
        "planning_unit_id": request.planning_unit_id,
        "strategy_version_id": request.strategy_version_id or "sv_default",
        "plan_id": request.plan_id or "plan_default",
        "action_type": request.action_type or "start_sip",
        "title": request.title,
        "description": request.description,
        "priority": request.priority or "medium",
        "deadline": request.deadline or request.target_date,
        "status": "pending" if request.plan_id else "planned",
        "planned_impact": request.planned_impact or {},
        "actual_impact": {},
        "created_at": now_str,
    }
    _action_repo.save_action(payload)
    return ActionPlanItemSchema(**payload)


@router.post("/actions/{action_id}/complete", response_model=ActionPlanItemSchema)
@router.post("/api/action-plan/actions/{action_id}/complete", response_model=ActionPlanItemSchema, include_in_schema=False)
def complete_action(
    action_id: str,
    request: ActionCompletionRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Marks an action as completed."""
    act = _action_repo.get_action(request.planning_unit_id, action_id)
    if not act:
        raise HTTPException(status_code=404, detail="Action not found")
    updated = _action_repo.update_action_status(
        request.planning_unit_id,
        action_id,
        "completed",
        metadata={"actual_impact": request.completion_preview},
    )
    return ActionPlanItemSchema(
        action_id=action_id,
        planning_unit_id=request.planning_unit_id,
        strategy_version_id=act.get("strategy_version_id", "sv_default"),
        title=act.get("title", ""),
        description=act.get("description"),
        priority=act.get("priority", "medium"),
        deadline=act.get("deadline"),
        status="completed",
        planned_impact=act.get("planned_impact", {}),
        actual_impact=request.completion_preview,
        created_at=act.get("created_at", datetime.now(timezone.utc).isoformat()),
    )


@router.get("/decisions", response_model=List[ActionDecisionRecord])
@router.get("/api/action-plan/decisions", response_model=List[ActionDecisionRecord], include_in_schema=False)
def list_decisions(
    planning_unit_id: str = Query(...),
    action_id: Optional[str] = Query(default=None),
    user_id: str = Depends(get_current_user_id),
):
    """Retrieves decision history records for actions."""
    recs = [
        d for d in _decision_history
        if d.get("planning_unit_id") == planning_unit_id
        and (not action_id or d.get("action_id") == action_id)
    ]
    return [ActionDecisionRecord(**r) for r in recs]


@router.post("/decisions", response_model=ActionDecisionResponse)
@router.post("/api/action-plan/decisions", response_model=ActionDecisionResponse, include_in_schema=False)
def confirm_decision(
    request: ActionDecisionInput,
    user_id: str = Depends(get_current_user_id),
):
    """Confirms an action decision and logs audit trail."""
    dec_id = f"dec_{uuid.uuid4().hex[:8]}"
    now_str = datetime.now(timezone.utc).isoformat()
    record = {
        "decision_id": dec_id,
        "planning_unit_id": request.planning_unit_id,
        "action_id": request.action_id,
        "decision": request.decision,
        "before_state": {},
        "after_state": request.after_state,
        "impact_preview": request.impact_preview,
        "confirmed_at": now_str,
        "historical": True,
    }
    _decision_history.append(record)
    return ActionDecisionResponse(
        decision_id=dec_id,
        action_id=request.action_id,
        decision=request.decision,
        confirmed_at=now_str,
        historical=True,
    )
