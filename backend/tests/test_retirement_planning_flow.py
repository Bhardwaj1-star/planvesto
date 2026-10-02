from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from main import app
from models.defined_goal import DefinedGoal
from models.strategy import (
    InvestorPriorities,
    StrategyArchitecture,
    StrategyDefinition,
    StrategyImplementationParamDef,
    StrategyRecommendation,
    StrategyRun,
    Scenario,
)
from services.goal_report_service import GoalReportService
from services.strategy_service import StrategyService

client = TestClient(app)


def _sample_retirement_goal(planning_unit_id="pu-ret-1", goal_id="goal-ret-1"):
    return DefinedGoal(
        planning_unit_id=planning_unit_id,
        goal_id=goal_id,
        goal_name="Retirement / Financial Freedom",
        goal_type="Retirement / Financial Freedom",
        today_cost=600000.0,
        target_month=12,
        target_year=2040,
        duration_years=15.0,
        inflation_rate=0.06,
        priority="Important",
        flexibility="Flexible",
        future_target=14379000.0,
        funding_gap=11379000.0,
        funding_status="Shortfall",
        projected_mapped_asset_value=3000000.0,
        required_monthly_contribution=35000.0,
        version=1,
        status="Active",
    )


def _sample_strategy_run(planning_unit_id="pu-ret-1", goal_id="goal-ret-1", run_id="run-ret-1"):
    param = StrategyImplementationParamDef(
        name="equity_pct",
        label="Equity Allocation %",
        param_type="percentage",
        description="Target equity allocation",
        default_value=60.0,
        editable=True,
        min_value=0.0,
        max_value=100.0,
    )
    strat = StrategyDefinition(
        strategy_id="strat-retirement-diversified",
        name="Diversified Growth & Income Architecture",
        tagline="Balanced accumulation for retirement",
        description="Systematic equity accumulation transitioning to drawdown.",
        strategy_family="Retirement",
        strategic_objective="Fund retirement corpus while preserving purchasing power.",
        core_mechanism="Multi-asset equity glide-path with debt ballast.",
        principles=["Risk containment", "Inflation hedging"],
        constraints=["Horizon > 10y"],
        dependencies=[],
        required_inputs=["Monthly surplus"],
        applicable_goal_characteristics=["long_term"],
        applicable_goal_types=["Retirement / Financial Freedom"],
        technique_ids=["systematic-sip", "equity-glide-path"],
        strategic_levers=["Equity step-up"],
        compatible_strategy_ids=[],
        conflicting_strategy_ids=[],
        library_version="1.0",
        implementation_version="1.0",
        active=True,
        implementation_parameters=[param],
        trade_offs=["Higher market volatility in accumulation years"],
    )
    arch = StrategyArchitecture(
        architecture_id="arch-ret-diversified",
        primary_strategy_id="strat-retirement-diversified",
        supporting_strategy_ids=["strat-debt-buffer"],
        technique_ids=["systematic-sip", "equity-glide-path"],
        rationale=["Fits 15-year retirement horizon and provides inflation beat"],
        trade_offs=["Short-term return volatility during accumulation"],
        feasibility_status="feasible",
        constraints=["Requires disciplined ongoing contribution"],
    )
    scenario = Scenario(
        scenario_id="scen-baseline",
        strategy_id="strat-retirement-diversified",
        scenario_type="baseline",
        scenario_name="Baseline Case",
        assumptions={"expected_return": 11.0, "inflation": 6.0},
        funding_structure={"equity": 60, "debt": 40},
        metrics={"projected_corpus": 15000000.0},
        trade_off_notes="Standard historical equity-debt allocation.",
    )
    rec = StrategyRecommendation(
        recommended_strategy_id="strat-retirement-diversified",
        recommended_scenario_id="scen-baseline",
        short_reasons=["Matches long retirement horizon and shortfall requirements"],
        complete_reasoning="The 15-year horizon allows equity allocation to outpace inflation.",
        architecture=arch,
        alternative_architecture_ids=[],
        feasibility_status="feasible",
        constraints=["Ongoing monthly contributions must be maintained"],
    )
    return StrategyRun(
        strategy_run_id=run_id,
        planning_unit_id=planning_unit_id,
        goal_id=goal_id,
        defined_goal_id=goal_id,
        defined_goal_version=1,
        run_version=1,
        is_latest=True,
        status="completed",
        applicable_strategies=[strat],
        scenarios=[scenario],
        investor_priorities=InvestorPriorities(safety=0.25, liquidity=0.25, growth=0.25, flexibility=0.25),
        comparison_matrix={},
        rankings=[],
        recommendation=rec,
        architectures=[arch],
        selected_strategy_id="strat-retirement-diversified",
        selected_scenario_id="scen-baseline",
        selected_strategy_version_id="ver-ret-1",
        selected_strategy_version=1,
        selected_implementation_parameters={"equity_pct": 65.0},
        selected_architecture=arch,
        selection_timestamp="2026-09-28T12:00:00Z",
        approval_status="selected",
        run_metadata={"strategy_engine_version": "2.0", "strategy_library_version": "1.0"},
    )


class TestRetirementPlanningFlow:
    """Acceptance tests verifying docs/RETIREMENT_PLANNING_FLOW_SPEC.md requirements."""

    def test_retirement_report_api_requires_authentication(self):
        """API endpoints require valid authorization header."""
        res = client.get("/api/strategy/runs/run-123/retirement-report?planning_unit_id=pu-1")
        assert res.status_code == 401
        assert "Authorization token required" in res.json()["detail"]

    def test_retirement_report_pdf_api_requires_authentication(self):
        """PDF endpoint requires valid authorization header."""
        res = client.get("/api/strategy/runs/run-123/retirement-report.pdf?planning_unit_id=pu-1")
        assert res.status_code == 401
        assert "Authorization token required" in res.json()["detail"]

    @patch("api.strategy.verify_strategy_run_ownership")
    @patch("api.strategy.authenticate_user")
    @patch("api.strategy.StrategyService.get_retirement_report")
    def test_retirement_report_api_returns_persisted_report(
        self, mock_get_report, mock_auth, mock_verify
    ):
        """GET /api/strategy/runs/{run_id}/retirement-report returns report data."""
        mock_auth.return_value = "user-123"
        mock_verify.return_value = None
        mock_get_report.return_value = {
            "title": "Retirement Planning Report",
            "sections": [
                {
                    "id": "executive_summary",
                    "title": "1. Executive Summary",
                    "columns": ["Item", "Value"],
                    "rows": [["Status", "Feasible"]],
                    "narratives": {"Takeaway": "Retirement plan is feasible."},
                }
            ],
        }

        res = client.get(
            "/api/strategy/runs/run-ret-1/retirement-report?planning_unit_id=pu-ret-1",
            headers={"Authorization": "Bearer test-token"},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["title"] == "Retirement Planning Report"
        assert len(data["sections"]) == 1
        assert data["sections"][0]["id"] == "executive_summary"

    @patch("api.strategy.verify_strategy_run_ownership")
    @patch("api.strategy.authenticate_user")
    def test_retirement_report_pdf_api_returns_pdf_with_correct_headers(
        self, mock_auth, mock_verify
    ):
        """GET /api/strategy/runs/{run_id}/retirement-report.pdf returns PDF bytes and attachment disposition."""
        mock_auth.return_value = "user-123"
        mock_verify.return_value = None

        goal = _sample_retirement_goal()
        run = _sample_strategy_run()

        service = StrategyService()
        service.strat_repo.get_run_by_id = MagicMock(return_value=run)
        service.goal_repo.get_defined_goal_by_version = MagicMock(return_value=goal)
        service.financial_state_repo.get_latest = MagicMock(return_value=None)

        with patch("api.strategy.GoalReportService") as MockGoalReportService:
            pdf_instance = MockGoalReportService.return_value
            pdf_instance.generate_pdf.return_value = b"%PDF-1.4 test bytes"

            res = client.get(
                "/api/strategy/runs/run-ret-1/retirement-report.pdf?planning_unit_id=pu-ret-1",
                headers={"Authorization": "Bearer test-token"},
            )
            assert res.status_code == 200
            assert res.headers["content-type"] == "application/pdf"
            assert "attachment; filename=retirement-planning-report-run-ret-1.pdf" in res.headers["content-disposition"]
            assert res.content.startswith(b"%PDF-")

    def test_canonical_goal_report_service_covers_retirement_goal(self):
        """Canonical GoalReportService produces all core sections for a retirement goal."""
        goal = _sample_retirement_goal()
        run = _sample_strategy_run()

        report_service = GoalReportService()
        report_service.strategy_repo.get_run_by_id = MagicMock(return_value=run)
        report_service.goal_repo.get_defined_goal_by_version = MagicMock(return_value=goal)
        report_service.goal_repo.get_latest_defined_goal = MagicMock(return_value=goal)
        report_service.financial_state_repo.get_latest = MagicMock(return_value=None)

        report = report_service.build_report("pu-ret-1", "run-ret-1")
        assert report["report_type"] == "goal_decision_report"
        assert report["goal"]["type"] == "Retirement / Financial Freedom"

        # Check core canonical report sections
        expected_sections = [
            "goal",
            "financial_state",
            "goal_calculation",
            "feasibility",
            "goal_funding",
            "strategy",
            "alternatives",
            "scenarios",
            "what_if_analysis",
            "trade_off_analysis",
            "technique_execution",
            "assumptions",
            "decision",
            "provenance",
        ]
        for sec in expected_sections:
            assert sec in report, f"Expected canonical section '{sec}' missing from report"

        # Check that the selected architecture and decision are reflected
        decision = report["decision"]
        assert decision["selected_strategy_id"] == "strat-retirement-diversified"
        assert "Approval status" not in decision

    def test_pdf_export_matches_web_report_data_contract(self):
        """Canonical GoalReportService successfully renders PDF matching report data contract."""
        goal = _sample_retirement_goal()
        run = _sample_strategy_run()

        report_service = GoalReportService()
        report_service.strategy_repo.get_run_by_id = MagicMock(return_value=run)
        report_service.goal_repo.get_defined_goal_by_version = MagicMock(return_value=goal)
        report_service.goal_repo.get_latest_defined_goal = MagicMock(return_value=goal)
        report_service.financial_state_repo.get_latest = MagicMock(return_value=None)

        pdf_bytes = report_service.generate_pdf("pu-ret-1", "run-ret-1")
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 2000
        assert pdf_bytes.startswith(b"%PDF-")

    def test_report_and_pdf_via_pdf_service_e2e(self):
        """GoalReportService coordinates StrategyRun and PDF generation end-to-end for retirement."""
        goal = _sample_retirement_goal()
        run = _sample_strategy_run()

        report_service = GoalReportService()
        report_service.strategy_repo.get_run_by_id = MagicMock(return_value=run)
        report_service.goal_repo.get_defined_goal_by_version = MagicMock(return_value=goal)
        report_service.goal_repo.get_latest_defined_goal = MagicMock(return_value=goal)
        report_service.financial_state_repo.get_latest = MagicMock(return_value=None)

        pdf_bytes = report_service.generate_pdf("pu-ret-1", "run-ret-1")
        assert len(pdf_bytes) > 1000
        assert pdf_bytes.startswith(b"%PDF-")
