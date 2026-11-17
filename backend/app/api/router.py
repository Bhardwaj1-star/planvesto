"""
api/router.py
Central API router mounting all approved feature routers.
Mounts both canonical /api/v1/... and backward-compatible /api/... endpoints.
"""

from fastapi import APIRouter

from app.api.routers.goal_planner import router as goal_planner_router
from app.api.routers.financial_state import router as financial_state_router
from app.api.routers.moneywheel import router as moneywheel_router
from app.api.routers.strategy_builder import router as strategy_builder_router
from app.api.routers.action_plan import router as action_plan_router
from app.api.routers.dashboard import router as dashboard_router
from app.api.routers.diary import router as diary_router
from app.api.routers.reports import router as reports_router

api_router = APIRouter()

# 1. Canonical /api/v1/... routes
api_router.include_router(goal_planner_router, prefix="/api/v1/goals")
api_router.include_router(financial_state_router, prefix="/api/v1/financial-state")
api_router.include_router(moneywheel_router, prefix="/api/v1/moneywheel")
api_router.include_router(strategy_builder_router, prefix="/api/v1/strategy-builder")
api_router.include_router(strategy_builder_router, prefix="/api/v1/strategy")
api_router.include_router(action_plan_router, prefix="/api/v1/action-plan")
api_router.include_router(dashboard_router, prefix="/api/v1/dashboard")
api_router.include_router(diary_router, prefix="/api/v1/diary")
api_router.include_router(reports_router, prefix="/api/v1")

# 2. Backward-compatible /api/... routes for frontend
api_router.include_router(goal_planner_router, prefix="/api/goals")
api_router.include_router(financial_state_router, prefix="/api/financial-state")
api_router.include_router(moneywheel_router, prefix="/api/moneywheel")
api_router.include_router(strategy_builder_router, prefix="/api/strategy")
api_router.include_router(strategy_builder_router, prefix="/api/goal-funding")
api_router.include_router(action_plan_router, prefix="/api/action-plan")
api_router.include_router(dashboard_router, prefix="/api/dashboard")
api_router.include_router(diary_router, prefix="/api/diary")
api_router.include_router(reports_router, prefix="/api")

__all__ = ["api_router"]
