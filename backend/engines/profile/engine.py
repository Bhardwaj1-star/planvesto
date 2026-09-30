from __future__ import annotations

from typing import Any

from engines.profile.behavioral import BehavioralRules
from engines.profile.constraints import ConstraintRules
from engines.profile.identity import build_identity_profile
from engines.profile.risk import build_risk_profile

ENGINE_VERSION = "profile-engine-v6"


def _metric(state: dict[str, Any], name: str) -> tuple[float | None, bool]:
    raw = state.get(name) or {}
    return raw.get("value"), bool(raw.get("available", False))


class ProfileEngine:
    """Resolve planning constraints from evidence; priorities never change authority."""

    def build(self, *, financial_state: dict[str, Any] | None,
              declared_constraints: list[dict[str, Any]] | None = None,
              observed_behavior: list[dict[str, Any]] | None = None,
              preferences: list[dict[str, Any]] | None = None,
              constraint_priorities: list[dict[str, Any]] | None = None,
              identity_evidence: list[dict[str, Any]] | None = None,
              assets: list[dict[str, Any]] | None = None,
              liabilities: list[dict[str, Any]] | None = None,
              goals: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        constraints: list[dict[str, Any]] = []
        behavioral_profile = BehavioralRules.resolve(observed_behavior or [])
        risk_profile = build_risk_profile(financial_state=financial_state, assets=assets, liabilities=liabilities, goals=goals)
        identity_profile = build_identity_profile(evidence=identity_evidence)

        for source, items in (("declared_constraint", declared_constraints or []),
                              ("observed_behavior", observed_behavior or []),
                              ("preference", preferences or [])):
            for item in items:
                normalized = BehavioralRules.normalize(item) if source == "observed_behavior" else ConstraintRules.normalize(item, source)  # type: ignore[arg-type]
                normalized["confidence"] = ConstraintRules.confidence(source, len(normalized["evidence"]))  # type: ignore[arg-type]
                constraints.append(normalized)

        if financial_state:
            income, income_ok = _metric(financial_state, "income_monthly")
            expenses, expenses_ok = _metric(financial_state, "expenses_monthly")
            surplus, surplus_ok = _metric(financial_state, "investable_surplus_monthly")
            reserve, reserve_ok = _metric(financial_state, "safety_reserve_months")
            emi, emi_ok = _metric(financial_state, "emi_burden_monthly")
            facts = []
            if surplus_ok and surplus is not None:
                facts.append(("monthly_investable_surplus", surplus, "INR/month", [{"field": "investable_surplus_monthly", "value": surplus}]))
            if reserve_ok and reserve is not None:
                facts.append(("safety_reserve_months", reserve, "months", [{"field": "safety_reserve_months", "value": reserve}]))
            if emi_ok and income_ok and income and income > 0 and emi is not None:
                facts.append(("debt_service_ratio", round(emi / income, 6), "ratio", [{"field": "emi_burden_monthly", "value": emi}, {"field": "income_monthly", "value": income}]))
            if expenses_ok and income_ok and income and income > 0 and expenses is not None:
                facts.append(("expense_ratio", round(expenses / income, 6), "ratio", [{"field": "expenses_monthly", "value": expenses}, {"field": "income_monthly", "value": income}]))
            for key, value, unit, evidence in facts:
                item = ConstraintRules.normalize({"key": key, "value": value, "unit": unit, "kind": "hard", "evidence": evidence}, "financial_state")
                item["confidence"] = ConstraintRules.confidence("financial_state", len(evidence))
                constraints.append(item)

        conflicts = ConstraintRules.conflicts(constraints)
        priorities = ConstraintRules.validate_priorities(constraints, constraint_priorities or [])
        priority_by_key = {item["key"]: item["rank"] for item in priorities}
        for item in constraints:
            item["priority_rank"] = priority_by_key.get(item["key"])

        return {
            "engine_version": ENGINE_VERSION,
            "constraints": constraints,
            "priorities": priorities,
            "conflicts": conflicts,
            "behavioral_profile": behavioral_profile,
            "risk_profile": risk_profile,
            "identity_profile": identity_profile,
            "unresolved_conflict_count": len(conflicts),
            "has_hard_constraints": any(c["kind"] == "hard" for c in constraints),
        }
