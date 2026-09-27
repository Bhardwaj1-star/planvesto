from services.retirement_report_pdf import RetirementReportPDFExporter
from services.retirement_report_renderer import RetirementReport


def test_retirement_report_pdf_renders_master_template_sections():
    report = RetirementReport(
        title="Retirement Planning Report",
        sections=[
            {
                "id": "executive_summary",
                "title": "1. Executive Summary",
                "description": "Summary",
                "columns": ["Detail", "Value"],
                "rows": [["Target corpus", 10000000], ["Funding status", "On Track"]],
                "narratives": {"Investor takeaway": "Plan is on track."},
            },
            {"id": "appendix_a", "title": "Appendix A — Strategy Definitions", "columns": ["ID", "Name"], "rows": [["S1", "Strategy"]]},
        ],
    )

    pdf = RetirementReportPDFExporter().to_pdf(report)

    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1000
