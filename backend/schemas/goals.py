from typing import Any, Literal

from pydantic import Field, model_validator

from schemas.base import StrictRequestModel


class AssetMappingInput(StrictRequestModel):
    asset_id: str = Field(min_length=1, max_length=100)
    allocation_type: Literal["currency", "percentage"]
    allocation_value: float = Field(ge=0, allow_inf_nan=False)
    expected_return: float | None = Field(default=None, ge=-0.99, le=1.0, allow_inf_nan=False)
    return_frequency: Literal["annual", "semi-annual", "semiannual", "half-yearly", "quarterly", "monthly"] = "annual"

    @model_validator(mode="after")
    def validate_allocation(self):
        if self.allocation_type == "percentage" and self.allocation_value > 100:
            raise ValueError("Percentage allocation cannot exceed 100")
        return self


class GoalInput(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    goal_id: str | None = Field(default=None, min_length=1, max_length=100)
    investor_id: str | None = Field(default=None, min_length=1, max_length=100)
    goal_name: str = Field(min_length=1, max_length=200)
    goal_type: str = Field(min_length=1, max_length=100)
    today_cost: float = Field(gt=0, allow_inf_nan=False)
    target_month: int = Field(ge=1, le=12)
    target_year: int = Field(ge=1900, le=2200)
    inflation_rate: float | None = Field(default=None, ge=0, le=1, allow_inf_nan=False)
    priority: str = Field(default="Important", min_length=1, max_length=50)
    flexibility: str = Field(default="Flexible", min_length=1, max_length=50)
    status: str = Field(default="Active", min_length=1, max_length=30)
    asset_mappings: list[AssetMappingInput] = Field(default_factory=list, max_length=100)
    specialized_data: dict[str, Any] = Field(default_factory=dict)


class GoalCalculateRequest(GoalInput):
    pass


class GoalSummary(StrictRequestModel):
    goal_id: str = Field(min_length=1, max_length=100)
    planning_unit_id: str = Field(min_length=1, max_length=100)
    goal_name: str = Field(min_length=1, max_length=200)
    target_amount: float = Field(allow_inf_nan=False)
    target_date: str | None = None
    priority: str | None = None
    flexibility: str | None = None
