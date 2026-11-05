from fastapi import APIRouter, Header

from api.auth import authenticate_user, verify_planning_unit_ownership
from models.goal_basket import GoalBasket
from schemas.goal_basket import GoalBasketBuildRequest, GoalBasketResponse
from services.goal_basket_service import GoalBasketService

router = APIRouter(prefix="/api/goal-baskets", tags=["Goal Baskets"])


@router.post("/preview", response_model=GoalBasketResponse)
def preview_goal_basket(request: GoalBasketBuildRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)

    basket = GoalBasket(
        basket_id=request.basket_id,
        planning_unit_id=request.planning_unit_id,
        name=request.name,
        description=request.description,
        goal_ids=request.goal_ids,
        priority=request.priority,
    )
    summary = GoalBasketService().build_basket_summary(basket)
    return GoalBasketResponse(
        basket_id=basket.basket_id,
        planning_unit_id=basket.planning_unit_id,
        name=basket.name,
        description=basket.description,
        goal_ids=summary.goal_ids,
        goal_count=summary.goal_count,
        goal_names=summary.goal_names,
        priorities=summary.priorities,
        total_required_monthly_contribution=summary.total_required_monthly_contribution,
        total_funding_gap=summary.total_funding_gap,
    )
