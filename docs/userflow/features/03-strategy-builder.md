# Strategy Builder

## 1. Feature Scope
Evaluates applicable strategies for a canonical DefinedGoal using current Financial State, investor priorities, risk/constraint evidence and strategy policy; compares alternatives; and creates the immutable StrategyVersion that becomes current only through explicit selection authority.

## 2. User / Request Inputs
POST /api/strategy/build:
- planning_unit_id
- goal_id
- optional investor_priorities

Investor priorities: safety, liquidity, growth, flexibility. Frontend currently sends equal 0.25 defaults when absent; service can reuse prior StrategyRun priorities, otherwise build fails.

Selection accepts planning_unit_id, strategy_run_id, selected strategy/scenario/architecture and implementation parameters. Preview/finalization require selected context plus exact DefinedGoal version.

## 3. Input Source / Authority Boundary
Consumes current DefinedGoal, current Financial State, investor priorities, Goal Rule Engine evidence, MoneyWheel constraints, Risk Profiler evidence, ConstraintAggregator output and canonical strategy library.

DefinedGoal supplies goal identity, target, duration, funding status/gap, required contribution, flexibility and priority. FinancialStateService remains Financial State authority. Investor priorities are decision preferences, not financial metrics.

## 4. Canonical Rules and Decision Logic
Eligibility uses filter_applicable_strategies() and remains pass / conditional / fail. These statuses are distinct from Goal Planner funding status and allocation funding statuses.

Decision evidence includes goal characteristics, horizon, funding status, flexibility, priority, liabilities, investor priorities, eligibility/feasibility, constraints, architecture/component fit and technique evidence. Scoring separates goal fit, horizon fit, funding fit, feasibility, component fit and technique execution. Current examples: pass=15, conditional=8, fail=0; failed eligibility receives infeasible score.

Applicable strategies can produce baseline, investor-modified/custom and what-if scenarios with assumptions, funding structure, metrics and trade-offs.

## 5. Lifecycle / State Transitions
Build StrategyRun → Select strategy/scenario/architecture → Implementation Preview → Finalize → Immutable StrategyVersion → Explicit current selection.

StrategyRun is evaluation/history. is_latest does not establish current authority. Finalization requires exact DefinedGoal version, selected strategy/scenario/architecture and implementation configuration.

## 6. Comparison / Recommendation Contract
Applicable Strategies → Scenarios → Comparison Matrix → Decision Evaluation → Rankings → Recommendation.

Ranking/recommendation are evaluation outputs only. Recommendation contains recommended IDs, reasons, architecture, alternatives, feasibility status and constraints.

## 7. Strategy Architecture
Canonical architecture identity = Goal ID + Primary Strategy ID. Supporting strategies, components and techniques are composition data and must not silently change architecture identity.

## 8. StrategyVersion Contract
Goal-bound StrategyVersion contains strategy_version_id, planning_unit_id, strategy_id, version, source, library_version, implementation_version, implementation_parameters, goal_id, defined_goal_id/version, architecture, decision_snapshot, source_strategy_run_id, status and created_at.

StrategyVersion is an immutable implementation snapshot. Investor edits use source=investor_edit and require parent_version.

## 9. Current Strategy Authority
Goal → goal_strategy_selections → StrategyVersion.

Current authority requires current DefinedGoal, same Goal, exact DefinedGoal binding, StrategyRun provenance, architecture, recommendation/strategy consistency and selected scenario/decision snapshot consistency. Latest StrategyRun/ranking/is_latest must never substitute for this authority.

## 10. Output Contract
Outputs: applicable strategies/eligibility, scenarios, comparison/ranking/recommendation, architecture, selected implementation context, immutable StrategyVersion and explicit current selection.

## 11. Ownership Boundary
- Strategy orchestration: evaluation flow
- StrategyVersion: immutable implementation configuration
- goal_strategy_selections: current strategy selection
- FinancialStateService: current Financial State
- Strategy rules: eligibility/decision policy

## 12. Downstream Dependencies
Current StrategyVersion feeds Action Plan, reports, multi-goal planning and execution. Revised DefinedGoal requires new strategy evaluation and StrategyVersion.

## 13. Versioning / Replanning Boundary
DefinedGoal v1 → StrategyVersion v1.
DefinedGoal v2 → new evaluation → StrategyVersion v2 → new selection.

A StrategyVersion bound to an old DefinedGoal version must not remain current.

## 14. Code Ownership
- API: backend/api/strategy.py, backend/api/strategy_version.py
- Schemas: backend/schemas/strategy.py
- Orchestration: backend/services/strategy_service.py
- StrategyVersion service: backend/services/strategy_version_service.py
- Engine: backend/engines/strategy/engine.py
- Eligibility: backend/engines/strategy/applicability.py
- Decision policy: backend/rules/strategy_decision.py
- Selection authority: backend/data/strategy_repository.py
- Model: backend/models/strategy_version.py
- Frontend: frontend/lib/api/strategy.ts

## 15. Regression Contract
Goal ownership/current DefinedGoal, current Financial State, pass/conditional/fail eligibility, distinct funding vocabulary, selection consistency, exact DefinedGoal version, stale-version rejection, architecture/provenance, immutability and current-selection correctness must remain enforced.

## 16. Known Implementation Gaps / Notes
1. Investor-priority fallback/default behavior must remain explicit.
2. StrategyRun remains evaluation provenance/history and must not become current authority.
3. Approval is a separate lifecycle boundary; recommendation/selection/finalization are not approval.
4. Goal revision must invalidate old current selection through exact DefinedGoal-version binding.

## 17. Important Boundaries
1. StrategyRun ≠ current strategy.
2. Recommendation ≠ approval.
3. Selection ≠ final implementation.
4. StrategyVersion ≠ StrategyRun.
5. Ranking ≠ authority.
6. Goal Planner ≠ Strategy Builder.
7. FinancialState ≠ strategy context.
8. Eligibility ≠ feasibility.

## 18. End-to-End Contract
Current DefinedGoal + Current Financial State + Investor Priorities → Rules/Constraints/Risk Evidence → Eligible Strategies → Scenarios → Comparison/Decision → Ranking/Recommendation → Architecture → User Selection → Implementation Preview → Finalization → Immutable StrategyVersion → goal_strategy_selections → Current Strategy Authority → Action Plan / Reports / Execution.

Scope: Strategy Builder only.