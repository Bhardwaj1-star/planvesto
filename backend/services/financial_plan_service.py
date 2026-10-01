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
            defined_goal = self.goal_repo.get_latest_defined_goal(planning_unit_id, res.goal_id)
            rows.append({
                "goal_id": res.goal_id,
                "goal_name": res.goal_name,
                "goal_type": res.goal_type,
                "priority": res.client_priority,
                "client_priority": res.client_priority,
                "resolved_priority": res.resolved_priority,
                "target_date": res.target_date,
                "today_cost": getattr(defined_goal, "today_cost", None),
                "future_target": getattr(defined_goal, "future_target", None),
                "funding_gap": getattr(defined_goal, "funding_gap", None),
                "projected_mapped_asset_value": getattr(defined_goal, "projected_mapped_asset_value", None),
                "required_monthly_contribution": res.required_monthly_contribution,
                "allocated_monthly_contribution": res.allocated_monthly_contribution,
                "monthly_shortfall": res.shortfall,
                "funding_status": res.funding_status,
                "strategy_id": res.recommended_strategy_id,
                "strategy_name": res.recommended_strategy_name,
                "feasibility_status": res.feasibility_status,
                "available_monthly_surplus": getattr(defined_goal, "available_monthly_surplus", None),
                "funding_strategies": getattr(defined_goal, "funding_strategies", []),
                "override_applied": res.override_applied,
                "override_reason": res.override_reason,
                "reasons": res.reasons,
                "notes": res.notes,
            })

        f_state = multi_plan.financial_state
        total_surplus = float(multi_plan.total_available_surplus or 0.0)
        total_allocated = float(multi_plan.total_allocated_contribution or 0.0)
        unallocated = max(0.0, total_surplus - total_allocated)
        fully_funded_count = sum(1 for r in rows if r.get("funding_status") == "fully_funded")
        partially_funded_count = sum(1 for r in rows if r.get("funding_status") in ("partially_funded", "unfunded"))

        goal_allocations = []
        for index, r in enumerate(rows, start=1):
            req = float(r.get("required_monthly_contribution") or 0.0)
            alloc = float(r.get("allocated_monthly_contribution") or 0.0)
            pct = (alloc / req * 100.0) if req > 0 else 100.0
            goal_allocations.append({
                "goal_id": r.get("goal_id"),
                "goal_name": r.get("goal_name"),
                "requested_amount": req,
                "allocated_amount": alloc,
                "shortfall": float(r.get("monthly_shortfall") or 0.0),
                "funding_percentage": pct,
                "priority_rank": index,
                "client_priority": r.get("client_priority"),
                "resolved_priority": r.get("resolved_priority"),
                "override_applied": r.get("override_applied", False),
                "override_reason": r.get("override_reason"),
            })

        action_items = [
            {
                "action_id": f"act_{a.get('sequence', idx)}",
                "category": "goal",
                "title": a.get("action", f"Fund {a.get('goal_name')}"),
                "description": a.get("action", ""),
                "priority": "high",
                "target_type": "goal",
                "target_id": a.get("goal_id"),
                "monthly_commitment": float(a.get("monthly_contribution") or 0.0),
                "lump_sum_commitment": 0.0,
                "deadline": a.get("target_date"),
                "status": a.get("funding_status", "pending"),
            }
            for idx, a in enumerate(multi_plan.action_plan, start=1)
        ]

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
            "summary": {
                "total_goals_count": len(rows),
                "fully_funded_goals_count": fully_funded_count,
                "partially_funded_goals_count": partially_funded_count,
                "total_funding_gap": float(multi_plan.monthly_gap or 0.0),
                "total_monthly_commitment": total_allocated,
            },
            "resource_allocation": {
                "total_monthly_surplus": total_surplus,
                "foundation_allocation": {
                    "emergency_fund_monthly": 0.0,
                    "debt_reduction_monthly": 0.0,
                    "mandatory_savings_monthly": 0.0,
                },
                "discretionary_surplus_monthly": total_surplus,
                "goal_allocations": goal_allocations,
                "total_allocated_monthly": total_allocated,
                "unallocated_surplus": unallocated,
            },
            "goal_plans": [
                {
                    "goal_id": r.get("goal_id"),
                    "goal_name": r.get("goal_name"),
                    "goal_type": r.get("goal_type"),
                    "target_amount": float(r.get("future_target") or r.get("today_cost") or 0.0),
                    "today_cost": r.get("today_cost"),
                    "target_date": r.get("target_date"),
                    "strategy_run_id": next(
                        (
                            run.strategy_run_id
                            for run in [self.strategy_repo.get_latest_run(planning_unit_id, r.get("goal_id"))]
                            if run and run.strategy_run_id
                        ),
                        None,
                    ),
                    "strategy_id": r.get("strategy_id"),
                    "strategy_name": r.get("strategy_name") or "Recommended Strategy",
                    "recommended_strategy_name": r.get("strategy_name") or "Recommended Strategy",
                    "monthly_required": float(r.get("required_monthly_contribution") or 0.0),
                    "monthly_allocation": float(r.get("allocated_monthly_contribution") or 0.0),
                    "monthly_shortfall": float(r.get("monthly_shortfall") or 0.0),
                    "funding_gap": float(r.get("funding_gap") or 0.0),
                    "projected_mapped_asset_value": r.get("projected_mapped_asset_value"),
                    "funding_status": r.get("funding_status"),
                    "feasibility_status": r.get("feasibility_status"),
                    "available_monthly_surplus": r.get("available_monthly_surplus"),
                    "funding_strategies": r.get("funding_strategies", []),
                    "is_feasible": r.get("feasibility_status") == "feasible",
                    "reasons": r.get("reasons", []),
                    "notes": r.get("notes", []),
                }
                for r in rows
            ],
            "strategy_runs": strategy_runs,
            "actions": multi_plan.action_plan,
            "action_plan": {
                "actions": action_items,
                "total_actions": len(action_items),
            },
            "trade_offs": multi_plan.trade_offs,
            "constraints": [
                entry
                for audit in multi_plan.audit_trail
                if audit.get("source") == "ConstraintAggregator"
                for entry in (audit.get("canonical_constraint_set", {}).get("constraints") or [])
            ],
            "constraint_conflicts": [
                entry
                for audit in multi_plan.audit_trail
                if audit.get("source") == "ConstraintAggregator"
                for entry in (audit.get("canonical_constraint_set", {}).get("conflicts") or [])
            ],
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
