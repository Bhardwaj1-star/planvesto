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
            "mapped_assets": self._mapped_assets(goal),
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
    def _table(rows: list[list[str]], widths: list[float] | None = None) -> Table:
        table = Table(rows, colWidths=widths, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        return table

    @staticmethod
    def _section(story: list[Any], title: str, styles: Any) -> None:
        story.extend([Spacer(1, 10), Paragraph(title, styles["Heading2"])])

    def _kv_rows(self, mapping: dict[str, Any], prefix: str = "") -> list[list[str]]:
        return [
            [self._label(key), self._fmt(value, prefix if isinstance(value, (int, float)) else "")]
            for key, value in mapping.items()
        ]

    def generate_pdf(self, planning_unit_id: str, strategy_run_id: str) -> bytes:
        report = self.build_report(planning_unit_id, strategy_run_id)
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
        )
        styles = getSampleStyleSheet()
        story: list[Any] = []

        goal = report["goal"]
        strategy = report["strategy"]
        story.extend(
            [
                Paragraph("Planvesto Financial Decision Report", styles["Title"]),
                Paragraph(str(goal["name"]), styles["Heading2"]),
                Paragraph(
                    f"Goal type: {self._label(goal.get('type'))} | "
                    f"Run: {report['provenance']['strategy_run_id']} | "
                    f"Version: {report['provenance']['run_version']}",
                    styles["BodyText"],
                ),
                Spacer(1, 12),
            ]
        )

        sections = [
            ("1. Executive Summary", [
                ["Item", "Value"],
                ["Goal", str(goal["name"])],
                ["Goal status", self._label(goal.get("status"))],
                ["Funding status", self._label(report["goal_calculation"].get("funding_status"))],
                ["Feasibility", self._label(report["feasibility"].get("feasibility_status"))],
                ["Funding gap", self._fmt(report["goal_calculation"].get("funding_gap"), "₹")],
                ["Required monthly contribution", self._fmt(report["goal_calculation"].get("required_monthly_contribution"), "₹")],
                ["Selected strategy", str(strategy.get("selected_strategy_name") or self.MISSING)],
                ["Decision status", self._label(report["decision"]["status"])],
            ]),
            ("2. Financial Position", [
                ["Metric", "Current"],
                *[[self._label(k), self._fmt(v, "₹" if isinstance(v, (int, float)) else "")]
                  for k, v in report["financial_state"].items()],
            ]),
            ("3. Goal & Calculation", [
                ["Calculation", "Value"],
                *[[self._label(k), self._fmt(v, "₹" if k in {"today_cost", "future_target", "funding_gap", "required_monthly_contribution", "projected_mapped_asset_value"} else "")]
                  for k, v in report["goal_calculation"].items()],
            ]),
            ("4. Feasibility & Funding Options", [
                ["Metric", "Value"],
                ["Feasibility status", self._label(report["feasibility"].get("feasibility_status"))],
                ["Reason", str(report["feasibility"].get("feasibility_reason") or self.MISSING)],
                ["Available monthly surplus", self._fmt(report["feasibility"].get("available_monthly_surplus"), "₹")],
                ["Contribution surplus gap", self._fmt(report["feasibility"].get("monthly_contribution_surplus_gap"), "₹")],
            ]),
        ]
        for title, rows in sections:
            self._section(story, title, styles)
            story.append(self._table(rows, [210, 315]))

        funding_strategies = report["feasibility"].get("funding_strategies") or []
        self._section(story, "5. Funding Solutions", styles)
        if funding_strategies:
            rows = [["Solution", "Status", "Lumpsum", "Monthly", "Starting", "Step-up", "Remaining Gap"]]
            for item in funding_strategies:
                rows.append([
                    str(item.get("strategy_name") or item.get("strategy_id") or self.MISSING),
                    self._label(item.get("status")),
                    self._fmt(item.get("required_lumpsum"), "₹"),
                    self._fmt(item.get("required_monthly_contribution"), "₹"),
                    self._fmt(item.get("starting_monthly_contribution"), "₹"),
                    self._fmt(item.get("annual_step_up")),
                    self._fmt(item.get("remaining_gap"), "₹"),
                ])
            story.append(self._table(rows, [92, 62, 65, 65, 70, 55, 70]))
        else:
            story.append(Paragraph(self.MISSING, styles["BodyText"]))

        self._section(story, "6. Strategy & Architecture", styles)
        story.append(self._table([
            ["Element", "Output"],
            ["Selected strategy", str(strategy.get("selected_strategy_name") or self.MISSING)],
            ["Selected scenario", str((strategy.get("selected_scenario") or {}).get("scenario_name") or self.MISSING)],
            ["Architecture", str(strategy["architecture"].get("architecture_id") or self.MISSING)],
            ["Solutions", str(strategy["architecture"].get("solution_ids") or self.MISSING)],
            ["Techniques", str(strategy["architecture"].get("technique_ids") or self.MISSING)],
            ["Supporting strategies", str(strategy["architecture"].get("supporting_strategy_ids") or self.MISSING)],
        ], [210, 315]))

        self._section(story, "7. Technique Execution Evidence", styles)
        technique_outputs = report.get("technique_execution") or []
        if technique_outputs:
            rows = [["Technique", "Status", "Warnings", "Outputs"]]
            for item in technique_outputs:
                rows.append([str(item.get("technique_id") or self.MISSING), self._label(item.get("status")), str(item.get("warnings") or ""), str(item.get("outputs") or "")])
            story.append(self._table(rows, [105, 65, 115, 170]))
        else:
            story.append(Paragraph("No technique execution evidence was persisted for this run.", styles["BodyText"]))

        self._section(story, "8. Why This Strategy", styles)
        for item in strategy.get("short_reasons") or []:
            story.append(Paragraph(f"• {item}", styles["BodyText"]))
        if strategy.get("rationale"):
            story.append(Spacer(1, 6))
            story.append(Paragraph(str(strategy["rationale"]), styles["BodyText"]))
        if strategy.get("constraints"):
            story.append(Spacer(1, 6))
            story.append(Paragraph("Constraints: " + "; ".join(map(str, strategy["constraints"])), styles["BodyText"]))

        self._section(story, "8. What-If Analysis", styles)
        what_ifs = report["what_if_analysis"]
        if what_ifs:
            rows = [["Scenario", "Strategy", "Selected", "Funding / Changes", "Outcomes", "Trade-off"]]
            for item in what_ifs:
                rows.append([
                    str(item["scenario"]),
                    str(item["strategy"]),
                    "Yes" if item["selected"] else "No",
                    str(item["funding_changes"]),
                    str(item["outcomes"]),
                    str(item["trade_off"]),
                ])
            story.append(self._table(rows, [85, 75, 45, 105, 105, 110]))
        else:
            story.append(Paragraph("No stored what-if scenarios are available.", styles["BodyText"]))

        self._section(story, "9. Trade-offs", styles)
        for item in report["trade_off_analysis"]:
            story.append(Paragraph(f"• {item['trade_off']}", styles["BodyText"]))
        if not report["trade_off_analysis"]:
            story.append(Paragraph(self.MISSING, styles["BodyText"]))

        self._section(story, "10. Alternatives", styles)
        alternatives = report["alternatives"]
        if alternatives:
            rows = [["Strategy", "Scenario", "Eligible", "Score", "Dimensions", "Reasons"]]
            for item in alternatives:
                rows.append([
                    str(item["strategy_name"]),
                    str(item["scenario_name"]),
                    str(item["eligible"]),
                    self._fmt(item["composite_score"]),
                    str(item["dimension_scores"]),
                    str(item["reasons"]),
                ])
            story.append(self._table(rows, [90, 85, 45, 55, 100, 105]))
        else:
            story.append(Paragraph("No alternative strategies were recorded.", styles["BodyText"]))

        self._section(story, "11. Assumptions & Evidence", styles)
        assumptions = report["assumptions"]
        story.append(self._table([
            ["Source", "Value"],
            ["Goal assumptions", str(assumptions["goal_assumptions"])],
            ["Scenario assumptions", str(assumptions["scenario_assumptions"])],
            ["Mapped assets", str(report["mapped_assets"])],
            ["Investor priorities", str(report["investor_priorities"])],
        ], [180, 345]))

        self._section(story, "12. Decision", styles)
        decision = report["decision"]
        story.append(self._table([
            ["Decision item", "Current state"],
            ["Status", self._label(decision["status"])],
            ["Selected strategy", str(decision.get("selected_strategy_id") or self.MISSING)],
            ["Selected scenario", str(decision.get("selected_scenario_id") or self.MISSING)],
            ["Selected architecture", str(decision.get("selected_architecture_id") or self.MISSING)],
            ["Implementation parameters", str(decision.get("implementation_parameters") or self.MISSING)],
            ["Selection timestamp", str(decision.get("selection_timestamp") or self.MISSING)],
        ], [210, 315]))

        self._section(story, "13. Data Provenance", styles)
        story.append(self._table([
            ["Field", "Value"],
            ["Strategy run", str(report["provenance"]["strategy_run_id"])],
            ["Run version", str(report["provenance"]["run_version"])],
            ["Defined Goal version", str(report["provenance"]["defined_goal_version"])],
            ["Run status", str(report["provenance"]["status"])],
            ["Report version", str(report["report_version"])],
        ], [210, 315]))

        doc.build(story)
        return buffer.getvalue()
