# Dashboard — Implementation Audit

**Audited baseline:** `55d8b40235087b7c1f0052d4736303665fb5e41e`  
**Status:** Source inspection only; production state not independently verified. No application code changed.

## Source evidence
- UI: `frontend/app/investor/financial-state/page.tsx`
- Client: `frontend/lib/api/dashboard.ts`
- API/engine: `backend/api/financial_state.py`, `backend/engines/financial_state/engine.py`
- Refresh helper: `frontend/lib/dashboard/realtime.ts`

## UI and data flow
The investor root redirects to `/investor/financial-state`. The page calls `getDashboard()` and renders net worth, assets/liabilities, cash flow and goals. The client uses the centralized API client, unlike Budgeting's direct Supabase aggregation.

The authenticated Financial State API provides build, latest-snapshot and history endpoints. It validates planning-unit ownership and investor ownership for individual scope. The engine computes income/expenses, surplus, assets, liabilities, EMI burden, net worth and insurance metrics. Metric availability is represented explicitly; surplus is only computed when income and expenses are available.

## Ownership and boundaries
Dashboard presentation is not itself the calculation authority. Budgeting separately aggregates cash flow and liability EMIs; Moneywheel derives diagnostic ratios; Goal Planner computes goal-specific funding. Same-name metrics are not proven numerically equivalent without matching scope, source rows, frequency conversion, categories, rounding and timestamps. A snapshot response does not prove recomputation on every render.

## Verification gaps
No tests were run. Verify exact `getDashboard()` route/service mapping; family/individual scope; missing versus zero metrics; ownership percentages and unclassified asset types; realtime event coverage and cleanup; reconciliation against Budgeting; snapshot ordering/timestamps; and browser behavior for empty goals/API failures. These are open questions, not confirmed defects.