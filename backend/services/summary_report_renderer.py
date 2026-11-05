from __future__ import annotations

from typing import Any
from reportlab.platypus import Paragraph, Spacer
from models.summary_report import SummaryReport
from report_engine.renderer import CommonPdfRenderer


class SummaryReportRenderer:
    """Render a SummaryReport to PDF using the unified CommonPdfRenderer."""

    def __init__(self):
        self.renderer = CommonPdfRenderer()

    def render(self, report: SummaryReport) -> bytes:
        story: list[Any] = [
            Paragraph("Summary Financial Planning Report", self.renderer.title_style),
            Paragraph("Executive Snapshot & Diagnostic Assessment", self.renderer.h2_style),
            Paragraph(
                f"Planning Unit: {report.provenance.get('planning_unit_id') if report.provenance else 'N/A'}",
                self.renderer.normal,
            ),
            Spacer(1, 10),
        ]

        # 1. Financial Snapshot
        snapshot = report.financial_snapshot or {}
        if snapshot:
            self.renderer.add_section_header(story, "1. Family Financial Snapshot")
            snap_rows = [["Metric", "Value"]]
            for k, v in snapshot.items():
                if isinstance(v, (int, float, str)):
                    snap_rows.append([self.renderer.label_text(k), self.renderer.fmt_value(v, "₹" if isinstance(v, (int, float)) else "")])
            if len(snap_rows) > 1:
                story.append(self.renderer.create_table(snap_rows, [220, 303]))

        # 2. Goals Portfolio
        if report.goals:
            self.renderer.add_section_header(story, "2. Goal Portfolio & Funding Status")
            goal_rows = [["ID", "Goal Name", "Target Amount", "Horizon", "Current Funding", "Net Gap", "Status"]]
            for g in report.goals:
                goal_rows.append([
                    Paragraph(str(g.id), self.renderer.normal),
                    Paragraph(str(g.name), self.renderer.normal),
                    self.renderer.fmt_value(g.target_amount, "₹"),
                    f"{g.horizon_years:.1f} Yrs",
                    self.renderer.fmt_value(g.current_funding, "₹"),
                    self.renderer.fmt_value(g.funding_gap, "₹"),
                    self.renderer.label_text(g.feasibility),
                ])
            story.append(self.renderer.create_table(goal_rows, [60, 110, 85, 55, 80, 80, 53]))

        # 3. Observations
        if report.observations:
            self.renderer.add_section_header(story, "3. Diagnostic Observations & Health Scan")
            obs_rows = [["Source", "Relevance", "Diagnostic Observation"]]
            for obs in report.observations:
                obs_rows.append([
                    str(obs.source),
                    f"{obs.relevance:.2f}",
                    Paragraph(str(obs.description), self.renderer.normal),
                ])
            story.append(self.renderer.create_table(obs_rows, [90, 70, 363]))

        # 4. Actions
        if report.actions:
            self.renderer.add_section_header(story, "4. Recommended Prioritized Actions")
            act_rows = [["Source", "Priority", "Recommended Action Step"]]
            for act in report.actions:
                act_rows.append([
                    str(act.source),
                    f"{act.priority:.2f}",
                    Paragraph(str(act.description), self.renderer.normal),
                ])
            story.append(self.renderer.create_table(act_rows, [90, 70, 363]))

        # 5. Risk Profile
        if report.risk_profile:
            self.renderer.add_section_header(story, "5. Risk Capacity & Boundary Profile")
            risk_rows = [["Dimension / Metric", "Value / Assessment"]]
            for k, val in report.risk_profile.items():
                if isinstance(val, dict):
                    v_str = str(val.get("value") or val.get("status") or val.get("score") or "Configured")
                else:
                    v_str = str(val)
                risk_rows.append([self.renderer.label_text(k), v_str])
            if len(risk_rows) > 1:
                story.append(self.renderer.create_table(risk_rows, [220, 303]))

        return self.renderer.build_document(story)
