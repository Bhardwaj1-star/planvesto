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
    """Generate the same complete report contract for every goal type."""

    def __init__(self):
        self.goal_repo = GoalRepository()
        self.strategy_repo = StrategyRepository()
        self.strategy_service = StrategyService()

    def _load(self, planning_unit_id: str, strategy_run_id: str):
        run = self.strategy_repo.get_run_by_id(planning_unit_id, strategy_run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Strategy run not found")
        goal = self.goal_repo.get_defined_goal_by_version(planning_unit_id, run.goal_id, run.defined_goal_version) or self.goal_repo.get_latest_defined_goal(planning_unit_id, run.goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Underlying goal not found")
        context = self.strategy_service._financial_context(planning_unit_id, goal)
        return run, goal, context

    @staticmethod
    def _goal_label(goal: Any) -> str:
        name = getattr(goal, "name", None) or getattr(goal, "goal_name", None)
        if name: return str(name)
        return str(getattr(goal, "goal_type", None) or "Financial Goal").replace("_", " ").title()

    @staticmethod
    def _goal_details(goal: Any) -> dict[str, Any]:
        metadata = getattr(goal, "version_metadata", None) or {}
        dynamic = metadata.get("dynamic_details") if isinstance(metadata, dict) else None
        if not isinstance(dynamic, dict): dynamic = {}
        return {str(key).replace("_", " ").replace("-", " ").title(): value for key, value in dynamic.items() if value not in (None, "", [], {})}

    @staticmethod
    def _mapped_assets(goal: Any) -> list[dict[str, Any]]:
        mappings = getattr(goal, "mapped_assets", None) or []
        rows: list[dict[str, Any]] = []
        for mapping in mappings:
            if hasattr(mapping, "model_dump"): mapping = mapping.model_dump(mode="json")
            if not isinstance(mapping, dict): continue
            rows.append({"asset_name": mapping.get("asset_name") or mapping.get("asset_id"), "allocation": mapping.get("allocated_amount"), "allocation_percentage": mapping.get("allocated_percentage"), "expected_return": mapping.get("expected_return"), "projected_value": mapping.get("projected_value")})
        return rows

    def build_report(self, planning_unit_id: str, strategy_run_id: str) -> dict[str, Any]:
        run, goal, context = self._load(planning_unit_id, strategy_run_id)
        strategy = next((s for s in run.applicable_strategies if s.strategy_id == run.selected_strategy_id), run.applicable_strategies[0] if run.applicable_strategies else None)
        return {
            "report_type": "goal_strategy_report", "goal_id": run.goal_id, "goal_name": self._goal_label(goal), "goal_type": getattr(goal, "goal_type", None), "goal_details": self._goal_details(goal), "mapped_assets": self._mapped_assets(goal), "strategy_run_id": strategy_run_id,
            "strategy": {"name": strategy.name if strategy else None, "objective": strategy.strategic_objective if strategy else None, "trade_offs": strategy.trade_offs if strategy else []},
            "recommendation": run.recommendation.model_dump(mode="json"), "selected_strategy_id": run.selected_strategy_id,
            "goal_calculation": {"today_cost": getattr(goal, "today_cost", None), "inflation_rate": getattr(goal, "inflation_rate", None), "future_target": getattr(goal, "future_target", None), "funding_gap": getattr(goal, "funding_gap", None), "required_monthly_contribution": getattr(goal, "required_monthly_contribution", None), "target_month": getattr(goal, "target_month", None), "target_year": getattr(goal, "target_year", None), "duration_years": getattr(goal, "duration_years", None), "funding_status": getattr(goal, "funding_status", None), "projected_mapped_asset_value": getattr(goal, "projected_mapped_asset_value", None)},
            "financial_state": {"annual_income": context.get("annual_income"), "annual_expenses": context.get("annual_expenses"), "monthly_surplus": context.get("monthly_surplus"), "assets": context.get("assets"), "liabilities": context.get("liabilities"), "net_worth": context.get("net_worth")},
        }

    @staticmethod
    def _table(rows: list[list[str]]) -> Table:
        table = Table(rows, colWidths=[210, 270])
        table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("PADDING", (0, 0), (-1, -1), 7)]))
        return table

    def generate_pdf(self, planning_unit_id: str, strategy_run_id: str) -> bytes:
        report = self.build_report(planning_unit_id, strategy_run_id)
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
        styles = getSampleStyleSheet()
        story = [Paragraph("Financial Goal Strategy Report", styles["Title"]), Paragraph(report["goal_name"], styles["Heading2"]), Paragraph(str(report.get("goal_type") or "Financial Goal"), styles["BodyText"]), Spacer(1, 12)]
        details = report.get("goal_details", {})
        if details:
            story.extend([Paragraph("Goal Details", styles["Heading2"]), self._table([["Item", "Value"], *[[str(k), str(v)] for k, v in details.items()]]), Spacer(1, 16)])
        calc = report["goal_calculation"]
        rows = [["Item", "Value"]] + [[key.replace("_", " ").title(), str(value)] for key, value in calc.items() if value is not None]
        if len(rows) > 1:
            story.extend([Paragraph("Goal Calculation", styles["Heading2"]), self._table(rows), Spacer(1, 16)])
        mapped_assets = report.get("mapped_assets", [])
        if mapped_assets:
            story.append(Paragraph("Goal-Funding Assets", styles["Heading2"]))
            asset_rows = [["Asset", "Allocated", "Allocation %", "Expected Return", "Projected Value"]]
            for asset in mapped_assets:
                asset_rows.append([str(asset.get("asset_name") or "—"), str(asset.get("allocation") if asset.get("allocation") is not None else "—"), str(asset.get("allocation_percentage") if asset.get("allocation_percentage") is not None else "—"), str(asset.get("expected_return") if asset.get("expected_return") is not None else "—"), str(asset.get("projected_value") if asset.get("projected_value") is not None else "—")])
            asset_table = Table(asset_rows, colWidths=[125, 85, 75, 90, 105], repeatRows=1)
            asset_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("PADDING", (0, 0), (-1, -1), 5)]))
            story.extend([asset_table, Spacer(1, 16)])
        strategy = report["strategy"]
        story.append(Paragraph("Strategy", styles["Heading2"]))
        story.append(Paragraph(str(strategy.get("name") or "Not selected"), styles["Heading3"]))
        if strategy.get("objective"): story.append(Paragraph(str(strategy["objective"]), styles["BodyText"]))
        if strategy.get("trade_offs"):
            story.extend([Spacer(1, 6), Paragraph("Trade-offs", styles["Heading3"])]); [story.append(Paragraph(f"• {trade_off}", styles["BodyText"])) for trade_off in strategy["trade_offs"]]
        story.append(Spacer(1, 12))
        story.append(Paragraph("Financial State", styles["Heading2"]))
        financial = report["financial_state"]
        story.append(self._table([["Item", "Value"], *[[k.replace("_", " ").title(), str(v) if v is not None else "Not available"] for k, v in financial.items()]]))
        story.append(Spacer(1, 16))
        rec = report["recommendation"]
        story.append(Paragraph("Recommendation", styles["Heading2"]))
        for reason in rec.get("short_reasons", []): story.append(Paragraph(f"• {reason}", styles["BodyText"]))
        if rec.get("complete_reasoning"): story.extend([Spacer(1, 6), Paragraph(str(rec["complete_reasoning"]), styles["BodyText"])] )
        doc.build(story)
        return buffer.getvalue()
