from typing import Any

from models.financial_state import FinancialState


TRACKED_METRICS = (
    "income_monthly",
    "expenses_monthly",
    "commitments_monthly",
    "investable_surplus_monthly",
    "total_assets",
    "total_liabilities",
    "emi_burden_monthly",
    "net_worth",
    "safety_reserve_months",
)


class ActionImpactEngine:
    """Compares projected and actual financial-state values without inventing rules."""

    def _metric_value(self, state: FinancialState | dict[str, Any], name: str) -> float | None:
        value = state.get(name) if isinstance(state, dict) else getattr(state, name, None)
        if isinstance(value, dict):
            value = value.get("value")
        elif hasattr(value, "value"):
            value = value.value
        return float(value) if value is not None else None

    def compare(
        self,
        projected_state: FinancialState | dict[str, Any],
        actual_state: FinancialState | dict[str, Any],
    ) -> dict[str, Any]:
        variances: list[dict[str, Any]] = []
        for metric in TRACKED_METRICS:
            projected = self._metric_value(projected_state, metric)
            actual = self._metric_value(actual_state, metric)
            if projected is None or actual is None:
                continue
            variance = actual - projected
            variances.append({
                "metric": metric,
                "projected": projected,
                "actual": actual,
                "variance": variance,
            })

        return {
            "projected_vs_actual": variances,
            "material_variances": [],
            "cause": {
                "status": "not_determined",
                "explanation": "Materiality and cause attribution require configured business rules and available transaction/source data.",
            },
        }
