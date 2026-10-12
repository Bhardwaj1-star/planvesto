# Action Plan — Persistence, UI and Integrations

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Persistence

`ActionPlanRepository` stores current action rows in `action_plan_items` and decisions in `action_decision_history`. It reads approval evidence from `strategy_approval_snapshots`. Listing is scoped by planning unit; optional strategy-version filters are applied server-side. Migration and live database policy state must be verified independently.

## UI

`frontend/app/investor/action-plan/page.tsx` loads goals, selected Strategy Versions and associated actions. It can honor `goalId` in the query string; otherwise it selects the first available goal. The page groups statuses for display (planned/confirmed are pending, completed is completed, cancelled is skipped). Frontend API helpers expose list, generation, create, completion and decision flows.

UI status grouping is presentation behavior, not a separate backend lifecycle. Browser behavior and every modal/preview path require independent testing.

## Integration boundaries

- Goal Planner: defines goal and funding/feasibility context.
- Strategy Builder: evaluates strategies/versions and selection.
- Approval snapshot: explicit prerequisite for implementation actions.
- Action Plan: records actions and their lifecycle.
- Financial State: authoritative current/actual state and snapshots.
- History/Diary: historical views; not execution authority.
- Reports: explain outcomes; not action state authority.

## Verification gaps

Check strategy-version replacement while actions are pending, ownership mismatch, repeated generation, delete retention, action ordering, query-param goal selection, status transitions, stale snapshots, completion preview fidelity and report/history consistency.
