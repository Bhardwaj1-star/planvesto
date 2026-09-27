from .retirement_report_renderer import RetirementReport
from .retirement_report_pdf import RetirementReportPDFExporter
from .strategy_service import StrategyService


class RetirementReportPDFService:
    """Generate PDF from the same persisted retirement report used by the web view."""

    def __init__(self):
        self.strategy_service = StrategyService()
        self.exporter = RetirementReportPDFExporter()

    def generate(self, planning_unit_id: str, strategy_run_id: str) -> bytes:
        data = self.strategy_service.get_retirement_report(planning_unit_id, strategy_run_id)
        report = RetirementReport(title=data["title"], sections=data["sections"])
        return self.exporter.to_pdf(report)
