from typing import Any

from pydantic import Field
from schemas.base import StrictRequestModel


class StrategyEditRequest(StrictRequestModel):
    planning_unit_id: str = Field(min_length=1, max_length=100)
    strategy_id: str = Field(min_length=1, max_length=100)
    parent_version: int = Field(ge=1)
    implementation_parameters: dict[str, Any] = Field(default_factory=dict, max_length=100)


class StrategyEditResult(StrictRequestModel):
    strategy_id: str
    strategy_version_id: str
    strategy_version: int
    parent_version: int
    suitability_reassessment_required: bool = True
    approval_snapshot_required: bool = False
    primary_replacement_required: bool = False
