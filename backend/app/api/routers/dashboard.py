"""
api/routers/dashboard.py
FastAPI router for Dashboard aggregation endpoint.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_current_user_id
from app.infrastructure.persistence.repositories.investor_profile import InvestorProfileRepository
from app.infrastructure.persistence.repositories.goal_planner import GoalPlannerRepository

router = APIRouter(tags=["Dashboard"])
_profile_repo = InvestorProfileRepository()
_goal_repo = GoalPlannerRepository()


def _image_key(goal_type: Optional[str]) -> str:
    value = (goal_type or "").strip().lower()
    if "home" in value or "house" in value or "property" in value:
        return "home"
    if "education" in value or "college" in value:
        return "education"
    if "travel" in value or "vacation" in value:
        return "travel"
    if "retirement" in value:
        return "retirement"
    if "wedding" in value or "marriage" in value:
        return "wedding"
    if "business" in value:
        return "business"
    return "default"


@router.get("")
@router.get("/api/dashboard", include_in_schema=False)
def get_dashboard(
    planning_unit_id: str = Query(...),
    scope: str = Query(default="family"),
    investor_id: Optional[str] = Query(default=None),
    user_id: str = Depends(get_current_user_id),
):
    """
    Returns aggregated dashboard metrics including financial state and active goals.
    """
    # 1. Fetch financial state snapshot
    saved = _profile_repo.get_latest_financial_state_snapshot(planning_unit_id)
    metric_zero = {"value": 0.0, "available": True, "reason": None}

    if saved and "financial_state" in saved:
        fs_data = saved["financial_state"]
        financial_state_data = {
            "net_worth": fs_data.get("net_worth", metric_zero),
            "total_assets": fs_data.get("total_assets", metric_zero),
            "asset_breakdown": fs_data.get("asset_breakdown", []),
            "asset_allocation": fs_data.get("asset_allocation", []),
            "total_liabilities": fs_data.get("total_liabilities", metric_zero),
            "liability_breakdown": fs_data.get("liability_breakdown", []),
            "liability_allocation": fs_data.get("liability_allocation", []),
            "income_monthly": fs_data.get("income_monthly", metric_zero),
            "income_annual": fs_data.get("income_annual", metric_zero),
            "expenses_monthly": fs_data.get("expenses_monthly", metric_zero),
            "expenses_annual": fs_data.get("expenses_annual", metric_zero),
            "investable_surplus_monthly": fs_data.get("investable_surplus_monthly", metric_zero),
            "investable_surplus_annual": fs_data.get("investable_surplus_annual", metric_zero),
        }
    else:
        financial_state_data = {
            "net_worth": metric_zero,
            "total_assets": metric_zero,
            "asset_breakdown": [],
            "asset_allocation": [],
            "total_liabilities": metric_zero,
            "liability_breakdown": [],
            "liability_allocation": [],
            "income_monthly": metric_zero,
            "income_annual": metric_zero,
            "expenses_monthly": metric_zero,
            "expenses_annual": metric_zero,
            "investable_surplus_monthly": metric_zero,
            "investable_surplus_annual": metric_zero,
        }

    # 2. Fetch goals
    raw_goals = _goal_repo.list_goals(planning_unit_id)
    goals: List[Dict[str, Any]] = []

    for summary in raw_goals:
        goal_id = str(summary.get("goal_id", ""))
        defined = _goal_repo.get_latest_defined_goal(planning_unit_id, goal_id) if goal_id else None

        if defined and defined.get("status") == "Cancelled":
            continue

        if defined:
            target = float(defined.get("future_target", 0.0))
            projected = float(defined.get("projected_mapped_asset_value", 0.0))
            coverage = min(max((projected / target * 100) if target > 0 else 0.0, 0.0), 100.0)
            target_year = int(defined.get("target_year", 2030))
            target_month = int(defined.get("target_month", 1))
            goals.append({
                "goal_id": defined.get("goal_id", goal_id),
                "goal_name": defined.get("goal_name", summary.get("goal_name", "Goal")),
                "goal_type": defined.get("goal_type", "others"),
                "target_amount": target,
                "target_date": f"{target_year:04d}-{target_month:02d}-01",
                "priority": defined.get("priority", "Important"),
                "flexibility": defined.get("flexibility", "Flexible"),
                "funding_status": defined.get("funding_status", "Shortfall"),
                "funding_gap": float(defined.get("funding_gap", 0.0)),
                "projected_mapped_asset_value": projected,
                "coverage_percentage": round(coverage, 1),
                "image_key": _image_key(defined.get("goal_type")),
            })
        else:
            goals.append({
                "goal_id": goal_id,
                "goal_name": str(summary.get("goal_name") or "Goal"),
                "goal_type": "others",
                "target_amount": float(summary.get("target_amount") or 0.0),
                "target_date": str(summary.get("target_date") or ""),
                "priority": str(summary.get("priority") or "Important"),
                "flexibility": str(summary.get("flexibility") or "Flexible"),
                "funding_status": None,
                "funding_gap": None,
                "projected_mapped_asset_value": None,
                "coverage_percentage": None,
                "image_key": "default",
            })

    return {
        "planning_unit_id": planning_unit_id,
        "scope": scope,
        "financial_state": financial_state_data,
        "goals": goals,
    }
