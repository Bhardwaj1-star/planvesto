# Goal Planner — Multi-Goal Planning Integration

**Source revision:** `5a3b060e1b27915ede226f5173364e23dca1263e`

## 1. Scope boundary

This document records the backend multi-goal planning path that consumes goals, selected strategy versions, reports, financial state and canonical constraints. It is distinct from single-goal `GoalEngine.calculate_defined_goal`.

Main service: [backend/services/multi_goal_planning_service.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/services/multi_goal_planning_service.py#L18-L191`).

## 2. Build prerequisites and per-goal inputs

`build_multi_goal_plan`, lines 38–130:

1. Loads base goals from `GoalRepository.list_goals(planning_unit_id)`.
2. If there are no goals, raises HTTP 404.
3. For each goal, requires `StrategyRepository.get_selected_strategy_version_id`; if absent, raises HTTP 404 with a message requiring a finalized StrategyVersion.
4. Builds a goal report through `GoalReportService.build_report` using that selected strategy version.
5. Extracts calculation fields and recommendation fields from the report.
6. Resolves priority rank from explicit `goal_order`, then `priority_ranks`, then stored goal priority rank, then loop order.
7. Constructs `GoalEvaluationInput` with target date/year/month, today cost, future target, funding gap, required monthly contribution and flexibility.
8. Stores strategy identity/version, feasibility, funding, available surplus, funding solution and reason data in a per-goal lookup for the orchestrator.

This means the current multi-goal builder is not a standalone goal-only calculation: it requires each goal to have a selected StrategyVersion and consumes GoalReportService output.

## 3. Shared Financial State mapping

At lines 87–120, it reads current family Financial State and maps metrics into orchestration context:
- annual income and expenses;
- monthly investable surplus;
- total assets and liabilities;
- net worth;
- financial assets and liquid assets;
- essential monthly expenses;
- monthly debt payments / EMI burden.

The code accepts dict-like metric values or objects with a `value` attribute.

## 4. Constraint aggregation and orchestration

At lines 122–157:
- `ConstraintAggregator.aggregate` receives all goal inputs, financial context and planning unit ID.
- `suggested_overrides()` produces effective overrides; explicit `rule_overrides` update that map.
- `MultiGoalOrchestrator.orchestrate` receives goals, financial context, a strategy evaluator callback and effective overrides.
- Constraint warnings are appended to planning notes.
- Hard constraint messages are appended to trade-offs.
- A canonical constraint set, constraint/conflict counts and hard-failure count are attached to the audit trail.

The underlying `MultiGoalOrchestrator`, `GoalEvaluationInput`, `MultiGoalPlanResult`, `ConstraintAggregator` and constraint policy implementation are dependencies; they are not fully described by this file alone.

## 5. Priority and goal-type rules

Source: [backend/rules/multi_goal.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/rules/multi_goal.py#L1-L39`).

- Status vocabulary types include funding statuses `fully_funded`, `partially_funded`, `unfunded`, `within_surplus`, `surplus_shortfall`, `requires_review`; feasibility `pass`, `conditional`, `infeasible`.
- `get_priority_rank` passes integer values through, parses numeric strings, otherwise normalizes priority and looks up `PRIORITY_RANKS`; unknown values rank 999.
- `is_higher_priority` treats a smaller rank as higher precedence.
- `can_discretionary_preempt_essential` returns false when the first goal is discretionary and the second is essential; otherwise true. Goal type classes come from `rules.goals`.

The actual priority allocation order and resource allocation behavior are executed downstream by `MultiGoalOrchestrator` and associated engine modules, not solely by these helper functions.

## 6. Related but separate Goal Basket preview

`POST /api/goal-baskets/preview` uses `GoalBasketService` and `GoalBasketEngine` to validate that requested goal IDs exist in the planning unit and summarize their names, count, priorities, required monthly contribution and funding gap.

The basket engine reads the goal list and sums `required_monthly_contribution` and `funding_gap` when those keys are available, defaulting missing values to zero. The base `GoalRepository.list_goals` query shown selects only goal identity, target, priority and flexibility fields, so those funding totals can be zero when the supplied rows do not contain those keys. This behavior is visible in [backend/engines/basket/engine.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/basket/engine.py#L1-L40`) and [backend/data/goal_repository.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/data/goal_repository.py#L25-L31`); it is recorded as an integration observation, not changed here.
