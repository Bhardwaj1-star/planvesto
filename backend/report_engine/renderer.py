"""Common PDF Renderer for all Planvesto reports.

Unifies ReportLab layout, styles, table formatting, page sizes, and fonts across:
- Goal Decision Report (Scope 1)
- Basket Decision Report (Scope 2)
- Complete Financial Plan (Scope 3)
- Summary Planning Report (Scope 4)
"""
from __future__ import annotations

from io import BytesIO
from typing import Any, List, Sequence
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class CommonPdfRenderer:
    """Consolidated ReportLab document builder for all canonical reports."""

    PRIMARY_COLOR = colors.HexColor("#0f172a")
    HEADER_TEXT_COLOR = colors.white
    GRID_COLOR = colors.HexColor("#cbd5e1")
    ALT_ROW_BG = colors.HexColor("#f8fafc")
    PAGE_MARGIN = 36

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.normal = self.styles["BodyText"]
        self.title_style = self.styles["Title"]
        self.h2_style = self.styles["Heading2"]
        self.h3_style = self.styles["Heading3"]

    @staticmethod
    def fmt_value(value: Any, prefix: str = "") -> str:
        if value is None:
            return "Not available"
        if isinstance(value, float):
            return f"{prefix}{value:,.2f}"
        if isinstance(value, int):
            return f"{prefix}{value:,}"
        return f"{prefix}{value}"

    @staticmethod
    def label_text(value: Any) -> str:
        return str(value or "").replace("_", " ").replace("-", " ").title()

    def create_table(
        self,
        rows: Sequence[Sequence[Any]],
        col_widths: Sequence[float] | None = None,
        repeat_rows: int = 1,
    ) -> Table:
        # Wrap string cells in Paragraph if they look long, or keep as is
        table = Table(rows, colWidths=col_widths, repeatRows=repeat_rows)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), self.PRIMARY_COLOR),
                    ("TEXTCOLOR", (0, 0), (-1, 0), self.HEADER_TEXT_COLOR),
                    ("GRID", (0, 0), (-1, -1), 0.5, self.GRID_COLOR),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 5),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, self.ALT_ROW_BG]),
                ]
            )
        )
        return table

    def add_section_header(self, story: list[Any], title: str) -> None:
        story.extend([Spacer(1, 12), Paragraph(title, self.h2_style), Spacer(1, 4)])

    def build_document(self, story: list[Any]) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=self.PAGE_MARGIN,
            leftMargin=self.PAGE_MARGIN,
            topMargin=self.PAGE_MARGIN,
            bottomMargin=self.PAGE_MARGIN,
        )
        doc.build(story)
        return buffer.getvalue()
