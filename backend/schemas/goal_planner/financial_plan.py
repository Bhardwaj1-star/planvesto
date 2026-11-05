from pydantic import BaseModel, Field


class FinancialPlanBuildRequest(BaseModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    rule_overrides: dict[str, dict] | None = None
