from __future__ import annotations

from typing import Any


def _value(state: dict[str, Any] | None, key: str) -> tuple[Any, bool]:
    item = (state or {}).get(key) or {}
    return item.get("value"), bool(item.get("available", False))


def build_risk_profile(
    *,
    financial_state: dict[str, Any] | None,
    assets: list[dict[str, Any]] | None = None,
    liabilities: list[dict[str, Any]] | None = None,
    goals: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build risk capacity, exposure and need from observable evidence only."""
    constraints: list[dict[str, Any]] = []
    income, income_ok = _value(financial_state, "income_monthly")
    surplus, surplus_ok = _value(financial_state, "investable_surplus_monthly")
    reserve, reserve_ok = _value(financial_state, "safety_reserve_months")
    emi, emi_ok = _value(financial_state, "emi_burden_monthly")

    if surplus_ok and surplus is not None:
        constraints.append({"key": "risk_capacity_surplus", "value": surplus, "unit": "INR/month", "kind": "hard", "source": "financial_state", "evidence": [{"field": "investable_surplus_monthly", "value": surplus}]})
    if reserve_ok and reserve is not None:
        constraints.append({"key": "risk_capacity_reserve", "value": reserve, "unit": "months", "kind": "hard", "source": "financial_state", "evidence": [{"field": "safety_reserve_months", "value": reserve}]})
    if income_ok and emi_ok and income and income > 0 and emi is not None:
        constraints.append({"key": "risk_capacity_debt_service_ratio", "value": round(emi / income, 6), "unit": "ratio", "kind": "hard", "source": "financial_state", "evidence": [{"field": "emi_burden_monthly", "value": emi}, {"field": "income_monthly", "value": income}]})

    assets = assets or []
    total_assets = sum(float(a.get("value", 0) or 0) for a in assets)
    if total_assets > 0:
        largest = max(float(a.get("value", 0) or 0) for a in assets)
        constraints.append({"key": "risk_exposure_max_asset_concentration", "value": round(largest / total_assets, 6), "unit": "ratio", "kind": "hard", "source": "financial_state", "evidence": [{"field": "assets", "count": len(assets), "total_value": total_assets}]})

    liabilities = liabilities or []
    total_debt = sum(float(x.get("outstanding", x.get("value", 0)) or 0) for x in liabilities)
    if total_debt > 0:
        constraints.append({"key": "risk_exposure_outstanding_debt", "value": total_debt, "unit": "INR", "kind": "hard", "source": "financial_state", "evidence": [{"field": "liabilities", "count": len(liabilities), "total_outstanding": total_debt}]})

    horizons = [g.get("time_horizon_years") for g in (goals or []) if isinstance(g.get("time_horizon_years"), (int, float)) and g.get("time_horizon_years") >= 0]
    if horizons:
        constraints.append({"key": "risk_need_shortest_goal_horizon", "value": min(horizons), "unit": "years", "kind": "hard", "source": "financial_state", "evidence": [{"field": "goals", "count": len(horizons), "horizons": horizons}]})

    for item in constraints:
        item["confidence"] = 1.0

    return {
        "dimensions": {
            "capacity": [x for x in constraints if x["key"].startswith("risk_capacity_")],
            "exposure": [x for x in constraints if x["key"].startswith("risk_exposure_")],
            "need": [x for x in constraints if x["key"].startswith("risk_need_")],
        },
        "constraints": constraints,
        "has_sufficient_evidence": bool(constraints),
    }
