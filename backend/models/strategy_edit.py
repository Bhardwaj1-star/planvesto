from typing import Any

from pydantic import BaseModel, Field


class StrategyEditRequest(BaseModel):
    planning_unit_id: str
    strategy_id: str
    parent_version: int = Field(ge=1)
    implementation_parameters: dict[str, Any] = Field(default_factory=dict)


class StrategyEditResult(BaseModel):
    strategy_id: str
    strategy_version_id: str
    strategy_version: int
    parent_version: int
    suitability_reassessment_required: bool = True
    approval_snapshot_required: bool = False
    primary_replacement_required: bool = False
