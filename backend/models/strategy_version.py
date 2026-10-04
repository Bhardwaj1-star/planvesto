from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

from models.strategy import StrategyArchitecture


StrategyVersionStatus = Literal["draft", "approved", "primary", "archived", "needs_review", "provisional"]


class StrategyVersion(BaseModel):
    """Immutable snapshot of an investor-specific strategy configuration.

    ``status`` is creation-time classification metadata, not a mutable lifecycle
    state. Approval and Primary status are represented by immutable approval
    snapshots and the current-primary pointer respectively. A version is never
    updated in place after insertion.
    """

    strategy_version_id: str | None = None
    planning_unit_id: str
    strategy_id: str
    version: int = Field(ge=1)
    parent_version: int | None = Field(default=None, ge=1)
    source: Literal["library", "investor_edit"] = "library"
    library_version: str
    implementation_version: str
    implementation_parameters: dict[str, Any] = Field(default_factory=dict)
    goal_id: str | None = None
    defined_goal_id: str | None = None
    defined_goal_version: int | None = Field(default=None, ge=1)
    architecture: StrategyArchitecture | None = None
    decision_snapshot: dict[str, Any] = Field(default_factory=dict)
    source_strategy_run_id: str | None = None
    status: StrategyVersionStatus = "draft"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @model_validator(mode="after")
    def validate_version(self) -> "StrategyVersion":
        if not self.planning_unit_id.strip():
            raise ValueError("planning_unit_id cannot be empty")
        if not self.strategy_id.strip():
            raise ValueError("strategy_id cannot be empty")
        if not self.library_version.strip():
            raise ValueError("library_version cannot be empty")
        if not self.implementation_version.strip():
            raise ValueError("implementation_version cannot be empty")
        if self.source == "investor_edit" and self.parent_version is None:
            raise ValueError("investor_edit versions require parent_version")
        goal_context = (self.goal_id, self.defined_goal_id, self.defined_goal_version)
        if any(value is not None for value in goal_context) and not all(
            value is not None for value in goal_context
        ):
            raise ValueError("Goal-bound Strategy Versions require Goal and DefinedGoal version context")
        if self.goal_id is not None and not self.goal_id.strip():
            raise ValueError("goal_id cannot be empty")
        if self.defined_goal_id is not None and not self.defined_goal_id.strip():
            raise ValueError("defined_goal_id cannot be empty")
        if self.goal_id is not None and (
            self.architecture is None
            or not self.source_strategy_run_id
        ):
            raise ValueError(
                "Goal-bound Strategy Versions require finalized architecture and StrategyRun provenance"
            )
        if self.architecture is not None and self.architecture.primary_strategy_id != self.strategy_id:
            raise ValueError("StrategyVersion architecture must use its primary strategy")
        return self
