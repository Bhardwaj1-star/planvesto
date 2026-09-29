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
from models.strategy import InvestorPriorities
from services.goal_report_service import GoalReportService
from services.strategy_service import StrategyService


class FinancialPlanService:
    """Build a live consolidated plan across all goals without introducing new DB tables."""

    def __init__(self):
        self.goal_repo = GoalRepository()
        self.strategy_repo = StrategyRepository()
        self.strategy_service = StrategyService()
        self.goal_report_service = GoalReportService()

    @staticmethod
    def _priority_rank(value: Any) -> int:
        return {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(str(value or "").lower(), 4)

    @staticmethod
    def _goal_row(report: dict[str, Any]) -> dict[str, Any]:
        calc = report.get("goal_calculation", {})
        rec = report.get("recommendation", {})
        return {
            "goal_id": report.get("goal_id"),
            "goal_name": report.get("goal_name"),
            "goal_type": report.get("goal_type"),
            "priority": calc.get("priority") or report.get("priority"),
            "target_date": f"{calc.get('target_year')}-{calc.get('target_month'):02d}" if calc.get("target_year") and calc.get("target_month") else None,
            "today_cost": calc.get("today_cost"),
            "future_target": calc.get("future_target"),
            "funding_gap": calc.get("funding_gap"),
            "required_monthly_contribution": calc.get("required_monthly_contribution") or 0.0,
            "funding_status": calc.get("funding_status"),
            "strategy_id": report.get("selected_strategy_id") or rec.get("recommended_strategy_id"),
            "strategy_name": report.get("strategy", {}).get("name"),
            "feasibility_status": rec.get("feasibility_status"),
            "reasoning": rec.get("complete_reasoning"),
            "reasons": rec.get("short_reasons", []),
        }

    def build_plan(self, planning_unit_id: str, priorities: InvestorPriorities | None = None) -> dict[str, Any]:
        goals = self.goal_repo.list_goals(planning_unit_id)
        if not goals:
            raise HTTPException(status_code=404, detail="No goals found for this planning unit")

        rows: list[dict[str, Any]] = []
        strategy_runs: list[str] = []
        for goal in goals:
            goal_id = goal["goal_id"]
            run = self.strategy_repo.get_latest_run(planning_unit_id, goal_id)
            if not run:
                if priorities is None:
                    raise HTTPException(status_code=400, detail=f"Strategy run missing for goal '{goal_id}'. Build the goal strategy first or provide investor priorities.")
                run = self.strategy_service.build_strategy(planning_unit_id, goal_id, priorities)
            report = self.goal_report_service.build_report(planning_unit_id, run.strategy_run_id)
            row = self._goal_row(report)
            row["priority"] = goal.get("priority") or row.get("priority")
            row["flexibility"] = goal.get("flexibility")
            rows.append(row)
            strategy_runs.append(run.strategy_run_id or "")

        rows.sort(key=lambda item: (self._priority_rank(item.get("priority")), item.get("target_date") or "9999-99"))
        financial_state = self.strategy_service._financial_context(planning_unit_id, next((self.goal_repo.get_latest_defined_goal(planning_unit_id, g["goal_id"]) for g in goals), None)) if goals else {}
        surplus = financial_state.get("monthly_surplus")
        required_total = round(sum(float(row.get("required_monthly_contribution") or 0) for row in rows), 2)
        surplus_value = float(surplus) if surplus is not None else None
        monthly_gap = round(required_total - surplus_value, 2) if surplus_value is not None else None

        if monthly_gap is None:
            funding_status = "requires_review"
        elif monthly_gap <= 0:
            funding_status = "within_current_surplus"
        else:
            funding_status = "surplus_shortfall"

        actions = []
        for index, row in enumerate(rows, start=1):
            contribution = float(row.get("required_monthly_contribution") or 0)
            actions.append({
                "sequence": index,
                "goal_id": row["goal_id"],
                "goal_name": row["goal_name"],
                "action": f"Fund {row['goal_name']} according to its selected strategy",
                "monthly_contribution": contribution,
                "target_date": row.get("target_date"),
                "strategy": row.get("strategy_name"),
            })

        return {
            "report_type": "complete_financial_plan",
            "planning_unit_id": planning_unit_id,
            "goals": rows,
            "goal_count": len(rows),
            "financial_state": {
                "annual_income": financial_state.get("annual_income"),
                "annual_expenses": financial_state.get("annual_expenses"),
                "monthly_surplus": surplus,
                "assets": financial_state.get("assets"),
                "liabilities": financial_state.get("liabilities"),
                "net_worth": financial_state.get("net_worth"),
            },
            "consolidated_funding": {
                "required_monthly_contribution": required_total,
                "available_monthly_surplus": surplus_value,
                "monthly_gap": monthly_gap,
                "funding_status": funding_status,
            },
            "strategy_runs": strategy_runs,
            "actions": actions,
            "planning_notes": [
                "Goals are ordered by recorded priority and then target date.",
                "The consolidated contribution is the sum of goal-level required monthly contributions; it must be reviewed against the investor's current surplus.",
                "The plan does not silently change a goal strategy when a combined funding shortfall exists; it exposes the conflict for the planning decision layer.",
            ],
        }

    @staticmethod
    def _table(rows: list[list[str]], widths: list[float] | None = None) -> Table:
        table = Table(rows, colWidths=widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        return table

    def generate_pdf(self, planning_unit_id: str) -> bytes:
        plan = self.build_plan(planning_unit_id)
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        story = [Paragraph("Complete Financial Plan", styles["Title"]), Paragraph(f"Planning Unit: {planning_unit_id}", styles["BodyText"]), Spacer(1, 14)]

        state = plan["financial_state"]
        story.extend([
            Paragraph("Financial State", styles["Heading2"]),
            self._table([["Metric", "Value"], *[[k.replace("_", " ").title(), str(v) if v is not None else "Not available"] for k, v in state.items()]]),
            Spacer(1, 14),
        ])

        funding = plan["consolidated_funding"]
        story.extend([
            Paragraph("Consolidated Funding", styles["Heading2"]),
            self._table([["Metric", "Value"], *[[k.replace("_", " ").title(), str(v) if v is not None else "Not available"] for k, v in funding.items()]]),
            Spacer(1, 14),
        ])

        goal_rows = [["Priority", "Goal", "Target", "Monthly", "Strategy", "Status"]]
        for row in plan["goals"]:
            goal_rows.append([str(row.get("priority") or "—"), str(row.get("goal_name") or "—"), str(row.get("target_date") or "—"), str(row.get("required_monthly_contribution") or 0), str(row.get("strategy_name") or "—"), str(row.get("feasibility_status") or "—")])
        story.extend([Paragraph("Goal Strategies", styles["Heading2"]), self._table(goal_rows, [55, 100, 65, 65, 105, 65]), Spacer(1, 14)])

        story.append(Paragraph("Action Plan", styles["Heading2"]))
        for action in plan["actions"]:
            story.append(Paragraph(f"{action['sequence']}. {action['action']} — {action['monthly_contribution']}/month; target {action.get('target_date') or 'review required'}.", styles["BodyText"]))
            story.append(Spacer(1, 5))

        story.append(Spacer(1, 10))
        story.append(Paragraph("Planning Notes", styles["Heading2"]))
        for note in plan["planning_notes"]:
            story.append(Paragraph(f"• {note}", styles["BodyText"]))

        doc.build(story)
        return buffer.getvalue()
