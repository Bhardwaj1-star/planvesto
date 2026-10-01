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
            "goal_calculation": {
                "today_cost": getattr(goal, "today_cost", None),
                "inflation_rate": getattr(goal, "inflation_rate", None),
                "future_target": getattr(goal, "future_target", None),
                "funding_gap": getattr(goal, "funding_gap", None),
                "required_monthly_contribution": getattr(goal, "required_monthly_contribution", None),
                "target_month": getattr(goal, "target_month", None),
                "target_year": getattr(goal, "target_year", None),
                "duration_years": getattr(goal, "duration_years", None),
                "funding_status": getattr(goal, "funding_status", None),
                "projected_mapped_asset_value": getattr(goal, "projected_mapped_asset_value", None),
                "funding_return_assumption": getattr(goal, "funding_return_assumption", None),
            },
            "goal_funding": {
                "feasibility_status": getattr(goal, "feasibility_status", None),
                "feasibility_reason": getattr(goal, "feasibility_reason", None),
                "available_monthly_surplus": getattr(goal, "available_monthly_surplus", None),
                "monthly_contribution_surplus_gap": getattr(goal, "monthly_contribution_surplus_gap", None),
                "required_monthly_contribution": getattr(goal, "required_monthly_contribution", None),
                "funding_gap": getattr(goal, "funding_gap", None),
                "funding_status": getattr(goal, "funding_status", None),
                "funding_return_assumption": getattr(goal, "funding_return_assumption", None),
                "funding_strategies": getattr(goal, "funding_strategies", []),
            },
            "goal_context": {
                "priority": getattr(goal, "priority", None),
                "flexibility": getattr(goal, "flexibility", None),
                "status": getattr(goal, "status", None),
                "version": getattr(goal, "version", None),
                "is_latest": getattr(goal, "is_latest", None),
            },
            "financial_state": {"annual_income": context.get("annual_income"), "annual_expenses": context.get("annual_expenses"), "monthly_surplus": context.get("monthly_surplus"), "assets": context.get("assets"), "liabilities": context.get("liabilities"), "net_worth": context.get("net_worth")},
        }

    @staticmethod
    def _table(rows: list[list[str]]) -> Table:
        table = Table(rows, colWidths=[210, 270])
        table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("PADDING", (0, 0), (-1, -1), 7)]))
        return table

    @staticmethod
    def _fmt(value: Any, prefix: str = "") -> str:
        if value is None:
            return "Not available"
        if isinstance(value, float):
            return f"{prefix}{value:,.2f}"
        if isinstance(value, int):
            return f"{prefix}{value:,}"
        return f"{prefix}{value}"

    @staticmethod
    def _label(value: Any) -> str:
        return str(value).replace("_", " ").replace("-", " ").title()

    @staticmethod
    def _section(story: list, title: str, styles: Any) -> None:
        story.extend([Spacer(1, 8), Paragraph(title, styles["Heading2"])])

    def generate_pdf(self, planning_unit_id: str, strategy_run_id: str) -> bytes:
        report = self.build_report(planning_unit_id, strategy_run_id)
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=42,
            leftMargin=42,
            topMargin=42,
            bottomMargin=42,
        )
        styles = getSampleStyleSheet()
        story: list[Any] = []

        story.extend([
            Paragraph(f"{report.get('goal_type') or 'Financial'} Goal Plan", styles["Title"]),
            Paragraph(report["goal_name"], styles["Heading2"]),
            Paragraph(
                "Client Financial Planning Report",
                styles["BodyText"],
            ),
            Spacer(1, 16),
        ])

        context_rows = [
            ["Planning Item", "Plan"],
            ["Goal Type", str(report.get("goal_type") or "Vacation / Travel")],
            ["Goal Priority", str(report["goal_context"].get("priority") or "Not available")],
            ["Goal Flexibility", str(report["goal_context"].get("flexibility") or "Not available")],
            ["Target Date", f"{report['goal_calculation'].get('target_month')}/{report['goal_calculation'].get('target_year')}"],
            ["Planning Horizon", self._fmt(report["goal_calculation"].get("duration_years")) + " years"],
        ]
        self._section(story, f"1. Your {report.get('goal_type') or 'Financial'} Goal", styles)
        story.append(self._table(context_rows))

        calc = report["goal_calculation"]
        calculation_rows = [
            ["Planning Item", "Amount / Assumption"],
            ["Current Cost", self._fmt(calc.get("today_cost"), "₹")],
            ["Inflation Assumption", self._fmt(calc.get("inflation_rate"))],
            ["Future Target", self._fmt(calc.get("future_target"), "₹")],
            ["Projected Mapped Assets", self._fmt(calc.get("projected_mapped_asset_value"), "₹")],
            ["Funding Gap", self._fmt(calc.get("funding_gap"), "₹")],
            ["Required Monthly Contribution", self._fmt(calc.get("required_monthly_contribution"), "₹")],
            ["Funding Return Assumption", self._fmt(calc.get("funding_return_assumption"))],
            ["Funding Status", str(calc.get("funding_status") or "Not available")],
        ]
        self._section(story, f"2. How Your {report.get('goal_type') or 'Financial'} Goal Is Funded", styles)
        story.append(self._table(calculation_rows))

        mapped_assets = report.get("mapped_assets", [])
        self._section(story, f"3. Assets Assigned to the {report.get('goal_type') or 'Goal'}", styles)
        if mapped_assets:
            asset_rows = [["Asset", "Allocated", "Allocation %", "Expected Return", "Projected Value"]]
            for asset in mapped_assets:
                asset_rows.append([
                    str(asset.get("asset_name") or "—"),
                    self._fmt(asset.get("allocation"), "₹"),
                    self._fmt(asset.get("allocation_percentage")),
                    self._fmt(asset.get("expected_return")),
                    self._fmt(asset.get("projected_value"), "₹"),
                ])
            table = Table(asset_rows, colWidths=[125, 85, 75, 90, 105], repeatRows=1)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(table)
        else:
            story.append(Paragraph("No assets are currently mapped to this goal.", styles["BodyText"]))

        funding = report["goal_funding"]
        self._section(story, f"4. Feasibility of the {report.get('goal_type') or 'Financial'} Goal", styles)
        feasibility_rows = [
            ["Feasibility Item", "Result"],
            ["Feasibility Status", str(funding.get("feasibility_status") or "Unknown")],
            ["Available Monthly Surplus", self._fmt(funding.get("available_monthly_surplus"), "₹")],
            ["Required Monthly Contribution", self._fmt(funding.get("required_monthly_contribution"), "₹")],
            ["Contribution Surplus Gap", self._fmt(funding.get("monthly_contribution_surplus_gap"), "₹")],
            ["Reason", str(funding.get("feasibility_reason") or "Not available")],
        ]
        story.append(self._table(feasibility_rows))

        self._section(story, "5. Funding Options", styles)
        funding_strategies = funding.get("funding_strategies") or []
        if funding_strategies:
            strategy_rows = [[
                "Funding Option", "Status", "Lumpsum", "Monthly",
                "Starting Monthly", "Annual Step-up", "Remaining Gap"
            ]]
            for item in funding_strategies:
                strategy_rows.append([
                    str(item.get("strategy_name") or item.get("strategy_id") or "—"),
                    str(item.get("status") or "—"),
                    self._fmt(item.get("required_lumpsum"), "₹"),
                    self._fmt(item.get("required_monthly_contribution"), "₹"),
                    self._fmt(item.get("starting_monthly_contribution"), "₹"),
                    self._fmt(item.get("annual_step_up")),
                    self._fmt(item.get("remaining_gap"), "₹"),
                ])
            table = Table(strategy_rows, colWidths=[95, 60, 65, 70, 80, 65, 65], repeatRows=1)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(table)
        else:
            story.append(Paragraph("No funding alternatives are available in the current plan.", styles["BodyText"]))

        self._section(story, "6. Selected Strategy", styles)
        strategy = report["strategy"]
        story.append(Paragraph(str(strategy.get("name") or "Not selected"), styles["Heading3"]))
        if strategy.get("objective"):
            story.append(Paragraph(str(strategy["objective"]), styles["BodyText"]))
        story.append(Paragraph(
            f"Selected Strategy ID: {report.get('selected_strategy_id') or 'Not selected'}",
            styles["BodyText"],
        ))

        self._section(story, "7. Trade-offs", styles)
        trade_offs = strategy.get("trade_offs") or []
        if trade_offs:
            for item in trade_offs:
                story.append(Paragraph(f"• {item}", styles["BodyText"]))
        else:
            story.append(Paragraph("No strategy trade-offs were recorded.", styles["BodyText"]))

        financial = report["financial_state"]
        self._section(story, "8. Your Financial Context", styles)
        financial_rows = [
            ["Financial Item", "Current Position"],
            ["Annual Income", self._fmt(financial.get("annual_income"), "₹")],
            ["Annual Expenses", self._fmt(financial.get("annual_expenses"), "₹")],
            ["Monthly Surplus", self._fmt(financial.get("monthly_surplus"), "₹")],
            ["Assets", str(financial.get("assets") if financial.get("assets") is not None else "Not available")],
            ["Liabilities", str(financial.get("liabilities") if financial.get("liabilities") is not None else "Not available")],
            ["Net Worth", self._fmt(financial.get("net_worth"), "₹")],
        ]
        story.append(self._table(financial_rows))

        self._section(story, "9. Recommendation & Reasoning", styles)
        recommendation = report["recommendation"]
        reasons = recommendation.get("short_reasons") or []
        if reasons:
            for reason in reasons:
                story.append(Paragraph(f"• {reason}", styles["BodyText"]))
        else:
            story.append(Paragraph("No short reasons were recorded.", styles["BodyText"]))
        complete_reasoning = recommendation.get("complete_reasoning")
        if complete_reasoning:
            story.extend([Spacer(1, 6), Paragraph(str(complete_reasoning), styles["BodyText"])])

        self._section(story, "10. Client Action Plan", styles)
        story.append(Paragraph(
            "The individual goal report records the selected strategy and funding path. "
            "Goal-specific executable actions should be taken from the selected strategy/scenario.",
            styles["BodyText"],
        ))

        self._section(story, "11. Report Context", styles)
        story.append(Paragraph(
            "This report uses the same generic Goal Engine and Goal Funding architecture used "
            "for other supported financial goals. Vacation is a goal type, not a separate calculation engine.",
            styles["BodyText"],
        ))

        doc.build(story)
        return buffer.getvalue()
