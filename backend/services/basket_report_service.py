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
from rules.multi_goal import get_priority_rank


class BasketReportService:
    """Build an actionable, client-ready basket-level report by aggregating 2-3 goals.

    Provides executive summary, priority laddering, shared pool contribution
    architecture, consolidated cash flow trajectory, bucket product architecture,
    timeline, and contingency matrix.
    """

    MISSING = "Not available"

    def __init__(self):
        self.goal_repo = GoalRepository()
        self.strategy_repo = StrategyRepository()
        self.goal_report_service = GoalReportService()

    @staticmethod
    def _priority_rank(value: Any) -> int:
        return get_priority_rank(value)

    @staticmethod
    def _fmt(value: Any, prefix: str = "") -> str:
        if value is None:
            return BasketReportService.MISSING
        if isinstance(value, float):
            return f"{prefix}{value:,.2f}"
        if isinstance(value, int):
            return f"{prefix}{value:,}"
        return f"{prefix}{value}"

    @classmethod
    def _extract_goal_data(cls, r: dict[str, Any]) -> dict[str, Any]:
        goal_info = r.get("goal") or {}
        calc = r.get("goal_calculation") or {}
        strat = r.get("strategy") or {}
        prov = r.get("provenance") or {}

        duration = goal_info.get("duration_years") or calc.get("duration_years") or 5
        try:
            duration = int(duration)
        except (ValueError, TypeError):
            duration = 5

        target_year = goal_info.get("target_year") or calc.get("target_year") or 2030
        try:
            target_year = int(target_year)
        except (ValueError, TypeError):
            target_year = 2030

        target_month = goal_info.get("target_month") or calc.get("target_month") or 12
        try:
            target_month = int(target_month)
        except (ValueError, TypeError):
            target_month = 12

        future_target = calc.get("future_target") or calc.get("today_cost") or 0.0
        try:
            future_target = float(future_target)
        except (ValueError, TypeError):
            future_target = 0.0

        funding_gap = calc.get("funding_gap") or 0.0
        try:
            funding_gap = float(funding_gap)
        except (ValueError, TypeError):
            funding_gap = 0.0

        req_monthly = calc.get("required_monthly_contribution") or 0.0
        try:
            req_monthly = float(req_monthly)
        except (ValueError, TypeError):
            req_monthly = 0.0

        projected_mapped = calc.get("projected_mapped_asset_value") or 0.0
        try:
            projected_mapped = float(projected_mapped)
        except (ValueError, TypeError):
            projected_mapped = 0.0

        today_cost = calc.get("today_cost") or 0.0
        try:
            today_cost = float(today_cost)
        except (ValueError, TypeError):
            today_cost = 0.0

        trade_offs: list[str] = []
        for item in r.get("trade_off_analysis") or strat.get("trade_offs") or []:
            if isinstance(item, dict):
                trade_offs.append(str(item.get("trade_off", "")))
            elif item:
                trade_offs.append(str(item))

        return {
            "goal_id": goal_info.get("id") or r.get("goal_id") or "goal",
            "goal_name": goal_info.get("name") or r.get("goal_name") or "Financial Goal",
            "goal_type": goal_info.get("type") or r.get("goal_type") or "General",
            "priority": goal_info.get("priority") or calc.get("priority") or r.get("priority") or "Medium",
            "duration_years": duration,
            "target_year": target_year,
            "target_month": target_month,
            "target_date": f"{target_year}-{target_month:02d}",
            "today_cost": today_cost,
            "future_target": future_target,
            "funding_gap": funding_gap,
            "required_monthly_contribution": req_monthly,
            "projected_mapped_asset_value": projected_mapped,
            "funding_status": calc.get("funding_status") or ("Shortfall" if funding_gap > 0 else "On Track"),
            "strategy_run_id": prov.get("strategy_run_id") or r.get("strategy_run_id") or "run",
            "strategy_name": strat.get("selected_strategy_name") or strat.get("name") or "Goal Funding",
            "objective": strat.get("rationale") or strat.get("objective") or "",
            "trade_offs": trade_offs,
        }

    @classmethod
    def _build_combined_cash_flow_trajectory(cls, goals: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not goals:
            return []

        max_duration = max(g["duration_years"] for g in goals)
        max_duration = max(1, min(max_duration, 35))
        start_year = 2026

        combined_opening = sum(g["projected_mapped_asset_value"] for g in goals)
        combined_monthly = sum(g["required_monthly_contribution"] for g in goals)
        return_rate = 0.09

        trajectory: list[dict[str, Any]] = []
        balance = combined_opening

        for yr in range(1, max_duration + 1):
            cal_year = start_year + yr - 1
            annual_inv = combined_monthly * 12.0
            growth = (balance + annual_inv / 2.0) * return_rate

            # Check if any goals mature in this year
            maturing_goals = [g for g in goals if g["duration_years"] == yr]
            outflow = sum(g["future_target"] for g in maturing_goals)
            if outflow > (balance + annual_inv + growth):
                outflow = balance + annual_inv + growth

            closing = max(0.0, balance + annual_inv + growth - outflow)
            maturing_names = ", ".join(g["goal_name"] for g in maturing_goals) if maturing_goals else "—"

            trajectory.append({
                "year_index": yr,
                "year": cal_year,
                "opening_balance": round(balance, 2),
                "annual_investment": round(annual_inv, 2),
                "growth": round(growth, 2),
                "outflow": round(outflow, 2),
                "maturing_goals": maturing_names,
                "closing_balance": round(closing, 2),
            })
            balance = closing

        return trajectory

    @classmethod
    def _build_basket_product_architecture(cls, goals: list[dict[str, Any]]) -> list[dict[str, Any]]:
        horizons = sorted(g["duration_years"] for g in goals)
        min_h = horizons[0] if horizons else 3
        max_h = horizons[-1] if horizons else 10

        return [
            {
                "bucket": f"Bucket 1: Near-Term Liquidity (0–{min(min_h, 2)} Yrs)",
                "instruments": "Liquid Mutual Funds, Arbitrage Funds, Short-term FDs",
                "allocation": "30%",
                "strategic_rule": f"Protects nearest maturing goal ({goals[0]['goal_name'] if goals else 'Earliest Goal'}) from market drawdowns; provides instant liquidity.",
            },
            {
                "bucket": f"Bucket 2: Fixed Income Stability (3–{min(max_h, 6)} Yrs)",
                "instruments": "Target Maturity Debt Funds, Corporate Bond Funds, Banking & PSU Debt",
                "allocation": "35%",
                "strategic_rule": "Locks in predictable yield compounding; acts as a buffer cushion between near-term and long-term milestones.",
            },
            {
                "bucket": f"Bucket 3: High Compounding Growth ({min(max_h, 7)}+ Yrs)",
                "instruments": "Nifty 50 Index Funds, Broad-Market Midcap 150 Index, Active Flexicap",
                "allocation": "35%",
                "strategic_rule": f"Primary wealth engine to outpace inflation for longer-horizon goals in the basket; rebalances into Bucket 1 on approach.",
            },
        ]

    @classmethod
    def _build_basket_action_plan_timeline(cls, goals: list[dict[str, Any]]) -> list[dict[str, Any]]:
        timeline = [
            {
                "timeline": "Immediate (Month 1)",
                "action": "Set up pooled auto-debit SIP; allocate existing earmarked assets across basket buckets; verify KYC.",
                "owner": "Investor / Advisor",
                "milestone": "Basket funding mechanism activated",
            },
            {
                "timeline": "Every 12 Months",
                "action": "Audit relative performance; apply 5–10% contribution step-up to the shared pool; rebalance asset mix if deviation > 5%.",
                "owner": "Investor",
                "milestone": "Annual discipline & rebalancing",
            },
        ]

        for g in sorted(goals, key=lambda x: x["duration_years"]):
            de_risk = max(1, g["duration_years"] - 2)
            timeline.append({
                "timeline": f"Year {de_risk} (Pre-Maturity: {g['goal_name']})",
                "action": f"Begin systematic de-risking (STP) of {g['goal_name']}'s target allocation from Bucket 3 to Bucket 1 (Liquid).",
                "owner": "Investor / System",
                "milestone": f"{g['goal_name']} capital protection locked",
            })
            timeline.append({
                "timeline": f"Year {g['duration_years']} (Disbursement: {g['goal_name']})",
                "action": f"Execute planned redemption for {g['goal_name']} (₹{g['future_target']:,.0f}) seamlessly from Bucket 1 without market penalty.",
                "owner": "Investor",
                "milestone": f"{g['goal_name']} funded; surplus redirects to remaining goals",
            })

        return timeline

    @classmethod
    def _build_basket_contingency_matrix(cls, goals: list[dict[str, Any]]) -> list[dict[str, Any]]:
        first_goal_name = goals[0]["goal_name"] if goals else "Primary Goal"
        later_goal_name = goals[-1]["goal_name"] if len(goals) > 1 else "Secondary Goal"
        return [
            {
                "risk_event": "Monthly Surplus Reduction / Cashflow Shock",
                "immediate_action": f"Prioritize contributions to {first_goal_name} (highest priority/nearest horizon).",
                "planning_change": f"Temporarily pause or scale down contributions to {later_goal_name} without breaking compounding corpus.",
                "what_not_to_do": "Do not stop SIPs across all goals or panic-sell equity buckets.",
            },
            {
                "risk_event": f"Cost Overrun in {first_goal_name} (+20%)",
                "immediate_action": "Assess impact on combined basket funding gap.",
                "planning_change": f"Reallocate a portion of future step-up increases to {first_goal_name} or extend {later_goal_name}'s horizon slightly.",
                "what_not_to_do": "Do not raid long-term equity growth assets to fund short-term deficits.",
            },
            {
                "risk_event": "Severe Market Drawdown (> 20%)",
                "immediate_action": "Verify that nearest goal's capital is securely locked in Bucket 1 (Liquid).",
                "planning_change": "Maintain ongoing SIPs into Bucket 3 to accumulate units at depressed NAV.",
                "what_not_to_do": "Do not halt monthly investments or liquidate Bucket 3 early.",
            },
        ]

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

        extracted_goals = [self._extract_goal_data(r) for r in goal_reports]

        # Sort goals by priority laddering: Priority Rank first, then earliest target year
        ordered_goals = sorted(
            extracted_goals,
            key=lambda g: (self._priority_rank(g.get("priority")), g.get("duration_years", 5)),
        )

        target_value = sum(g["future_target"] for g in ordered_goals)
        projected_value = sum(g["projected_mapped_asset_value"] for g in ordered_goals)
        funding_gap = sum(g["funding_gap"] for g in ordered_goals)
        required_monthly = sum(g["required_monthly_contribution"] for g in ordered_goals)

        # Build priority ladder & shared pool allocation
        shared_pool_allocation: list[dict[str, Any]] = []
        for idx, g in enumerate(ordered_goals, start=1):
            pct = (g["required_monthly_contribution"] / required_monthly * 100.0) if required_monthly > 0 else 0.0
            shared_pool_allocation.append({
                "ladder_rank": idx,
                "goal_id": g["goal_id"],
                "goal_name": g["goal_name"],
                "priority": g["priority"],
                "target_date": g["target_date"],
                "required_monthly_contribution": g["required_monthly_contribution"],
                "allocation_share_pct": f"{pct:.1f}%",
                "allocation_status": "Primary Claim" if idx == 1 else f"Priority #{idx}",
            })

        combined_trajectory = self._build_combined_cash_flow_trajectory(ordered_goals)
        product_arch = self._build_basket_product_architecture(ordered_goals)
        action_timeline = self._build_basket_action_plan_timeline(ordered_goals)
        contingency_matrix = self._build_basket_contingency_matrix(ordered_goals)

        return {
            "report_type": "goal_basket_report",
            "report_version": "1.0",
            "planning_unit_id": planning_unit_id,
            "basket": {
                "name": basket_name.strip() or "Goal Basket",
                "goal_ids": unique_goal_ids,
                "goal_count": len(ordered_goals),
            },
            "summary": {
                "combined_future_target": round(target_value, 2),
                "combined_projected_mapped_asset_value": round(projected_value, 2),
                "combined_funding_gap": round(funding_gap, 2),
                "combined_required_monthly_contribution": round(required_monthly, 2),
                "funding_status": "Shortfall" if funding_gap > 0 else "On Track",
                "goal_count": len(ordered_goals),
            },
            "priority_ladder": shared_pool_allocation,
            "shared_pool_allocation": shared_pool_allocation,
            "goals": ordered_goals,
            "strategy_summary": [
                {
                    "goal_id": g["goal_id"],
                    "goal_name": g["goal_name"],
                    "strategy_name": g["strategy_name"],
                    "objective": g["objective"],
                    "trade_offs": g["trade_offs"],
                }
                for g in ordered_goals
            ],
            "combined_cash_flow_trajectory": combined_trajectory,
            "product_architecture": product_arch,
            "action_plan_timeline": action_timeline,
            "contingency_matrix": contingency_matrix,
            "planning_note": (
                "This basket report aggregates client-selected goals into a coherent shared funding and investment architecture. "
                "It enables joint cashflow management, priority-based resource allocation, and milestone de-risking without replacing the Complete Financial Plan."
            ),
        }

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

    def generate_pdf(self, planning_unit_id: str, basket_name: str, goal_ids: list[str]) -> bytes:
        report = self.build_report(planning_unit_id, basket_name, goal_ids)
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
        )
        styles = getSampleStyleSheet()
        normal = styles["BodyText"]
        story: list[Any] = []

        basket_meta = report["basket"]
        summary = report["summary"]

        story.extend([
            Paragraph("Planvesto Goal Basket Report", styles["Title"]),
            Paragraph(f"Basket: {basket_meta['name']}", styles["Heading2"]),
            Paragraph(f"Goals Grouped: {basket_meta['goal_count']} | Planning Unit: {planning_unit_id}", styles["Normal"]),
            Spacer(1, 10),
        ])

        # 1. Executive Basket Summary
        self._section(story, "1. Executive Basket Summary & Combined Totals", styles)
        story.append(self._table([
            ["Basket Metric", "Consolidated Value"],
            ["Combined Future Target", self._fmt(summary.get("combined_future_target"), "₹")],
            ["Combined Earmarked / Mapped Assets", self._fmt(summary.get("combined_projected_mapped_asset_value"), "₹")],
            ["Combined Net Funding Gap", self._fmt(summary.get("combined_funding_gap"), "₹")],
            ["Combined Required Monthly SIP", self._fmt(summary.get("combined_required_monthly_contribution"), "₹")],
            ["Overall Basket Funding Status", str(summary.get("funding_status"))],
            ["Total Goals in Basket", str(summary.get("goal_count"))],
        ], [220, 303]))

        # 2. Goals in Basket
        self._section(story, "2. Individual Goals Breakdown in Basket", styles)
        g_rows = [["Goal Name", "Priority", "Target Date", "Future Target", "Funding Gap", "Required/Mo", "Strategy"]]
        for g in report["goals"]:
            g_rows.append([
                Paragraph(str(g.get("goal_name") or "—"), normal),
                str(g.get("priority") or "—"),
                str(g.get("target_date") or "—"),
                self._fmt(g.get("future_target"), "₹"),
                self._fmt(g.get("funding_gap"), "₹"),
                self._fmt(g.get("required_monthly_contribution"), "₹"),
                Paragraph(str(g.get("strategy_name") or "—"), normal),
            ])
        story.append(self._table(g_rows, [85, 55, 60, 75, 75, 75, 98]))

        # 3. Priority Ladder & Shared Pool Allocation
        self._section(story, "3. Priority Laddering & Shared Pool Allocation", styles)
        p_rows = [["Ladder Rank", "Goal Name", "Priority", "Target Horizon", "Required/Mo", "Pool Share", "Allocation Claim"]]
        for p in report["priority_ladder"]:
            p_rows.append([
                f"#{p['ladder_rank']}",
                Paragraph(str(p["goal_name"]), normal),
                str(p["priority"]),
                str(p["target_date"]),
                self._fmt(p["required_monthly_contribution"], "₹"),
                str(p["allocation_share_pct"]),
                Paragraph(str(p["allocation_status"]), normal),
            ])
        story.append(self._table(p_rows, [60, 95, 55, 65, 75, 65, 108]))

        # 4. Combined Multi-Year Cash Flow Trajectory
        trajectory = report.get("combined_cash_flow_trajectory") or []
        self._section(story, "4. Combined Multi-Year Cash Flow Trajectory Projection", styles)
        if trajectory:
            t_rows = [["Year", "Opening (₹)", "Investment (₹)", "Returns (₹)", "Outflows (₹)", "Maturing Milestones", "Closing (₹)"]]
            for item in trajectory:
                t_rows.append([
                    str(item["year"]),
                    self._fmt(item["opening_balance"]),
                    self._fmt(item["annual_investment"]),
                    self._fmt(item["growth"]),
                    self._fmt(item["outflow"]),
                    Paragraph(str(item.get("maturing_goals") or "—"), normal),
                    self._fmt(item["closing_balance"]),
                ])
            story.append(self._table(t_rows, [45, 75, 75, 75, 75, 105, 73]))
            story.append(Spacer(1, 6))
            story.append(Paragraph("<b>What the Consolidated Cashflow Demonstrates:</b> This joint cashflow models pooled contributions across the basket, displaying how intermediate disbursements are met without disrupting the compounding trajectory of longer-horizon goals.", normal))
        else:
            story.append(Paragraph(self.MISSING, normal))

        # 5. Basket Product Architecture
        b_arch = report.get("product_architecture") or []
        self._section(story, "5. Basket Product & Asset Allocation Architecture", styles)
        if b_arch:
            arch_rows = [["Bucket / Horizon", "Recommended Instruments", "Allocation", "Strategic Role & Multi-Goal Transition"]]
            for b in b_arch:
                arch_rows.append([
                    Paragraph(str(b.get("bucket")), normal),
                    Paragraph(str(b.get("instruments")), normal),
                    str(b.get("allocation")),
                    Paragraph(str(b.get("strategic_rule")), normal),
                ])
            story.append(self._table(arch_rows, [120, 155, 60, 188]))

        # 6. Combined Action Plan Timeline
        timeline = report.get("action_plan_timeline") or []
        self._section(story, "6. Combined Action Plan Timeline & Staggered Milestones", styles)
        if timeline:
            time_rows = [["Execution Window", "Action Step", "Owner", "Key Milestone"]]
            for t in timeline:
                time_rows.append([
                    Paragraph(str(t.get("timeline")), normal),
                    Paragraph(str(t.get("action")), normal),
                    str(t.get("owner")),
                    Paragraph(str(t.get("milestone")), normal),
                ])
            story.append(self._table(time_rows, [95, 218, 90, 120]))

        # 7. Basket Contingency Matrix
        contingency = report.get("contingency_matrix") or []
        self._section(story, "7. Basket Contingency & Trade-Off Matrix", styles)
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

        # 8. Planning Notes
        self._section(story, "8. Governance & Planning Notes", styles)
        story.append(Paragraph(report.get("planning_note", ""), normal))

        doc.build(story)
        return buffer.getvalue()
