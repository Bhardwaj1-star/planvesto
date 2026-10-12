# Reports Center — Report Surfaces and Endpoint Contracts

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## UI options

`frontend/app/investor/reports/page.tsx` presents Complete Financial Plan, Goal Basket Decision Report, Individual Goal Report and Summary Planning Report. It loads goals from Goal Planner data, reads saved baskets from localStorage and checks selected Strategy Versions. UI availability depends on goals, basket selection and strategy-version presence.

A localStorage basket is a client-side selection, not proof of a persisted basket-level strategy run. The UI's “at least two goals” basket requirement is a front-end condition; backend validation must be checked separately.

## Backend report families

- Summary JSON/PDF: `backend/api/summary_report.py`, prefix `/api/summary-report`; ownership checked before service generation.
- Basket report/PDF: `backend/api/basket_report.py`, prefix `/api/basket-report`; accepts planning unit, basket name and goal IDs.
- Individual goal report: Goal-report routes/services use strategy-run or selected Strategy Version lineage; inspect the exact API module for version-specific route.
- Complete plan: Financial Plan service/API assembles a live consolidated output across goals without introducing a separate plan table in the service comment.
- PDF helpers are exposed through `frontend/lib/api/strategy.ts`.

## Preconditions and semantics

The UI requires a selected Strategy Version for an individual report and passes goal/version identifiers to goal-report navigation. Report generation should be grounded in the selected run/version; a goal alone is not enough to establish which strategy output is being reported.

## Important caveat

A report option displayed in the UI does not prove every backend precondition is met or every described section is available. Check request contract, service validation and actual schema before relying on UI copy.
