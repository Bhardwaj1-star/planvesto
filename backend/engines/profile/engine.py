from __future__ import annotations

from typing import Any

from engines.profile.constraints import ConstraintRules

ENGINE_VERSION = "profile-engine-v3"


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

        for source, items in (
            ("declared_constraint", declared_constraints or []),
            ("observed_behavior", observed_behavior or []),
            ("preference", preferences or []),
        ):
            for item in items:
                normalized = ConstraintRules.normalize(item, source)  # type: ignore[arg-type]
                normalized["confidence"] = ConstraintRules.confidence(source, len(normalized["evidence"]))  # type: ignore[arg-type]
                constraints.append(normalized)

        if financial_state:
            income, income_ok = _metric(financial_state, "income_monthly")
            expenses, expenses_ok = _metric(financial_state, "expenses_monthly")
            surplus, surplus_ok = _metric(financial_state, "investable_surplus_monthly")
            reserve, reserve_ok = _metric(financial_state, "safety_reserve_months")
            emi, emi_ok = _metric(financial_state, "emi_burden_monthly")

            if surplus_ok and surplus is not None:
                constraints.append(ConstraintRules.normalize({
                    "key": "monthly_investable_surplus", "value": surplus, "unit": "INR/month",
                    "kind": "hard", "evidence": [{"field": "investable_surplus_monthly", "value": surplus}],
                }, "financial_state"))
            if reserve_ok and reserve is not None:
                constraints.append(ConstraintRules.normalize({
                    "key": "safety_reserve_months", "value": reserve, "unit": "months",
                    "kind": "hard", "evidence": [{"field": "safety_reserve_months", "value": reserve}],
                }, "financial_state"))
            if emi_ok and income_ok and income and income > 0 and emi is not None:
                constraints.append(ConstraintRules.normalize({
                    "key": "debt_service_ratio", "value": round(emi / income, 6), "unit": "ratio",
                    "kind": "hard", "evidence": [{"field": "emi_burden_monthly", "value": emi}, {"field": "income_monthly", "value": income}],
                }, "financial_state"))
            if expenses_ok and income_ok and income and income > 0 and expenses is not None:
                constraints.append(ConstraintRules.normalize({
                    "key": "expense_ratio", "value": round(expenses / income, 6), "unit": "ratio",
                    "kind": "hard", "evidence": [{"field": "expenses_monthly", "value": expenses}, {"field": "income_monthly", "value": income}],
                }, "financial_state"))

            for item in constraints:
                if item["source"] == "financial_state":
                    item["confidence"] = ConstraintRules.confidence("financial_state", len(item["evidence"]))

        conflicts = ConstraintRules.conflicts(constraints)
        return {
            "engine_version": ENGINE_VERSION,
            "constraints": constraints,
            "conflicts": conflicts,
            "unresolved_conflict_count": len(conflicts),
            "has_hard_constraints": any(c["kind"] == "hard" for c in constraints),
        }
