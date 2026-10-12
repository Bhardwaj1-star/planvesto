# Dashboard — Route, Service and Response Flow

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## API contract

`backend/api/dashboard.py` registers `GET /api/dashboard`. Required query: `planning_unit_id`; `scope` defaults to `family`; `investor_id` is optional but valid only for individual scope. The route authenticates, verifies planning-unit ownership, rejects scopes other than `family` or `individual`, requires investor ID for individual scope, validates investor ownership, and rejects investor ID for family scope.

## Service composition

`DashboardService.build()` obtains current Financial State via `FinancialStateService.current(planning_unit_id, scope, investor_id)`. It exposes a deliberate subset of state fields rather than serializing every engine field. It then uses `GoalRepository.list_goals()` and each goal's latest DefinedGoal snapshot to assemble goal cards.

Cancelled defined goals are excluded from the active dashboard list. If a goal summary has no resolvable latest DefinedGoal, the service emits a fallback summary using available row fields and leaves funding-derived fields null. This fallback is not evidence that the goal has completed feasibility processing.

## Response shape

`backend/schemas/dashboard.py` defines `DashboardResponse` with planning unit, scope, financial-state dictionary and list of `DashboardGoal` records. Goal fields include target amount/date, priority/flexibility, funding status/gap, projected mapped asset value, coverage percentage and image key.

## Boundaries

The endpoint assembles current data; it does not itself persist a new Financial State snapshot in the shown service path. Snapshot creation and freshness are owned by Financial State flows. Same-named dashboard metrics should not be assumed equal to Budgeting metrics without matching source rows, categories, period conversion, scope and timestamp.
