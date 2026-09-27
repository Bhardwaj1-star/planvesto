from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class RetirementReport:
    title: str
    sections: list[dict[str, Any]]

    def as_dict(self) -> dict[str, Any]:
        return {"title": self.title, "sections": self.sections}


class RetirementReportRenderer:
    """Map stored Planvesto planning outputs into the retirement report master template.

    This layer is presentation-only. Missing source data is represented explicitly;
    it is never inferred or silently replaced with a made-up value.
    """

    MISSING = "Not available"

    @staticmethod
    def _value(source: Any, *keys: str, default: Any = MISSING) -> Any:
        if source is None:
            return default
        for key in keys:
            if isinstance(source, dict) and key in source:
                value = source[key]
            else:
                value = getattr(source, key, None)
            if value is not None and value != "":
                return value
        return default

    @classmethod
    def _row(cls, label: str, value: Any, *extra: Any) -> list[Any]:
        return [label, cls.MISSING if value is None else value, *extra]

    @staticmethod
    def _date(value: Any) -> str:
        if value:
            return str(value)
        return datetime.now(timezone.utc).date().isoformat()

    def render(self, *, defined_goal, financial_context=None, rule_assessment=None,
               strategy_result=None, investor=None) -> RetirementReport:
        context = financial_context or {}
        investor = investor or {}
        run = strategy_result
        recommendation = self._value(run, "recommendation", default=None)
        priorities = self._value(run, "investor_priorities", default=None)
        architecture = self._value(recommendation, "architecture", default=None)
        rankings = self._value(run, "rankings", default=[])
        scenarios = self._value(run, "scenarios", default=[])
        mapped_assets = self._value(defined_goal, "mapped_assets", default=[])
        metadata = self._value(run, "run_metadata", default={}) or {}
        diagnostics = self._value(rule_assessment, "diagnostics", default=[])

        target_retirement_age = self._value(context, "retirement_age", "target_retirement_age")
        current_age = self._value(context, "current_age")
        years_to_retirement = self._value(defined_goal, "duration_years")
        retirement_horizon = self._value(context, "retirement_horizon", default=years_to_retirement)
        retirement_income = self._value(context, "desired_retirement_income", "retirement_income")
        retirement_spending = self._value(context, "current_retirement_spending", "retirement_spending")
        retirement_duration = self._value(context, "retirement_duration", "longevity_horizon")

        financial_rows = [
            self._row("Annual income", self._value(context, "annual_income", "income")),
            self._row("Annual expenses", self._value(context, "annual_expenses", "expenses")),
            self._row("Monthly surplus", self._value(context, "monthly_surplus", "surplus")),
            self._row("Financial assets", self._value(context, "financial_assets", "assets")),
            self._row("Retirement-linked assets", self._value(context, "retirement_assets")),
            self._row("Liabilities", self._value(context, "liabilities")),
            self._row("Net worth", self._value(context, "net_worth")),
        ]

        requirement_rows = [
            self._row("Current retirement spending", retirement_spending, self._value(defined_goal, "today_cost")),
            self._row("Inflation assumption", self._value(defined_goal, "inflation_rate"), self._value(defined_goal, "future_target")),
            self._row("Years to retirement", years_to_retirement, self._value(defined_goal, "target_year")),
            self._row("Retirement duration", retirement_duration, retirement_duration),
            self._row("Required retirement corpus", self._value(defined_goal, "future_target"), self._value(defined_goal, "future_target")),
            self._row("Existing mapped resources", self._value(defined_goal, "mapped_assets"), self._value(defined_goal, "projected_mapped_asset_value")),
            self._row("Funding requirement", self._value(defined_goal, "funding_gap"), self._value(defined_goal, "funding_gap")),
        ]

        funding_rows = [
            self._row("Target corpus", self._value(defined_goal, "future_target")),
            self._row("Projected existing resources", self._value(defined_goal, "projected_mapped_asset_value")),
            self._row("Funding gap / surplus", self._value(defined_goal, "funding_gap")),
            self._row("Required monthly contribution", self._value(defined_goal, "required_monthly_contribution")),
            self._row("Funding status", self._value(defined_goal, "funding_status")),
        ]

        priority_rows = [
            self._row("Safety", self._value(priorities, "safety")),
            self._row("Liquidity", self._value(priorities, "liquidity")),
            self._row("Growth", self._value(priorities, "growth")),
            self._row("Flexibility", self._value(priorities, "flexibility")),
        ]

        strategy_rows = [
            self._row("Recommended strategy", self._value(recommendation, "recommended_strategy_id")),
            self._row("Recommended scenario", self._value(recommendation, "recommended_scenario_id")),
            self._row("Primary strategy architecture", self._value(architecture, "primary_strategy_id")),
            self._row("Supporting strategies", self._value(architecture, "supporting_strategy_ids")),
            self._row("Techniques", self._value(architecture, "technique_ids")),
            self._row("Feasibility status", self._value(recommendation, "feasibility_status")),
            self._row("Strategy version", self._value(run, "selected_strategy_version")),
        ]

        architecture_rows = [
            self._row("Primary strategy", self._value(architecture, "primary_strategy_id")),
            self._row("Supporting strategy 1", (self._value(architecture, "supporting_strategy_ids", default=[]) or [self.MISSING])[0]),
            self._row("Supporting strategy 2", ((self._value(architecture, "supporting_strategy_ids", default=[]) or [self.MISSING, self.MISSING]) + [self.MISSING])[1]),
            self._row("Techniques", self._value(architecture, "technique_ids")),
            self._row("Funding structure", self._value(run, "selected_implementation_parameters", default={})),
            self._row("Implementation parameters", self._value(run, "selected_implementation_parameters", default={})),
        ]

        accumulation_rows = [
            self._row("Starting corpus", self._value(context, "starting_corpus", "current_corpus")),
            self._row("Ongoing contribution", self._value(defined_goal, "required_monthly_contribution")),
            self._row("Contribution frequency", self._value(context, "contribution_frequency")),
            self._row("Contribution escalation / step-up", self._value(context, "contribution_step_up", "step_up")),
            self._row("Expected return assumption", self._value(defined_goal, "funding_return_assumption")),
            self._row("Target retirement corpus", self._value(defined_goal, "future_target")),
            self._row("Review frequency", self._value(context, "review_frequency")),
        ]

        transition_rows = [
            self._row("Transition start", self._value(context, "transition_start")),
            self._row("Target retirement corpus", self._value(defined_goal, "future_target")),
            self._row("Liquidity requirement", self._value(context, "transition_liquidity")),
            self._row("Income requirement at retirement", retirement_income),
            self._row("Transition strategy", self._value(context, "transition_strategy")),
            self._row("Key trigger / review rule", self._value(context, "transition_trigger")),
        ]

        income_rows = [
            self._row("Initial retirement income requirement", retirement_income),
            self._row("Income escalation rule", self._value(context, "income_escalation")),
            self._row("Expected retirement duration", retirement_duration),
            self._row("Income funding architecture", self._value(context, "income_funding_architecture")),
            self._row("Liquidity reserve / buffer", self._value(context, "liquidity_buffer")),
            self._row("Review / withdrawal rule", self._value(context, "withdrawal_review_rule")),
        ]

        scenario_rows = []
        for scenario in scenarios:
            scenario_rows.append([
                self._value(scenario, "scenario_name"),
                self._value(scenario, "assumptions", default={}),
                self._value(scenario, "funding_structure", default={}),
                self._value(scenario, "metrics", default={}),
                self._value(scenario, "trade_off_notes"),
            ])
        if not scenario_rows:
            scenario_rows.append([self.MISSING] * 5)

        risk_rows = [
            self._row("Funding shortfall", self._value(context, "funding_shortfall_effect"), self._value(context, "funding_shortfall_response")),
            self._row("Return uncertainty", self._value(context, "return_uncertainty_effect"), self._value(context, "return_uncertainty_response")),
            self._row("Inflation / spending change", self._value(context, "inflation_effect"), self._value(context, "inflation_response")),
            self._row("Income change", self._value(context, "income_change_effect"), self._value(context, "income_change_response")),
            self._row("Retirement date change", self._value(context, "retirement_date_effect"), self._value(context, "retirement_date_response")),
            self._row("Major financial event", self._value(context, "major_event_effect"), self._value(context, "major_event_response")),
        ]

        roadmap_rows = [
            self._row("Now", self._value(context, "action_now"), self._value(context, "purpose_now"), self._value(context, "trigger_now")),
            self._row("Next review", self._value(context, "action_review"), self._value(context, "purpose_review"), self._value(context, "trigger_review")),
            self._row("Before retirement", self._value(context, "action_pre_retirement"), self._value(context, "purpose_pre_retirement"), self._value(context, "trigger_pre_retirement")),
            self._row("At retirement", self._value(context, "action_retirement"), self._value(context, "purpose_retirement"), self._value(context, "trigger_retirement")),
            self._row("After retirement", self._value(context, "action_post_retirement"), self._value(context, "purpose_post_retirement"), self._value(context, "trigger_post_retirement")),
        ]

        review_rows = [
            self._row("Income changes materially", self._value(context, "income_review")),
            self._row("Expenses / lifestyle changes", self._value(context, "expense_review")),
            self._row("Large asset or liability change", self._value(context, "balance_sheet_review")),
            self._row("Retirement date changes", self._value(context, "retirement_date_review")),
            self._row("Retirement goal changes", self._value(context, "goal_review")),
            self._row("Material strategy change", self._value(context, "strategy_review")),
            self._row("Scheduled review", self._value(context, "scheduled_review")),
        ]

        provenance_rows = [
            self._row("Goal inputs", self._value(defined_goal, "goal_id"), "DefinedGoal", self._value(defined_goal, "version")),
            self._row("Financial state", bool(context), "Financial State Snapshot", self._value(context, "version")),
            self._row("Calculation assumptions", {"inflation_rate": self._value(defined_goal, "inflation_rate"), "funding_return_assumption": self._value(defined_goal, "funding_return_assumption")}, "DefinedGoal", self._value(defined_goal, "version")),
            self._row("Strategy engine", self._value(metadata, "strategy_engine_version"), "Planvesto Strategy Engine", self._value(run, "run_version")),
            self._row("Strategy library", self._value(metadata, "strategy_library_version"), "Planvesto Strategy Library", self._value(metadata, "library_version")),
        ]

        decision_rows = [
            self._row("Selected strategy", self._value(run, "selected_strategy_id")),
            self._row("Selected scenario", self._value(run, "selected_scenario_id")),
            self._row("Selected architecture", self._value(run, "selected_architecture")),
            self._row("Implementation parameters", self._value(run, "selected_implementation_parameters", default={})),
            self._row("Approval status", self._value(run, "approval_status")),
            self._row("Approval timestamp", self._value(run, "selection_timestamp")),
            self._row("Plan version", self._value(run, "run_version")),
        ]

        history_rows = [[
            self._value(run, "run_version"),
            self._value(run, "created_at"),
            self._value(metadata, "trigger"),
            self._value(run, "selected_strategy_id"),
            self._value(run, "status"),
        ]]

        sections = [
            {"id": "executive_summary", "title": "1. Executive Summary", "description": "This section gives the investor the complete picture before the detailed analysis.", "columns": ["Report Detail", "Value"], "rows": [self._row("Investor", self._value(investor, "name")), self._row("Report Date", self._date(self._value(run, "created_at", default=None))), self._row("Plan Version", self._value(run, "run_version")), self._row("Planning Status", self._value(run, "status")), self._row("Current age", current_age), self._row("Target retirement age", target_retirement_age), self._row("Years to retirement", years_to_retirement), self._row("Retirement objective", self._value(defined_goal, "goal_name")), self._row("Required retirement corpus", self._value(defined_goal, "future_target")), self._row("Current mapped retirement resources", self._value(defined_goal, "mapped_assets")), self._row("Projected value of mapped resources", self._value(defined_goal, "projected_mapped_asset_value")), self._row("Funding gap / surplus", self._value(defined_goal, "funding_gap")), self._row("Required ongoing contribution", self._value(defined_goal, "required_monthly_contribution")), self._row("Strategy status", self._value(recommendation, "feasibility_status"))], "narratives": {"Investor takeaway": self._value(metadata, "executive_takeaway"), "Decision required": self._value(metadata, "investor_decision_required")}},
            {"id": "retirement_objective", "title": "2. Your Retirement Objective", "description": "The retirement plan starts with the investor’s defined objective rather than with a financial product.", "columns": ["Dimension", "Investor-specific value"], "rows": [self._row("Current age", current_age), self._row("Expected retirement age", target_retirement_age), self._row("Planning horizon", retirement_horizon), self._row("Desired retirement lifestyle", self._value(context, "retirement_lifestyle")), self._row("Desired retirement income / spending", retirement_income), self._row("Target retirement date", self._value(context, "target_retirement_date")), self._row("Longevity / planning age", self._value(context, "longevity_assumption")), self._row("Other retirement objectives", self._value(context, "other_retirement_objectives"))], "narratives": {"Goal definition": self._value(metadata, "defined_retirement_goal_description", default=self._value(defined_goal, "goal_name"))}},
            {"id": "financial_position", "title": "3. Current Financial Position", "description": "This section presents the financial state used by the planning system at the time the plan was generated.", "columns": ["Category", "Value", "Included in retirement plan?", "Notes"], "rows": [[r[0], r[1], self._value(context, r[0].lower().replace(" ", "_" ) + "_inclusion"), self._value(context, r[0].lower().replace(" ", "_") + "_notes")] for r in financial_rows], "narratives": {"Resource mapping": [self._value(a, "asset_name") for a in mapped_assets] if mapped_assets else self.MISSING}},
            {"id": "retirement_requirement", "title": "4. Retirement Requirement Calculation", "description": "The retirement requirement is the quantitative foundation of the plan. The final report should show the values produced by the relevant Planvesto calculation engines and the assumptions that produced them.", "columns": ["Calculation", "Input / Assumption", "Output"], "rows": requirement_rows, "narratives": {"Calculation interpretation": self._value(metadata, "retirement_calculation_interpretation")}},
            {"id": "funding_gap", "title": "5. Funding Gap & Feasibility", "columns": ["Metric", "Value", "Interpretation"], "rows": [[r[0], r[1], self._value(metadata, r[0].lower().replace(" ", "_") + "_interpretation")] for r in funding_rows], "narratives": {"Feasibility assessment": self._value(metadata, "feasibility_assessment")}},
            {"id": "investor_priorities", "title": "6. Investor Priorities", "columns": ["Priority", "Weight", "Meaning in this plan"], "rows": [[r[0], r[1], self._value(metadata, r[0].lower() + "_interpretation")] for r in priority_rows], "narratives": {"Priority rationale": self._value(metadata, "priority_rationale")}},
            {"id": "strategy_recommendation", "title": "7. Strategy Recommendation", "description": "This is the core decision section. It reproduces the strategy selected/recommended by the Planvesto Strategy Engine, including its rationale, constraints and trade-offs.", "columns": ["Strategy element", "Planvesto output"], "rows": strategy_rows, "narratives": {"Why this strategy?": self._value(recommendation, "complete_reasoning"), "Key trade-offs": self._value(architecture, "trade_offs", default=[]), "Constraints": self._value(recommendation, "constraints", default=[])}},
            {"id": "strategy_architecture", "title": "8. Strategy Architecture", "columns": ["Component", "Role in the retirement plan"], "rows": architecture_rows, "narratives": {"Architecture rationale": self._value(architecture, "rationale", default=[])}},
            {"id": "accumulation_plan", "title": "9. Accumulation Plan Until Retirement", "columns": ["Element", "Plan value / rule"], "rows": accumulation_rows, "narratives": {"Implementation instructions": self._value(metadata, "accumulation_implementation")}},
            {"id": "retirement_transition", "title": "10. Retirement Transition Plan", "columns": ["Transition item", "Plan output"], "rows": transition_rows, "narratives": {"Transition rationale": self._value(metadata, "transition_rationale")}},
            {"id": "retirement_income", "title": "11. Retirement Income Strategy", "columns": ["Income element", "Plan output"], "rows": income_rows, "narratives": {"Retirement income strategy": self._value(metadata, "retirement_income_strategy")}},
            {"id": "scenario_analysis", "title": "12. Scenario Analysis", "description": "Scenarios show how outcomes change when assumptions or implementation parameters change. They are not presented as guarantees.", "columns": ["Scenario", "Key assumptions", "Funding outcome", "Corpus / income outcome", "Trade-off"], "rows": scenario_rows, "narratives": {"Scenario interpretation": self._value(metadata, "scenario_interpretation")}},
            {"id": "risks_constraints", "title": "13. Risks, Constraints & Contingency Actions", "columns": ["Risk / constraint", "Potential effect", "Plan response / trigger"], "rows": risk_rows, "narratives": {"Risk notes": self._value(metadata, "risk_notes")}},
            {"id": "implementation_roadmap", "title": "14. Implementation Roadmap", "columns": ["When", "Action", "Purpose", "Planvesto trigger"], "rows": roadmap_rows, "narratives": {"Implementation notes": self._value(metadata, "implementation_notes")}},
            {"id": "monitoring_review", "title": "15. Monitoring & Review Framework", "description": "A retirement plan is intended to be updated when material inputs change. The report should specify what triggers a new Planvesto strategy run.", "columns": ["Review trigger", "What should be reassessed"], "rows": review_rows},
            {"id": "assumptions_provenance", "title": "16. Assumptions & Data Provenance", "description": "Every material number in the investor report should be traceable to an investor input, a Planvesto calculation, a strategy-engine output, or an explicitly recorded assumption.", "columns": ["Assumption / input", "Value", "Source", "As-of / version"], "rows": provenance_rows, "narratives": {"Limitations and data quality": self._value(metadata, "limitations_and_data_quality")}},
            {"id": "investor_decision", "title": "17. Investor Decision & Approval", "description": "This section records what the investor has selected or approved. It must not imply approval when the system status is not approved.", "columns": ["Decision item", "Status / value"], "rows": decision_rows, "narratives": {"Investor acknowledgement": self._value(metadata, "investor_acknowledgement")}},
            {"id": "plan_history", "title": "18. Plan History", "description": "The investor-facing report should preserve version context so the current plan can be distinguished from previous versions.", "columns": ["Version", "Date", "Reason for change", "Strategy / goal change", "Status"], "rows": history_rows},
            {"id": "appendix_calculations", "title": "Appendix A — Detailed Calculation Outputs", "narratives": {"Calculation output table": self._value(metadata, "calculation_output_table")}},
            {"id": "appendix_strategy", "title": "Appendix B — Strategy Engine Output", "narratives": {"Strategy engine raw or structured output": {"rankings": rankings, "comparison_matrix": self._value(run, "comparison_matrix", default={})}}},
            {"id": "appendix_glossary", "title": "Appendix C — Glossary", "columns": ["Term", "Meaning"], "rows": [["Goal", "The defined financial objective being planned."], ["Funding gap", "The difference between required resources and projected available resources under the plan assumptions."], ["Strategy", "The architecture used to fund and achieve the defined goal."], ["Scenario", "A defined set of assumptions or modifications used to examine an alternative outcome."], ["Technique", "A method used within a strategy architecture."], ["Strategy run", "A versioned engine execution for a defined goal and investor priorities."], ["Plan version", "The investor-facing version of the approved/current plan."]]},
            {"id": "appendix_rules", "title": "Appendix D — Report Generation Rules", "narratives": {"Rules": ["Do not invent investor values to complete a report.", "Every numeric output must be traceable to a stored input or calculation.", "Display the calculation date and relevant goal/strategy version.", "Clearly distinguish investor inputs, calculated outputs, assumptions, and scenario values.", "Do not present scenario outcomes as guarantees.", "Do not show a strategy as approved unless the system approval state is approved.", "When required data is missing, explicitly show the missing-data state rather than silently substituting a value."]}},
        ]
        return RetirementReport(title="Retirement Planning Report", sections=sections)
