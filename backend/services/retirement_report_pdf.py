from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.enums import TA_CENTER

from .retirement_report_renderer import RetirementReport


class RetirementReportPDFExporter:
    """Create a client-facing PDF without changing planning calculations."""

    def to_pdf(self, report: RetirementReport) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=42,
            leftMargin=42,
            topMargin=42,
            bottomMargin=42,
            title=report.title,
        )
        styles = getSampleStyleSheet()
        title = styles["Title"]
        title.alignment = TA_CENTER
        heading = styles["Heading2"]
        body = styles["BodyText"]
        story = [Paragraph(report.title, title), Spacer(1, 18)]
        for section in report.sections:
            story.append(KeepTogether([Paragraph(str(section.get("title", "")), heading)]))
            self._append_value(story, section.get("data"), body, level=0)
            story.append(Spacer(1, 12))
        doc.build(story)
        return buffer.getvalue()

    def _append_value(self, story, value, style, level=0):
        if value is None:
            story.append(Paragraph("—", style))
            return
        if isinstance(value, dict):
            for key, child in value.items():
                label = str(key).replace("_", " ").title()
                story.append(Paragraph(f"<b>{label}:</b>", style))
                self._append_value(story, child, style, level + 1)
            return
        if isinstance(value, (list, tuple)):
            for child in value:
                story.append(Paragraph(f"• {str(child)}", style))
            return
        story.append(Paragraph(str(value), style))
