from fastapi import HTTPException
from data.goal_repository import GoalRepository
from data.strategy_repository import StrategyRepository
from data.strategy_version_repository import StrategyVersionRepository
from engines.strategy.engine import StrategyEngine
from engines.strategy.scenario import create_custom_scenario
from models.defined_goal import DefinedGoal
from models.strategy import InvestorPriorities, Scenario, StrategyRun
from schemas.strategy import CustomScenarioRequest, PriorityWeightsRequest, StrategyBuildRequest, StrategySelectRequest
from services.strategy_version_service import StrategyVersionService


class StrategyService:
    def __init__(self):
        self.goal_repo = GoalRepository()
        self.strat_repo = StrategyRepository()
        self.engine = StrategyEngine()
        self.strategy_version_service = StrategyVersionService(
            StrategyVersionRepository(self.strat_repo.db)
        )

    def build_strategy(self, planning_unit_id: str, goal_id: str, priorities: InvestorPriorities | None = None) -> StrategyRun:
        defined_goal = self.goal_repo.get_latest_defined_goal(planning_unit_id, goal_id)
        if not defined_goal:
            raise HTTPException(status_code=404, detail="No DefinedGoal found for this goal. Please complete Goal Planning first.")
        prev_run = self.strat_repo.get_latest_run(planning_unit_id, goal_id)
        if priorities is None:
            if prev_run and prev_run.investor_priorities:
                priorities = prev_run.investor_priorities
            else:
                raise HTTPException(status_code=400, detail="Investor priorities must be provided before strategy comparison and ranking.")
        result = self.engine.execute(defined_goal=defined_goal, priorities=priorities)
        run_version = (prev_run.run_version + 1) if prev_run else 1
        run = StrategyRun(
            planning_unit_id=planning_unit_id, goal_id=goal_id,
            defined_goal_id=defined_goal.defined_goal_id or "", defined_goal_version=defined_goal.version,
            run_version=run_version, is_latest=True, status="completed",
            applicable_strategies=result.applicable_strategies, scenarios=result.scenarios,
            investor_priorities=result.priorities, comparison_matrix=result.comparison_matrix,
            rankings=result.rankings, recommendation=result.recommendation,
            run_metadata={"trigger": "manual_build"},
        )
        run.strategy_run_id = self.strat_repo.save_run(run)
        return run

    def add_custom_scenario(self, request: CustomScenarioRequest) -> StrategyRun:
        run = self.strat_repo.get_run_by_id(request.planning_unit_id, request.strategy_run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Strategy run not found")
        defined_goal = self.goal_repo.get_defined_goal_by_version(request.planning_unit_id, run.goal_id, run.defined_goal_version)
        if not defined_goal:
            raise HTTPException(status_code=404, detail="Underlying DefinedGoal snapshot not found")
        matched_strat = next((s for s in run.applicable_strategies if s.strategy_id == request.strategy_id), None)
        if not matched_strat:
            raise HTTPException(status_code=400, detail="Specified strategy is not applicable to this run")
        custom_scen = create_custom_scenario(strategy=matched_strat, defined_goal=defined_goal, custom_name=request.scenario_name, custom_assumptions=request.assumptions, custom_funding=request.funding_structure)
        existing_customs = [s for s in run.scenarios if s.is_investor_modified]
        existing_customs.append(custom_scen)
        result = self.engine.execute(defined_goal=defined_goal, priorities=run.investor_priorities, custom_scenarios=existing_customs)
        new_run = StrategyRun(
            planning_unit_id=run.planning_unit_id, goal_id=run.goal_id,
            defined_goal_id=run.defined_goal_id, defined_goal_version=run.defined_goal_version,
            run_version=run.run_version + 1, is_latest=True, status="completed",
            applicable_strategies=result.applicable_strategies, scenarios=result.scenarios,
            investor_priorities=result.priorities, comparison_matrix=result.comparison_matrix,
            rankings=result.rankings, recommendation=result.recommendation,
            selected_strategy_id=run.selected_strategy_id, selected_scenario_id=run.selected_scenario_id,
            selected_strategy_version_id=run.selected_strategy_version_id,
            selected_strategy_version=run.selected_strategy_version,
            selected_implementation_parameters=run.selected_implementation_parameters,
            run_metadata={"trigger": "custom_scenario_added"},
        )
        new_run.strategy_run_id = self.strat_repo.save_run(new_run)
        return new_run

    def update_priorities(self, request: PriorityWeightsRequest) -> StrategyRun:
        run = self.strat_repo.get_run_by_id(request.planning_unit_id, request.strategy_run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Strategy run not found")
        defined_goal = self.goal_repo.get_defined_goal_by_version(request.planning_unit_id, run.goal_id, run.defined_goal_version)
        if not defined_goal:
            raise HTTPException(status_code=404, detail="Underlying DefinedGoal snapshot not found")
        custom_scens = [s for s in run.scenarios if s.is_investor_modified]
        result = self.engine.execute(defined_goal=defined_goal, priorities=request.priorities, custom_scenarios=custom_scens)
        new_run = StrategyRun(
            planning_unit_id=run.planning_unit_id, goal_id=run.goal_id,
            defined_goal_id=run.defined_goal_id, defined_goal_version=run.defined_goal_version,
            run_version=run.run_version + 1, is_latest=True, status="completed",
            applicable_strategies=result.applicable_strategies, scenarios=result.scenarios,
            investor_priorities=result.priorities, comparison_matrix=result.comparison_matrix,
            rankings=result.rankings, recommendation=result.recommendation,
            selected_strategy_id=run.selected_strategy_id, selected_scenario_id=run.selected_scenario_id,
            selected_strategy_version_id=run.selected_strategy_version_id,
            selected_strategy_version=run.selected_strategy_version,
            selected_implementation_parameters=run.selected_implementation_parameters,
            run_metadata={"trigger": "priorities_updated"},
        )
        new_run.strategy_run_id = self.strat_repo.save_run(new_run)
        return new_run

    def select_strategy(self, request: StrategySelectRequest) -> StrategyRun:
        run = self.strat_repo.get_run_by_id(request.planning_unit_id, request.strategy_run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Strategy run not found")
        matched_strat = next((s for s in run.applicable_strategies if s.strategy_id == request.selected_strategy_id), None)
        if not matched_strat:
            raise HTTPException(status_code=400, detail=f"Selected strategy '{request.selected_strategy_id}' does not exist in this strategy run's applicable strategies.")
        matched_scen = next((sc for sc in run.scenarios if sc.scenario_id == request.selected_scenario_id), None)
        if not matched_scen:
            raise HTTPException(status_code=400, detail=f"Selected scenario '{request.selected_scenario_id}' does not exist in this strategy run.")
        if matched_scen.strategy_id != request.selected_strategy_id:
            raise HTTPException(status_code=400, detail=f"Selected scenario '{request.selected_scenario_id}' belongs to strategy '{matched_scen.strategy_id}', which does not match selected strategy '{request.selected_strategy_id}'.")

        try:
            version = self.strategy_version_service.create_version(
                planning_unit_id=request.planning_unit_id,
                strategy_id=request.selected_strategy_id,
                parameters=request.selected_implementation_parameters,
                source="library",
                status="draft",
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        self.strat_repo.update_selection(
            planning_unit_id=request.planning_unit_id, strategy_run_id=request.strategy_run_id,
            selected_strategy_id=request.selected_strategy_id, selected_scenario_id=request.selected_scenario_id,
            selected_params=version.implementation_parameters,
            selected_strategy_version_id=version.strategy_version_id or "",
            selected_strategy_version=version.version,
        )
        run.selected_strategy_id = request.selected_strategy_id
        run.selected_scenario_id = request.selected_scenario_id
        run.selected_strategy_version_id = version.strategy_version_id
        run.selected_strategy_version = version.version
        run.selected_implementation_parameters = version.implementation_parameters
        return run

    def get_latest_run(self, planning_unit_id: str, goal_id: str) -> StrategyRun:
        run = self.strat_repo.get_latest_run(planning_unit_id, goal_id)
        if not run:
            raise HTTPException(status_code=404, detail="No strategy run found for this goal")
        return run

    def get_run_history(self, planning_unit_id: str, goal_id: str):
        return self.strat_repo.get_run_history(planning_unit_id, goal_id)

    def on_defined_goal_updated(self, planning_unit_id: str, goal_id: str, new_defined_goal: DefinedGoal) -> None:
        prev_run = self.strat_repo.get_latest_run(planning_unit_id, goal_id)
        if not prev_run:
            return
        priorities = prev_run.investor_priorities
        custom_scens = [s for s in prev_run.scenarios if s.is_investor_modified]
        result = self.engine.execute(defined_goal=new_defined_goal, priorities=priorities, custom_scenarios=custom_scens)
        sel_strat_id = sel_scen_id = None
        sel_params = {}
        sel_timestamp = None
        if prev_run.selected_strategy_id and prev_run.selected_scenario_id:
            strat_match = next((s for s in result.applicable_strategies if s.strategy_id == prev_run.selected_strategy_id), None)
            scen_match = next((sc for sc in result.scenarios if sc.scenario_id == prev_run.selected_scenario_id), None)
            if strat_match and scen_match and scen_match.strategy_id == prev_run.selected_strategy_id:
                sel_strat_id, sel_scen_id = prev_run.selected_strategy_id, prev_run.selected_scenario_id
                sel_params, sel_timestamp = prev_run.selected_implementation_parameters or {}, prev_run.selection_timestamp
        new_run = StrategyRun(
            planning_unit_id=planning_unit_id, goal_id=goal_id,
            defined_goal_id=new_defined_goal.defined_goal_id or "", defined_goal_version=new_defined_goal.version,
            run_version=prev_run.run_version + 1, is_latest=True, status="recalculated",
            applicable_strategies=result.applicable_strategies, scenarios=result.scenarios,
            investor_priorities=result.priorities, comparison_matrix=result.comparison_matrix,
            rankings=result.rankings, recommendation=result.recommendation,
            selected_strategy_id=sel_strat_id, selected_scenario_id=sel_scen_id,
            selected_strategy_version_id=prev_run.selected_strategy_version_id if sel_strat_id else None,
            selected_strategy_version=prev_run.selected_strategy_version if sel_strat_id else None,
            selected_implementation_parameters=sel_params, selection_timestamp=sel_timestamp,
            run_metadata={"trigger": "automatic_recalculation", "triggered_by_defined_goal_version": new_defined_goal.version},
        )
        self.strat_repo.save_run(new_run)
