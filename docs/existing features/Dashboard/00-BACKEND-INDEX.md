# Dashboard — Backend Evidence Index

**Branch:** `main` · **Audited baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`  
**Status:** Source inspection only; no tests run or production database queried.

## Component documents

| Document | Scope |
|---|---|
| [01 — Route, service and response flow](01-ROUTE-SERVICE-AND-RESPONSE.md) | Authenticated endpoint, service composition and output fields |
| [02 — Financial metrics and goal summaries](02-FINANCIAL-METRICS-AND-GOAL-SUMMARIES.md) | Metric provenance, availability and goal coverage derivation |
| [03 — UI, refresh and feature boundaries](03-UI-REFRESH-AND-INTEGRATIONS.md) | Dashboard page, API client, realtime helper and adjacent features |
| [04 — Tests and evidence gaps](04-TESTS-AND-EVIDENCE-GAPS.md) | Unverified calculations, scope and UI states |

## Runtime path

```text
/investor root -> /investor/financial-state
  -> frontend/lib/api/dashboard.ts
  -> GET /api/dashboard
  -> auth + planning-unit/scope validation
  -> DashboardService
     -> FinancialStateService.current()
     -> GoalRepository list/latest defined goal
  -> dashboard response
```

## Primary source paths

`frontend/app/investor/financial-state/page.tsx`, `frontend/lib/api/dashboard.ts`, `frontend/lib/dashboard/realtime.ts`, `backend/api/dashboard.py`, `backend/services/dashboard_service.py`, `backend/schemas/dashboard.py`, `backend/engines/financial_state/engine.py`.

The existing [implementation audit](00-IMPLEMENTATION-AUDIT.md) remains a short overview. This component set separates response assembly, metric meaning, presentation and verification. Dashboard is a presentation/aggregation surface; its response should not become an independent financial calculation authority.
