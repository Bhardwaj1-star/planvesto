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
            "ratio_constraints": self._build_ratio_constraints(f_state),
            "family_cash_flow_trajectory": self._build_family_cash_flow_trajectory(rows, total_allocated, f_state.get("net_worth")),
            "moneywheel_health_scan": self._build_moneywheel_health_scan(f_state),
            "contingency_matrix": self._build_family_contingency_matrix(),
            "governance_protocol": self._build_governance_protocol(),
        }

    @classmethod
    def _build_family_cash_flow_trajectory(
        cls,
        goals: list[dict[str, Any]],
        total_monthly_allocated: float,
        net_worth: Any,
    ) -> list[dict[str, Any]]:
        horizons = []
        for g in goals:
            t_date = str(g.get("target_date") or "")
            if "-" in t_date:
                try:
                    yr = int(t_date.split("-")[0])
                    horizons.append(max(1, yr - 2026))
                except (ValueError, TypeError):
                    pass
        max_horizon = max(horizons) if horizons else 15
        max_horizon = max(5, min(max_horizon, 30))

        try:
            opening = float(net_worth or 0.0) * 0.4
        except (ValueError, TypeError):
            opening = 0.0

        if opening <= 0:
            opening = sum(float(g.get("projected_mapped_asset_value") or 0.0) for g in goals)

        return_rate = 0.09
        annual_contribution = float(total_monthly_allocated or 0.0) * 12.0

        trajectory: list[dict[str, Any]] = []
        balance = opening

        for yr in range(1, max_horizon + 1):
            cal_year = 2026 + yr - 1
            growth = (balance + annual_contribution / 2.0) * return_rate

            # Check maturing goals for this year
            maturing_goals = [
                g for g in goals
                if str(g.get("target_date") or "").startswith(str(cal_year))
            ]
            outflow = sum(float(g.get("future_target") or g.get("today_cost") or 0.0) for g in maturing_goals)
            if outflow > (balance + annual_contribution + growth):
                outflow = balance + annual_contribution + growth

            closing = max(0.0, balance + annual_contribution + growth - outflow)
            maturing_names = ", ".join(str(g.get("goal_name")) for g in maturing_goals) if maturing_goals else "—"

            trajectory.append({
                "year_index": yr,
                "year": cal_year,
                "opening_balance": round(balance, 2),
                "annual_investment": round(annual_contribution, 2),
                "growth": round(growth, 2),
                "outflow": round(outflow, 2),
                "maturing_goals": maturing_names,
                "closing_balance": round(closing, 2),
            })
            balance = closing

        return trajectory

    @classmethod
    def _build_moneywheel_health_scan(cls, f_state: dict[str, Any]) -> list[dict[str, Any]]:
        income = float(f_state.get("annual_income") or 0.0)
        expenses = float(f_state.get("annual_expenses") or 0.0)
        monthly_exp = expenses / 12.0 if expenses > 0 else 1.0
        liabilities = float(f_state.get("liabilities") or 0.0)
        assets = float(f_state.get("assets") or 0.0)
        financial_assets = float(f_state.get("financial_assets") or (assets * 0.6))

        savings_pct = ((income - expenses) / income * 100.0) if income > 0 else 0.0
        dti_pct = (liabilities / income * 100.0) if income > 0 else 0.0
        emergency_months = (financial_assets * 0.2) / monthly_exp if monthly_exp > 0 else 6.0

        return [
            {
                "metric": "Savings Rate",
                "current_value": f"{savings_pct:.1f}%",
                "healthy_benchmark": ">= 25.0%",
                "status": "Healthy" if savings_pct >= 25 else "Attention Required",
            },
            {
                "metric": "Debt-to-Income (DTI)",
                "current_value": f"{dti_pct:.1f}%",
                "healthy_benchmark": "< 40.0%",
                "status": "Healthy" if dti_pct < 40 else "Elevated Debt",
            },
            {
                "metric": "Emergency Fund Buffer",
                "current_value": f"{emergency_months:.1f} Months",
                "healthy_benchmark": ">= 6.0 Months",
                "status": "Adequate" if emergency_months >= 6.0 else "Build Buffer",
            },
            {
                "metric": "Financial Asset Ratio",
                "current_value": f"{(financial_assets / assets * 100):.1f}%" if assets > 0 else "—",
                "healthy_benchmark": ">= 50.0%",
                "status": "Healthy" if (assets > 0 and (financial_assets / assets) >= 0.5) else "Asset Heavy",
            },
        ]

    @classmethod
    def _build_ratio_constraints(cls, f_state: dict[str, Any]) -> list[dict[str, Any]]:
        income = float(f_state.get("annual_income") or 0.0)
        expenses = float(f_state.get("annual_expenses") or 0.0)
        monthly_exp = expenses / 12.0 if expenses > 0 else 1.0
        liabilities = float(f_state.get("liabilities") or 0.0)
        assets = float(f_state.get("assets") or 0.0)
        financial_assets = float(f_state.get("financial_assets") or (assets * 0.6))

        savings_pct = ((income - expenses) / income * 100.0) if income > 0 else 0.0
        dti_pct = (liabilities / income * 100.0) if income > 0 else 0.0
        emergency_months = (financial_assets * 0.2) / monthly_exp if monthly_exp > 0 else 6.0
        fin_asset_pct = (financial_assets / assets * 100.0) if assets > 0 else 50.0

        return [
            {
                "rule_id": "RULE-SAVINGS-RATE",
                "rule_name": "Savings Rate Guardrail",
                "category": "foundation",
                "current_ratio": round(savings_pct, 1),
                "target_threshold": 25.0,
                "condition": ">= 25.0%",
                "status": "pass" if savings_pct >= 25 else ("conditional" if savings_pct >= 15 else "fail"),
                "reason": "Measures the percentage of gross income directed towards savings and goal investments.",
                "corrective_action": "Optimize discretionary expenditures to direct at least 25% of annual income into goals." if savings_pct < 25 else None,
            },
            {
                "rule_id": "RULE-DTI-RATIO",
                "rule_name": "Debt-to-Income (DTI) Limit",
                "category": "debt",
                "current_ratio": round(dti_pct, 1),
                "target_threshold": 40.0,
                "condition": "< 40.0%",
                "status": "pass" if dti_pct < 40 else "fail",
                "reason": "Ensures that annual debt obligations remain manageable relative to earning capacity.",
                "corrective_action": "Accelerate debt prepayment to bring leverage below 40% before expanding aggressive goals." if dti_pct >= 40 else None,
            },
            {
                "rule_id": "RULE-EMERGENCY-BUFFER",
                "rule_name": "Emergency Liquidity Buffer",
                "category": "liquidity",
                "current_ratio": round(emergency_months, 1),
                "target_threshold": 6.0,
                "condition": ">= 6.0 Months",
                "status": "pass" if emergency_months >= 6.0 else "conditional",
                "reason": "Protects against premature goal liquidation during unexpected family income interruptions.",
                "corrective_action": "Maintain 6 months of mandatory living expenses in liquid fixed deposits or overnight funds." if emergency_months < 6.0 else None,
            },
            {
                "rule_id": "RULE-FINANCIAL-ASSETS",
                "rule_name": "Liquid Financial Asset Mix",
                "category": "asset_allocation",
                "current_ratio": round(fin_asset_pct, 1),
                "target_threshold": 50.0,
                "condition": ">= 50.0%",
                "status": "pass" if fin_asset_pct >= 50.0 else "conditional",
                "reason": "Prevents over-concentration of family net worth in illiquid physical real estate or gold.",
                "corrective_action": "Direct upcoming surplus flows into diversified financial market instruments." if fin_asset_pct < 50.0 else None,
            },
        ]

    @classmethod
    def _build_family_contingency_matrix(cls) -> list[dict[str, Any]]:
        return [
            {
                "risk_event": "Loss of Primary Earner Income",
                "immediate_action": "File term life insurance claim (recommended: 15–20x annual family expenses) and activate Emergency Fund.",
                "planning_change": "Ring-fence living expenses; temporarily freeze discretionary vacation goals; preserve child education & retirement corpus.",
                "what_not_to_do": "Do not liquidate long-term compounding investments at distress valuations or borrow against credit cards.",
            },
            {
                "risk_event": "Critical Medical Illness in Family",
                "immediate_action": "Initiate cashless claim under primary health insurance floater policy + super top-up cover.",
                "planning_change": "Utilize dedicated liquid healthcare contingency reserve for non-payable hospital expenses without touching goal SIPs.",
                "what_not_to_do": "Do not break fixed deposits or pause goal SIPs for medical costs covered under health policy.",
            },
            {
                "risk_event": "Broad Equity Market Drawdown (> 25%)",
                "immediate_action": "Verify that all goals maturing within 3 years are securely insulated in liquid and short-duration debt.",
                "planning_change": "Maintain uninterrupted monthly SIPs across long-term goals; rebalance fixed income surplus into equities.",
                "what_not_to_do": "Do not panic-sell equity mutual funds or pause automatic monthly SIP mandates.",
            },
            {
                "risk_event": "Sharp Interest Rate Increase",
                "immediate_action": "Audit floating home loan interest rate and remaining EMI tenure.",
                "planning_change": "Direct a portion of discretionary surplus toward accelerated loan principal prepayments.",
                "what_not_to_do": "Do not reduce insurance protection coverage or emergency liquidity to fund EMI surges.",
            },
        ]

    @classmethod
    def _build_governance_protocol(cls) -> list[dict[str, Any]]:
        return [
            {
                "cadence": "Annual Review (Every 12M)",
                "action": "Audit portfolio performance against benchmark; apply 5–10% contribution step-up across all active goals.",
            },
            {
                "cadence": "Asset Allocation Drift",
                "action": "Rebalance equity vs debt if portfolio allocation drifts by more than +/- 5% from target weights.",
            },
            {
                "cadence": "3 Years Before Goal Horizon",
                "action": "Activate systematic transfer (STP) from Equity to Liquid/Debt to protect accumulated capital from drawdown.",
            },
            {
                "cadence": "Major Life Event",
                "action": "Re-run multi-goal financial plan upon marriage, childbirth, major salary increase, or property acquisition.",
            },
        ]

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
    def _table(rows: list[list[Any]], widths: list[float] | None = None) -> Table:
        table = Table(rows, colWidths=widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ]))
        return table

    @staticmethod
    def _section(story: list[Any], title: str, styles: Any) -> None:
        story.extend([Spacer(1, 12), Paragraph(title, styles["Heading2"]), Spacer(1, 4)])

    def generate_pdf(self, planning_unit_id: str) -> bytes:
        plan = self.build_plan(planning_unit_id)
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        normal = styles["BodyText"]
        story: list[Any] = []

        story.extend([
            Paragraph("Planvesto Complete Financial Plan", styles["Title"]),
            Paragraph(f"Consolidated Family Wealth Roadmap & Multi-Goal Strategy", styles["Heading2"]),
            Paragraph(f"Planning Unit: {planning_unit_id} | Total Family Goals: {plan.get('goal_count', 0)}", styles["Normal"]),
            Spacer(1, 10),
        ])

        # 1. Family Financial State
        state = plan["financial_state"]
        self._section(story, "1. Consolidated Family Financial Position & Net Worth", styles)
        story.append(self._table([
            ["Financial Position Metric", "Consolidated Value"],
            *[[k.replace("_", " ").title(), self._fmt(v, "₹" if isinstance(v, (int, float)) else "")]
              for k, v in state.items()],
        ], [220, 303]))

        # 2. MoneyWheel Health Scan
        health_scan = plan.get("moneywheel_health_scan") or self._build_moneywheel_health_scan(state)
        self._section(story, "2. MoneyWheel Diagnostic Health & Vulnerability Scan", styles)
        if health_scan:
            h_rows = [["Diagnostic Metric", "Current Value", "Healthy Benchmark", "Diagnostic Assessment"]]
            for h in health_scan:
                h_rows.append([
                    Paragraph(str(h["metric"]), normal),
                    str(h["current_value"]),
                    str(h["healthy_benchmark"]),
                    Paragraph(str(h["status"]), normal),
                ])
            story.append(self._table(h_rows, [130, 110, 130, 153]))

        # 3. Consolidated Funding & Surplus Allocation
        funding = plan["consolidated_funding"]
        self._section(story, "3. Consolidated Funding Capacity & Resource Waterfall", styles)
        story.append(self._table([
            ["Funding Parameter", "Value"],
            ["Total Available Monthly Surplus", self._fmt(funding.get("available_monthly_surplus"), "₹")],
            ["Total Required Monthly Contribution", self._fmt(funding.get("required_monthly_contribution"), "₹")],
            ["Total Allocated Monthly Contribution", self._fmt(funding.get("allocated_monthly_contribution"), "₹")],
            ["Net Monthly Gap / Buffer", self._fmt(funding.get("monthly_gap"), "₹")],
            ["Consolidated Funding Status", str(funding.get("funding_status") or "Within Surplus")],
            ["Resource Competition Detected", "Yes" if funding.get("competition_detected") else "No"],
        ], [220, 303]))

        # 4. Goal Strategies & Allocation
        self._section(story, "4. Prioritized Goals & Capital Allocation Waterfall", styles)
        goal_rows = [["Priority", "Goal Name", "Target Horizon", "Required/Mo", "Allocated/Mo", "Funding Status"]]
        for row in plan["goals"]:
            priority_label = str(row.get("resolved_priority") or row.get("priority") or "—")
            if row.get("override_applied"):
                priority_label += "*"
            goal_rows.append([
                priority_label,
                Paragraph(str(row.get("goal_name") or "—"), normal),
                str(row.get("target_date") or "—"),
                self._fmt(row.get("required_monthly_contribution"), "₹"),
                self._fmt(row.get("allocated_monthly_contribution"), "₹"),
                Paragraph(str(row.get("funding_status") or "—"), normal),
            ])
        story.append(self._table(goal_rows, [60, 140, 75, 80, 80, 88]))

        # 5. Multi-Year Family Wealth & Cash Flow Projection
        trajectory = plan.get("family_cash_flow_trajectory") or []
        self._section(story, "5. Consolidated Multi-Year Family Wealth & Cash Flow Projection", styles)
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
            story.append(Paragraph("<b>What the Consolidated Wealth Projection Demonstrates:</b> This trajectory models overall family wealth accumulation, showing that recurring surplus allocations comfortably support staggered goal maturities across the family's financial roadmap.", normal))

        # 6. Trade-offs & System Overrides
        if plan.get("trade_offs"):
            self._section(story, "6. Resource Trade-offs & Conflict Resolutions", styles)
            for to in plan["trade_offs"]:
                story.append(Paragraph(f"• {to}", normal))
                story.append(Spacer(1, 3))

        overrides = [g for g in plan["goals"] if g.get("override_applied")]
        if overrides:
            story.append(Spacer(1, 6))
            story.append(Paragraph("<b>System Priority Adjustments:</b>", normal))
            for g in overrides:
                story.append(Paragraph(
                    f"• <b>{g['goal_name']}</b>: Client Priority was <i>{g['client_priority']}</i>, resolved by system rules to <i>{g['resolved_priority']}</i>.<br/>"
                    f"&nbsp;&nbsp;<b>Reason:</b> {g.get('override_reason') or 'Financial ratio constraint.'}",
                    normal,
                ))
                story.append(Spacer(1, 3))

        # 7. Master Action Plan
        actions = plan.get("actions") or []
        self._section(story, "7. Master Implementation Action Plan", styles)
        if actions:
            act_rows = [["#", "Action Item", "Monthly Commitment", "Target Date"]]
            for a in actions:
                act_rows.append([
                    str(a.get("sequence", "—")),
                    Paragraph(str(a.get("action") or ""), normal),
                    self._fmt(a.get("monthly_contribution"), "₹"),
                    str(a.get("target_date") or "Immediate"),
                ])
            story.append(self._table(act_rows, [30, 273, 110, 110]))

        # 8. Master Contingency Matrix
        contingency = plan.get("contingency_matrix") or self._build_family_contingency_matrix()
        self._section(story, "8. Family Crisis & Master Contingency Management Matrix", styles)
        if contingency:
            c_rows = [["Risk Scenario", "Immediate Crisis Action", "Strategic Planning Adjustment", "What NOT To Do"]]
            for c in contingency:
                c_rows.append([
                    Paragraph(str(c.get("risk_event")), normal),
                    Paragraph(str(c.get("immediate_action")), normal),
                    Paragraph(str(c.get("planning_change")), normal),
                    Paragraph(str(c.get("what_not_to_do")), normal),
                ])
            story.append(self._table(c_rows, [105, 140, 140, 138]))

        # 9. Governance & Review Protocol
        protocol = plan.get("governance_protocol") or self._build_governance_protocol()
        self._section(story, "9. Annual Review, Governance & Rebalancing Protocol", styles)
        if protocol:
            p_rows = [["Review Cadence / Trigger", "Governance & Portfolio Action Required"]]
            for p in protocol:
                p_rows.append([
                    Paragraph(str(p.get("cadence")), normal),
                    Paragraph(str(p.get("action")), normal),
                ])
            story.append(self._table(p_rows, [160, 363]))

        # 10. Planning Notes
        if plan.get("planning_notes"):
            self._section(story, "10. Strategic Planning Notes", styles)
            for note in plan["planning_notes"]:
                story.append(Paragraph(f"• {note}", normal))
                story.append(Spacer(1, 3))

        doc.build(story)
        return buffer.getvalue()

