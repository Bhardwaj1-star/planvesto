from __future__ import annotations

from typing import Any

ENGINE_VERSION = "profile-engine-v2"

SOURCE_PRIORITY = {
    "financial_state": 4,
    "observed_behavior": 3,
    "declared_constraint": 2,
    "preference": 1,
}


def _confidence(source: str, corroborated: bool = False) -> float:
    base = SOURCE_PRIORITY.get(source, 0) / 4.0
    return round(min(1.0, base + (0.15 if corroborated else 0.0)), 4)


def _constraint(
    key: str,
    value: Any,
    *,
    source: str,
    kind: str = "soft",
    evidence: list[dict[str, Any]] | None = None,
    valid: bool = True,
) -> dict[str, Any]:
    evidence = evidence or []
    return {
        "key": key,
        "value": value,
        "kind": kind,
        "source": source,
        "confidence": _confidence(source, len(evidence) > 1),
        "evidence": evidence,
        "valid": valid,
    }


def _metric(state: dict[str, Any], name: str) -> tuple[float | None, bool]:
    raw = state.get(name) or {}
    return raw.get("value"), bool(raw.get("available", False))


class ProfileEngine:
    """Resolve planning constraints from evidence; never infer personality labels."""

    def build(
        self,
        *,
        financial_state: dict[str, Any] | None,
        declared_constraints: list[dict[str, Any]] | None = None,
        observed_behavior: list[dict[str, Any]] | None = None,
        preferences: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        constraints: list[dict[str, Any]] = []
        conflicts: list[dict[str, Any]] = []

        for item in declared_constraints or []:
            constraints.append(_constraint(
                item["key"], item.get("value"), source="declared_constraint",
                kind=item.get("kind", "soft"), evidence=item.get("evidence", []),
            ))

        for item in observed_behavior or []:
            constraints.append(_constraint(
                item["key"], item.get("value"), source="observed_behavior",
                kind=item.get("kind", "soft"), evidence=item.get("evidence", []),
            ))

        for item in preferences or []:
            constraints.append(_constraint(
                item["key"], item.get("value"), source="preference",
                kind="soft", evidence=item.get("evidence", []),
            ))

        if financial_state:
            income, income_ok = _metric(financial_state, "income_monthly")
            expenses, expenses_ok = _metric(financial_state, "expenses_monthly")
            surplus, surplus_ok = _metric(financial_state, "investable_surplus_monthly")
            reserve, reserve_ok = _metric(financial_state, "safety_reserve_months")
            emi, emi_ok = _metric(financial_state, "emi_burden_monthly")

            if surplus_ok and surplus is not None:
                constraints.append(_constraint(
                    "monthly_investable_surplus", surplus, source="financial_state", kind="hard",
                    evidence=[{"field": "investable_surplus_monthly", "value": surplus}],
                ))
            if reserve_ok and reserve is not None:
                constraints.append(_constraint(
                    "safety_reserve_months", reserve, source="financial_state", kind="hard",
                    evidence=[{"field": "safety_reserve_months", "value": reserve}],
                ))
            if emi_ok and income_ok and income and income > 0 and emi is not None:
                constraints.append(_constraint(
                    "debt_service_ratio", round(emi / income, 6), source="financial_state", kind="hard",
                    evidence=[{"field": "emi_burden_monthly", "value": emi}, {"field": "income_monthly", "value": income}],
                ))
            if expenses_ok and income_ok and income and income > 0 and expenses is not None:
                constraints.append(_constraint(
                    "expense_ratio", round(expenses / income, 6), source="financial_state", kind="hard",
                    evidence=[{"field": "expenses_monthly", "value": expenses}, {"field": "income_monthly", "value": income}],
                ))

        # Conflicts are explicit. We never silently choose between competing declarations.
        grouped: dict[str, list[dict[str, Any]]] = {}
        for item in constraints:
            grouped.setdefault(item["key"], []).append(item)
        for key, items in grouped.items():
            values = {repr(item["value"]) for item in items if item["valid"]}
            if len(values) > 1:
                conflicts.append({
                    "key": key,
                    "status": "unresolved",
                    "constraint_ids": [f"{key}:{i}" for i in range(len(items))],
                    "reason": "Multiple evidence sources provide conflicting values.",
                })

        return {
            "engine_version": ENGINE_VERSION,
            "constraints": constraints,
            "conflicts": conflicts,
            "unresolved_conflict_count": len(conflicts),
            "has_hard_constraints": any(c["kind"] == "hard" for c in constraints),
        }
