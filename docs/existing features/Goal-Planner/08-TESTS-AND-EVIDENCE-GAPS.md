# Goal Planner — Test Evidence and Open Verification Gaps

**Source revision:** `5a3b060e1b27915ede226f5173364e23dca1263e`

## 1. Test files found and inspected

| Test file | Evidence area | Verified examples |
|---|---|---|
| [test_goal_calculations.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/tests/test_goal_calculations.py`) | GoalEngine calculations and input validation | Target-date goal calculation, retirement corpus calculation, percentage allocation >100 rejection, expected-return bounds |
| [test_goal_feasibility_prerequisites.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/tests/test_goal_feasibility_prerequisites.py`) | Financial State prerequisite and feasibility status | Missing snapshot/surplus stays unknown; missing income/expenses are surfaced; sufficient surplus is feasible; positive insufficient surplus constrained; zero surplus with a gap infeasible; latest read refreshes feasibility |
| [test_goal_funding_strategies.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/tests/test_goal_funding_strategies.py`) | Funding-path generation | Core path IDs, SIP fit, existing-assets case, constrained SIP gap/trade-offs |
| [test_multi_goal_planning_service.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/tests/test_multi_goal_planning_service.py`) | Multi-goal aggregation | Shared-surplus shortfall, priority-ranked allocation, required selected strategy version |

The tests were inspected as source, not executed during this documentation pass.

## 2. Runtime facts with direct source evidence

- Goal API routes and ownership-check calls are in `backend/api/goals.py`.
- Goal calculation and retirement branch are in `backend/engines/goal/engine.py`.
- Financial-surplus feasibility is in `backend/services/goal_service.py::_apply_feasibility`.
- Snapshot and mapping persistence are in `backend/data/goal_repository.py`.
- Multi-goal orchestration requires a selected StrategyVersion for every goal in `backend/services/multi_goal_planning_service.py`.

## 3. Specific gaps that remain unverified

These are evidence boundaries, not recommendations.

1. **Live database schema:** Python references table and column names, but the actual deployed Supabase schema, migrations, indexes, foreign keys and RLS policies were not inspected.
2. **Full dependency closure:** The calculation imports `engines.calculation.canonical` and `rules.assumptions`; multi-goal flow imports orchestration and constraints modules. This document references them but does not yet trace every function in those dependencies.
3. **Specialized-target reachability:** `backend/engines/goal/specialized.py::calculate_specialized_target` exists, but the inspected `GoalEngine.calculate_defined_goal` does not call it. All repository callers have not yet been exhaustively searched.
4. **Version-change comparisons:** `has_material_change` compares cost, target month/year, mapping allocation type/value and dynamic details; the service separately checks status, priority and flexibility. Effects of changes to inflation rate, mapped asset expected return/frequency and priority rank need call-path/test verification.
5. **Mapping persistence and latest marker:** Source updates the prior latest flag before inserting the new snapshot, then inserts mapping rows in a separate operation. Transaction/rollback guarantees were not verified in the inspected Python.
6. **Goal Basket fields:** Basket summary expects optional funding values on goal-list rows, while the repository list query selects a narrower set of columns. The resulting live API output should be verified against actual DB/API behavior.
7. **Strategy update side effects:** `GoalService` catches exceptions from `StrategyService.on_defined_goal_updated` after saving a material new version. Downstream implementation was not traced here.
8. **Tests not run:** Test source assertions are evidence of intended coverage, not evidence that tests currently pass.

## 4. No inferred redesign decisions

This document does not choose which existing implementation to replace, merge or remove. The purpose of this feature folder is to preserve code-grounded facts and identify unverified edges so later cross-feature comparison can use evidence instead of assumptions.
