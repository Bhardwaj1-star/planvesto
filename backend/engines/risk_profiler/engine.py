"""Authoritative Risk Profiler Engine.

Locked Architecture:
    Canonical Risk Required + Risk Capacity + Risk Tolerance -> RiskProfile / RiskBoundary -> Investment Engine

Guarantees:
  1. Risk Required is consumed from the canonical financial calculation layer; never locally recalculated.
  2. Risk Capacity is a structured assessment derived from observable financial constraints (surplus, reserve, debt service, concentration, liabilities).
  3. Risk Tolerance reuses BehavioralRules and observed dimensions (soft, product selection only); never converts observations into an invented personality score.
  4. Every constraint retains:
       key + value + unit + kind + source + evidence + confidence + validity
  5. Deterministic and backward-compatible with legacy dictionary consumers.
"""

from __future__ import annotations

from typing import Any
import engines.calculation.canonical as canonical_calc
from engines.profile.behavioral import BehavioralRules
from engines.profile.constraints import ConstraintRules
from engines.risk_profiler.models import (
    RiskAssessmentStatus,
    RiskDimension,
    RiskProfile,
)


def _value(state: dict[str, Any] | None, key: str) -> tuple[Any, bool]:
    item = (state or {}).get(key) or {}
    return item.get("value"), bool(item.get("available", False))


class RiskProfilerEngine:
    """Consolidated Risk Profiler assembling Risk Required, Capacity, and Tolerance."""

    def build(
        self,
        *,
        financial_state: dict[str, Any] | None = None,
        assets: list[dict[str, Any]] | None = None,
        liabilities: list[dict[str, Any]] | None = None,
        goals: list[dict[str, Any]] | None = None,
        observed_behavior: list[dict[str, Any]] | None = None,
        declared_constraints: list[dict[str, Any]] | None = None,
        risk_required_override: float | None = None,
    ) -> RiskProfile:
        all_constraints: list[dict[str, Any]] = []

        # ======================================================================
        # 1. CANONICAL RISK REQUIRED (Consumed Fact)
        # ======================================================================
        req_value: float | None = None
        req_available = False
        req_evidence: list[dict[str, Any]] = []

        if risk_required_override is not None:
            try:
                req_value = float(risk_required_override)
                req_available = True
                req_evidence = [{"field": "risk_required_override", "value": req_value}]
            except (TypeError, ValueError):
                req_value = None

        if not req_available and goals:
            for g in goals:
                f_target = g.get("future_target") or g.get("target_amount")
                c_fund = g.get("current_funding") or g.get("current_goal_funding") or g.get("mapped_assets_value")
                dur = g.get("time_horizon_years") or g.get("duration_years")
                if f_target is not None and c_fund is not None and dur is not None:
                    calced = canonical_calc.calculate_risk_required(f_target, c_fund, dur)
                    if calced is not None:
                        req_value = calced
                        req_available = True
                        req_evidence = [
                            {"field": "future_target", "value": f_target},
                            {"field": "current_funding", "value": c_fund},
                            {"field": "duration_years", "value": dur},
                            {"source": "canonical_calculation"},
                        ]
                        break

        req_constraint: dict[str, Any] | None = None
        if req_available and req_value is not None:
            req_constraint = {
                "key": "risk_need_required_return",
                "value": req_value,
                "unit": "%",
                "kind": "hard",
                "source": "canonical_calculation",
                "evidence": req_evidence,
                "confidence": 1.0,
                "validity": {"status": "valid", "valid_from": None, "valid_until": None},
                "valid_from": None,
                "valid_until": None,
            }
            all_constraints.append(req_constraint)

        risk_required = RiskDimension(
            name="risk_required",
            value=req_value,
            unit="%",
            available=req_available,
            source="canonical_calculation",
            evidence=req_evidence,
            confidence=1.0,
            status="authoritative" if req_available else "unavailable",
            constraints=[req_constraint] if req_constraint else [],
        )

        # ======================================================================
        # 2. RISK CAPACITY (Derived from Observable Financial State & Balance Sheet)
        # ======================================================================
        capacity_constraints: list[dict[str, Any]] = []
        income, income_ok = _value(financial_state, "income_monthly")
        surplus, surplus_ok = _value(financial_state, "investable_surplus_monthly")
        reserve, reserve_ok = _value(financial_state, "safety_reserve_months")
        emi, emi_ok = _value(financial_state, "emi_burden_monthly")

        if surplus_ok and surplus is not None:
            capacity_constraints.append({
                "key": "risk_capacity_surplus",
                "value": surplus,
                "unit": "INR/month",
                "kind": "hard",
                "source": "financial_state",
                "evidence": [{"field": "investable_surplus_monthly", "value": surplus}],
                "confidence": 1.0,
                "validity": {"status": "valid", "valid_from": None, "valid_until": None},
                "valid_from": None,
                "valid_until": None,
            })
        if reserve_ok and reserve is not None:
            capacity_constraints.append({
                "key": "risk_capacity_reserve",
                "value": reserve,
                "unit": "months",
                "kind": "hard",
                "source": "financial_state",
                "evidence": [{"field": "safety_reserve_months", "value": reserve}],
                "confidence": 1.0,
                "validity": {"status": "valid", "valid_from": None, "valid_until": None},
                "valid_from": None,
                "valid_until": None,
            })
        if income_ok and emi_ok and income and income > 0 and emi is not None:
            dti_ratio = canonical_calc.calculate_debt_to_income_ratio(emi, income, as_percentage=False)
            if dti_ratio is not None:
                capacity_constraints.append({
                    "key": "risk_capacity_debt_service_ratio",
                    "value": dti_ratio,
                    "unit": "ratio",
                    "kind": "hard",
                    "source": "financial_state",
                    "evidence": [{"field": "emi_burden_monthly", "value": emi}, {"field": "income_monthly", "value": income}],
                    "confidence": 1.0,
                    "validity": {"status": "valid", "valid_from": None, "valid_until": None},
                    "valid_from": None,
                    "valid_until": None,
                })

        # Asset exposure
        assets_list = assets or []
        total_assets = sum(float(a.get("value", 0) or 0) for a in assets_list)
        if total_assets > 0:
            largest = max(float(a.get("value", 0) or 0) for a in assets_list)
            conc = canonical_calc.calculate_portfolio_concentration(largest, total_assets, as_percentage=False)
            if conc is not None:
                capacity_constraints.append({
                    "key": "risk_exposure_max_asset_concentration",
                    "value": conc,
                    "unit": "ratio",
                    "kind": "hard",
                    "source": "financial_state",
                    "evidence": [{"field": "assets", "count": len(assets_list), "total_value": total_assets}],
                    "confidence": 1.0,
                    "validity": {"status": "valid", "valid_from": None, "valid_until": None},
                    "valid_from": None,
                    "valid_until": None,
                })

        # Debt exposure
        liabilities_list = liabilities or []
        total_debt = sum(float(x.get("outstanding", x.get("value", 0)) or 0) for x in liabilities_list)
        if total_debt > 0:
            capacity_constraints.append({
                "key": "risk_exposure_outstanding_debt",
                "value": total_debt,
                "unit": "INR",
                "kind": "hard",
                "source": "financial_state",
                "evidence": [{"field": "liabilities", "count": len(liabilities_list), "total_outstanding": total_debt}],
                "confidence": 1.0,
                "validity": {"status": "valid", "valid_from": None, "valid_until": None},
                "valid_from": None,
                "valid_until": None,
            })

        # Horizon need
        horizons = [
            g.get("time_horizon_years")
            for g in (goals or [])
            if isinstance(g.get("time_horizon_years"), (int, float)) and g.get("time_horizon_years") >= 0
        ]
        if horizons:
            capacity_constraints.append({
                "key": "risk_need_shortest_goal_horizon",
                "value": min(horizons),
                "unit": "years",
                "kind": "hard",
                "source": "financial_state",
                "evidence": [{"field": "goals", "count": len(horizons), "horizons": horizons}],
                "confidence": 1.0,
                "validity": {"status": "valid", "valid_from": None, "valid_until": None},
                "valid_from": None,
                "valid_until": None,
            })

        # Declared constraints
        for item in (declared_constraints or []):
            norm = ConstraintRules.normalize(item, "declared_constraint")
            capacity_constraints.append(norm)

        all_constraints.extend(capacity_constraints)
        has_capacity = bool(capacity_constraints)

        risk_capacity = RiskDimension(
            name="risk_capacity",
            value=float(len(capacity_constraints)) if has_capacity else None,
            unit="constraints",
            available=has_capacity,
            source="financial_state",
            evidence=[{"constraint_count": len(capacity_constraints)}],
            confidence=1.0 if has_capacity else 0.0,
            status="authoritative" if has_capacity else "unavailable",
            constraints=capacity_constraints,
        )

        # ======================================================================
        # 3. RISK TOLERANCE (Behavioral Profile from BehavioralRules)
        # ======================================================================
        behavioral_resolution = BehavioralRules.resolve(observed_behavior or [])
        behavioral_constraints: list[dict[str, Any]] = []
        observed_dimensions: list[str] = []

        for dimension_name, dimension_data in behavioral_resolution["dimensions"].items():
            if dimension_data["status"] == "observed":
                observed_dimensions.append(dimension_name)
                behavioral_constraints.extend(dimension_data["constraints"])

        all_constraints.extend(behavioral_constraints)
        has_tolerance = bool(observed_dimensions)

        risk_tolerance = RiskDimension(
            name="risk_tolerance",
            value=float(len(observed_dimensions)) if has_tolerance else None,
            unit="observed_dimensions",
            available=has_tolerance,
            source="observed_behavior",
            evidence=[{
                "observed_dimensions": observed_dimensions,
                "constraint_count": len(behavioral_constraints),
                "downstream_use": "product_selection",
            }],
            confidence=0.75 if has_tolerance else 0.0,
            status="observed" if has_tolerance else "insufficient_evidence",
            constraints=behavioral_constraints,
        )

        # ======================================================================
        # 4. DIMENSIONS (Backward Compatibility), CONFLICTS, & BOUNDARY
        # ======================================================================
        dimensions = {
            "capacity": [x for x in all_constraints if x["key"].startswith("risk_capacity_")],
            "exposure": [x for x in all_constraints if x["key"].startswith("risk_exposure_")],
            "need": [x for x in all_constraints if x["key"].startswith("risk_need_")],
        }

        conflicts = ConstraintRules.conflicts(all_constraints)

        # Decision status
        status: RiskAssessmentStatus
        if risk_required.available and risk_capacity.available and risk_tolerance.available:
            status = "complete"
        elif any((risk_required.available, risk_capacity.available, risk_tolerance.available)):
            status = "partial"
        else:
            status = "requires_review"

        decision_boundary = {
            "risk_required": {"value": risk_required.value, "unit": risk_required.unit, "available": risk_required.available},
            "risk_capacity": {"available": risk_capacity.available, "constraint_count": len(capacity_constraints)},
            "risk_tolerance": {"available": risk_tolerance.available, "observed_dimensions": observed_dimensions},
            "status": status,
        }

        return RiskProfile(
            risk_required=risk_required,
            risk_capacity=risk_capacity,
            risk_tolerance=risk_tolerance,
            status=status,
            constraints=all_constraints,
            decision_boundary=decision_boundary,
            dimensions=dimensions,
            has_sufficient_evidence=bool(all_constraints),
            conflicts=conflicts,
        )


# Authoritative functional entrypoint
def build_risk_profile(
    *,
    financial_state: dict[str, Any] | None = None,
    assets: list[dict[str, Any]] | None = None,
    liabilities: list[dict[str, Any]] | None = None,
    goals: list[dict[str, Any]] | None = None,
    observed_behavior: list[dict[str, Any]] | None = None,
    declared_constraints: list[dict[str, Any]] | None = None,
    risk_required_override: float | None = None,
) -> RiskProfile:
    """Build authoritative RiskProfile from canonical facts, capacity, and tolerance."""
    return RiskProfilerEngine().build(
        financial_state=financial_state,
        assets=assets,
        liabilities=liabilities,
        goals=goals,
        observed_behavior=observed_behavior,
        declared_constraints=declared_constraints,
        risk_required_override=risk_required_override,
    )
