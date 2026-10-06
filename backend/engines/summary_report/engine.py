import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

from data.goal_repository import GoalRepository
from data.financial_state_repository import FinancialStateSnapshotRepository
from data.moneywheel_repository import MoneywheelRepository
from services.financial_state_service import FinancialStateService
from services.moneywheel_service import MoneywheelService
from engines.risk_profiler.engine import RiskProfilerEngine
from models.summary_report import SummaryReport, GoalSummary, Observation, ActionItem

logger = logging.getLogger(__name__)


class SummaryReportEngine:
    """Aggregates canonical outputs from the core engines into a SummaryReport.
    The engine is deliberately lightweight – it does not re‑calculate any
    financial fact, it only consumes the canonical outputs.
    """

    def __init__(self, planning_unit_id: str):
        self.planning_unit_id = planning_unit_id
        self.goal_repo = GoalRepository()
        self.financial_state_repo = FinancialStateSnapshotRepository()
        self.moneywheel_repo = MoneywheelRepository()
        self.financial_state_service = FinancialStateService(snapshot_repository=self.financial_state_repo)

    def _fetch_financial_state(self) -> dict:
        try:
            state = self.financial_state_service.current(self.planning_unit_id, "family")
            if hasattr(state, "model_dump"):
                return state.model_dump(mode="json")
            if isinstance(state, dict):
                return state
        except Exception as e:
            logger.warning("Could not fetch financial state: %s", e)
        return {}

    def _fetch_moneywheel(self) -> dict:
        try:
            latest = self.moneywheel_repo.get_latest(self.planning_unit_id)
            if latest:
                return latest
        except Exception as e:
            logger.warning("Could not fetch moneywheel snapshot: %s", e)
        return {}

    def _fetch_risk_profile(self, financial_state: dict) -> dict:
        try:
            rp = RiskProfilerEngine().build(financial_state=financial_state)
            if hasattr(rp, "model_dump"):
                return rp.model_dump(mode="json")
            if hasattr(rp, "dict"):
                return rp.dict()
        except Exception as e:
            logger.warning("Could not build risk profile: %s", e)
        return {}

    def _fetch_goals(self) -> List[GoalSummary]:
        result: List[GoalSummary] = []
        try:
            goals_meta = self.goal_repo.list_goals(self.planning_unit_id)
            for g in goals_meta:
                g_id = g.get("goal_id")
                if not g_id:
                    continue
                dg = self.goal_repo.get_latest_defined_goal(self.planning_unit_id, g_id)
                target = dg.future_target if dg else float(g.get("target_amount") or 0.0)
                horizon = dg.duration_years if dg else 5.0
                current_funding = dg.projected_mapped_asset_value if dg else 0.0
                gap = dg.funding_gap if dg else target
                req_contrib = dg.required_monthly_contribution if dg else 0.0
                status = dg.funding_status if dg else "pending"

                result.append(
                    GoalSummary(
                        id=str(g_id),
                        name=str(g.get("goal_name") or dg.goal_name if dg else "Financial Goal"),
                        target_amount=float(target or 0.0),
                        horizon_years=float(horizon or 0.0),
                        current_funding=float(current_funding or 0.0),
                        funding_gap=float(gap or 0.0),
                        feasibility=str(status or "pending"),
                        required_contribution=float(req_contrib) if req_contrib is not None else None,
                    )
                )
        except Exception as e:
            logger.warning("Could not fetch goals: %s", e)
        return result

    def _generate_observations(self, mw: dict, rp: dict) -> List[Observation]:
        observations: List[Observation] = []
        ratios = mw.get("ratios") or []
        for r in ratios:
            name = r.get("ratio_name") or r.get("name")
            val = r.get("value")
            status = r.get("status")
            if name == "debt_to_income_ratio" and val is not None and val > 40:
                observations.append(
                    Observation(
                        description="Debt‑to‑Income ratio is elevated (>40%), which limits additional borrowing capacity.",
                        relevance=0.9,
                        source="MoneyWheel",
                    )
                )
            elif name == "savings_rate" and val is not None and val < 20:
                observations.append(
                    Observation(
                        description="Savings rate is below the recommended 20% benchmark.",
                        relevance=0.85,
                        source="MoneyWheel",
                    )
                )
            elif name == "liquid_asset_ratio" and status in ("vulnerable", "critical"):
                observations.append(
                    Observation(
                        description="Emergency liquid reserve coverage is below recommended safe buffer.",
                        relevance=0.95,
                        source="MoneyWheel",
                    )
                )

        if not observations:
            observations.append(
                Observation(
                    description="Portfolio and financial state metrics are within standard operating bands.",
                    relevance=0.7,
                    source="DiagnosticEngine",
                )
            )
        return observations

    def _generate_actions(self, observations: List[Observation]) -> List[ActionItem]:
        actions: List[ActionItem] = []
        for obs in observations:
            if "Debt‑to‑Income" in obs.description:
                actions.append(
                    ActionItem(
                        description="Consider reducing high‑interest consumer debt to improve investable cash‑flow.",
                        priority=0.85,
                        source="MoneyWheel",
                    )
                )
            if "Emergency liquid" in obs.description or "liquid reserve" in obs.description:
                actions.append(
                    ActionItem(
                        description="Build a minimum 6-month essential expense reserve before taking aggressive long-term risks.",
                        priority=0.95,
                        source="MoneyWheel",
                    )
                )
            if "Savings rate" in obs.description:
                actions.append(
                    ActionItem(
                        description="Audit discretionary monthly expenditures and automate an additional 5% savings step-up.",
                        priority=0.8,
                        source="MoneyWheel",
                    )
                )

        if not actions:
            actions.append(
                ActionItem(
                    description="Maintain current automated monthly SIP allocations and review performance annually.",
                    priority=0.7,
                    source="StrategyEngine",
                )
            )
        return actions

    def build_report(self) -> SummaryReport:
        logger.info("Building SummaryReport for planning unit %s", self.planning_unit_id)
        f_state = self._fetch_financial_state()
        mw = self._fetch_moneywheel()
        rp = self._fetch_risk_profile(f_state)
        goals = self._fetch_goals()

        observations = self._generate_observations(mw, rp)
        actions = self._generate_actions(observations)

        # Snapshot representation
        snapshot = dict(f_state)
        if not snapshot and mw.get("financial_state_snapshot"):
            snapshot = mw.get("financial_state_snapshot")

        report = SummaryReport(
            financial_snapshot=snapshot,
            goals=goals,
            observations=observations,
            actions=actions,
            investment_allocation={},
            risk_profile=rp,
            provenance={
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "planning_unit_id": self.planning_unit_id,
            },
        )
        return report
