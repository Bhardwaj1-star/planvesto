import logging
from backend.engines.summary_report.engine import SummaryReportEngine
from backend.models.summary_report import SummaryReport

logger = logging.getLogger(__name__)

class SummaryReportService:
    """Public service API for building the summary financial planning report.
    It isolates the engine from the web layer and can be used by background
    jobs or other internal components.
    """

    @staticmethod
    def generate(planning_unit_id: str) -> SummaryReport:
        logger.info("Generating summary report for planning unit %s", planning_unit_id)
        engine = SummaryReportEngine(planning_unit_id)
        report = engine.build_report()
        return report
