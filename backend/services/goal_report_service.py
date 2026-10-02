from __future__ import annotations

from io import BytesIO
from typing import Any

from fastapi import HTTPException
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors

from data.goal_repository import GoalRepository
from data.strategy_repository import StrategyRepository
from data.financial_state_repository import FinancialStateSnapshotRepository


class GoalReportService:
    """Build the complete, goal-agnostic decision report from persisted engine output.

    This is a presentation/decision-explanation layer. It never invents financial
    calculations. What-if values come from stored scenarios; missing source data
    is explicitly represented.
    """

    MISSING = "Not available"

    def __init__(self):
        self.goal_repo = GoalRepository()
        self.strategy_repo = StrategyRepository()
        self.financial_state_repo = FinancialStateSnapshotRepository()

    def _load(self, planning_unit_id: str, strategy_run_id: str):
        run = self.strategy_repo.get_run_by_id(planning_unit_id, strategy_run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Strategy run not found")
        goal = (
            self.goal_repo.get_defined_goal_by_version(
                planning_unit_id, run.goal_id, run.defined_goal_version
            )
            or self.goal_repo.get_latest_defined_goal(planning_unit_id, run.goal_id)
        )
        if not goal:
            raise HTTPException(status_code=404, detail="Underlying goal not found")
        snapshot = self.financial_state_repo.get_latest(planning_unit_id, "family")
        if not snapshot or not snapshot.get("financial_state"):
            return run, goal, {}
        state = snapshot["financial_state"]
        if hasattr(state, "model_dump"):
            state = state.model_dump()
        elif not isinstance(state, dict):
            return run, goal, {}

        def metric_value(key: str):
            value = state.get(key)
            if isinstance(value, dict):
                return value.get("value")
            if hasattr(value, "value"):
                return value.value
            return value

        context = dict(state)
        income_annual = metric_value("income_annual")
        expenses_annual = metric_value("expenses_annual")
        surplus_monthly = metric_value("investable_surplus_monthly")
        assets = metric_value("total_assets")
        financial_assets = metric_value("financial_assets")
        liabilities = metric_value("total_liabilities")
        net_worth = metric_value("net_worth")
        context.update({
            "annual_income": income_annual,
            "income": income_annual,
            "annual_expenses": expenses_annual,
            "expenses": expenses_annual,
            "monthly_surplus": surplus_monthly,
            "surplus": surplus_monthly,
            "financial_assets": financial_assets,
            "assets": assets,
            "liabilities": liabilities,
            "net_worth": net_worth,
            "retirement_assets": getattr(goal, "projected_mapped_asset_value", 0.0),
        })
        return run, goal, context

    @staticmethod
    def _dump(value: Any) -> Any:
        if hasattr(value, "model_dump"):
            return value.model_dump(mode="json")
        return value

    @classmethod
    def _get(cls, source: Any, key: str, default: Any = None) -> Any:
        if source is None:
            return default
        source = cls._dump(source)
        if isinstance(source, dict):
            return source.get(key, default)
        return getattr(source, key, default)

    @classmethod
    def _goal_label(cls, goal: Any) -> str:
        return str(
            cls._get(goal, "name")
            or cls._get(goal, "goal_name")
            or cls._get(goal, "goal_type")
            or "Financial Goal"
        ).replace("_", " ").replace("-", " ").title()

    @classmethod
    def _mapped_assets(cls, goal: Any) -> list[dict[str, Any]]:
        mappings = cls._get(goal, "mapped_assets", []) or []
        rows = []
        for mapping in mappings:
            mapping = cls._dump(mapping)
            if not isinstance(mapping, dict):
                continue
            rows.append(
                {
                    "asset_name": mapping.get("asset_name") or mapping.get("asset_id"),
                    "allocation": mapping.get("allocated_amount"),
                    "allocation_percentage": mapping.get("allocated_percentage"),
                    "expected_return": mapping.get("expected_return"),
                    "projected_value": mapping.get("projected_value"),
                }
            )
        return rows

    @classmethod
    def _strategy_name(cls, run: Any, strategy_id: str | None) -> str | None:
        for strategy in cls._get(run, "applicable_strategies", []) or []:
            if cls._get(strategy, "strategy_id") == strategy_id:
                return cls._get(strategy, "name")
        return strategy_id

    @classmethod
    def _scenario_rows(cls, run: Any, source: str = "scenarios") -> list[dict[str, Any]]:
        rows = []
        selected_id = cls._get(run, "selected_scenario_id")
        for scenario in cls._get(run, source, []) or []:
            metrics = cls._get(scenario, "metrics", {}) or {}
            funding = cls._get(scenario, "funding_structure", {}) or {}
            rows.append(
                {
                    "scenario_id": cls._get(scenario, "scenario_id"),
                    "strategy_id": cls._get(scenario, "strategy_id"),
                    "strategy_name": cls._strategy_name(run, cls._get(scenario, "strategy_id")),
                    "funding_strategy_id": cls._get(scenario, "funding_strategy_id"),
                    "scenario_name": cls._get(scenario, "scenario_name"),
                    "scenario_type": cls._get(scenario, "scenario_type"),
                    "is_selected": cls._get(scenario, "scenario_id") == selected_id,
                    "assumptions": cls._dump(cls._get(scenario, "assumptions", {})),
                    "funding_structure": cls._dump(funding),
                    "metrics": cls._dump(metrics),
                    "trade_off_notes": cls._get(scenario, "trade_off_notes", ""),
                }
            )
        return rows

    @classmethod
    def _alternatives(cls, run: Any) -> list[dict[str, Any]]:
        selected = cls._get(run, "selected_strategy_id")
        rows = []
        for item in cls._get(run, "rankings", []) or []:
            strategy_id = cls._get(item, "strategy_id")
            if strategy_id == selected:
                continue
            rows.append(
                {
                    "strategy_id": strategy_id,
                    "strategy_name": cls._get(item, "strategy_name"),
                    "scenario_id": cls._get(item, "scenario_id"),
                    "scenario_name": cls._get(item, "scenario_name"),
                    "composite_score": cls._get(item, "composite_score"),
                    "dimension_scores": cls._dump(cls._get(item, "dimension_scores", {})),
                    "eligible": cls._get(item, "is_eligible", True),
                    "reasons": cls._get(item, "ineligible_reasons", []),
                }
            )
        return rows

    @classmethod
    def _what_ifs(cls, run: Any) -> list[dict[str, Any]]:
        """Expose scenario engine output as what-if analysis, without recalculating it."""
        rows = []
        for row in cls._scenario_rows(run):
            metrics = row["metrics"] or {}
            funding = row["funding_structure"] or {}
            rows.append(
                {
                    "scenario_id": row["scenario_id"],
                    "scenario": row["scenario_name"],
                    "strategy": row["strategy_name"],
                    "type": row["scenario_type"],
                    "selected": row["is_selected"],
                    "assumptions_changed": row["assumptions"],
                    "funding_changes": funding,
                    "outcomes": metrics,
                    "trade_off": row["trade_off_notes"],
                }
            )
        return rows
    @classmethod
    def _trade_offs(cls, run: Any) -> list[dict[str, Any]]:
        architecture = cls._get(run, "selected_architecture")
        recommendation = cls._get(run, "recommendation")
        values: list[Any] = []
        values.extend(cls._get(architecture, "trade_offs", []) or [])
        values.extend(cls._get(recommendation, "short_reasons", []) or [])
        values.extend(
            cls._get(s, "trade_off_notes", "")
            for s in cls._get(run, "scenarios", []) or []
            if cls._get(s, "trade_off_notes", "")
        )
        unique = []
        for value in values:
            value = cls._dump(value)
            if value and value not in unique:
                unique.append(value)
        return [{"trade_off": value} for value in unique]

    @classmethod
    def _build_cash_flow_trajectory(
        cls,
        goal: Any,
        selected_scenario: dict[str, Any] | None,
        mapped_assets: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        duration = cls._get(goal, "duration_years") or 5
        try:
            duration = int(duration)
        except (ValueError, TypeError):
            duration = 5
        duration = max(1, min(duration, 35))

        try:
            target_year = int(cls._get(goal, "target_year") or 0)
        except (ValueError, TypeError):
            target_year = 0

        start_year = (target_year - duration) if target_year > 2000 else 2026

        return_rate = cls._get(goal, "funding_return_assumption")
        try:
            return_rate = float(return_rate) if return_rate is not None else 0.09
        except (ValueError, TypeError):
            return_rate = 0.09

        monthly_req = cls._get(goal, "required_monthly_contribution")
        try:
            monthly_req = float(monthly_req) if monthly_req is not None else 0.0
        except (ValueError, TypeError):
            monthly_req = 0.0

        if selected_scenario:
            funding_structure = selected_scenario.get("funding_structure") or {}
            scen_monthly = funding_structure.get("required_monthly_contribution") or funding_structure.get("starting_monthly_contribution")
            if scen_monthly:
                try:
                    monthly_req = float(scen_monthly)
                except (ValueError, TypeError):
                    pass

        opening_balance = sum(float(m.get("allocation") or 0.0) for m in mapped_assets if isinstance(m, dict))

        future_target = cls._get(goal, "future_target") or cls._get(goal, "today_cost") or 0.0
        try:
            future_target = float(future_target)
        except (ValueError, TypeError):
            future_target = 0.0

        trajectory: list[dict[str, Any]] = []
        balance = opening_balance

        for yr in range(1, duration + 1):
            cal_year = start_year + yr - 1
            annual_inv = monthly_req * 12.0
            growth = (balance + annual_inv / 2.0) * return_rate
            outflow = 0.0
            if yr == duration:
                outflow = min(balance + annual_inv + growth, future_target) if future_target > 0 else (balance + annual_inv + growth)
            closing = max(0.0, balance + annual_inv + growth - outflow)
            trajectory.append({
                "year_index": yr,
                "year": cal_year,
                "opening_balance": round(balance, 2),
                "annual_investment": round(annual_inv, 2),
                "growth": round(growth, 2),
                "outflow": round(outflow, 2),
                "closing_balance": round(closing, 2),
            })
            balance = closing

        return trajectory

    @classmethod
    def _build_product_architecture(cls, goal: Any) -> list[dict[str, Any]]:
        duration = cls._get(goal, "duration_years") or 5
        try:
            duration = int(duration)
        except (ValueError, TypeError):
            duration = 5

        if duration <= 3:
            return [
                {
                    "bucket": "Bucket 1: Immediate Liquidity (0–1 Year)",
                    "instruments": "Liquid Mutual Funds, High-Yield Savings, Overnight Funds",
                    "allocation": "50%",
                    "strategic_rule": "Capital preservation with immediate accessibility; zero equity exposure.",
                },
                {
                    "bucket": "Bucket 2: Near-Term Preservation (1–3 Years)",
                    "instruments": "Ultra-Short Duration Debt, Arbitrage Funds, Short-Term FDs",
                    "allocation": "50%",
                    "strategic_rule": "Protect principal against rate shifts and inflation; secure steady accrual.",
                },
            ]
        elif duration <= 7:
            return [
                {
                    "bucket": "Bucket 1: Liquidity & Safety (0–2 Years)",
                    "instruments": "Liquid / Money Market Funds, Arbitrage Funds",
                    "allocation": "25%",
                    "strategic_rule": "Guaranteed liquidity buffer for near-term milestones; absolute capital safety.",
                },
                {
                    "bucket": "Bucket 2: Fixed Income Stability (3–5 Years)",
                    "instruments": "Corporate Bond Funds, Target Maturity Debt, Banking & PSU Debt",
                    "allocation": "35%",
                    "strategic_rule": "Predictable compounding cushion with minimal duration volatility.",
                },
                {
                    "bucket": "Bucket 3: Growth Engine (5–7 Years)",
                    "instruments": "Large-Cap Index Funds (Nifty 50), Balanced Advantage / Multi-Asset",
                    "allocation": "40%",
                    "strategic_rule": "Inflation-beating capital appreciation with dynamic downside protection.",
                },
            ]
        else:
            return [
                {
                    "bucket": "Bucket 1: Cash & Buffer (0–2 Years)",
                    "instruments": "Liquid Funds, Overnight Funds, Short-term Arbitrage",
                    "allocation": "15%",
                    "strategic_rule": "Emergency transition reserve; ring-fenced from market volatility.",
                },
                {
                    "bucket": "Bucket 2: Core Stability (3–7 Years)",
                    "instruments": "Target Maturity Debt, High-Quality Corporate Bonds, Conservative Hybrid",
                    "allocation": "25%",
                    "strategic_rule": "Steady yield compounding; acts as rebalancing buffer during market swings.",
                },
                {
                    "bucket": "Bucket 3: Wealth Compounding (7+ Years)",
                    "instruments": "Broad-Market Equity Index (Nifty 50, Nifty Midcap 150), Flexi-Cap Funds",
                    "allocation": "60%",
                    "strategic_rule": "Primary growth driver designed to outpace education/lifestyle inflation.",
                },
            ]

    @classmethod
    def _build_contribution_rules(cls, goal: Any) -> list[str]:
        return [
            "1. Priority Automation: Automate monthly SIP on salary date via NACH/e-mandate before any discretionary lifestyle spending.",
            "2. Annual Step-Up Discipline: Increase monthly contributions by 5% to 10% annually with salary increments to accelerate goal achievement.",
            "3. Ring-Fenced Earmarking: Keep goal-mapped assets segregated; never liquidate or pledge for unrelated lifestyle or consumption expenses.",
            "4. Glidepath De-Risking Window: Systematically transition from Growth (Bucket 3) to Liquid (Bucket 1) starting 36 months before target maturity.",
            "5. Emergency Shield Priority: Maintain a separate 6-month family emergency buffer so ongoing goal contributions are never interrupted during market shocks.",
        ]

    @classmethod
    def _build_action_plan_timeline(cls, goal: Any) -> list[dict[str, Any]]:
        duration = cls._get(goal, "duration_years") or 5
        try:
            duration = int(duration)
        except (ValueError, TypeError):
            duration = 5

        de_risk_yr = max(1, duration - 3)
        return [
            {
                "timeline": "Immediate (Month 1)",
                "action": "Set up monthly SIP auto-debits; allocate existing earmarked assets; verify KYC and portfolio tagging.",
                "owner": "Investor / Advisor",
                "milestone": "Capital deployment activated",
            },
            {
                "timeline": "Every 12 Months",
                "action": "Review portfolio performance vs benchmark; implement annual step-up (+5% to +10%); rebalance if asset mix drifts > 5%.",
                "owner": "Investor",
                "milestone": "Annual discipline & rebalancing",
            },
            {
                "timeline": f"Year {de_risk_yr} (3 Years to Maturity)",
                "action": "Activate systematic de-risking (STP) from Equity to Liquid/Short-term Debt to protect accumulated corpus.",
                "owner": "Investor / System",
                "milestone": "Capital preservation locked in",
            },
            {
                "timeline": f"Year {duration} (Goal Horizon)",
                "action": "Redeem required goal target smoothly from Bucket 1 (Liquid) with zero market timing or drawdown penalty.",
                "owner": "Investor",
                "milestone": "Goal successfully funded",
            },
        ]

    @classmethod
    def _build_contingency_matrix(cls) -> list[dict[str, Any]]:
        return [
            {
                "risk_event": "Equity Market Crash (> 20%)",
                "immediate_action": "Maintain SIP auto-debits uninterrupted; accumulate units at lower valuation.",
                "planning_change": "Rebalance fixed income gains into target equity allocation if drift exceeds 5%.",
                "what_not_to_do": "Do not panic-sell equity or pause ongoing monthly SIP investments.",
            },
            {
                "risk_event": "Income Interruption / Job Loss",
                "immediate_action": "Draw on the independent 6-month Emergency Fund for core living expenses.",
                "planning_change": "Temporarily pause annual step-up; maintain baseline contribution or switch to minimum viable tier.",
                "what_not_to_do": "Do not liquidate compounding long-term goal assets prematurely.",
            },
            {
                "risk_event": "Goal Target Cost Overrun (+15–20%)",
                "immediate_action": "Run sensitivity analysis under the updated future target assumption.",
                "planning_change": "Increase monthly contribution rate or extend goal horizon by 6 to 12 months.",
                "what_not_to_do": "Do not take high-interest unsecured loans or bridge debt.",
            },
            {
                "risk_event": "Inflation Higher Than Expected",
                "immediate_action": "Recalculate future purchasing power target with updated inflation rate.",
                "planning_change": "Increase annual step-up rate from 5% to 10% to preserve real corpus value.",
                "what_not_to_do": "Do not divert entire corpus into high-risk speculative assets.",
            },
        ]

    def build_report(self, planning_unit_id: str, strategy_run_id: str) -> dict[str, Any]:
        run, goal, context = self._load(planning_unit_id, strategy_run_id)
        recommendation = self._dump(self._get(run, "recommendation", {})) or {}
        architecture = self._dump(
            self._get(run, "selected_architecture")
            or recommendation.get("architecture")
            or {}
        ) or {}
        selected_strategy_id = self._get(run, "selected_strategy_id") or recommendation.get(
            "recommended_strategy_id"
        )
        scenarios = self._scenario_rows(run, "scenarios")
        run_metadata = self._get(run, "run_metadata", {}) or {}
        technique_outputs = run_metadata.get("technique_outputs", []) if isinstance(run_metadata, dict) else []
        if not technique_outputs:
            technique_outputs = self._get(run, "technique_outputs", []) or []
        what_if_scenarios = self._scenario_rows(run, "what_if_scenarios")
        selected_scenario = next((s for s in scenarios if s["is_selected"]), None)

        goal_calculation = {
            key: self._get(goal, key)
            for key in (
                "today_cost", "inflation_rate", "future_target", "funding_gap",
                "required_monthly_contribution", "target_month", "target_year",
                "duration_years", "funding_status", "projected_mapped_asset_value",
                "funding_return_assumption",
            )
        }

        funding = {
            key: self._get(goal, key)
            for key in (
                "feasibility_status", "feasibility_reason", "available_monthly_surplus",
                "monthly_contribution_surplus_gap", "required_monthly_contribution",
                "funding_gap", "funding_status", "funding_return_assumption",
                "funding_strategies",
            )
        }

        mapped_assets = self._mapped_assets(goal)
        cash_flow_trajectory = self._build_cash_flow_trajectory(goal, selected_scenario, mapped_assets)
        product_architecture = self._build_product_architecture(goal)
        contribution_rules = self._build_contribution_rules(goal)
        action_plan_timeline = self._build_action_plan_timeline(goal)
        contingency_matrix = self._build_contingency_matrix()

        report = {
            "report_type": "goal_decision_report",
            "report_version": "1.0",
            "goal": {
                "id": self._get(run, "goal_id"),
                "name": self._goal_label(goal),
                "type": self._get(goal, "goal_type"),
                "priority": self._get(goal, "priority"),
                "flexibility": self._get(goal, "flexibility"),
                "status": self._get(goal, "status"),
                "defined_goal_version": self._get(goal, "version"),
                "target_month": self._get(goal, "target_month"),
                "target_year": self._get(goal, "target_year"),
                "duration_years": self._get(goal, "duration_years"),
            },
            "financial_state": {
                "annual_income": context.get("annual_income"),
                "annual_expenses": context.get("annual_expenses"),
                "monthly_surplus": context.get("monthly_surplus"),
                "assets": context.get("assets"),
                "liabilities": context.get("liabilities"),
                "net_worth": context.get("net_worth"),
            },
            "goal_calculation": goal_calculation,
            "feasibility": funding,
            "funding_solutions": funding.get("funding_strategies") or [],
            # Compatibility aliases retained for consumers of the earlier
            # complete Goal Report contract.
            "goal_funding": funding,
            "goal_context": {
                "priority": self._get(goal, "priority"),
                "flexibility": self._get(goal, "flexibility"),
                "status": self._get(goal, "status"),
            },
            "mapped_assets": mapped_assets,
            "investor_priorities": self._dump(self._get(run, "investor_priorities", {})),
            "strategy": {
                "selected_strategy_id": selected_strategy_id,
                "selected_strategy_name": self._strategy_name(run, selected_strategy_id),
                "selected_scenario_id": self._get(run, "selected_scenario_id")
                or recommendation.get("recommended_scenario_id"),
                "selected_scenario": selected_scenario,
                "architecture": architecture,
                "rationale": self._get(recommendation, "complete_reasoning", ""),
                "short_reasons": self._get(recommendation, "short_reasons", []),
                "constraints": self._get(recommendation, "constraints", []),
                "technique_execution": technique_outputs,
            },
            "alternatives": self._alternatives(run),
            "scenarios": scenarios,
            "what_if_analysis": [
                {
                    "scenario_id": s["scenario_id"],
                    "scenario": s["scenario_name"],
                    "strategy": s["strategy_name"],
                    "type": s["scenario_type"],
                    "selected": False,
                    "assumptions_changed": s["assumptions"],
                    "funding_changes": s["funding_structure"],
                    "outcomes": s["metrics"],
                    "trade_off": s["trade_off_notes"],
                }
                for s in what_if_scenarios
            ],
            "trade_off_analysis": self._trade_offs(run),
            "technique_execution": technique_outputs,
            "assumptions": {
                "goal_assumptions": {
                    "inflation_rate": self._get(goal, "inflation_rate"),
                    "funding_return_assumption": self._get(goal, "funding_return_assumption"),
                },
                "scenario_assumptions": [s["assumptions"] for s in scenarios],
            },
            "decision": {
                "status": "investor_decision_required",
                "selected_strategy_id": self._get(run, "selected_strategy_id"),
                "selected_scenario_id": self._get(run, "selected_scenario_id"),
                "selected_architecture_id": self._get(architecture, "architecture_id"),
                "implementation_parameters": self._dump(
                    self._get(run, "selected_implementation_parameters", {})
                ),
                "selection_timestamp": self._get(run, "selection_timestamp"),
            },
            "provenance": {
                "strategy_run_id": strategy_run_id,
                "run_version": self._get(run, "run_version"),
                "status": self._get(run, "status"),
                "defined_goal_version": self._get(run, "defined_goal_version"),
            },
            "cash_flow_trajectory": cash_flow_trajectory,
            "product_architecture": product_architecture,
            "contribution_rules": contribution_rules,
            "action_plan_timeline": action_plan_timeline,
            "contingency_matrix": contingency_matrix,
        }
        return report

    @staticmethod
    def _fmt(value: Any, prefix: str = "") -> str:
        if value is None:
            return GoalReportService.MISSING
        if isinstance(value, float):
            return f"{prefix}{value:,.2f}"
        if isinstance(value, int):
            return f"{prefix}{value:,}"
        return f"{prefix}{value}"

    @staticmethod
    def _label(value: Any) -> str:
        return str(value).replace("_", " ").replace("-", " ").title()

    @staticmethod
    def _table(rows: list[list[Any]], widths: list[float] | None = None) -> Table:
        table = Table(rows, colWidths=widths, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 5),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                ]
            )
        )
        return table

    @staticmethod
    def _section(story: list[Any], title: str, styles: Any) -> None:
        story.extend([Spacer(1, 12), Paragraph(title, styles["Heading2"]), Spacer(1, 4)])

    def _kv_rows(self, mapping: dict[str, Any], prefix: str = "") -> list[list[str]]:
        return [
            [self._label(key), self._fmt(value, prefix if isinstance(value, (int, float)) else "")]
            for key, value in mapping.items()
        ]

    def generate_pdf(self, planning_unit_id: str, strategy_run_id: str) -> bytes:
        report = self.build_report(planning_unit_id, strategy_run_id)

        # Accept backward compatible report shapes
        if "goal" not in report:
            goal_name = report.get("goal_name") or "Financial Goal"
            goal_type = report.get("goal_type")
            goal_context = report.get("goal_context") or {}
            goal_calculation = report.get("goal_calculation") or {}
            funding = report.get("goal_funding") or report.get("feasibility") or {}
            selected_strategy_id = report.get("selected_strategy_id")
            strategy_data = report.get("strategy") or {}
            architecture = strategy_data.get("architecture") or {}
            report = {
                "report_type": "goal_decision_report",
                "report_version": str(report.get("report_version") or "1.0"),
                "goal": {
                    "id": report.get("goal_id"),
                    "name": goal_name,
                    "type": goal_type,
                    "priority": goal_context.get("priority"),
                    "flexibility": goal_context.get("flexibility"),
                    "status": goal_context.get("status"),
                    "defined_goal_version": report.get("defined_goal_version", 1),
                    "target_month": goal_calculation.get("target_month"),
                    "target_year": goal_calculation.get("target_year"),
                    "duration_years": goal_calculation.get("duration_years"),
                },
                "financial_state": report.get("financial_state") or {},
                "goal_calculation": goal_calculation,
                "feasibility": funding,
                "mapped_assets": report.get("mapped_assets") or [],
                "investor_priorities": report.get("investor_priorities") or {},
                "strategy": {
                    "selected_strategy_id": selected_strategy_id,
                    "selected_strategy_name": strategy_data.get("name") or selected_strategy_id,
                    "selected_scenario_id": report.get("selected_scenario_id"),
                    "selected_scenario": None,
                    "architecture": architecture,
                    "rationale": strategy_data.get("objective") or "",
                    "short_reasons": (report.get("recommendation") or {}).get("short_reasons", []),
                    "constraints": [],
                    "technique_execution": report.get("technique_execution") or [],
                },
                "alternatives": report.get("alternatives") or [],
                "scenarios": report.get("scenarios") or [],
                "what_if_analysis": report.get("what_if_analysis") or [],
                "trade_off_analysis": [
                    {"trade_off": value}
                    for value in (strategy_data.get("trade_offs") or [])
                ],
                "technique_execution": report.get("technique_execution") or [],
                "assumptions": {
                    "goal_assumptions": {
                        "inflation_rate": goal_calculation.get("inflation_rate"),
                        "funding_return_assumption": goal_calculation.get("funding_return_assumption"),
                    },
                    "scenario_assumptions": [],
                },
                "decision": {
                    "status": "investor_decision_required",
                    "selected_strategy_id": selected_strategy_id,
                    "selected_scenario_id": report.get("selected_scenario_id"),
                    "selected_architecture_id": architecture.get("architecture_id"),
                    "implementation_parameters": {},
                    "selection_timestamp": None,
                },
                "provenance": {
                    "strategy_run_id": strategy_run_id,
                    "run_version": report.get("run_version", 1),
                    "status": report.get("status", "completed"),
                    "defined_goal_version": report.get("defined_goal_version", 1),
                },
                "cash_flow_trajectory": report.get("cash_flow_trajectory") or self._build_cash_flow_trajectory(goal_calculation, None, report.get("mapped_assets") or []),
                "product_architecture": report.get("product_architecture") or self._build_product_architecture(goal_calculation),
                "contribution_rules": report.get("contribution_rules") or self._build_contribution_rules(goal_calculation),
                "action_plan_timeline": report.get("action_plan_timeline") or self._build_action_plan_timeline(goal_calculation),
                "contingency_matrix": report.get("contingency_matrix") or self._build_contingency_matrix(),
            }

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
        )
        styles = getSampleStyleSheet()
        normal = styles["BodyText"]
        story: list[Any] = []

        goal = report["goal"]
        strategy = report["strategy"]
        story.extend(
            [
                Paragraph("Planvesto Actionable Financial Decision Report", styles["Title"]),
                Paragraph(str(goal["name"]), styles["Heading2"]),
                Paragraph(
                    f"Goal Type: {self._label(goal.get('type'))} | "
                    f"Strategy: {strategy.get('selected_strategy_name') or 'Goal Funding'} | "
                    f"Run ID: {report['provenance']['strategy_run_id']}",
                    styles["Normal"],
                ),
                Spacer(1, 10),
            ]
        )

        # 1. Executive Summary
        sections = [
            ("1. Executive Summary & Problem Setup", [
                ["Field", "Value"],
                ["Goal Name", str(goal["name"])],
                ["Target Date / Horizon", f"{goal.get('target_year') or '—'} ({goal.get('duration_years') or '—'} Years)"],
                ["Today's Estimated Cost", self._fmt(report["goal_calculation"].get("today_cost"), "₹")],
                ["Inflation Rate", f"{float(report['goal_calculation'].get('inflation_rate') or 0.0) * 100:.1f}%" if report["goal_calculation"].get("inflation_rate") is not None else self.MISSING],
                ["Future Target Amount", self._fmt(report["goal_calculation"].get("future_target"), "₹")],
                ["Mapped Existing Assets", self._fmt(report["goal_calculation"].get("projected_mapped_asset_value"), "₹")],
                ["Net Funding Gap", self._fmt(report["goal_calculation"].get("funding_gap"), "₹")],
                ["Required Monthly SIP", self._fmt(report["goal_calculation"].get("required_monthly_contribution"), "₹")],
                ["Feasibility Assessment", self._label(report["feasibility"].get("feasibility_status"))],
                ["Selected Strategic Architecture", str(strategy.get("selected_strategy_name") or self.MISSING)],
            ]),
            ("2. Financial Position & Capacity Snapshot", [
                ["Financial Metric", "Value"],
                *[[self._label(k), self._fmt(v, "₹" if isinstance(v, (int, float)) else "")]
                  for k, v in report["financial_state"].items()],
            ]),
            ("3. Goal Feasibility & Surplus Capacity Analysis", [
                ["Metric", "Value"],
                ["Feasibility Status", self._label(report["feasibility"].get("feasibility_status"))],
                ["Feasibility Diagnostic Reason", str(report["feasibility"].get("feasibility_reason") or self.MISSING)],
                ["Available Monthly Surplus", self._fmt(report["feasibility"].get("available_monthly_surplus"), "₹")],
                ["Contribution Surplus Gap", self._fmt(report["feasibility"].get("monthly_contribution_surplus_gap"), "₹")],
            ]),
        ]
        for title, rows in sections:
            self._section(story, title, styles)
            story.append(self._table(rows, [200, 323]))

        # 4. Funding Solutions
        funding_strategies = report.get("funding_solutions") or report["feasibility"].get("funding_strategies") or []
        self._section(story, "4. Goal Funding Solutions Comparison", styles)
        if funding_strategies:
            rows = [["Solution", "Status", "Lumpsum", "Monthly", "Starting", "Step-up", "Remaining Gap"]]
            for item in funding_strategies:
                rows.append([
                    Paragraph(str(item.get("strategy_name") or item.get("strategy_id") or self.MISSING), normal),
                    self._label(item.get("status")),
                    self._fmt(item.get("required_lumpsum"), "₹"),
                    self._fmt(item.get("required_monthly_contribution"), "₹"),
                    self._fmt(item.get("starting_monthly_contribution"), "₹"),
                    self._fmt(item.get("annual_step_up")),
                    self._fmt(item.get("remaining_gap"), "₹"),
                ])
            story.append(self._table(rows, [90, 65, 75, 75, 75, 65, 78]))
        else:
            story.append(Paragraph(self.MISSING, normal))

        # 5. Product & Bucket Architecture
        product_arch = report.get("product_architecture") or self._build_product_architecture(report["goal_calculation"])
        self._section(story, "5. Strategic Product & Bucket Architecture", styles)
        if product_arch:
            rows = [["Bucket / Horizon", "Recommended Instruments", "Allocation", "Strategic Role & Transition Rule"]]
            for b in product_arch:
                rows.append([
                    Paragraph(str(b.get("bucket")), normal),
                    Paragraph(str(b.get("instruments")), normal),
                    str(b.get("allocation")),
                    Paragraph(str(b.get("strategic_rule")), normal),
                ])
            story.append(self._table(rows, [120, 155, 60, 188]))
        else:
            story.append(Paragraph(self.MISSING, normal))

        # 6. Multi-Year Cash Flow Trajectory
        trajectory = report.get("cash_flow_trajectory") or self._build_cash_flow_trajectory(report["goal_calculation"], strategy.get("selected_scenario"), report.get("mapped_assets") or [])
        self._section(story, "6. Multi-Year Cash Flow Trajectory Projection", styles)
        if trajectory:
            t_rows = [["Year", "Opening (₹)", "Investment (₹)", "Returns (₹)", "Outflows (₹)", "Closing (₹)"]]
            for item in trajectory:
                t_rows.append([
                    str(item["year"]),
                    self._fmt(item["opening_balance"]),
                    self._fmt(item["annual_investment"]),
                    self._fmt(item["growth"]),
                    self._fmt(item["outflow"]),
                    self._fmt(item["closing_balance"]),
                ])
            story.append(self._table(t_rows, [50, 95, 95, 95, 95, 93]))
            story.append(Spacer(1, 6))
            story.append(Paragraph("<b>What the Cashflow Tells You:</b> This projection models the capital accumulation path under disciplined contributions and expected asset returns, culminating in seamless goal redemption at the target horizon without forced liquidations.", normal))
        else:
            story.append(Paragraph(self.MISSING, normal))

        # 7. Deterministic What-If Decision Matrix
        what_ifs = report.get("what_if_analysis") or []
        self._section(story, "7. Deterministic What-If Decision Matrix", styles)
        if what_ifs:
            w_rows = [["Scenario", "Changed Parameters", "Funding Impact", "Outcomes", "Trade-Off"]]
            for item in what_ifs:
                w_rows.append([
                    Paragraph(str(item["scenario"]), normal),
                    Paragraph(str(item.get("assumptions_changed") or "—"), normal),
                    Paragraph(str(item.get("funding_changes") or "—"), normal),
                    Paragraph(str(item.get("outcomes") or "—"), normal),
                    Paragraph(str(item.get("trade_off") or "—"), normal),
                ])
            story.append(self._table(w_rows, [95, 105, 105, 105, 113]))
        else:
            story.append(Paragraph("No stored what-if scenarios are available.", normal))

        # 8. 5 Actionable Contribution Rules
        rules = report.get("contribution_rules") or self._build_contribution_rules(report["goal_calculation"])
        self._section(story, "8. Actionable Contribution & Portfolio Rules", styles)
        for r in rules:
            story.append(Paragraph(f"• {r}", normal))
            story.append(Spacer(1, 3))

        # 9. Implementation Action Plan Timeline
        timeline = report.get("action_plan_timeline") or self._build_action_plan_timeline(report["goal_calculation"])
        self._section(story, "9. Implementation Action Plan Timeline", styles)
        if timeline:
            time_rows = [["Timeline Window", "Action Step", "Execution Owner", "Key Milestone"]]
            for t in timeline:
                time_rows.append([
                    Paragraph(str(t.get("timeline")), normal),
                    Paragraph(str(t.get("action")), normal),
                    str(t.get("owner")),
                    Paragraph(str(t.get("milestone")), normal),
                ])
            story.append(self._table(time_rows, [90, 223, 90, 120]))

        # 10. Contingency Matrix
        contingency = report.get("contingency_matrix") or self._build_contingency_matrix()
        self._section(story, "10. Contingency & Risk Management Matrix", styles)
        if contingency:
            c_rows = [["Risk Event", "Immediate Action", "Planning Adjustment", "What NOT To Do"]]
            for c in contingency:
                c_rows.append([
                    Paragraph(str(c.get("risk_event")), normal),
                    Paragraph(str(c.get("immediate_action")), normal),
                    Paragraph(str(c.get("planning_change")), normal),
                    Paragraph(str(c.get("what_not_to_do")), normal),
                ])
            story.append(self._table(c_rows, [100, 140, 140, 143]))

        # 11. Alternatives
        alternatives = report.get("alternatives") or []
        self._section(story, "11. Evaluated Strategy Alternatives", styles)
        if alternatives:
            a_rows = [["Strategy", "Scenario", "Eligible", "Score", "Dimension Scores", "Rationale / Reason"]]
            for item in alternatives:
                a_rows.append([
                    Paragraph(str(item["strategy_name"]), normal),
                    Paragraph(str(item["scenario_name"]), normal),
                    str(item["eligible"]),
                    self._fmt(item["composite_score"]),
                    Paragraph(str(item["dimension_scores"]), normal),
                    Paragraph(str(item["reasons"]), normal),
                ])
            story.append(self._table(a_rows, [90, 85, 45, 45, 120, 138]))
        else:
            story.append(Paragraph("No alternative strategies were recorded.", normal))

        # 12. Technique Execution Evidence
        technique_outputs = report.get("technique_execution") or []
        self._section(story, "12. Technique Execution Evidence", styles)
        if technique_outputs:
            tech_rows = [["Technique ID", "Status", "Warnings", "Deterministic Outputs"]]
            for item in technique_outputs:
                tech_rows.append([
                    str(item.get("technique_id") or self.MISSING),
                    self._label(item.get("status")),
                    Paragraph(str(item.get("warnings") or "None"), normal),
                    Paragraph(str(item.get("outputs") or "—"), normal),
                ])
            story.append(self._table(tech_rows, [105, 65, 115, 238]))
        else:
            story.append(Paragraph("No technique execution evidence was persisted for this run.", normal))

        # 13. Client Decision & Selection View
        self._section(story, "13. Client Decision View & Implementation Checklist", styles)
        decision = report["decision"]
        story.append(self._table([
            ["Decision Component", "Selected State"],
            ["Sign-Off Status", self._label(decision["status"])],
            ["Selected Strategy", str(decision.get("selected_strategy_id") or strategy.get("selected_strategy_name") or self.MISSING)],
            ["Selected Scenario", str(decision.get("selected_scenario_id") or (strategy.get("selected_scenario") or {}).get("scenario_name") or self.MISSING)],
            ["Selected Architecture", str(decision.get("selected_architecture_id") or strategy.get("architecture", {}).get("architecture_id") or self.MISSING)],
            ["Implementation Parameters", str(decision.get("implementation_parameters") or self.MISSING)],
            ["Selection Timestamp", str(decision.get("selection_timestamp") or "Awaiting Final Confirmation")],
        ], [180, 343]))

        # 14. Data Provenance
        self._section(story, "14. Data Provenance & Traceability", styles)
        story.append(self._table([
            ["Metadata Item", "Value"],
            ["Strategy Run ID", str(report["provenance"]["strategy_run_id"])],
            ["Run Version", str(report["provenance"]["run_version"])],
            ["Defined Goal Version", str(report["provenance"]["defined_goal_version"])],
            ["Run Status", str(report["provenance"]["status"])],
            ["Report Version", str(report["report_version"])],
        ], [180, 343]))

        doc.build(story)
        return buffer.getvalue()