from io import BytesIO
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

from .retirement_report_renderer import RetirementReport


class RetirementReportPDFExporter:
    """Render the Planvesto retirement master-template structure as a PDF."""

    def to_pdf(self, report: RetirementReport) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=16 * mm,
            leftMargin=16 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
            title=report.title,
        )
        styles = getSampleStyleSheet()
        title = ParagraphStyle("ReportTitle", parent=styles["Title"], alignment=TA_CENTER, spaceAfter=14)
        heading = ParagraphStyle("ReportHeading", parent=styles["Heading2"], fontSize=15, leading=18, textColor=colors.HexColor("#315f91"), spaceBefore=10, spaceAfter=7)
        body = ParagraphStyle("ReportBody", parent=styles["BodyText"], fontSize=9, leading=12, spaceAfter=5)
        small = ParagraphStyle("ReportSmall", parent=body, fontSize=8, leading=10)

        story = [Paragraph(escape(report.title), title)]
        for index, section in enumerate(report.sections):
            if index and section["id"].startswith("appendix_"):
                story.append(PageBreak())
            story.append(Paragraph(escape(section.get("title", "")), heading))
            if section.get("description"):
                story.append(Paragraph(escape(str(section["description"])), body))
            columns = section.get("columns")
            rows = section.get("rows")
            if columns and rows is not None:
                self._append_table(story, columns, rows, small)
            for label, value in (section.get("narratives") or {}).items():
                story.append(Paragraph(f"<b>{escape(str(label))}</b>", body))
                self._append_value(story, value, body)
            story.append(Spacer(1, 7))

        doc.build(story, onFirstPage=self._footer, onLaterPages=self._footer)
        return buffer.getvalue()

    def _append_table(self, story, columns, rows, style):
        normalized = [[self._cell(c) for c in columns]]
        for row in rows:
            normalized.append([self._cell(v) for v in row])
        table = Table(normalized, repeatRows=1, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9eef3")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7.5),
            ("LEADING", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#9aa5ad")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(table)
        story.append(Spacer(1, 7))

    def _cell(self, value):
        if value is None:
            value = "Not available"
        if isinstance(value, (dict, list, tuple)):
            if isinstance(value, dict):
                value = "; ".join(f"{k}: {v}" for k, v in value.items())
            else:
                value = "; ".join(str(v) for v in value)
        return Paragraph(escape(str(value)).replace("\n", "<br/>"), ParagraphStyle("Cell", fontSize=7.5, leading=9))

    def _append_value(self, story, value, style):
        if value is None:
            story.append(Paragraph("Not available", style))
            return
        if isinstance(value, dict):
            for key, child in value.items():
                story.append(Paragraph(f"<b>{escape(str(key))}:</b> {escape(str(child))}", style))
            return
        if isinstance(value, (list, tuple)):
            for child in value:
                story.append(Paragraph(f"• {escape(str(child))}", style))
            return
        story.append(Paragraph(escape(str(value)), style))

    @staticmethod
    def _footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawCentredString(A4[0] / 2, 8 * mm, f"Planvesto • Retirement Planning Report • {doc.page}")
        canvas.restoreState()
