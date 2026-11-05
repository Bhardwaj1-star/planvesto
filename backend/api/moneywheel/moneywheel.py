from fastapi import APIRouter, Header

from api.auth import authenticate_user, verify_planning_unit_ownership
from data.moneywheel_repository import MoneywheelRepository
from schemas.moneywheel import MoneywheelCalculateRequest, MoneywheelResponse
from models.moneywheel import MoneywheelResult
from rules.moneywheel import CANONICAL_RATIO_KEYS, RULES
from services.financial_state_service import FinancialStateService
from services.moneywheel_service import MoneywheelService

router = APIRouter(prefix="/api/moneywheel", tags=["Moneywheel"])


def _service():
    return MoneywheelService(MoneywheelRepository())


@router.post("/calculate", response_model=MoneywheelResponse)
def calculate_moneywheel(request: MoneywheelCalculateRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    # Client-provided financial_state_snapshot is intentionally ignored.
    financial_state = FinancialStateService().current(request.planning_unit_id, "family")
    return MoneywheelResponse(result=_service().calculate_from_financial_state(financial_state))


def _unavailable_ratio(key: str) -> dict:
    rule = RULES[key]
    return {
        "key": key,
        "name": rule["name"],
        "value": None,
        "unit": rule["unit"],
        "status": "unavailable",
        "formula": rule["formula"],
        "explanation": "This signal was not available in the snapshot.",
        "available": False,
    }


def _canonical_ratios(rows: list[dict]) -> list[dict]:
    by_key = {str(row.get("key")): row for row in rows if isinstance(row, dict) and row.get("key")}
    normalized: list[dict] = []

    for key in CANONICAL_RATIO_KEYS:
        row = by_key.get(key)
        if row is None:
            row = _unavailable_ratio(key)
        normalized.append(row)

    return normalized


def _canonical_result(row: dict) -> MoneywheelResult:
    metadata = dict(row.get("metadata") or {})
    metadata["snapshot_id"] = row.get("snapshot_id")
    metadata.pop("rules", None)

    raw_ratios = row.get("ratios") or []
    ratios = _canonical_ratios(raw_ratios)

    return MoneywheelResult(
        planning_unit_id=row["planning_unit_id"],
        overall_status=row.get("overall_status"),
        ratios=ratios,
        rule_set_version=row["rule_set_version"],
        calculated_at=row["calculated_at"],
        metadata=metadata,
    )


@router.get("/latest/{planning_unit_id}")
def latest_moneywheel(planning_unit_id: str, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    row = _service().repository.get_latest(planning_unit_id)
    return _canonical_result(row) if row else None


@router.get("/history/{planning_unit_id}")
def moneywheel_history(planning_unit_id: str, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(planning_unit_id, user_id)
    return [_canonical_result(row) for row in _service().repository.get_history(planning_unit_id)]
