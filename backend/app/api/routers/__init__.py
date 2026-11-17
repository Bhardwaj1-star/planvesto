"""
api/routers/__init__.py
Feature routers module.
"""

from app.api.routers.goal_planner import router as goal_planner_router
from app.api.routers.financial_state import router as financial_state_router
from app.api.routers.moneywheel import router as moneywheel_router
from app.api.routers.strategy_builder import router as strategy_builder_router
from app.api.routers.action_plan import router as action_plan_router

__all__ = [
    "goal_planner_router",
    "financial_state_router",
    "moneywheel_router",
    "strategy_builder_router",
    "action_plan_router",
]
