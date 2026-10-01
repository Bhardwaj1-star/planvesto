from fastapi import HTTPException
from data.goal_repository import GoalRepository
from data.strategy_repository import StrategyRepository
from data.strategy_version_repository import StrategyVersionRepository
from data.financial_state_repository import FinancialStateSnapshotRepository
from engines.strategy.engine import StrategyEngine
from engines.strategy.scenario import create_custom_scenario
from engines.rules.engine import RuleEngine
from models.defined_goal import DefinedGoal
from models.strategy import InvestorPriorities, StrategyRun
from schemas.strategy import CustomScenarioRequest, PriorityWeightsRequest, StrategyBuildRequest, StrategySelectRequest
from services.strategy_version_service import StrategyVersionService
from services.retirement_report_renderer import RetirementReportRenderer
from engines.constraints.aggregator import ConstraintAggregator
from engines.constraints.models import ConstraintSet
from engines.risk_profiler.engine import RiskProfilerEngine
from engines.orchestration.models import GoalEvaluationInput
from engines.moneywheel.engine import MoneywheelEngine
from models.moneywheel import MoneywheelInput


class StrategyService:
    def __init__(self):
        self.goal_repo = GoalRepository()
        self.strat_repo = StrategyRepository()
        self.financial_state_repo = FinancialStateSnapshotRepository()
        self.engine = StrategyEngine()
        self.rule_engine = RuleEngine()
        self.constraint_aggregator = ConstraintAggregator()
        self.strategy_version_service = StrategyVersionService(StrategyVersionRepository(self.strat_repo.db))
        self.report_renderer = RetirementReportRenderer()

    @staticmethod
    def _metric_value(state: dict, key: str):
        value = state.get(key)
        if isinstance(value, dict): return value.get("value")
        if hasattr(value, "value"): return value.value
        return value

    def _financial_context(self, planning_unit_id: str, defined_goal: DefinedGoal) -> dict:
        snapshot = self.financial_state_repo.get_latest(planning_unit_id, "family")
        if not snapshot or not snapshot.get("financial_state"): return {}
        state = snapshot["financial_state"]
        if hasattr(state, "model_dump"): state = state.model_dump()
        elif not isinstance(state, dict): return {}
        context = dict(state)
        income_annual = self._metric_value(state, "income_annual")
        expenses_annual = self._metric_value(state, "expenses_annual")
        surplus_monthly = self._metric_value(state, "investable_surplus_monthly")
        assets = self._metric_value(state, "total_assets")
        liabilities = self._metric_value(state, "total_liabilities")
        net_worth = self._metric_value(state, "net_worth")
        context.update({"annual_income": income_annual, "income": income_annual, "annual_expenses": expenses_annual, "expenses": expenses_annual, "monthly_surplus": surplus_monthly, "surplus": surplus_monthly, "financial_assets": assets, "assets": assets, "liabilities": liabilities, "net_worth": net_worth, "retirement_assets": getattr(defined_goal, "projected_mapped_asset_value", 0.0)})
        return context

    def _rule_assessment(self, defined_goal: DefinedGoal, financial_context: dict):
        return self.rule_engine.assess(defined_goal, financial_context)

    def _build_constraint_set(
        self,
        rule_assessment,
        financial_context: dict,
        planning_unit_id: str,
        defined_goal: DefinedGoal | None = None,
    ) -> ConstraintSet:
        """Build the authoritative canonical ConstraintSet consumed by StrategyEngine.

        Domain ownership remains decentralized:
        - RuleEngine -> goal diagnostics / hard goal gates
        - MoneyWheel ratio evaluator -> financial-state constraints
        - RiskProfilerEngine -> risk-capacity / risk-required / risk-tolerance constraints

        The aggregator is the only normalization boundary downstream engines consume.
        """
        goal_inputs: list[GoalEvaluationInput] = []
        if defined_goal is not None:
            goal_inputs.append(
                GoalEvaluationInput(
                    goal_id=defined_goal.goal_id,
                    goal_name=defined_goal.goal_name,
                    goal_type=defined_goal.goal_type,
                    client_priority=defined_goal.priority,
                    target_month=defined_goal.target_month,
                    target_year=defined_goal.target_year,
                    today_cost=defined_goal.today_cost,
                    future_target=defined_goal.future_target,
                    funding_gap=defined_goal.funding_gap,
                    required_monthly_contribution=defined_goal.required_monthly_contribution,
                    flexibility=defined_goal.flexibility,
                    defined_goal=defined_goal,
                )
            )

        # Build RiskProfile from the same authoritative financial-state snapshot.
        # No risk rule is invented here; RiskProfilerEngine owns the assessment.
        risk_state = dict(financial_context or {})
        income_monthly = self._metric_value(risk_state, "income_monthly")
        if income_monthly is None:
            annual_income = self._metric_value(risk_state, "annual_income")
            if annual_income is not None:
                risk_state["income_monthly"] = annual_income / 12.0
        if self._metric_value(risk_state, "investable_surplus_monthly") is None:
            surplus = self._metric_value(risk_state, "monthly_surplus")
            if surplus is not None:
                risk_state["investable_surplus_monthly"] = surplus
        if self._metric_value(risk_state, "emi_burden_monthly") is None:
            emi = self._metric_value(risk_state, "monthly_debt_payments")
            if emi is not None:
                risk_state["emi_burden_monthly"] = emi

        assets = self.goal_repo.get_planning_unit_assets(planning_unit_id)
        liabilities_total = self._metric_value(financial_context, "liabilities")
        liabilities = []
        if liabilities_total is not None and liabilities_total > 0:
            liabilities = [{"value": liabilities_total, "outstanding": liabilities_total}]

        risk_goals = [
            {
                "goal_id": g.goal_id,
                "goal_name": g.goal_name,
                "goal_type": g.goal_type,
                "future_target": g.future_target,
                "current_funding": g.projected_mapped_asset_value,
                "time_horizon_years": g.duration_years,
            }
            for g in ([defined_goal] if defined_goal is not None else [])
        ]
        risk_profile = RiskProfilerEngine().build(
            financial_state=risk_state,
            assets=assets,
            liabilities=liabilities,
            goals=risk_goals,
        )

        # MoneyWheel remains the authoritative financial-state diagnostic engine.
        # Missing optional inputs stay missing; this layer does not invent them.
        moneywheel_result = None
        if defined_goal is not None:
            moneywheel_input = MoneywheelInput(
                planning_unit_id=planning_unit_id,
                gross_monthly_income=self._metric_value(financial_context, "annual_income") / 12.0
                if self._metric_value(financial_context, "annual_income") is not None
                else self._metric_value(financial_context, "monthly_income"),
                monthly_surplus=self._metric_value(financial_context, "monthly_surplus"),
                monthly_expenses=self._metric_value(financial_context, "annual_expenses") / 12.0
                if self._metric_value(financial_context, "annual_expenses") is not None
                else self._metric_value(financial_context, "monthly_expenses"),
                essential_monthly_expenses=self._metric_value(financial_context, "essential_monthly_expenses"),
                liquid_assets=self._metric_value(financial_context, "liquid_assets"),
                monthly_debt_payments=self._metric_value(financial_context, "monthly_debt_payments"),
                total_assets=self._metric_value(financial_context, "assets"),
                total_liabilities=self._metric_value(financial_context, "liabilities"),
                financial_assets=self._metric_value(financial_context, "financial_assets"),
                current_goal_funding=defined_goal.projected_mapped_asset_value,
                goal_target_amount=defined_goal.future_target,
                projected_goal_funding=defined_goal.projected_mapped_asset_value,
                future_goal_target=defined_goal.future_target,
                goal_duration_years=defined_goal.duration_years,
            )
            moneywheel_result = MoneywheelEngine().build(moneywheel_input)

        return self.constraint_aggregator.aggregate(
            rule_assessment=rule_assessment,
            goals=goal_inputs,
            financial_context=financial_context,
            moneywheel_result=moneywheel_result,
            risk_profile_constraints=risk_profile.constraints,
            planning_unit_id=planning_unit_id,
        )

    def _execute(self, defined_goal: DefinedGoal, priorities: InvestorPriorities, financial_context: dict, custom_scenarios=None, planning_unit_id: str = ""):
        rule_assessment = self._rule_assessment(defined_goal, financial_context)
        constraint_set = self._build_constraint_set(rule_assessment, financial_context, planning_unit_id, defined_goal)
        if constraint_set.has_hard_failures:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Goal failed hard planning constraints.",
                    "constraints": [c.model_dump() for c in constraint_set.hard_constraints],
                },
            )
        return self.engine.execute(
            defined_goal=defined_goal,
            priorities=priorities,
            custom_scenarios=custom_scenarios,
            financial_context=financial_context,
            rule_assessment=rule_assessment,
            constraint_set=constraint_set,
        ), rule_assessment, constraint_set

    def build_strategy(self, planning_unit_id: str, goal_id: str, priorities: InvestorPriorities | None = None) -> StrategyRun:
        defined_goal = self.goal_repo.get_latest_defined_goal(planning_unit_id, goal_id)
        if not defined_goal: raise HTTPException(status_code=404, detail="No DefinedGoal found for this goal. Please complete Goal Planning first.")
        prev_run = self.strat_repo.get_latest_run(planning_unit_id, goal_id)
        if priorities is None: priorities = prev_run.investor_priorities if prev_run else None
        if priorities is None: raise HTTPException(status_code=400, detail="Investor priorities must be provided before strategy comparison and ranking.")
        financial_context = self._financial_context(planning_unit_id, defined_goal)
        result, rule_assessment, constraint_set = self._execute(defined_goal, priorities, financial_context, planning_unit_id=planning_unit_id)
        run = StrategyRun(planning_unit_id=planning_unit_id, goal_id=goal_id, defined_goal_id=defined_goal.defined_goal_id or "", defined_goal_version=defined_goal.version, run_version=(prev_run.run_version + 1) if prev_run else 1, is_latest=True, status="completed", applicable_strategies=result.applicable_strategies, scenarios=result.scenarios, investor_priorities=result.priorities, comparison_matrix=result.comparison_matrix, rankings=result.rankings, recommendation=result.recommendation, architectures=result.architectures, run_metadata={"trigger": "manual_build", "financial_state_context_available": bool(financial_context), "rule_assessment": {"eligible": rule_assessment.eligible, "diagnostics": [r.__dict__ for r in rule_assessment.diagnostics], "hard_constraints": [r.__dict__ for r in rule_assessment.hard_constraints], "soft_constraints": [r.__dict__ for r in rule_assessment.soft_constraints], "canonical_constraint_set": constraint_set.model_dump()}})
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
        result, _, _cs = self._execute(defined_goal, run.investor_priorities, financial_context, custom_scens, planning_unit_id=request.planning_unit_id)
        new_run = StrategyRun(planning_unit_id=run.planning_unit_id, goal_id=run.goal_id, defined_goal_id=run.defined_goal_id, defined_goal_version=run.defined_goal_version, run_version=run.run_version + 1, is_latest=True, status="completed", applicable_strategies=result.applicable_strategies, scenarios=result.scenarios, investor_priorities=result.priorities, comparison_matrix=result.comparison_matrix, rankings=result.rankings, recommendation=result.recommendation, architectures=result.architectures, selected_strategy_id=run.selected_strategy_id, selected_scenario_id=run.selected_scenario_id, selected_strategy_version_id=run.selected_strategy_version_id, selected_strategy_version=run.selected_strategy_version, selected_implementation_parameters=run.selected_implementation_parameters, selected_architecture=run.selected_architecture, run_metadata={"trigger": "custom_scenario_added"})
        new_run.strategy_run_id = self.strat_repo.save_run(new_run)
        return new_run

    def update_priorities(self, request: PriorityWeightsRequest) -> StrategyRun:
        run = self.strat_repo.get_run_by_id(request.planning_unit_id, request.strategy_run_id)
        if not run: raise HTTPException(status_code=404, detail="Strategy run not found")
        defined_goal = self.goal_repo.get_defined_goal_by_version(request.planning_unit_id, run.goal_id, run.defined_goal_version)
        if not defined_goal: raise HTTPException(status_code=404, detail="Underlying DefinedGoal snapshot not found")
        custom_scens = [s for s in run.scenarios if s.is_investor_modified]
        financial_context = self._financial_context(request.planning_unit_id, defined_goal)
        result, _, _cs = self._execute(defined_goal, request.priorities, financial_context, custom_scens, planning_unit_id=request.planning_unit_id)
        new_run = StrategyRun(planning_unit_id=run.planning_unit_id, goal_id=run.goal_id, defined_goal_id=run.defined_goal_id, defined_goal_version=run.defined_goal_version, run_version=run.run_version + 1, is_latest=True, status="completed", applicable_strategies=result.applicable_strategies, scenarios=result.scenarios, investor_priorities=result.priorities, comparison_matrix=result.comparison_matrix, rankings=result.rankings, recommendation=result.recommendation, architectures=result.architectures, selected_strategy_id=run.selected_strategy_id, selected_scenario_id=run.selected_scenario_id, selected_strategy_version_id=run.selected_strategy_version_id, selected_strategy_version=run.selected_strategy_version, selected_implementation_parameters=run.selected_implementation_parameters, selected_architecture=run.selected_architecture, run_metadata={"trigger": "priorities_updated"})
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
        self.strat_repo.update_selection(request.planning_unit_id, request.strategy_run_id, request.selected_strategy_id, request.selected_scenario_id, version.implementation_parameters, architecture, version.strategy_version_id, version.version)
        run.selected_strategy_id = request.selected_strategy_id; run.selected_scenario_id = request.selected_scenario_id; run.selected_strategy_version_id = version.strategy_version_id; run.selected_strategy_version = version.version; run.selected_implementation_parameters = version.implementation_parameters; run.selected_architecture = architecture
        return run

    def get_latest_run(self, planning_unit_id: str, goal_id: str) -> StrategyRun:
        run = self.strat_repo.get_latest_run(planning_unit_id, goal_id)
        if not run: raise HTTPException(status_code=404, detail="No strategy run found for this goal")
        return run

    def get_run_history(self, planning_unit_id: str, goal_id: str): return self.strat_repo.get_run_history(planning_unit_id, goal_id)

    def get_retirement_report(self, planning_unit_id: str, strategy_run_id: str):
        run = self.strat_repo.get_run_by_id(planning_unit_id, strategy_run_id)
        if not run: raise HTTPException(status_code=404, detail="Strategy run not found")
        defined_goal = self.goal_repo.get_defined_goal_by_version(planning_unit_id, run.goal_id, run.defined_goal_version) or self.goal_repo.get_latest_defined_goal(planning_unit_id, run.goal_id)
        if not defined_goal: raise HTTPException(status_code=404, detail="Underlying DefinedGoal snapshot not found")
        financial_context = self._financial_context(planning_unit_id, defined_goal)
        assessment = self._rule_assessment(defined_goal, financial_context)
        return self.report_renderer.render(defined_goal=defined_goal, financial_context=financial_context, rule_assessment=assessment, strategy_result=run).as_dict()

    def on_defined_goal_updated(self, planning_unit_id: str, goal_id: str, new_defined_goal: DefinedGoal) -> None:
        prev = self.strat_repo.get_latest_run(planning_unit_id, goal_id)
        if not prev: return
        financial_context = self._financial_context(planning_unit_id, new_defined_goal)
        result, _, _cs = self._execute(new_defined_goal, prev.investor_priorities, financial_context, [s for s in prev.scenarios if s.is_investor_modified], planning_unit_id=planning_unit_id)
        selected_arch = None
        if prev.selected_architecture: selected_arch = next((a for a in result.architectures if a.architecture_id == prev.selected_architecture.architecture_id), None)
        elif prev.selected_strategy_id: selected_arch = next((a for a in result.architectures if a.primary_strategy_id == prev.selected_strategy_id), None)
        selection_valid = selected_arch is not None and next((s for s in result.applicable_strategies if s.strategy_id == prev.selected_strategy_id), None) is not None and next((s for s in result.scenarios if s.scenario_id == prev.selected_scenario_id and s.strategy_id == prev.selected_strategy_id), None) is not None
        new_run = StrategyRun(planning_unit_id=planning_unit_id, goal_id=goal_id, defined_goal_id=new_defined_goal.defined_goal_id or "", defined_goal_version=new_defined_goal.version, run_version=prev.run_version + 1, is_latest=True, status="recalculated", applicable_strategies=result.applicable_strategies, scenarios=result.scenarios, investor_priorities=result.priorities, comparison_matrix=result.comparison_matrix, rankings=result.rankings, recommendation=result.recommendation, architectures=result.architectures, selected_strategy_id=prev.selected_strategy_id if selection_valid else None, selected_scenario_id=prev.selected_scenario_id if selection_valid else None, selected_strategy_version_id=prev.selected_strategy_version_id if selection_valid else None, selected_strategy_version=prev.selected_strategy_version if selection_valid else None, selected_implementation_parameters=prev.selected_implementation_parameters if selection_valid else {}, selected_architecture=selected_arch if selection_valid else None, selection_timestamp=prev.selection_timestamp if selection_valid else None, run_metadata={"trigger": "automatic_recalculation", "triggered_by_defined_goal_version": new_defined_goal.version})
        self.strat_repo.save_run(new_run)
