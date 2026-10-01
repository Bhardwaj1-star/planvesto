from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors

from backend.models.summary_report import SummaryReport

class SummaryReportRenderer:
    """Render a SummaryReport to PDF.
    The implementation mirrors the existing GoalReportService PDF output –
    sections are laid out as simple tables with minimal styling. The goal is
    to provide a usable PDF without inventing any new business rules.
    """

    @staticmethod
    def _table(header: list[str], rows: list[list[str]]) -> Table:
        data = [header] + rows
        table = Table(data, colWidths=[120] * len(header))
        style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
        table.setStyle(style)
        return table

    def render(self, report: SummaryReport) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("Summary Financial Planning Report", styles["Title"]),
            Spacer(1, 12),
        ]

        # Financial Snapshot – dump as preformatted JSON string
        snapshot = report.financial_snapshot
        if snapshot:
            story.append(Paragraph("Financial Snapshot", styles["Heading2"]))
            story.append(Paragraph(f"<pre>{snapshot}</pre>", styles["BodyText"]))
            story.append(Spacer(1, 12))

        # Goals
        if report.goals:
            story.append(Paragraph("Goals", styles["Heading2"]))
            goal_rows = []
            for g in report.goals:
                goal_rows.append([
                    str(g.id),
                    g.name,
                    f"{g.target_amount:.2f} {g.currency}",
                    f"{g.horizon_years:.1f} yr",
                    f"{g.current_funding:.2f}",
                    f"{g.funding_gap:.2f}",
                    g.feasibility,
                ])
            header = ["ID", "Name", "Target", "Horizon", "Funding", "Gap", "Feasibility"]
            story.append(self._table(header, goal_rows))
            story.append(Spacer(1, 12))

        # Observations
        if report.observations:
            story.append(Paragraph("Observations", styles["Heading2"]))
            obs_rows = [[obs.source, f"{obs.relevance:.2f}", obs.description] for obs in report.observations]
            story.append(self._table(["Source", "Relevance", "Description"], obs_rows))
            story.append(Spacer(1, 12))

        # Actions
        if report.actions:
            story.append(Paragraph("Recommended Actions", styles["Heading2"]))
            act_rows = [[act.source, f"{act.priority:.2f}", act.description] for act in report.actions]
            story.append(self._table(["Source", "Priority", "Description"], act_rows))
            story.append(Spacer(1, 12))

        # Investment Allocation (if present)
        if report.investment_allocation:
            story.append(Paragraph("Investment Allocation", styles["Heading2"]))
            # Simple key/value rendering
            rows = [[k, str(v)] for k, v in report.investment_allocation.items()]
            story.append(self._table(["Key", "Value"], rows))
            story.append(Spacer(1, 12))

        # Risk Profile (if present)
        if report.risk_profile:
            story.append(Paragraph("Risk Profile", styles["Heading2"]))
            rows = []
            for key, val in report.risk_profile.items():
                rows.append([str(key), str(val)])
            story.append(self._table(["Metric", "Value"], rows))
            story.append(Spacer(1, 12))

        doc.build(story)
        return buffer.getvalue()
