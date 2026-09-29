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
from services.multi_goal_planning_service import MultiGoalPlanningService
from services.strategy_service import StrategyService


class FinancialPlanService:
    """Build a live consolidated plan across all goals without introducing new DB tables."""

    def __init__(
        self,
        goal_repo: GoalRepository | None = None,
        strategy_repo: StrategyRepository | None = None,
        strategy_service: StrategyService | None = None,
        goal_report_service: GoalReportService | None = None,
        multi_goal_service: MultiGoalPlanningService | None = None,
    ):
        self.goal_repo = goal_repo or GoalRepository()
        self.strategy_repo = strategy_repo or StrategyRepository()
        self.strategy_service = strategy_service or StrategyService()
        self.goal_report_service = goal_report_service or GoalReportService()
        self.multi_goal_service = multi_goal_service or MultiGoalPlanningService(
            goal_repo=self.goal_repo,
            strategy_repo=self.strategy_repo,
            strategy_service=self.strategy_service,
            goal_report_service=self.goal_report_service,
        )

    @staticmethod
    def _priority_rank(value: Any) -> int:
        return {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(str(value or "").lower(), 4)

    @staticmethod
    def _goal_row(report: dict[str, Any]) -> dict[str, Any]:
        calc = report.get("goal_calculation", {})
        rec = report.get("recommendation", {})
        client_p = calc.get("priority") or report.get("priority")
        return {
            "goal_id": report.get("goal_id"),
            "goal_name": report.get("goal_name"),
            "goal_type": report.get("goal_type"),
            "priority": client_p,
            "client_priority": client_p,
            "resolved_priority": client_p,
            "target_date": f"{calc.get('target_year')}-{calc.get('target_month'):02d}" if calc.get("target_year") and calc.get("target_month") else None,
            "today_cost": calc.get("today_cost"),
            "future_target": calc.get("future_target"),
            "funding_gap": calc.get("funding_gap"),
            "required_monthly_contribution": calc.get("required_monthly_contribution") or 0.0,
            "allocated_monthly_contribution": calc.get("required_monthly_contribution") or 0.0,
            "monthly_shortfall": 0.0,
            "funding_status": calc.get("funding_status"),
            "strategy_id": report.get("selected_strategy_id") or rec.get("recommended_strategy_id"),
            "strategy_name": report.get("strategy", {}).get("name"),
            "feasibility_status": rec.get("feasibility_status"),
            "reasoning": rec.get("complete_reasoning"),
            "reasons": rec.get("short_reasons", []),
            "override_applied": False,
            "override_reason": None,
        }

    def build_plan(
        self,
        planning_unit_id: str,
        priorities: InvestorPriorities | None = None,
        rule_overrides: dict[str, dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Builds one coherent consolidated financial plan using MultiGoalPlanningService."""
        multi_plan = self.multi_goal_service.build_multi_goal_plan(
            planning_unit_id=planning_unit_id,
            priorities=priorities,
            rule_overrides=rule_overrides,
        )

        # Retrieve strategy run ids for auditability
        goals = self.goal_repo.list_goals(planning_unit_id)
        strategy_runs: list[str] = []
        for g in goals:
            run = self.strategy_repo.get_latest_run(planning_unit_id, g["goal_id"])
            if run and run.strategy_run_id:
                strategy_runs.append(run.strategy_run_id)

        rows: list[dict[str, Any]] = []
        for res in multi_plan.goals:
            rows.append({
                "goal_id": res.goal_id,
                "goal_name": res.goal_name,
                "goal_type": res.goal_type,
                "priority": res.client_priority,
                "client_priority": res.client_priority,
                "resolved_priority": res.resolved_priority,
                "target_date": res.target_date,
                "required_monthly_contribution": res.required_monthly_contribution,
                "allocated_monthly_contribution": res.allocated_monthly_contribution,
                "monthly_shortfall": res.shortfall,
                "funding_status": res.funding_status,
                "strategy_id": res.recommended_strategy_id,
                "strategy_name": res.recommended_strategy_name,
                "feasibility_status": res.feasibility_status,
                "override_applied": res.override_applied,
                "override_reason": res.override_reason,
                "reasons": res.reasons,
                "notes": res.notes,
            })

        f_state = multi_plan.financial_state
        return {
            "report_type": "complete_financial_plan",
            "planning_unit_id": planning_unit_id,
            "goals": rows,
            "goal_count": len(rows),
            "financial_state": {
                "annual_income": f_state.get("annual_income"),
                "annual_expenses": f_state.get("annual_expenses"),
                "monthly_surplus": multi_plan.total_available_surplus,
                "assets": f_state.get("assets"),
                "liabilities": f_state.get("liabilities"),
                "net_worth": f_state.get("net_worth"),
            },
            "consolidated_funding": {
                "required_monthly_contribution": multi_plan.total_required_contribution,
                "allocated_monthly_contribution": multi_plan.total_allocated_contribution,
                "available_monthly_surplus": multi_plan.total_available_surplus,
                "monthly_gap": multi_plan.monthly_gap,
                "funding_status": multi_plan.overall_funding_status,
                "competition_detected": multi_plan.competing_resources_detected,
            },
            "strategy_runs": strategy_runs,
            "actions": multi_plan.action_plan,
            "trade_offs": multi_plan.trade_offs,
            "audit_trail": multi_plan.audit_trail,
            "planning_notes": multi_plan.planning_notes,
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

        goal_rows = [["Priority", "Goal", "Target", "Required/Mo", "Allocated/Mo", "Status"]]
        for row in plan["goals"]:
            priority_label = row.get("resolved_priority") or row.get("priority") or "—"
            if row.get("override_applied"):
                priority_label += "*"
            goal_rows.append([
                priority_label,
                str(row.get("goal_name") or "—"),
                str(row.get("target_date") or "—"),
                str(row.get("required_monthly_contribution") or 0),
                str(row.get("allocated_monthly_contribution") or 0),
                str(row.get("funding_status") or "—"),
            ])
        story.extend([Paragraph("Goal Strategies & Allocation", styles["Heading2"]), self._table(goal_rows, [60, 95, 65, 75, 75, 75]), Spacer(1, 14)])

        if plan.get("trade_offs"):
            story.append(Paragraph("Trade-offs & Constraints", styles["Heading2"]))
            for to in plan["trade_offs"]:
                story.append(Paragraph(f"• {to}", styles["BodyText"]))
            story.append(Spacer(1, 10))

        overrides = [g for g in plan["goals"] if g.get("override_applied")]
        if overrides:
            story.append(Paragraph("System Priority Adjustments & Rule Explanations", styles["Heading2"]))
            for g in overrides:
                story.append(Paragraph(
                    f"• <b>{g['goal_name']}</b>: Client Priority was <i>{g['client_priority']}</i>, resolved by system rules to <i>{g['resolved_priority']}</i>.<br/>"
                    f"&nbsp;&nbsp;<b>Reason:</b> {g.get('override_reason') or 'Financial ratio constraint.'}",
                    styles["BodyText"],
                ))
            story.append(Spacer(1, 10))

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
