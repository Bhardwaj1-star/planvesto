"""Authoritative Strategy Builder decision and scoring policy slots."""
from __future__ import annotations

from typing import Any
from rules.eligibility import EligibilityStatus

# Decision Scoring Benchmarks & Weights
INFEASIBLE_DECISION_SCORE: float = -1000.0

PRIMARY_GOAL_TYPE_MATCH_SCORE: float = 25.0
OTHER_GOAL_TYPE_MATCH_SCORE: float = 10.0
CHARACTERISTIC_MATCH_SCORE: float = 5.0

OPTIMAL_HORIZON_SCORE: float = 30.0
BASELINE_HORIZON_SCORE: float = 15.0

FEASIBILITY_PASS_SCORE: float = 15.0
FEASIBILITY_CONDITIONAL_SCORE: float = 8.0
FEASIBILITY_FAIL_SCORE: float = 0.0

TECHNIQUE_EXECUTION_MAX_SCORE: float = 10.0


def calculate_goal_fit_score(
    canonical_goal_type: str,
    applicable_types: list[str],
    applicable_characteristics: list[str],
    duration_years: float,
    funding_status: str,
    flexibility: str,
    priority: str,
) -> float:
    """Calculate goal fit score based on type alignment and goal characteristics."""
    types_clean = [t.strip().lower() for t in applicable_types]
    score = (
        PRIMARY_GOAL_TYPE_MATCH_SCORE
        if canonical_goal_type in types_clean
        else (OTHER_GOAL_TYPE_MATCH_SCORE if "other" in types_clean else 0.0)
    )

    chars = set(applicable_characteristics)
    funding_clean = funding_status.lower()
    if funding_clean in chars or funding_clean.replace(" ", "_") in chars:
        score += CHARACTERISTIC_MATCH_SCORE

    if duration_years >= 7 and "long_term" in chars:
        score += CHARACTERISTIC_MATCH_SCORE
    elif duration_years <= 5 and "near_term" in chars:
        score += CHARACTERISTIC_MATCH_SCORE

    if flexibility == "Fixed" and "fixed_timeline" in chars:
        score += CHARACTERISTIC_MATCH_SCORE

    if priority in ("Critical", "High") and "high_priority" in chars:
        score += CHARACTERISTIC_MATCH_SCORE

    return score


def calculate_horizon_fit_score(duration_years: float, strategy_id: str) -> float:
    """Calculate horizon alignment score for the strategy."""
    if (
        (duration_years >= 10 and strategy_id in ("strat-dynamic-accumulation", "strat-calibrated-growth"))
        or (4 <= duration_years < 10 and strategy_id in ("strat-calibrated-growth", "strat-high-liquidity-flex"))
        or (duration_years < 4 and strategy_id in ("strat-cap-preservation", "strat-high-liquidity-flex"))
    ):
        return OPTIMAL_HORIZON_SCORE
    return BASELINE_HORIZON_SCORE


def calculate_funding_fit_score(
    funding_status: str,
    total_liabilities: float,
    strategy_id: str,
) -> float:
    """Calculate funding fit score reflecting debt priority and funding state."""
    if funding_status == "Shortfall" and total_liabilities > 0 and strategy_id == "strat-debt-reduction":
        return 25.0
    if funding_status == "On Track" and strategy_id in ("strat-high-liquidity-flex", "strat-cap-preservation"):
        return 25.0
    if funding_status == "Shortfall" and strategy_id in ("strat-calibrated-growth", "strat-dynamic-accumulation"):
        return 20.0
    return 15.0


def calculate_feasibility_score(status: EligibilityStatus | str) -> float:
    """Calculate feasibility score from eligibility status."""
    val = status.value if hasattr(status, "value") else str(status)
    if val == "pass":
        return FEASIBILITY_PASS_SCORE
    if val == "conditional":
        return FEASIBILITY_CONDITIONAL_SCORE
    return FEASIBILITY_FAIL_SCORE


def calculate_component_score(
    rationale: list[str],
    supporting_strategy_ids: list[str],
) -> float:
    """Calculate component architecture fit score."""
    score = 0.0
    if any("activated by component metadata" in r for r in rationale):
        score += 10.0
    if supporting_strategy_ids:
        score += 5.0
    return score


def calculate_technique_execution_score(technique_outputs: list[dict[str, Any]] | None) -> float:
    """Score implementation readiness from executed technique outputs."""
    outputs = technique_outputs or []
    if not outputs:
        return 0.0
    points = {"calculated": 1.0, "insufficient_inputs": 0.5, "not_implemented": 0.0}
    raw = sum(points.get(str(item.get("status")), 0.0) for item in outputs)
    return round(min(TECHNIQUE_EXECUTION_MAX_SCORE, raw), 2)


def evaluate_decision_score(
    *,
    status: EligibilityStatus | str,
    goal_fit_score: float,
    horizon_fit_score: float,
    funding_fit_score: float,
    feasibility_score: float,
    component_fit_score: float,
    technique_execution_score: float = 0.0,
) -> float:
    """Evaluate total decision score. Returns INFEASIBLE_DECISION_SCORE if eligibility failed."""
    val = status.value if hasattr(status, "value") else str(status)
    if val == "fail":
        return INFEASIBLE_DECISION_SCORE
    return round(
        goal_fit_score + horizon_fit_score + funding_fit_score + feasibility_score + component_fit_score + technique_execution_score,
        2,
    )
