# Goal Planner — Backend Evidence Index

**Repository:** `Bhardwaj1-star/planvesto`  
**Branch:** `main`  
**Audited source revision:** `5a3b060e1b27915ede226f5173364e23dca1263e`  
**Purpose:** Code-derived inventory and traceability for the Goal Planner backend.  
**Document status:** Initial source pass; not a redesign specification and not a claim that every repository dependency has been audited.

## Evidence rules

- The backend code at the source revision above is the evidence for implementation claims.
- File paths and line ranges below point to the audited revision, not to a future moving line number.
- “Implemented” means visible in the inspected source; it does not prove production deployment or live database contents.
- Existing feature documents and Real-Life Decision Cases are context only. They are not treated as proof of runtime behavior.
- The backend source exposes Supabase table names and queries. This audit did not inspect the live database schema or production rows.
- No application code was changed as part of this documentation pass.

## Component documents

| Document | Component | Main verified code positions |
|---|---|---|
| [01 — API and request boundary](01-API-AND-REQUEST-BOUNDARY.md) | Goal endpoints, auth and ownership checks | [api/goals.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/api/goals.py#L1-L57`) |
| [02 — Taxonomy and data contracts](02-TAXONOMY-AND-DATA-CONTRACTS.md) | Goal types, input schemas, DefinedGoal output | [rules/goals.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/rules/goals.py#L1-L99`), [schemas/goals.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/schemas/goals.py#L1-L62`), [models/defined_goal.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/models/defined_goal.py#L1-L80`) |
| [03 — Goal calculation engine](03-GOAL-CALCULATION-ENGINE.md) | Duration, target, retirement, generic goal calculation | [engines/goal/engine.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/goal/engine.py#L17-L173`) |
| [04 — Asset mapping and funding projections](04-ASSET-MAPPING-AND-FUNDING-PROJECTIONS.md) | Asset allocation, return defaults, funding gap and funding paths | [asset_projection.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/goal/asset_projection.py#L1-L74`), [funding_gap.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/goal/funding_gap.py#L1-L90`), [funding_strategies.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/engines/goal/funding_strategies.py#L1-L198`) |
| [05 — Feasibility and workflow readiness](05-FEASIBILITY-AND-WORKFLOW-READINESS.md) | Financial State prerequisite, surplus fit and status generation | [services/goal_service.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/services/goal_service.py#L83-L242`) |
| [06 — Persistence and versions](06-PERSISTENCE-AND-VERSIONING.md) | Supabase reads/writes, snapshots, material changes and version history | [data/goal_repository.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/data/goal_repository.py#L9-L94`), [services/goal_service.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/services/goal_service.py#L242-L333`) |
| [07 — Multi-goal planning boundary](07-MULTI-GOAL-PLANNING.md) | Shared-surplus planning, priorities, constraints and selected StrategyVersion dependency | [services/multi_goal_planning_service.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/services/multi_goal_planning_service.py#L18-L191`), [rules/multi_goal.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/rules/multi_goal.py#L1-L39`) |
| [08 — Tests and evidence gaps](08-TESTS-AND-EVIDENCE-GAPS.md) | Tests found, observed code boundaries, unresolved verification | [test_goal_calculations.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/tests/test_goal_calculations.py`), [test_goal_feasibility_prerequisites.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/tests/test_goal_feasibility_prerequisites.py`), [test_goal_funding_strategies.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/tests/test_goal_funding_strategies.py`), [test_multi_goal_planning_service.py](`https://github.com/Bhardwaj1-star/planvesto/blob/5a3b060e1b27915ede226f5173364e23dca1263e/backend/tests/test_multi_goal_planning_service.py`) |

## Runtime entry points

- `backend/main.py:4-5, 27-29` imports and registers the Goal and Goal Basket routers.
- `backend/api/goals.py:6-7` declares router prefix `/api/goals` and tag `Goal Planner & DefinedGoal`.
- `backend/api/goal_basket.py:7-8` declares router prefix `/api/goal-baskets`; basket preview is a separate endpoint and is documented only as an adjacent integration boundary, not silently merged into the defined-goal lifecycle.

## Observed high-level flow

```text
HTTP /api/goals
  -> authenticate + ownership checks
  -> GoalService
      -> retirement-context enrichment when relevant
      -> GoalRepository asset lookup
      -> GoalEngine.calculate_defined_goal
      -> FinancialStateService current family snapshot
      -> GoalService._apply_feasibility
      -> funding strategy evaluations
      -> (save endpoint) GoalRepository snapshot persistence
      -> on material update, StrategyService.on_defined_goal_updated attempt
  -> DefinedGoal response
```

The preview endpoint follows the calculation and feasibility path but does not call `save_defined_goal_snapshot` in its route/service path. The save endpoint persists a versioned snapshot.

## Explicitly outside this first pass

- Live Supabase table definitions, indexes, RLS policies and production rows were not inspected.
- Every caller elsewhere in the repository has not yet been exhaustively traced.
- Frontend field usage and UI behavior are not asserted here.
- This folder is a code inventory, not authorization to refactor or freeze business rules.
