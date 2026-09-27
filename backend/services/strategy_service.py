from fastapi import HTTPException
from data.goal_repository import GoalRepository
from data.strategy_repository import StrategyRepository
from data.strategy_version_repository import StrategyVersionRepository
from data.financial_state_repository import FinancialStateSnapshotRepository
from engines.strategy.engine import StrategyEngine
from engines.strategy.scenario import create_custom_scenario
from engines.rules.engine import RuleEngine
from models.defined_goal import DefinedGoal
from models import rule_assessment
from models.strategy import InvestorPriorities, Scenario, StrategyRun
from schemas.strategy import CustomScenarioRequest, PriorityWeightsRequest, StrategyBuildRequest, StrategySelectRequest, StrategyApprovalRequest
from services.strategy_version_service import StrategyVersionService
from services.retirement_report_renderer import RetirementReportRenderer


class StrategyService:
    def __init__(self):
        self.goal_repo = GoalRepository()
        self.strat_repo = StrategyRepository()
        self.financial_state_repo = FinancialStateSnapshotRepository()
        self.engine = StrategyEngine()
        self.rule_engine = RuleEngine()
        self.strategy_version_service = StrategyVersionService(StrategyVersionRepository(self.strat_repo.db))
        self.report_renderer = RetirementReportRenderer()

    def _financial_context(self, planning_unit_id: str, defined_goal: DefinedGoal) -> dict:
        snapshot = self.financial_state_repo.get_latest(planning_unit_id, "family")
        if snapshot and snapshot.get("financial_state"):
            return snapshot["financial_state"]
        return {}

    def _rule_assessment(self, defined_goal: DefinedGoal, financial_context: dict):
        return self.rule_engine.assess(defined_goal, financial_context)

    def _execute(self, defined_goal: DefinedGoal, priorities: InvestorPriorities, financial_context: dict, custom_scenarios=None):
        rule_assessment = self._rule_assessment(defined_goal, financial_context)
        if not rule_assessment.eligible:
            raise HTTPException(status_code=422, detail={"message": "Goal failed hard planning constraints.", "constraints": [r.__dict__ for r in rule_assessment.hard_constraints]})
        result = self.engine.execute(defined_goal=defined_goal, priorities=priorities, custom_scenarios=custom_scenarios, financial_context=financial_context, rule_assessment=rule_assessment)
        return result, rule_assessment

    def build_strategy(self, planning_unit_id: str, goal_id: str, priorities: InvestorPriorities | None = None) -> StrategyRun:
        defined_goal = self.goal_repo.get_latest_defined_goal(planning_unit_id, goal_id)
        if not defined_goal:
            raise HTTPException(status_code=404, detail="No DefinedGoal found for this goal. Please complete Goal Planning first.")
        prev_run = self.strat_repo.get_latest_run(planning_unit_id, goal_id)
        if priorities is None:
            priorities = prev_run.investor_priorities if prev_run else None
        if priorities is None:
            raise HTTPException(status_code=400, detail="Investor priorities must be provided before strategy comparison and ranking.")
        financial_context = self._financial_context(planning_unit_id, defined_goal)
        result, rule_assessment = self._execute(defined_goal, priorities, financial_context)
        run = StrategyRun(planning_unit_id=planning_unit_id, goal_id=goal_id, defined_goal_id=defined_goal.defined_goal_id or "", defined_goal_version=defined_goal.version, run_version=(prev_run.run_version + 1) if prev_run else 1, is_latest=True, status="completed", applicable_strategies=result.applicable_strategies, scenarios=result.scenarios, investor_priorities=result.priorities, comparison_matrix=result.comparison_matrix, rankings=result.rankings, recommendation=result.recommendation, architectures=result.architectures, run_metadata={"trigger": "manual_build", "financial_state_context_available": bool(financial_context), "rule_assessment": {"eligible": rule_assessment.eligible, "diagnostics": [r.__dict__ for r in rule_assessment.diagnostics], "hard_constraints": [r.__dict__ for r in rule_assessment.hard_constraints], "soft_constraints": [r.__dict__ for r in rule_assessment.soft_constraints]}})
        run.strategy_run_id = self.strat_repo.save_run(run)
        return run

    def add_custom_scenario(self, request: CustomScenarioRequest) -> StrategyRun:
        run = self.strat_repo.get_run_by_id(request.planning_unit_id, request.strategy_run_id)
        if not run: raise HTTPException(status_code=404, detail="Strategy run not found")
        defined_goal = self.goal_repo.get_defined_goal_by_version(request.planning_unit_id, run.goal_id, run.defined_goal_version)
        if not defined_goal: raise HTTPException(status_code=404, detail="Underlying DefinedGoal snapshot not found")
        matched_strat = next((s for s in run.applicable_strategies if s.strategy_id == request.strategy_id), None)
        if not matched_strat: raise HTTPException(status_code=400, detail="Specified strategy is not applicable to this run")
        custom = create_custom_scenario(matched_strat, defined_goal, request.scenario_name, request.assumptions, request.funding_structure)
        custom_scens = [s for s in run.scenarios if s.is_investor_modified] + [custom]
        financial_context = self._financial_context(request.planning_unit_id, defined_goal)
        result, _ = self._execute(defined_goal, run.investor_priorities, financial_context, custom_scens)
        new_run = StrategyRun(planning_unit_id=run.planning_unit_id, goal_id=run.goal_id, defined_goal_id=run.defined_goal_id, defined_goal_version=run.defined_goal_version, run_version=run.run_version + 1, is_latest=True, status="completed", applicable_strategies=result.applicable_strategies, scenarios=result.scenarios, investor_priorities=result.priorities, comparison_matrix=result.comparison_matrix, rankings=result.rankings, recommendation=result.recommendation, architectures=result.architectures, selected_strategy_id=run.selected_strategy_id, selected_scenario_id=run.selected_scenario_id, selected_strategy_version_id=run.selected_strategy_version_id, selected_strategy_version=run.selected_strategy_version, selected_implementation_parameters=run.selected_implementation_parameters, selected_architecture=run.selected_architecture, approval_status="selected" if run.selected_strategy_id else "not_selected", run_metadata={"trigger": "custom_scenario_added", "approval_invalidated": run.approval_status == "approved"})
        new_run.strategy_run_id = self.strat_repo.save_run(new_run)
        return new_run

    def update_priorities(self, request: PriorityWeightsRequest) -> StrategyRun:
        run = self.strat_repo.get_run_by_id(request.planning_unit_id, request.strategy_run_id)
        if not run: raise HTTPException(status_code=404, detail="Strategy run not found")
        defined_goal = self.goal_repo.get_defined_goal_by_version(request.planning_unit_id, run.goal_id, run.defined_goal_version)
        if not defined_goal: raise HTTPException(status_code=404, detail="Underlying DefinedGoal snapshot not found")
        custom_scens = [s for s in run.scenarios if s.is_investor_modified]
        financial_context = self._financial_context(request.planning_unit_id, defined_goal)
        result, _ = self._execute(defined_goal, request.priorities, financial_context, custom_scens)
        new_run = StrategyRun(planning_unit_id=run.planning_unit_id, goal_id=run.goal_id, defined_goal_id=run.defined_goal_id, defined_goal_version=run.defined_goal_version, run_version=run.run_version + 1, is_latest=True, status="completed", applicable_strategies=result.applicable_strategies, scenarios=result.scenarios, investor_priorities=result.priorities, comparison_matrix=result.comparison_matrix, rankings=result.rankings, recommendation=result.recommendation, architectures=result.architectures, selected_strategy_id=run.selected_strategy_id, selected_scenario_id=run.selected_scenario_id, selected_strategy_version_id=run.selected_strategy_version_id, selected_strategy_version=run.selected_strategy_version, selected_implementation_parameters=run.selected_implementation_parameters, selected_architecture=run.selected_architecture, approval_status="selected" if run.selected_strategy_id else "not_selected", run_metadata={"trigger": "priorities_updated", "approval_invalidated": run.approval_status == "approved"})
        new_run.strategy_run_id = self.strat_repo.save_run(new_run)
        return new_run

    def select_strategy(self, request: StrategySelectRequest) -> StrategyRun:
        run = self.strat_repo.get_run_by_id(request.planning_unit_id, request.strategy_run_id)
        if not run: raise HTTPException(status_code=404, detail="Strategy run not found")
        matched = next((s for s in run.applicable_strategies if s.strategy_id == request.selected_strategy_id), None)
        if not matched: raise HTTPException(status_code=400, detail=f"Selected strategy '{request.selected_strategy_id}' does not exist in this strategy run's applicable strategies.")
        scenario = next((s for s in run.scenarios if s.scenario_id == request.selected_scenario_id), None)
        if not scenario: raise HTTPException(status_code=400, detail=f"Selected scenario '{request.selected_scenario_id}' does not exist in this strategy run.")
        if scenario.strategy_id != request.selected_strategy_id: raise HTTPException(status_code=400, detail="Selected scenario does not match selected strategy.")
        architecture = next((a for a in run.architectures if a.architecture_id == request.selected_architecture_id), None) if request.selected_architecture_id else next((a for a in run.architectures if a.primary_strategy_id == request.selected_strategy_id), None)
        if architecture is None: raise HTTPException(status_code=400, detail="A valid strategy architecture is required for selection.")
        try: version = self.strategy_version_service.create_version(planning_unit_id=request.planning_unit_id, strategy_id=request.selected_strategy_id, parameters=request.selected_implementation_parameters, source="library", status="draft")
        except ValueError as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc
        self.strat_repo.update_selection(request.planning_unit_id, request.strategy_run_id, request.selected_strategy_id, request.selected_scenario_id, version.implementation_parameters, architecture, "selected", version.strategy_version_id, version.version)
        run.selected_strategy_id = request.selected_strategy_id; run.selected_scenario_id = request.selected_scenario_id; run.selected_strategy_version_id = version.strategy_version_id; run.selected_strategy_version = version.version; run.selected_implementation_parameters = version.implementation_parameters; run.selected_architecture = architecture; run.approval_status = "selected"
        return run

    def approve_strategy(self, request: StrategyApprovalRequest) -> StrategyRun:
        raise HTTPException(status_code=410, detail="Legacy approval flow retired. Use StrategyApprovalService through /api/strategy/approve.")

    def get_latest_run(self, planning_unit_id: str, goal_id: str) -> StrategyRun:
        run = self.strat_repo.get_latest_run(planning_unit_id, goal_id)
        if not run: raise HTTPException(status_code=404, detail="No strategy run found for this goal")
        return run

    def get_run_history(self, planning_unit_id: str, goal_id: str): return self.strat_repo.get_run_history(planning_unit_id, goal_id)

    def get_retirement_report(self, planning_unit_id: str, strategy_run_id: str):
        run = self.strat_repo.get_run_by_id(planning_unit_id, strategy_run_id)
        if not run: raise HTTPException(status_code=404, detail="Strategy run not found")
        defined_goal = self.goal_repo.get_defined_goal_by_version(planning_unit_id, run.goal_id, run.defined_goal_version)
        if not defined_goal: raise HTTPException(status_code=404, detail="Underlying DefinedGoal snapshot not found")
        financial_context = self._financial_context(planning_unit_id, defined_goal)
        assessment = self._rule_assessment(defined_goal, financial_context)
        report = self.report_renderer.render(defined_goal=defined_goal, financial_context=financial_context, rule_assessment=assessment, strategy_result=run)
        return report.as_dict()

    def on_defined_goal_updated(self, planning_unit_id: str, goal_id: str, new_defined_goal: DefinedGoal) -> None:
        prev = self.strat_repo.get_latest_run(planning_unit_id, goal_id)
        if not prev: return
        financial_context = self._financial_context(planning_unit_id, new_defined_goal)
        result, _ = self._execute(new_defined_goal, prev.investor_priorities, financial_context, [s for s in prev.scenarios if s.is_investor_modified])
        selected_arch = None
        if prev.selected_architecture: selected_arch = next((a for a in result.architectures if a.architecture_id == prev.selected_architecture.architecture_id), None)
        elif prev.selected_strategy_id: selected_arch = next((a for a in result.architectures if a.primary_strategy_id == prev.selected_strategy_id), None)
        selection_valid = selected_arch is not None and next((s for s in result.applicable_strategies if s.strategy_id == prev.selected_strategy_id), None) is not None and next((s for s in result.scenarios if s.scenario_id == prev.selected_scenario_id and s.strategy_id == prev.selected_strategy_id), None) is not None
        new_run = StrategyRun(planning_unit_id=planning_unit_id, goal_id=goal_id, defined_goal_id=new_defined_goal.defined_goal_id or "", defined_goal_version=new_defined_goal.version, run_version=prev.run_version + 1, is_latest=True, status="recalculated", applicable_strategies=result.applicable_strategies, scenarios=result.scenarios, investor_priorities=result.priorities, comparison_matrix=result.comparison_matrix, rankings=result.rankings, recommendation=result.recommendation, architectures=result.architectures, selected_strategy_id=prev.selected_strategy_id if selection_valid else None, selected_scenario_id=prev.selected_scenario_id if selection_valid else None, selected_strategy_version_id=prev.selected_strategy_version_id if selection_valid else None, selected_strategy_version=prev.selected_strategy_version if selection_valid else None, selected_implementation_parameters=prev.selected_implementation_parameters if selection_valid else {}, selected_architecture=selected_arch if selection_valid else None, selection_timestamp=prev.selection_timestamp if selection_valid else None, approval_status="selected" if selection_valid else "not_selected", run_metadata={"trigger": "automatic_recalculation", "triggered_by_defined_goal_version": new_defined_goal.version, "approval_invalidated": prev.approval_status == "approved"})
        self.strat_repo.save_run(new_run)
