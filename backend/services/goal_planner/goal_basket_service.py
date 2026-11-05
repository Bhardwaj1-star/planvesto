from __future__ import annotations

from data.goal_repository import GoalRepository
from engines.basket.engine import GoalBasketEngine
from models.goal_basket import GoalBasket, GoalBasketSummary


class GoalBasketService:
    def __init__(self, goal_repo: GoalRepository | None = None, engine: GoalBasketEngine | None = None):
        self.goal_repo = goal_repo or GoalRepository()
        self.engine = engine or GoalBasketEngine()

    def build_basket_summary(self, basket: GoalBasket) -> GoalBasketSummary:
        goals = self.goal_repo.list_goals(basket.planning_unit_id)
        return self.engine.build_summary(basket, goals)
