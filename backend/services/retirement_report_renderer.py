from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RetirementReport:
    title: str
    sections: list[dict[str, Any]]

    def as_dict(self) -> dict[str, Any]:
        return {"title": self.title, "sections": self.sections}


class RetirementReportRenderer:
    """Build a client-facing retirement planning report from Strategy Builder output.

    Rendering is deliberately presentation-only: calculations, ranking and strategy
    selection remain owned by the planning engines.
    """

    def render(self, *, defined_goal, financial_context=None, rule_assessment=None,
               strategy_result=None, investor=None) -> RetirementReport:
        investor = investor or {}
        context = financial_context or {}
        recommendation = getattr(strategy_result, "recommendation", None)
        rankings = getattr(strategy_result, "rankings", [])
        architecture = getattr(recommendation, "architecture", None)

        diagnostics = []
        if rule_assessment is not None:
            diagnostics = [
                {
                    "rule_id": d.rule_id,
                    "passed": d.passed,
                    "severity": d.severity,
                    "message": d.message,
                    "evidence": d.evidence,
                }
                for d in rule_assessment.diagnostics
            ]

        strategy_summary = {
            "recommended_strategy_id": getattr(recommendation, "recommended_strategy_id", ""),
            "recommended_scenario_id": getattr(recommendation, "recommended_scenario_id", ""),
            "short_reasons": getattr(recommendation, "short_reasons", []),
            "complete_reasoning": getattr(recommendation, "complete_reasoning", ""),
            "feasibility_status": getattr(recommendation, "feasibility_status", ""),
            "constraints": getattr(recommendation, "constraints", []),
        }

        architecture_summary = None
        if architecture is not None:
            architecture_summary = {
                "primary_strategy_id": architecture.primary_strategy_id,
                "supporting_strategy_ids": architecture.supporting_strategy_ids,
                "technique_ids": architecture.technique_ids,
                "rationale": architecture.rationale,
                "trade_offs": architecture.trade_offs,
                "feasibility_status": architecture.feasibility_status,
                "constraints": architecture.constraints,
            }

        sections = [
            {
                "id": "executive_summary",
                "title": "Retirement Planning Summary",
                "data": {
                    "investor_name": investor.get("name"),
                    "goal_name": defined_goal.goal_name,
                    "horizon_years": defined_goal.duration_years,
                    "funding_status": defined_goal.funding_status,
                    "target": defined_goal.future_target,
                    "funding_gap": defined_goal.funding_gap,
                },
            },
            {"id": "financial_state", "title": "Financial State", "data": context},
            {"id": "diagnostics", "title": "Financial Health Diagnostics", "data": diagnostics},
            {"id": "strategy_analysis", "title": "Strategy Analysis", "data": rankings},
            {"id": "recommendation", "title": "Recommended Strategy", "data": strategy_summary},
            {"id": "architecture", "title": "Strategy Architecture", "data": architecture_summary},
            {
                "id": "implementation_notes",
                "title": "Implementation Notes",
                "data": {
                    "constraints": strategy_summary["constraints"],
                    "note": "This report describes the planning strategy. Product selection and portfolio implementation are downstream modules.",
                },
            },
        ]
        return RetirementReport(title="Retirement Planning Report", sections=sections)
