from pydantic import BaseModel, Field
from typing import Literal


class PlanningOrchestrationRequest(BaseModel):
    planning_unit_id: str
    scope: Literal["family", "individual"] = "family"
    investor_id: str | None = None
    goal_version_ids: list[str] = Field(default_factory=list)
    strategy_version_id: str | None = None
