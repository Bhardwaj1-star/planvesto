"""
api/routers/goal_planner.py
FastAPI router for Goal Planner endpoints.
"""

from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid
from fastapi import APIRouter, Depends, Header, HTTPException, Query

from app.api.dependencies import get_current_user_id
from app.api.schemas.financial_state import FinancialStateRequest
from app.domain.shared.value_objects import CalendarMonth
from app.api.routers.financial_state import _build_financial_state_snapshot
from app.api.schemas.goal_planner import (
    GoalCalculateRequest,
    GoalCreateRequest,
    GoalSummaryResponse,
    DefinedGoalResponse,
)
from app.domain.canonical.goal_taxonomy import CanonicalGoalId
from app.domain.shared.value_objects import Money, Rate
from app.domain.features.goal_planner.requirement import (
    GoalInstance,
    plan_goal_requirement,
)
from app.domain.features.goal_planner.feasibility import (
    evaluate_fund_feasibility,
)
from app.domain.canonical.financial_categories import CanonicalAssetCategoryId
from app.domain.features.investor_profile.financial_state.models import AssetRecord
from app.infrastructure.persistence.repositories.goal_planner import (
    GoalPlannerRepository,
)
from app.infrastructure.persistence.repositories.investor_profile import (
    InvestorProfileRepository,
)

router = APIRouter(tags=["Goal Planner"])
_goal_repo = GoalPlannerRepository()
_profile_repo = InvestorProfileRepository()



def _metric_amount(state: Dict[str, Any], key: str) -> Optional[Decimal]:
    raw = state.get(key)
    if isinstance(raw, dict):
        if raw.get("available") is False or raw.get("value") is None:
            return None
        raw = raw.get("value")
    if raw is None:
        return None
    try:
        return Decimal(str(raw))
    except Exception:
        return None


def _financial_feasibility_context(planning_unit_id: str, goal_id: Optional[str] = None, user_id: str = "") -> Dict[str, Any]:
    """Rebuild canonical Financial State from persisted onboarding facts before evaluation."""
    today = date.today()
    request = FinancialStateRequest(planning_unit_id=planning_unit_id, scope="family")
    _, rebuilt_state, _, _, _ = _build_financial_state_snapshot(
        request, user_id, today, CalendarMonth(year=today.year, month=today.month)
    )
    _profile_repo.save_financial_state_snapshot(
        planning_unit_id=planning_unit_id, scope="family", investor_id=None,
        snapshot=rebuilt_state,
    )
    saved = _profile_repo.get_latest_financial_state_snapshot(planning_unit_id, scope="family")
    state = (saved or {}).get("financial_state") or {}
    if not isinstance(state, dict) or not state:
        return {"available_monthly_surplus": None, "existing_goal_sip": Decimal("0"), "source": None}

    income = _metric_amount(state, "income_monthly")
    expenses = _metric_amount(state, "expenses_monthly")
    savings = _metric_amount(state, "monthly_savings_investments")
    if savings is None:
        savings = _metric_amount(state, "existing_monthly_investments")
    if savings is None:
        savings = _metric_amount(state, "existing_sips_monthly")
    sip_by_goal = state.get("existing_goal_sips_by_goal") or {}
    if savings is None and isinstance(sip_by_goal, dict) and sip_by_goal:
        savings = sum((Decimal(str(value or 0)) for value in sip_by_goal.values()), Decimal("0"))
    if savings is None and income is not None:
        savings_rate = _metric_amount(state, "savings_investment_rate")
        if savings_rate is not None:
            savings = income * savings_rate / Decimal("100")

    if income is not None and expenses is not None:
        available = income - expenses - (savings or Decimal("0"))
        source = "income_monthly - expenses_monthly - monthly_savings_investments"
    else:
        available = _metric_amount(state, "investable_surplus_monthly")
        source = "financial_state.investable_surplus_monthly" if available is not None else None

    existing_sip = Decimal(str(sip_by_goal.get(goal_id, 0) or 0)) if goal_id and isinstance(sip_by_goal, dict) else Decimal("0")
    if not existing_sip and goal_id:
        existing_sip = Decimal(str(state.get("existing_goal_sip_monthly", 0) or 0))

    return {
        "available_monthly_surplus": available,
        "existing_goal_sip": existing_sip,
        "source": source,
    }


def _apply_current_feasibility(defined: Dict[str, Any], planning_unit_id: str, user_id: str = "") -> Dict[str, Any]:
    """Refresh affordability against the latest Financial State without changing goal inputs."""
    context = _financial_feasibility_context(planning_unit_id, str(defined.get("goal_id", "")), user_id)
    surplus = context["available_monthly_surplus"]
    metadata = defined.get("version_metadata") or {}
    required = Decimal(str(
        defined.get("required_monthly_contribution")
        or metadata.get("required_monthly_contribution")
        or metadata.get("required_monthly_sip")
        or 0
    ))
    existing_sip = context["existing_goal_sip"] or Decimal(str(metadata.get("existing_goal_sip_monthly", 0) or 0))
    additional_required = max(Decimal("0"), required - existing_sip)
    funding_gap = Decimal(str(defined.get("funding_gap", 0) or 0))

    defined["available_monthly_surplus"] = surplus
    defined["required_monthly_contribution"] = required
    defined["additional_required_monthly_sip"] = additional_required
    defined["existing_goal_sip_monthly"] = existing_sip
    defined["feasibility_source"] = context["source"]

    if funding_gap <= 0:
        status, case = "feasible", "case_1_affordable"
        gap, increase_pct = Decimal("0"), Decimal("0")
        reason = "Eligible mapped assets cover the future goal target. No additional SIP is required."
    elif surplus is None:
        status, case = "unknown", None
        gap, increase_pct = None, None
        reason = "Financial State monthly income, expenses and available surplus are unavailable. Complete Financial State before assessing Fund Feasibility."
    else:
        gap = max(Decimal("0"), additional_required - surplus)
        increase_pct = (gap / surplus * Decimal("100")) if surplus > 0 else None
        if additional_required <= surplus:
            status, case = "feasible", "case_1_affordable"
            reason = "The additional SIP required fits within Available Monthly Surplus. The goal is affordable to fund, but is not yet achieved."
        elif surplus > 0:
            status, case = "constrained", "case_2_capacity_shortfall"
            reason = "Available Monthly Surplus is below the additional SIP required. Review Case 2A or Case 2B funding options."
        else:
            status, case = "infeasible", "case_2_capacity_shortfall"
            reason = "There is no positive Available Monthly Surplus for the additional SIP. Review Case 2A or supported Case 2B alternatives."

    defined["feasibility_status"] = status
    defined["fund_feasibility_case"] = case
    defined["surplus_gap"] = gap
    defined["required_surplus_increase_pct"] = increase_pct
    defined["feasibility_reason"] = reason
    defined["is_feasible_under_current_conditions"] = status == "feasible"
    defined["funding_strategies"] = [
        {
            "strategy_id": "sip", "strategy_type": "sip", "strategy_name": "SIP",
            "description": "Fund the remaining gap through additional monthly contributions.",
            "status": status, "required_lumpsum": 0,
            "required_monthly_contribution": float(additional_required),
            "starting_monthly_contribution": float(additional_required), "annual_step_up": None,
            "remaining_gap": float(funding_gap), "reason": reason,
            "constraints": [], "trade_offs": ["Affordability does not mean the goal is already achieved."],
        },
        {
            "strategy_id": "step_up_sip", "strategy_type": "step_up_sip", "strategy_name": "Step-Up SIP",
            "description": "Assess a planned annual increase in monthly contributions.",
            "status": "requires_investor_scenario", "required_lumpsum": 0,
            "required_monthly_contribution": float(additional_required),
            "starting_monthly_contribution": float(additional_required), "annual_step_up": None,
            "remaining_gap": float(funding_gap),
            "reason": "The investor must choose a step-up schedule; no assumed increase is applied.",
            "constraints": ["Verify that each future contribution increase is affordable."],
            "trade_offs": ["Higher future contributions reduce future disposable cash flow."],
        },
        {
            "strategy_id": "lumpsum_plus_sip", "strategy_type": "lumpsum_plus_sip", "strategy_name": "Lump Sum + SIP",
            "description": "Combine an investor-selected upfront amount with monthly contributions.",
            "status": "requires_investor_scenario", "required_lumpsum": 0,
            "required_monthly_contribution": float(additional_required),
            "starting_monthly_contribution": float(additional_required), "annual_step_up": None,
            "remaining_gap": float(funding_gap),
            "reason": "Select a verified, liquid and uncommitted asset and enter a proposed lump sum. No asset is assumed available automatically.",
            "constraints": ["Check liquidity, lock-ins, risk, suitability and competing goals."],
            "trade_offs": ["Using a lump sum reduces liquidity and may affect other goals."],
        },
    ]
    return defined

def _build_goal_instance(req: GoalCalculateRequest, goal_id: str, investor_id: str) -> GoalInstance:
    # Resolve canonical goal ID safely
    raw_type = (req.canonical_id or req.goal_type or "others").lower().strip()
    if not raw_type.startswith("goal_"):
        candidate = f"goal_{raw_type}"
    else:
        candidate = raw_type

    cid = CanonicalGoalId.OTHERS
    for c in CanonicalGoalId:
        if c.value == candidate or c.value == raw_type:
            cid = c
            break

    target_date = date(req.target_year, max(1, min(12, req.target_month)), 1)
    as_of = date.today()

    # Inflation rate normalization
    if req.inflation_rate_pct is not None:
        inflation_pct = req.inflation_rate_pct
    elif req.inflation_rate is not None:
        if req.inflation_rate <= Decimal("1.0"):
            inflation_pct = req.inflation_rate * Decimal("100.0")
        else:
            inflation_pct = req.inflation_rate
    else:
        inflation_pct = Decimal("6.0")

    mapped_assets: List[AssetRecord] = []
    for m in req.asset_mappings:
        val = m.current_value
        pct = m.allocation_percentage if m.allocation_percentage is not None else (m.allocation_value or Decimal("100.0"))
        mapped_assets.append(
            AssetRecord(
                id=m.asset_id,
                category=CanonicalAssetCategoryId.MUTUAL_FUNDS,
                name=m.asset_name or "Asset",
                value=Money.from_amount(val),
                as_of_date=as_of,
                ownership_share=Rate.from_percentage(pct),
                is_accessible=True,
                access_restrictions=[],
                is_committed=False,
                committed_goal_id=None,
            )
        )

    return GoalInstance(
        id=goal_id,
        investor_id=investor_id,
        canonical_id=cid,
        name=req.goal_name,
        target_date=target_date,
        current_cost=Money.from_amount(req.today_cost),
        applicable_inflation_rate=Rate.from_percentage(inflation_pct),
        expected_annual_return=Rate.from_percentage(req.expected_return_pct),
        created_at=as_of,
        mapped_assets=mapped_assets,
    )


def _build_defined_response(
    request: GoalCalculateRequest,
    goal: GoalInstance,
    goal_id: str,
    user_id: str,
) -> DefinedGoalResponse:
    as_of = date.today()
    context = _financial_feasibility_context(request.planning_unit_id, goal_id)
    raw_surplus = context["available_monthly_surplus"]
    surplus = Money.from_amount(raw_surplus if raw_surplus is not None else 0)
    goal.existing_goal_sip = Money.from_amount(context["existing_goal_sip"])
    feasibility = evaluate_fund_feasibility(goal, as_of, surplus)

    diff_days = (goal.target_date - as_of).days
    duration_years = max(Decimal("1.0"), Decimal(str(round(max(0, diff_days) / 365.25, 1))))

    funding_gap = feasibility.remaining_funding_gap.amount
    projected_assets = feasibility.projected_existing_funding.amount
    future_target = feasibility.future_goal_target.amount
    if funding_gap <= Decimal("0.0"):
        funding_status = "Overfunded"
    elif projected_assets >= future_target:
        funding_status = "On Track"
    else:
        funding_status = "Shortfall"

    feasibility_status = ("unknown" if raw_surplus is None else "feasible" if feasibility.is_feasible_under_current_conditions else "constrained" if raw_surplus > 0 else "infeasible")
    req_sip = feasibility.required_monthly_sip.amount if feasibility.required_monthly_sip else Decimal("0.0")

    clean_goal_type = request.goal_type or (goal.canonical_id.value.replace("goal_", "") if goal.canonical_id else "others")

    response = DefinedGoalResponse(
        goal_id=goal_id,
        defined_goal_id=str(uuid.uuid4()),
        planning_unit_id=request.planning_unit_id,
        goal_name=request.goal_name,
        goal_type=clean_goal_type,
        version=1,
        is_latest=True,
        today_cost=request.today_cost,
        future_target=future_target,
        funding_gap=funding_gap,
        projected_mapped_asset_value=projected_assets,
        required_monthly_sip=req_sip,
        required_monthly_contribution=req_sip,
        available_monthly_surplus=raw_surplus,
        additional_required_monthly_sip=max(Decimal("0"), req_sip - context["existing_goal_sip"]),
        surplus_gap=(max(Decimal("0"), max(Decimal("0"), req_sip - context["existing_goal_sip"]) - raw_surplus) if raw_surplus is not None else None),
        required_surplus_increase_pct=((max(Decimal("0"), max(Decimal("0"), req_sip - context["existing_goal_sip"]) - raw_surplus) / raw_surplus * Decimal("100")) if raw_surplus is not None and raw_surplus > 0 else None),
        fund_feasibility_case=("case_1_affordable" if funding_gap <= 0 or raw_surplus is not None and max(Decimal("0"), req_sip - context["existing_goal_sip"]) <= raw_surplus else "case_2_capacity_shortfall" if raw_surplus is not None else None),
        feasibility_reason=("Eligible mapped assets cover the future goal target." if funding_gap <= 0 else "Financial State monthly income, expenses and available surplus are unavailable. Complete Financial State before assessing Fund Feasibility." if raw_surplus is None else "The additional SIP required fits within Available Monthly Surplus. The goal is affordable to fund, but is not yet achieved." if feasibility_status == "feasible" else "Available Monthly Surplus is below the additional SIP required. Review Case 2A or Case 2B funding options."),
        feasibility_source=context["source"],
        existing_goal_sip_monthly=context["existing_goal_sip"],
        is_feasible_under_current_conditions=(feasibility_status == "feasible"),
        feasibility_status=feasibility_status,
        funding_status=funding_status,
        duration_years=duration_years,
        target_month=request.target_month,
        target_year=request.target_year,
        inflation_rate=goal.applicable_inflation_rate.percentage,
        flexibility=request.flexibility,
        status=request.status,
        priority=request.priority if isinstance(request.priority, str) else "Important",
        explanation=feasibility.explanation,
        version_metadata={
            "dynamic_details": request.dynamic_details or {},
            "required_monthly_contribution": str(req_sip),
            "required_monthly_sip": str(req_sip),
            "existing_goal_sip_monthly": str(context["existing_goal_sip"]),
            "available_monthly_surplus": str(raw_surplus) if raw_surplus is not None else None,
            "feasibility_status": feasibility_status,
        },
        mapped_assets=[
            {
                "asset_id": m.asset_id,
                "asset_name": m.asset_name or "Asset",
                "allocation_type": m.allocation_type or "percentage",
                "allocation_value": float(m.allocation_value or 100),
                "allocated_amount": float(m.current_value),
                "allocated_percentage": float(m.allocation_percentage or 100),
                "expected_return": float(m.expected_annual_return_pct or 10),
                "return_frequency": m.return_frequency or "annual",
                "projected_value": 0.0,
            }
            for m in request.asset_mappings
        ],
    )
    return DefinedGoalResponse(**_apply_current_feasibility(response.model_dump(), request.planning_unit_id, user_id))


@router.get("", response_model=List[GoalSummaryResponse])
@router.get("/api/goals", response_model=List[GoalSummaryResponse], include_in_schema=False)
def list_goals(
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """List all goals for the given planning unit."""
    rows = _goal_repo.list_goals(planning_unit_id)
    results = []
    for r in rows:
        results.append(
            GoalSummaryResponse(
                goal_id=str(r.get("goal_id", "")),
                planning_unit_id=str(r.get("planning_unit_id", planning_unit_id)),
                goal_name=str(r.get("goal_name", "")),
                target_amount=Decimal(str(r.get("target_amount", 0))),
                target_date=str(r.get("target_date", "")),
                priority=int(r.get("priority", 1)) if str(r.get("priority", "")).isdigit() else 1,
                flexibility=str(r.get("flexibility", "Flexible")),
            )
        )
    return results


@router.get("/{goal_id}/defined/latest")
@router.get("/api/goals/{goal_id}/defined/latest", include_in_schema=False)
def get_latest_defined_goal(
    goal_id: str,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Retrieve the latest defined goal state for a specific goal."""
    defined = _goal_repo.get_latest_defined_goal(planning_unit_id, goal_id)
    if defined:
        return _apply_current_feasibility(defined, planning_unit_id, user_id)

    # If no defined record yet, fetch basic goal and evaluate default feasibility
    goal_raw = _goal_repo.get_goal(planning_unit_id, goal_id)
    if not goal_raw:
        # Return fallback defined goal shape so frontend doesn't crash
        return {
            "defined_goal_id": f"def_{goal_id}",
            "goal_id": goal_id,
            "planning_unit_id": planning_unit_id,
            "version": 1,
            "is_latest": True,
            "goal_name": "Goal",
            "goal_type": "others",
            "today_cost": 0.0,
            "future_target": 0.0,
            "funding_gap": 0.0,
            "funding_status": "Shortfall",
            "feasibility_status": "unknown",
            "feasibility_reason": "Goal details pending",
            "available_monthly_surplus": None,
            "required_monthly_contribution": 0.0,
            "target_month": 1,
            "target_year": date.today().year + 5,
            "duration_years": 5.0,
            "inflation_rate": 6.0,
            "mapped_assets": [],
        }

    # Evaluate using domain
    today_cost = float(goal_raw.get("target_amount", 0))
    target_date_str = str(goal_raw.get("target_date", f"{date.today().year + 5}-01-01"))
    try:
        t_date = date.fromisoformat(target_date_str[:10])
    except Exception:
        t_date = date(date.today().year + 5, 1, 1)

    fallback = {
        "defined_goal_id": f"def_{goal_id}",
        "goal_id": goal_id,
        "planning_unit_id": planning_unit_id,
        "version": 1,
        "is_latest": True,
        "goal_name": str(goal_raw.get("goal_name", "Goal")),
        "goal_type": "others",
        "today_cost": today_cost,
        "future_target": today_cost * 1.33,
        "funding_gap": today_cost * 1.33,
        "funding_status": "Shortfall",
        "feasibility_status": "feasible" if today_cost == 0 else "constrained",
        "feasibility_reason": "Preliminary calculation from saved goal",
        "available_monthly_surplus": 0.0,
        "required_monthly_contribution": round((today_cost * 1.33) / 60.0, 2),
        "target_month": t_date.month,
        "target_year": t_date.year,
        "duration_years": max(1, t_date.year - date.today().year),
        "inflation_rate": 6.0,
        "mapped_assets": [],
    }
    return _apply_current_feasibility(fallback, planning_unit_id, user_id)


@router.get("/{goal_id}/defined/versions")
@router.get("/api/goals/{goal_id}/defined/versions", include_in_schema=False)
def get_defined_goal_versions(
    goal_id: str,
    planning_unit_id: str = Query(...),
    user_id: str = Depends(get_current_user_id),
):
    """Retrieve version history for a defined goal."""
    latest = get_latest_defined_goal(goal_id, planning_unit_id, user_id)
    return [
        {
            "defined_goal_id": latest.get("defined_goal_id", f"def_{goal_id}"),
            "goal_id": goal_id,
            "version": latest.get("version", 1),
            "is_latest": True,
            "today_cost": latest.get("today_cost", 0),
            "future_target": latest.get("future_target", 0),
            "projected_mapped_asset_value": 0,
            "funding_gap": latest.get("funding_gap", 0),
            "funding_status": latest.get("funding_status", "Shortfall"),
            "created_at": date.today().isoformat(),
        }
    ]


@router.post("/calculate", response_model=DefinedGoalResponse)
@router.post("/api/goals/calculate", response_model=DefinedGoalResponse, include_in_schema=False)
def calculate_goal_preview(
    request: GoalCalculateRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Calculates goal requirement and fund feasibility preview using Chapter 10 domain logic."""
    temp_id = request.goal_id or str(uuid.uuid4())
    goal = _build_goal_instance(request, temp_id, user_id)
    return _build_defined_response(request, goal, temp_id, user_id)


@router.post("", response_model=DefinedGoalResponse)
@router.post("/api/goals", response_model=DefinedGoalResponse, include_in_schema=False)
def save_goal(
    request: GoalCreateRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Saves and defines a goal using Chapter 10 domain evaluation."""
    goal_id = request.goal_id or str(uuid.uuid4())
    goal = _build_goal_instance(request, goal_id, user_id)
    resp = _build_defined_response(request, goal, goal_id, user_id)

    # Persist goal record
    _goal_repo.ensure_goal_record(
        planning_unit_id=request.planning_unit_id,
        goal_id=goal_id,
        goal_name=request.goal_name,
        today_cost=float(request.today_cost),
        target_month=request.target_month,
        target_year=request.target_year,
        priority=str(request.priority),
        flexibility=request.flexibility,
    )

    # Persist defined goal record
    _goal_repo.save_defined_goal(
        planning_unit_id=request.planning_unit_id,
        defined_goal_payload=resp.model_dump(),
    )

    return resp
