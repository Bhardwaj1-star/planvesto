# Dashboard — UI, Refresh and Integration Boundaries

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## UI and client

The investor root redirects to `/investor/financial-state`; the page imports `frontend/lib/api/dashboard.ts` and renders financial metrics and goal summaries. The client uses the centralized API client. The realtime helper is `frontend/lib/dashboard/realtime.ts`; the audit does not establish that every underlying table/event is covered by realtime refresh.

## Neighboring features

- Dashboard: concise current-state overview.
- Budgeting: its own monthly category aggregation and budget-limit behavior.
- Financial State: authoritative normalized metrics and snapshots.
- Goal Planner: goal definition, calculation and funding/feasibility.
- Moneywheel: diagnostic ratios.
- Reports Center: formatted decision outputs.

Do not reconcile or merge these outputs solely because labels overlap. Reconciliation requires same scope (family/individual), source, categories, period, units, rounding and timestamp.

## Verification gaps

Confirm loading/empty/error states in browser; scope and investor selection; goal-card fallback when no latest DefinedGoal exists; canceled-goal behavior; coverage calculation boundaries; realtime subscription event coverage and cleanup; latest snapshot ordering and timestamps; and numerical comparison with Budgeting. No test or production behavior is claimed as verified here.
