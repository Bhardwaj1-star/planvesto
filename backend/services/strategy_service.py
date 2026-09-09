from fastapi import HTTPException
from data.goal_repository import GoalRepository
from data.strategy_repository import StrategyRepository
from engines.strategy.engine import StrategyEngine
from engines.strategy.scenario import create_custom_scenario
from models.defined_goal import DefinedGoal
from models.strategy import (
    InvestorPriorities,
    Scenario,
    StrategyRun,
)
from schemas.strategy import (
    CustomScenarioRequest,
    PriorityWeightsRequest,
    StrategyBuildRequest,
    StrategySelectRequest,
)


class StrategyService:
    def __init__(self):
        self.goal_repo = GoalRepository()
        self.strat_repo = StrategyRepository()
        self.engine = StrategyEngine()

    def build_strategy(
        self,
        planning_unit_id: str,
        goal_id: str,
        priorities: InvestorPriorities | None = None,
    ) -> StrategyRun:
        defined_goal = self.goal_repo.get_latest_defined_goal(planning_unit_id, goal_id)
        if not defined_goal:
            raise HTTPException(
                status_code=404,
                detail="No DefinedGoal found for this goal. Please complete Goal Planning first.",
            )

        if priorities is None:
            # Check if previous run had priorities
            prev_run = self.strat_repo.get_latest_run(planning_unit_id, goal_id)
            if prev_run:
                priorities = prev_run.investor_priorities
            else:
                priorities = InvestorPriorities()

        result = self.engine.execute(
            defined_goal=defined_goal,
            priorities=priorities,
        )

        prev_run = self.strat_repo.get_latest_run(planning_unit_id, goal_id)
        run_version = (prev_run.run_version + 1) if prev_run else 1

        run = StrategyRun(
            planning_unit_id=planning_unit_id,
            goal_id=goal_id,
            defined_goal_id=defined_goal.defined_goal_id or "",
            defined_goal_version=defined_goal.version,
            run_version=run_version,
            is_latest=True,
            status="completed",
            applicable_strategies=result.applicable_strategies,
            scenarios=result.scenarios,
            investor_priorities=result.priorities,
            comparison_matrix=result.comparison_matrix,
            rankings=result.rankings,
            recommendation=result.recommendation,
            run_metadata={"trigger": "manual_build"},
        )

        run_id = self.strat_repo.save_run(run)
        run.strategy_run_id = run_id
        return run

    def add_custom_scenario(self, request: CustomScenarioRequest) -> StrategyRun:
        run = self.strat_repo.get_run_by_id(request.planning_unit_id, request.strategy_run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Strategy run not found")

        defined_goal = self.goal_repo.get_defined_goal_by_version(
            request.planning_unit_id, run.goal_id, run.defined_goal_version
        )
        if not defined_goal:
            raise HTTPException(status_code=404, detail="Underlying DefinedGoal snapshot not found")

        matched_strat = next((s for s in run.applicable_strategies if s.strategy_id == request.strategy_id), None)
        if not matched_strat:
            raise HTTPException(status_code=400, detail="Specified strategy is not applicable to this run")

        custom_scen = create_custom_scenario(
            strategy=matched_strat,
            defined_goal=defined_goal,
            custom_name=request.scenario_name,
            custom_assumptions=request.assumptions,
            custom_funding=request.funding_structure,
        )

        existing_customs = [s for s in run.scenarios if s.is_investor_modified]
        existing_customs.append(custom_scen)

        # Re-execute engine with all customs
        result = self.engine.execute(
            defined_goal=defined_goal,
            priorities=run.investor_priorities,
            custom_scenarios=existing_customs,
        )

        new_run = StrategyRun(
            planning_unit_id=run.planning_unit_id,
            goal_id=run.goal_id,
            defined_goal_id=run.defined_goal_id,
            defined_goal_version=run.defined_goal_version,
            run_version=run.run_version + 1,
            is_latest=True,
            status="completed",
            applicable_strategies=result.applicable_strategies,
            scenarios=result.scenarios,
            investor_priorities=result.priorities,
            comparison_matrix=result.comparison_matrix,
            rankings=result.rankings,
            recommendation=result.recommendation,
            selected_strategy_id=run.selected_strategy_id,
            selected_scenario_id=run.selected_scenario_id,
            selected_implementation_parameters=run.selected_implementation_parameters,
            run_metadata={"trigger": "custom_scenario_added"},
        )

        run_id = self.strat_repo.save_run(new_run)
        new_run.strategy_run_id = run_id
        return new_run

    def update_priorities(self, request: PriorityWeightsRequest) -> StrategyRun:
        run = self.strat_repo.get_run_by_id(request.planning_unit_id, request.strategy_run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Strategy run not found")

        defined_goal = self.goal_repo.get_defined_goal_by_version(
            request.planning_unit_id, run.goal_id, run.defined_goal_version
        )
        if not defined_goal:
            raise HTTPException(status_code=404, detail="Underlying DefinedGoal snapshot not found")

        custom_scens = [s for s in run.scenarios if s.is_investor_modified]
        result = self.engine.execute(
            defined_goal=defined_goal,
            priorities=request.priorities,
            custom_scenarios=custom_scens,
        )

        new_run = StrategyRun(
            planning_unit_id=run.planning_unit_id,
            goal_id=run.goal_id,
            defined_goal_id=run.defined_goal_id,
            defined_goal_version=run.defined_goal_version,
            run_version=run.run_version + 1,
            is_latest=True,
            status="completed",
            applicable_strategies=result.applicable_strategies,
            scenarios=result.scenarios,
            investor_priorities=result.priorities,
            comparison_matrix=result.comparison_matrix,
            rankings=result.rankings,
            recommendation=result.recommendation,
            selected_strategy_id=run.selected_strategy_id,
            selected_scenario_id=run.selected_scenario_id,
            selected_implementation_parameters=run.selected_implementation_parameters,
            run_metadata={"trigger": "priorities_updated"},
        )

        run_id = self.strat_repo.save_run(new_run)
        new_run.strategy_run_id = run_id
        return new_run

    def select_strategy(self, request: StrategySelectRequest) -> StrategyRun:
        run = self.strat_repo.get_run_by_id(request.planning_unit_id, request.strategy_run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Strategy run not found")

        # Validate selection matches an existing scenario
        matched_scen = next((sc for sc in run.scenarios if sc.scenario_id == request.selected_scenario_id), None)
        if not matched_scen:
            raise HTTPException(status_code=400, detail="Selected scenario not found in this strategy run")

        self.strat_repo.update_selection(
            planning_unit_id=request.planning_unit_id,
            strategy_run_id=request.strategy_run_id,
            selected_strategy_id=request.selected_strategy_id,
            selected_scenario_id=request.selected_scenario_id,
            selected_params=request.selected_implementation_parameters,
        )

        run.selected_strategy_id = request.selected_strategy_id
        run.selected_scenario_id = request.selected_scenario_id
        run.selected_implementation_parameters = request.selected_implementation_parameters
        return run

    def get_latest_run(self, planning_unit_id: str, goal_id: str) -> StrategyRun:
        run = self.strat_repo.get_latest_run(planning_unit_id, goal_id)
        if not run:
            raise HTTPException(status_code=404, detail="No strategy run found for this goal")
        return run

    def get_run_history(self, planning_unit_id: str, goal_id: str):
        return self.strat_repo.get_run_history(planning_unit_id, goal_id)

    def on_defined_goal_updated(
        self,
        planning_unit_id: str,
        goal_id: str,
        new_defined_goal: DefinedGoal,
    ) -> None:
        """
        Automatic Recalculation Trigger:
        When a new DefinedGoal version is created due to material goal changes,
        automatically recalculate the Strategy Run while preserving history.
        """
        prev_run = self.strat_repo.get_latest_run(planning_unit_id, goal_id)
        if not prev_run:
            return  # No run existed yet, nothing to recalculate

        priorities = prev_run.investor_priorities
        custom_scens = [s for s in prev_run.scenarios if s.is_investor_modified]

        result = self.engine.execute(
            defined_goal=new_defined_goal,
            priorities=priorities,
            custom_scenarios=custom_scens,
        )

        new_run = StrategyRun(
            planning_unit_id=planning_unit_id,
            goal_id=goal_id,
            defined_goal_id=new_defined_goal.defined_goal_id or "",
            defined_goal_version=new_defined_goal.version,
            run_version=prev_run.run_version + 1,
            is_latest=True,
            status="recalculated",
            applicable_strategies=result.applicable_strategies,
            scenarios=result.scenarios,
            investor_priorities=result.priorities,
            comparison_matrix=result.comparison_matrix,
            rankings=result.rankings,
            recommendation=result.recommendation,
            selected_strategy_id=prev_run.selected_strategy_id,
            selected_scenario_id=prev_run.selected_scenario_id,
            selected_implementation_parameters=prev_run.selected_implementation_parameters,
            run_metadata={
                "trigger": "automatic_recalculation",
                "triggered_by_defined_goal_version": new_defined_goal.version,
            },
        )
        self.strat_repo.save_run(new_run)
