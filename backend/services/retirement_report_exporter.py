from html import escape
from .retirement_report_renderer import RetirementReport


class RetirementReportExporter:
    """Presentation exporter. It does not calculate or mutate planning results."""

    def to_html(self, report: RetirementReport) -> str:
        parts = [
            "<!doctype html><html><head><meta charset='utf-8'>",
            "<title>Retirement Planning Report</title>",
            "<style>body{font-family:Arial,sans-serif;max-width:900px;margin:40px auto;padding:0 24px;color:#222}h1{margin-bottom:8px}h2{border-bottom:1px solid #ddd;padding-bottom:8px}section{margin:28px 0}.item{margin:6px 0}.key{font-weight:600}</style>",
            "</head><body>",
            f"<h1>{escape(report.title)}</h1>",
        ]
        for section in report.sections:
            parts.append(f"<section><h2>{escape(str(section.get('title', '')))}</h2>")
            parts.append(self._render_value(section.get("data")))
            parts.append("</section>")
        parts.append("</body></html>")
        return "".join(parts)

    def _render_value(self, value) -> str:
        if value is None:
            return "<div class='item'>—</div>"
        if isinstance(value, dict):
            return "<div>" + "".join(
                f"<div class='item'><span class='key'>{escape(str(k))}:</span> {self._render_value(v)}</div>"
                for k, v in value.items()
            ) + "</div>"
        if isinstance(value, (list, tuple)):
            return "<ul>" + "".join(f"<li>{self._render_value(v)}</li>" for v in value) + "</ul>"
        return escape(str(value))
