from __future__ import annotations

from typing import Any

ENGINE_VERSION = "profile-engine-v1"

RISK_WEIGHTS = {
    "loss_reaction": 0.30,
    "volatility_comfort": 0.25,
    "capital_stability": 0.20,
    "investment_experience": 0.15,
    "time_horizon_comfort": 0.10,
}
BEHAVIOR_WEIGHTS = {
    "loss_reaction": 0.30,
    "decision_discipline": 0.25,
    "recency_resistance": 0.20,
    "herding_resistance": 0.15,
    "plan_adherence": 0.10,
}
IDENTITY_WEIGHTS = {
    "goal_orientation": 0.35,
    "planning_orientation": 0.25,
    "decision_ownership": 0.20,
    "investment_experience": 0.20,
}


def _band(score: float) -> str:
    if score < 25:
        return "low"
    if score < 50:
        return "moderate-low"
    if score < 75:
        return "moderate-high"
    return "high"


def _score(answers: dict[str, float], weights: dict[str, float]) -> tuple[float, dict[str, float], list[str], float]:
    supplied = {k: float(v) for k, v in answers.items() if k in weights}
    total_weight = sum(weights[k] for k in supplied)
    if not supplied or total_weight <= 0:
        return 0.0, {}, ["Insufficient questionnaire data"], 0.0
    components = {k: round((v / 4.0) * 100.0 * weights[k], 4) for k, v in supplied.items()}
    score = round(sum(components.values()) / total_weight, 4)
    confidence = round(total_weight, 4)
    missing = [k for k in weights if k not in supplied]
    explanations = [f"{k}: {round(answers[k], 2)}/4" for k in supplied]
    if missing:
        explanations.append(f"Missing inputs: {', '.join(missing)}")
    return score, components, explanations, confidence


def _metric(state: dict[str, Any], name: str) -> tuple[float | None, bool]:
    raw = state.get(name) or {}
    return raw.get("value"), bool(raw.get("available", False))


def _capacity(financial_state: dict[str, Any] | None) -> tuple[float, dict[str, float], list[str], float]:
    if not financial_state:
        return 0.0, {}, ["Financial state unavailable; capacity cannot be established"], 0.0

    income, income_ok = _metric(financial_state, "income_monthly")
    savings_rate, savings_ok = _metric(financial_state, "savings_investment_rate")
    reserve, reserve_ok = _metric(financial_state, "safety_reserve_months")
    expenses, expenses_ok = _metric(financial_state, "expenses_monthly")
    emi, emi_ok = _metric(financial_state, "emi_burden_monthly")

    parts: dict[str, float] = {}
    if savings_ok and savings_rate is not None:
        parts["savings_rate"] = max(0.0, min(100.0, float(savings_rate) * 5.0))
    if reserve_ok and reserve is not None:
        parts["reserve"] = max(0.0, min(100.0, float(reserve) / 12.0 * 100.0))
    if emi_ok and income_ok and emi is not None and income and income > 0:
        parts["debt_service"] = max(0.0, min(100.0, (1.0 - float(emi) / float(income) / 0.50) * 100.0))
    if expenses_ok and income_ok and expenses is not None and income and income > 0:
        parts["cash_flow_headroom"] = max(0.0, min(100.0, (1.0 - float(expenses) / float(income)) * 100.0 * 2.0))

    if not parts:
        return 0.0, {}, ["Financial capacity inputs are unavailable"], 0.0
    score = round(sum(parts.values()) / len(parts), 4)
    explanations = [f"{k}: {round(v, 2)}/100" for k, v in parts.items()]
    return score, parts, explanations, round(len(parts) / 4.0, 4)


class ProfileEngine:
    def build(
        self,
        *,
        financial_state: dict[str, Any] | None,
        risk_tolerance_answers: dict[str, float],
        behavioral_answers: dict[str, float],
        identity_answers: dict[str, float],
    ) -> dict[str, Any]:
        capacity_score, capacity_components, capacity_explanations, capacity_confidence = _capacity(financial_state)
        tolerance_score, tolerance_components, tolerance_explanations, tolerance_confidence = _score(risk_tolerance_answers, RISK_WEIGHTS)
        behavior_score, behavior_components, behavior_explanations, behavior_confidence = _score(behavioral_answers, BEHAVIOR_WEIGHTS)
        identity_score, identity_components, identity_explanations, identity_confidence = _score(identity_answers, IDENTITY_WEIGHTS)

        completeness = round((capacity_confidence + tolerance_confidence + behavior_confidence + identity_confidence) / 4.0, 4)
        return {
            "risk_capacity": {"key": "risk_capacity", "score": capacity_score, "band": _band(capacity_score), "confidence": capacity_confidence, "components": capacity_components, "explanations": capacity_explanations},
            "risk_tolerance": {"key": "risk_tolerance", "score": tolerance_score, "band": _band(tolerance_score), "confidence": tolerance_confidence, "components": tolerance_components, "explanations": tolerance_explanations},
            "behavioral_profile": {"key": "behavioral_profile", "score": behavior_score, "band": _band(behavior_score), "confidence": behavior_confidence, "components": behavior_components, "explanations": behavior_explanations},
            "investor_identity": {"key": "investor_identity", "score": identity_score, "band": _band(identity_score), "confidence": identity_confidence, "components": identity_components, "explanations": identity_explanations},
            "completeness": completeness,
            "engine_version": ENGINE_VERSION,
        }
