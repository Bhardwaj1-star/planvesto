import logging
from typing import List

# Placeholder imports – actual engine modules provide these functions
# In a real implementation these would query the corresponding services
# or call the engine classes directly.
from engines.risk_profiler.engine import RiskProfilerEngine
from backend.engines.risk_profiler.engine import build_risk_profile
from backend.engines.risk_profiler.models import RiskProfile
from backend.engines.goal.engine import GoalEngine
from backend.engines.investment.engine import InvestmentEngine
from backend.engines.moneywheel.engine import MoneyWheelEngine
from backend.models.summary_report import SummaryReport, GoalSummary, Observation, ActionItem

logger = logging.getLogger(__name__)

class SummaryReportEngine:
    """Aggregates outputs from the four core engines into a SummaryReport.
    The engine is deliberately lightweight – it does not re‑calculate any
    financial fact, it only consumes the canonical outputs.
    """

    def __init__(self, planning_unit_id: str):
        self.planning_unit_id = planning_unit_id

    # ---------------------------------------------------------------------
    # Core data fetch helpers (placeholder – replace with real service calls)
    # ---------------------------------------------------------------------
    def _fetch_moneywheel(self) -> dict:
        # In production this would call MoneyWheelEngine.build(planning_unit_id)
        return MoneyWheelEngine.build(self.planning_unit_id).dict()

    def _fetch_risk_profile(self) -> dict:
        # RiskProfilerEngine consumes the canonical risk required and builds a profile
        rp = RiskProfilerEngine.build(self.planning_unit_id)
        return rp.dict()

    def _fetch_goals(self) -> List[dict]:
        # GoalEngine returns a list of goal objects – we map to GoalSummary
        goals = GoalEngine.build(self.planning_unit_id)
        result: List[GoalSummary] = []
        for g in goals:
            result.append(
                GoalSummary(
                    id=str(g.id),
                    name=g.name,
                    target_amount=g.target_amount,
                    horizon_years=g.duration_years,
                    current_funding=g.current_funding,
                    funding_gap=g.funding_gap,
                    feasibility=g.feasibility,
                    required_contribution=g.required_monthly_contribution,
                )
            )
        return result

    def _fetch_investment(self) -> dict:
        # InvestmentEngine produces allocation details
        inv = InvestmentEngine.build(self.planning_unit_id)
        return inv.dict()

    # ---------------------------------------------------------------------
    # Observation & Action generation (simple rule‑based examples)
    # ---------------------------------------------------------------------
    def _generate_observations(self, mw: dict, rp: dict) -> List[Observation]:
        observations: List[Observation] = []
        # Example: high DTI observation
        dti = mw.get("debt_to_income_ratio", {}).get("value")
        if dti is not None and dti > 40:
            observations.append(
                Observation(
                    description="Debt‑to‑Income ratio is high, which may limit borrowing capacity.",
                    relevance=0.9,
                    source="MoneyWheel",
                )
            )
        # Example: risk capacity breach
        risk_capacity = rp.get("risk_capacity", {}).get("available", False)
        if not risk_capacity:
            observations.append(
                Observation(
                    description="Risk Capacity constraints indicate the investor cannot tolerate the required risk.",
                    relevance=0.95,
                    source="RiskProfiler",
                )
            )
        return observations

    def _generate_actions(self, observations: List[Observation]) -> List[ActionItem]:
        actions: List[ActionItem] = []
        for obs in observations:
            if "Debt‑to‑Income" in obs.description:
                actions.append(
                    ActionItem(
                        description="Consider reducing high‑interest debt to improve cash‑flow.",
                        priority=0.85,
                        source="MoneyWheel",
                    )
                )
            if "Risk Capacity" in obs.description:
                actions.append(
                    ActionItem(
                        description="Review asset allocation to lower overall portfolio volatility.",
                        priority=0.9,
                        source="RiskProfiler",
                    )
                )
        return actions

    # ---------------------------------------------------------------------
    # Public entry point
    # ---------------------------------------------------------------------
    def build_report(self) -> SummaryReport:
        logger.info("Building SummaryReport for planning unit %s", self.planning_unit_id)
        mw = self._fetch_moneywheel()
        rp = self._fetch_risk_profile()
        goals = self._fetch_goals()
        investment = self._fetch_investment()

        observations = self._generate_observations(mw, rp)
        actions = self._generate_actions(observations)

        report = SummaryReport(
            financial_snapshot=mw,
            goals=goals,
            observations=observations,
            actions=actions,
            investment_allocation=investment,
            risk_profile=rp,
            provenance={"generated_at": "2026-10-01T21:59:00+05:30", "planning_unit_id": self.planning_unit_id},
        )
        return report
