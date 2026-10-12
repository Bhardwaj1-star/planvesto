# Reports Center — Implementation Audit

**Audited baseline:** `55d8b40235087b7c1f0052d4736303665fb5e41e`  
**Status:** Source inspection only; production state not independently verified. No application code changed.

## Source evidence
UI: `frontend/app/investor/reports/page.tsx`; client helpers: `frontend/lib/api/strategy.ts`; services surfaced by repository search: `backend/services/goal_report_service.py`, `backend/services/basket_report_service.py`, `backend/services/financial_plan_service.py`.

## Options and UI flow
The page at `/investor/reports` loads goals through `loadGoalPlannerData()`, reads saved planning baskets from localStorage and checks the selected strategy version. It presents Complete Financial Plan, Goal Basket Decision Report (UI requires at least two goals), Individual Goal Report (requires selected Strategy Version) and Summary Planning Report. Individual report navigation passes goal and strategy-version IDs to `/investor/goal-report`. API helpers expose PDF downloads for goal strategy, complete plan, basket and summary reports. A basket in localStorage is not proof of a persisted basket-level strategy run.

## Generation and data authority
The UI delegates PDF downloads to backend API helpers. GoalReportService, BasketReportService and FinancialPlanService are present; the latter composes goal, strategy and multi-goal services. The backend planning-system flow says reports consume canonical outputs and export layers are presentation adapters, not independent business-logic authorities. UI descriptions about trade-offs, shared allocation or health scans must be checked against actual service/schema before assuming all fields are present.

## Verification gaps
Repository search surfaced goal-report, basket-report and retirement PDF tests, but none were run. Verify availability against backend requirements, selected-version lineage, basket validation, PDF errors/empty states, schema/data freshness, web/PDF parity, formatting and summary use of canonical Financial State/Moneywheel outputs. Confirm exact renderer path before edits.