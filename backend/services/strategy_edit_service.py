from fastapi import HTTPException

from data.primary_strategy_repository import PrimaryStrategyRepository
from data.strategy_version_repository import StrategyVersionRepository
from models.strategy_edit import StrategyEditRequest, StrategyEditResult
from services.strategy_version_service import StrategyVersionService


class StrategyEditService:
    """Creates a new immutable Strategy Version for an investor edit.

    Suitability is deliberately reassessed downstream; this service does not
    invent financial suitability rules.
    """

    def __init__(self, version_repository: StrategyVersionRepository):
        self.version_repository = version_repository
        self.version_service = StrategyVersionService(version_repository)
        self.primary_repository = PrimaryStrategyRepository(version_repository.client)

    def edit_strategy(self, request: StrategyEditRequest) -> StrategyEditResult:
        parent = self.version_repository.get_version(
            request.planning_unit_id, request.strategy_id, request.parent_version
        )
        if parent is None:
            raise HTTPException(status_code=404, detail="Parent Strategy Version not found")

        version = self.version_service.create_version(
            planning_unit_id=request.planning_unit_id,
            strategy_id=request.strategy_id,
            parameters=request.implementation_parameters,
            parent_version=request.parent_version,
            source="investor_edit",
            status="approved" if parent.status in {"approved", "primary"} else "draft",
        )

        current = self.primary_repository.get_current(request.planning_unit_id)
        is_primary = bool(current and current.strategy_version_id == parent.strategy_version_id)

        return StrategyEditResult(
            strategy_id=version.strategy_id,
            strategy_version_id=version.strategy_version_id or "",
            strategy_version=version.version,
            parent_version=request.parent_version,
            suitability_reassessment_required=True,
            approval_snapshot_required=False,
            primary_replacement_required=is_primary,
        )
