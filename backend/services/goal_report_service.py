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
from services.strategy_service import StrategyService


class GoalReportService:
    """Goal-agnostic report/PDF service built from the persisted StrategyRun."""

    def __init__(self):
        self.goal_repo = GoalRepository()
        self.strategy_repo = StrategyRepository()
        self.strategy_service = StrategyService()

    def _load(self, planning_unit_id: str, strategy_run_id: str):
        run = self.strategy_repo.get_run_by_id(planning_unit_id, strategy_run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Strategy run not found")
        goal = self.goal_repo.get_defined_goal_by_version(
            planning_unit_id, run.goal_id, run.defined_goal_version
        ) or self.goal_repo.get_latest_defined_goal(planning_unit_id, run.goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Underlying goal not found")
        context = self.strategy_service._financial_context(planning_unit_id, goal)
        return run, goal, context

    @staticmethod
    def _goal_label(goal: Any) -> str:
        name = getattr(goal, "name", None) or getattr(goal, "goal_name", None)
        if name:
            return str(name)
        goal_type = getattr(goal, "goal_type", None) or "Financial Goal"
        return str(goal_type).replace("_", " ").title()

    @staticmethod
    def _goal_specific_details(goal: Any) -> dict[str, Any]:
        metadata = getattr(goal, "version_metadata", None) or {}
        dynamic = metadata.get("dynamic_details") if isinstance(metadata, dict) else None
        if not isinstance(dynamic, dict):
            dynamic = {}

        # Never expose retirement-only calculation metadata as generic goal details.
        details: dict[str, Any] = {}
        goal_type = str(getattr(goal, "goal_type", "") or "")
        if goal_type == "Vehicle":
            for key, label in (
                ("vehicleType", "Vehicle Type"),
                ("vehicleCondition", "Vehicle Condition"),
            ):
                value = dynamic.get(key)
                if value not in (None, ""):
                    details[label] = value
        elif goal_type == "Retirement / Financial Freedom":
            for key, label in (
                ("currentAge", "Current Age"),
                ("lifeExpectancy", "Life Expectancy"),
            ):
                value = dynamic.get(key)
                if value not in (None, ""):
                    details[label] = value
        else:
            for key, value in dynamic.items():
                if value not in (None, ""):
                    details[str(key).replace("_", " ").title()] = value
        return details

    def build_report(self, planning_unit_id: str, strategy_run_id: str) -> dict[str, Any]:
        run, goal, context = self._load(planning_unit_id, strategy_run_id)
        strategy = next(
            (s for s in run.applicable_strategies if s.strategy_id == run.selected_strategy_id),
            run.applicable_strategies[0] if run.applicable_strategies else None,
        )
        return {
            "report_type": "goal_strategy_report",
            "goal_id": run.goal_id,
            "goal_name": self._goal_label(goal),
            "goal_type": getattr(goal, "goal_type", None),
            "goal_details": self._goal_specific_details(goal),
            "strategy_run_id": strategy_run_id,
            "strategy": {
                "name": strategy.name if strategy else None,
                "objective": strategy.strategic_objective if strategy else None,
                "trade_offs": strategy.trade_offs if strategy else [],
            },
            "recommendation": run.recommendation.model_dump(mode="json"),
            "selected_strategy_id": run.selected_strategy_id,
            "approval_status": run.approval_status,
            "goal_calculation": {
                "today_cost": getattr(goal, "today_cost", None),
                "future_target": getattr(goal, "future_target", None),
                "funding_gap": getattr(goal, "funding_gap", None),
                "required_monthly_contribution": getattr(goal, "required_monthly_contribution", None),
                "target_month": getattr(goal, "target_month", None),
                "target_year": getattr(goal, "target_year", None),
                "duration_years": getattr(goal, "duration_years", None),
                "funding_status": getattr(goal, "funding_status", None),
                "projected_mapped_asset_value": getattr(goal, "projected_mapped_asset_value", None),
            },
            "financial_state": {
                "annual_income": context.get("annual_income"),
                "annual_expenses": context.get("annual_expenses"),
                "monthly_surplus": context.get("monthly_surplus"),
                "assets": context.get("assets"),
                "liabilities": context.get("liabilities"),
                "net_worth": context.get("net_worth"),
            },
        }

    def generate_pdf(self, planning_unit_id: str, strategy_run_id: str) -> bytes:
        report = self.build_report(planning_unit_id, strategy_run_id)
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("Financial Goal Strategy Report", styles["Title"]),
            Paragraph(report["goal_name"], styles["Heading2"]),
            Spacer(1, 12),
        ]

        details = report.get("goal_details", {})
        if details:
            story.append(Paragraph("Goal Details", styles["Heading2"]))
            rows = [["Item", "Value"], *[[str(k), str(v)] for k, v in details.items()]]
            table = Table(rows, colWidths=[210, 270])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]))
            story.extend([table, Spacer(1, 16)])

        rows = [["Item", "Value"]]
        calc = report["goal_calculation"]
        for key, value in calc.items():
            if value is not None:
                rows.append([key.replace("_", " ").title(), str(value)])
        if len(rows) > 1:
            table = Table(rows, colWidths=[210, 270])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]))
            story.extend([table, Spacer(1, 16)])

        strategy = report["strategy"]
        story.append(Paragraph("Strategy", styles["Heading2"]))
        story.append(Paragraph(str(strategy.get("name") or "Not selected"), styles["Heading3"]))
        if strategy.get("objective"):
            story.append(Paragraph(str(strategy["objective"]), styles["BodyText"]))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Financial State", styles["Heading2"]))
        financial = report["financial_state"]
        rows = [[k.replace("_", " ").title(), str(v) if v is not None else "Not available"] for k, v in financial.items()]
        table = Table([["Item", "Value"], *rows], colWidths=[210, 270])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("PADDING", (0, 0), (-1, -1), 7),
        ]))
        story.extend([table, Spacer(1, 16)])

        rec = report["recommendation"]
        story.append(Paragraph("Recommendation", styles["Heading2"]))
        for reason in rec.get("short_reasons", []):
            story.append(Paragraph(f"• {reason}", styles["BodyText"]))
        if rec.get("complete_reasoning"):
            story.append(Spacer(1, 6))
            story.append(Paragraph(str(rec["complete_reasoning"]), styles["BodyText"]))

        doc.build(story)
        return buffer.getvalue()
