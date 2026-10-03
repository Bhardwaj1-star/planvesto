from fastapi import APIRouter, Header

from api.auth import authenticate_user, verify_planning_unit_ownership
from data.moneywheel_repository import MoneywheelRepository
from schemas.moneywheel import MoneywheelCalculateRequest, MoneywheelResponse
from models.moneywheel import MoneywheelResult
from rules.moneywheel import RULES, RULE_DEFINITIONS
from services.financial_state_service import FinancialStateService
from services.moneywheel_service import MoneywheelService

router = APIRouter(prefix="/api/moneywheel", tags=["Moneywheel"])

_CANONICAL_RATIO_KEYS = (
    "savings_rate",
    "liquid_asset_ratio",
    "debt_to_income_ratio",
    "leverage_ratio",
    "financial_asset_ratio",
    "insurance_coverage_ratio",
    "goal_funding_ratio",
    "future_funding_ratio",
    "required_rate_of_return",
)

_LEGACY_RATIO_ALIASES = {
    "savings_ratio": "savings_rate",
    "liquid_asset_to_total_asset": "liquid_asset_ratio",
    "insurance_gap_ratio": "insurance_coverage_ratio",
}


def _service():
    return MoneywheelService(MoneywheelRepository())


@router.post("/calculate", response_model=MoneywheelResponse)
def calculate_moneywheel(request: MoneywheelCalculateRequest, authorization: str | None = Header(default=None)):
    user_id = authenticate_user(authorization)
    verify_planning_unit_ownership(request.planning_unit_id, user_id)
    # Client-provided financial_state_snapshot is intentionally ignored.
    financial_state = FinancialStateService().build(request.planning_unit_id, "family")
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
        "explanation": "This signal was not stored in the legacy Moneywheel snapshot.",
        "available": False,
    }


def _canonical_ratios(rows: list[dict]) -> tuple[list[dict], list[str]]:
    by_key = {str(row.get("key")): row for row in rows if isinstance(row, dict) and row.get("key")}
    normalized: list[dict] = []
    legacy_keys: list[str] = []

    for key in _CANONICAL_RATIO_KEYS:
        row = by_key.get(key)
        if row is None:
            for legacy_key, canonical_key in _LEGACY_RATIO_ALIASES.items():
                if canonical_key == key and legacy_key in by_key:
                    row = dict(by_key[legacy_key])
                    row["key"] = key
                    legacy_keys.append(legacy_key)
                    break
        if row is None:
            row = _unavailable_ratio(key)

        normalized.append(row)

    return normalized, legacy_keys


def _rule_from_ratio(row: dict, key: str) -> dict:
    definition = RULE_DEFINITIONS[key]
    return {
        "key": key,
        "name": definition["name"],
        "value": row.get("value"),
        "unit": definition["unit"],
        "formula": definition["formula"],
        "explanation": row.get("explanation") or "Coverage was stored in the legacy Moneywheel snapshot.",
        "available": bool(row.get("available", row.get("value") is not None)),
    }


def _unavailable_rule(key: str, reason: str) -> dict:
    definition = RULE_DEFINITIONS[key]
    return {
        "key": key,
        "name": definition["name"],
        "value": None,
        "unit": definition["unit"],
        "formula": definition["formula"],
        "explanation": reason,
        "available": False,
    }


def _canonical_rules(rows: list[dict], metadata: dict) -> tuple[list[dict], bool]:
    stored_rules = metadata.pop("rules", None)
    if isinstance(stored_rules, list) and len(stored_rules) == 2:
        return stored_rules, False

    by_key = {str(row.get("key")): row for row in rows if isinstance(row, dict) and row.get("key")}
    rules: list[dict] = []

    expense_source = by_key.get("expense_coverage") or by_key.get("emergency_fund_coverage")
    if expense_source is not None:
        rules.append(_rule_from_ratio(expense_source, "expense_coverage"))
    else:
        rules.append(_unavailable_rule("expense_coverage", "Legacy snapshot did not store expense coverage."))

    emergency_source = by_key.get("emergency_coverage")
    if emergency_source is not None:
        rules.append(_rule_from_ratio(emergency_source, "emergency_coverage"))
    else:
        rules.append(
            _unavailable_rule(
                "emergency_coverage",
                "Legacy snapshot did not store essential-expense emergency coverage separately.",
            )
        )

    return rules, True


def _canonical_result(row: dict) -> MoneywheelResult:
    metadata = dict(row.get("metadata") or {})
    metadata["snapshot_id"] = row.get("snapshot_id")

    raw_ratios = row.get("ratios") or []
    ratios, legacy_ratio_keys = _canonical_ratios(raw_ratios)
    rules, rules_reconstructed = _canonical_rules(raw_ratios, metadata)

    if legacy_ratio_keys or rules_reconstructed:
        metadata["legacy_normalization"] = {
            "applied": True,
            "legacy_ratio_keys": legacy_ratio_keys,
            "rules_reconstructed": rules_reconstructed,
        }

    return MoneywheelResult(
        planning_unit_id=row["planning_unit_id"],
        overall_status=row.get("overall_status"),
        ratios=ratios,
        rules=rules,
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
