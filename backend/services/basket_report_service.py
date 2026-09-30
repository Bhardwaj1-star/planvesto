from __future__ import annotations

from io import BytesIO
from typing import Any

from fastapi import HTTPException
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from data.goal_repository import GoalRepository
from data.strategy_repository import StrategyRepository
from services.goal_report_service import GoalReportService


class BasketReportService:
    """Build a basket-level report by aggregating existing goal-level reports.

    Basket membership is supplied by the caller for now; this deliberately avoids
    introducing a new database schema until basket persistence is finalized.
    """

    def __init__(self):
        self.goal_repo = GoalRepository()
        self.strategy_repo = StrategyRepository()
        self.goal_report_service = GoalReportService()

    @staticmethod
    def _priority_rank(value: Any) -> int:
        return {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(str(value or "").lower(), 4)

    def build_report(
        self,
        planning_unit_id: str,
        basket_name: str,
        goal_ids: list[str],
    ) -> dict[str, Any]:
        if not goal_ids:
            raise HTTPException(status_code=400, detail="At least one goal is required for a basket report")

        unique_goal_ids = list(dict.fromkeys(goal_ids))
        goal_reports: list[dict[str, Any]] = []
        missing: list[str] = []

        for goal_id in unique_goal_ids:
            run = self.strategy_repo.get_latest_run(planning_unit_id, goal_id)
            if not run or not run.strategy_run_id:
                missing.append(goal_id)
                continue
            try:
                goal_reports.append(
                    self.goal_report_service.build_report(planning_unit_id, run.strategy_run_id)
                )
            except HTTPException:
                missing.append(goal_id)

        if missing:
            raise HTTPException(
                status_code=404,
                detail={"message": "Some goals do not have a usable strategy report", "goal_ids": missing},
            )

        required_monthly = sum(
            float(r.get("goal_calculation", {}).get("required_monthly_contribution") or 0.0)
            for r in goal_reports
        )
        funding_gap = sum(
            float(r.get("goal_calculation", {}).get("funding_gap") or 0.0)
            for r in goal_reports
        )
        projected_value = sum(
            float(r.get("goal_calculation", {}).get("projected_mapped_asset_value") or 0.0)
            for r in goal_reports
        )
        target_value = sum(
            float(r.get("goal_calculation", {}).get("future_target") or 0.0)
            for r in goal_reports
        )

        ordered = sorted(
            goal_reports,
            key=lambda r: self._priority_rank(
                r.get("goal_calculation", {}).get("priority")
                or r.get("priority")
                or "low"
            ),
        )

        return {
            "report_type": "goal_basket_report",
            "planning_unit_id": planning_unit_id,
            "basket": {
                "name": basket_name.strip() or "Goal Basket",
                "goal_ids": unique_goal_ids,
                "goal_count": len(goal_reports),
            },
            "summary": {
                "combined_future_target": target_value,
                "combined_projected_mapped_asset_value": projected_value,
                "combined_funding_gap": funding_gap,
                "combined_required_monthly_contribution": required_monthly,
                "funding_status": "Shortfall" if funding_gap > 0 else "On Track",
            },
            "goals": [
                {
                    "goal_id": r.get("goal_id"),
                    "goal_name": r.get("goal_name"),
                    "goal_type": r.get("goal_type"),
                    "priority": r.get("goal_calculation", {}).get("priority") or r.get("priority"),
                    "target_date": (
                        f"{r.get('goal_calculation', {}).get('target_year')}-{int(r.get('goal_calculation', {}).get('target_month')):02d}"
                        if r.get("goal_calculation", {}).get("target_year") and r.get("goal_calculation", {}).get("target_month")
                        else None
                    ),
                    "future_target": r.get("goal_calculation", {}).get("future_target"),
                    "projected_mapped_asset_value": r.get("goal_calculation", {}).get("projected_mapped_asset_value"),
                    "funding_gap": r.get("goal_calculation", {}).get("funding_gap"),
                    "required_monthly_contribution": r.get("goal_calculation", {}).get("required_monthly_contribution"),
                    "funding_status": r.get("goal_calculation", {}).get("funding_status"),
                    "strategy_run_id": r.get("strategy_run_id"),
                    "strategy_name": r.get("strategy", {}).get("name"),
                }
                for r in ordered
            ],
            "strategy_summary": [
                {
                    "goal_id": r.get("goal_id"),
                    "goal_name": r.get("goal_name"),
                    "strategy_name": r.get("strategy", {}).get("name"),
                    "objective": r.get("strategy", {}).get("objective"),
                    "trade_offs": r.get("strategy", {}).get("trade_offs", []),
                }
                for r in ordered
            ],
            "planning_note": "This basket report aggregates existing goal-level calculations and strategies. It does not replace the Complete Financial Plan or independently allocate investor resources.",
        }

    @staticmethod
    def _table(rows: list[list[str]], widths: list[float]) -> Table:
        table = Table(rows, colWidths=widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        return table

    def generate_pdf(self, planning_unit_id: str, basket_name: str, goal_ids: list[str]) -> bytes:
        report = self.build_report(planning_unit_id, basket_name, goal_ids)
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("Goal Basket Report", styles["Title"]),
            Paragraph(report["basket"]["name"], styles["Heading2"]),
            Spacer(1, 12),
        ]

        summary = report["summary"]
        story.extend([
            Paragraph("Basket Summary", styles["Heading2"]),
            self._table(
                [["Metric", "Value"]] + [[k.replace("_", " ").title(), str(v)] for k, v in summary.items()],
                [240, 240],
            ),
            Spacer(1, 14),
        ])

        rows = [["Goal", "Priority", "Target", "Gap", "Required/Mo", "Strategy"]]
        for goal in report["goals"]:
            rows.append([
                str(goal.get("goal_name") or "—"),
                str(goal.get("priority") or "—"),
                str(goal.get("target_date") or "—"),
                str(goal.get("funding_gap") or 0),
                str(goal.get("required_monthly_contribution") or 0),
                str(goal.get("strategy_name") or "—"),
            ])
        story.extend([
            Paragraph("Goals in Basket", styles["Heading2"]),
            self._table(rows, [90, 60, 60, 75, 75, 120]),
            Spacer(1, 14),
            Paragraph("Planning Note", styles["Heading2"]),
            Paragraph(report["planning_note"], styles["BodyText"]),
        ])

        doc.build(story)
        return buffer.getvalue()
