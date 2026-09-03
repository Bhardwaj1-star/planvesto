from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.strategy_service import save_strategy


router = APIRouter(prefix="/api/strategy", tags=["Strategy"])


class StrategyRequest(BaseModel):
    user_id: str
    name: str = ""
    email: str = ""

    goal_amount: float = Field(gt=0)
    time_horizon_years: int = Field(gt=0, le=100)
    current_corpus: float = Field(ge=0)
    monthly_investment: float = Field(ge=0)
    existing_investments: float = Field(ge=0)
    expected_annual_return: float = Field(ge=0, le=100)


@router.post("/build")
def build_strategy(request: StrategyRequest):
    try:
        result = save_strategy(
            user_id=request.user_id,
            name=request.name,
            email=request.email,
            goal_amount=request.goal_amount,
            time_horizon_years=request.time_horizon_years,
            current_corpus=request.current_corpus,
            monthly_investment=request.monthly_investment,
            existing_investments=request.existing_investments,
            expected_annual_return=request.expected_annual_return,
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )