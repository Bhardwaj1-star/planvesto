from typing import Any

from services.financial_state_service import FinancialStateService
from data.goal_repository import GoalRepository


class DashboardService:
    def __init__(self):
        self.financial_state_service = FinancialStateService()
        self.goal_repository = GoalRepository()

    def build(self, planning_unit_id: str, scope: str = "family", investor_id: str | None = None) -> dict[str, Any]:
        # Always rebuild from the current source tables. The snapshot is a derived
        # cache and can become stale when onboarding/profile writes update source data
        # without explicitly rebuilding financial_state_snapshots.
        state = self.financial_state_service.build(planning_unit_id, scope, investor_id)
        financial_state_data = state.model_dump(mode="json")

        # Dashboard deliberately exposes only decision-useful financial state.
        dashboard_financial_state = {
            "net_worth": financial_state_data.get("net_worth"),
            "total_assets": financial_state_data.get("total_assets"),
            "asset_breakdown": financial_state_data.get("asset_breakdown", []),
            "asset_allocation": financial_state_data.get("asset_allocation", []),
            "total_liabilities": financial_state_data.get("total_liabilities"),
            "liability_breakdown": financial_state_data.get("liability_breakdown", []),
            "liability_allocation": financial_state_data.get("liability_allocation", []),
            "income_monthly": financial_state_data.get("income_monthly"),
            "income_annual": financial_state_data.get("income_annual"),
            "expenses_monthly": financial_state_data.get("expenses_monthly"),
            "expenses_annual": financial_state_data.get("expenses_annual"),
            "investable_surplus_monthly": financial_state_data.get("investable_surplus_monthly"),
            "investable_surplus_annual": financial_state_data.get("investable_surplus_annual"),
        }

        goals: list[dict[str, Any]] = []
        for summary in self.goal_repository.list_goals(planning_unit_id):
            goal_id = summary.get("goal_id")
            defined = self.goal_repository.get_latest_defined_goal(planning_unit_id, goal_id) if goal_id else None

            # Cancelled goals remain available through goal history, but they are not
            # part of the active dashboard journey or goal count.
            if defined and defined.status == "Cancelled":
                continue
            if defined:
                target = float(defined.future_target)
                projected = float(defined.projected_mapped_asset_value)
                coverage = min(max((projected / target * 100) if target > 0 else 0, 0), 100)
                goals.append({
                    "goal_id": defined.goal_id,
                    "goal_name": defined.goal_name,
                    "goal_type": defined.goal_type,
                    "target_amount": target,
                    "target_date": f"{defined.target_year:04d}-{defined.target_month:02d}-01",
                    "priority": defined.priority,
                    "flexibility": defined.flexibility,
                    "funding_status": defined.funding_status,
                    "funding_gap": defined.funding_gap,
                    "projected_mapped_asset_value": projected,
                    "coverage_percentage": round(coverage, 1),
                    "image_key": self._image_key(defined.goal_type),
                })
            else:
                goals.append({
                    "goal_id": goal_id,
                    "goal_name": summary.get("goal_name") or "Goal",
                    "goal_type": "Other",
                    "target_amount": float(summary.get("target_amount") or 0),
                    "target_date": summary.get("target_date"),
                    "priority": summary.get("priority"),
                    "flexibility": summary.get("flexibility"),
                    "funding_status": None,
                    "funding_gap": None,
                    "projected_mapped_asset_value": None,
                    "coverage_percentage": None,
                    "image_key": "default",
                })

        return {
            "planning_unit_id": planning_unit_id,
            "scope": scope,
            "financial_state": dashboard_financial_state,
            "goals": goals,
        }

    @staticmethod
    def _image_key(goal_type: str | None) -> str:
        value = (goal_type or "").strip().lower()
        if "home" in value or "house" in value or "property" in value:
            return "home"
        if "education" in value or "child" in value or "college" in value:
            return "education"
        if "travel" in value or "vacation" in value:
            return "travel"
        if "retirement" in value:
            return "retirement"
        if "wedding" in value or "marriage" in value:
            return "wedding"
        if "business" in value:
            return "business"
        return "default"
