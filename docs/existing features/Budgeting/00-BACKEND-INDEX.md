# Budgeting — Implementation Evidence Index

**Repository:** `Bhardwaj1-star/planvesto`  
**Branch:** `main`  
**Audited source revision:** `6d2fca0ac37d6dee32c0678047c1df46459b3298`  
**Purpose:** Fresh, code-grounded inventory of the Budgeting feature across its frontend data layer, page, database migrations, and adjacent financial-state calculations.  
**Document status:** Initial source audit. This is not a redesign specification, and it does not claim that every caller or deployed database behavior has been verified.

## Evidence rules

- Implementation claims are based on source files at the audited revision, not on feature-description documents.
- “Implemented” means present in inspected source; it does not prove production deployment or live database state.
- Existing feature descriptions and decision-case documents were not treated as evidence of runtime behavior.
- The live Supabase schema, production rows, realtime delivery, and browser behavior were not independently queried or executed in this pass.
- No application code or decision logic was changed.

## Component documents

| Document | Scope |
|---|---|
| [01 — UI entry and data boundary](01-UI-AND-DATA-BOUNDARY.md) | Route, UI state, load/save/retry flow, realtime refresh |
| [02 — Data contracts and category taxonomy](02-DATA-CONTRACTS-AND-CATEGORY-TAXONOMY.md) | TypeScript shapes, Need/Want classification, category defaults |
| [03 — Monthly calculations and status rules](03-MONTHLY-CALCULATIONS-AND-STATUS-RULES.md) | Frequency normalization, aggregation, variance, savings target |
| [04 — Persistence and realtime behavior](04-PERSISTENCE-AND-REALTIME.md) | Budget-limit upsert, database table, RLS migration history, subscription |
| [05 — Source data and integration boundaries](05-SOURCE-DATA-AND-INTEGRATION-BOUNDARIES.md) | Income/expense/liability reads and relation to Financial State |
| [06 — UI behavior and user-visible states](06-UI-BEHAVIOR-AND-USER-VISIBLE-STATES.md) | Presentation behavior and controls actually found in page source |
| [07 — Database and security evidence](07-DATABASE-AND-SECURITY-EVIDENCE.md) | Table definition, ownership policies and later hardening migrations |
| [08 — Tests and evidence gaps](08-TESTS-AND-EVIDENCE-GAPS.md) | Test evidence status and unresolved verification questions |

## Verified runtime entry points

- Frontend route: `frontend/app/investor/budgeting/page.tsx`.
- Data access and calculation layer: `frontend/lib/api/budgeting.ts`.
- Persisted user-defined limits: `public.budget_limits`, introduced by `frontend/supabase/migrations/016_budget_limits.sql`.
- The page reads `income`, `expenses`, `liabilities`, and `budget_limits` directly through the frontend Supabase client. No dedicated Budgeting backend API route was found in the inspected implementation.
- The backend has a separate Financial State API and service. Similar metrics do not establish that Budgeting and Financial State use identical aggregation rules.

## Observed high-level flow

```text
/investor/budgeting
  -> loadBudgetData()
      -> read planning-unit ID from localStorage
      -> query income, expenses, liabilities, budget_limits in parallel
      -> normalize values to monthly amounts
      -> aggregate expense categories and liability EMIs
      -> apply stored/default Need-Want classification
      -> derive variance/status and overview totals
  -> render Budgeting UI
  -> (edit/save) saveBudgetLimits()
      -> upsert each category limit
  -> refresh data
  -> realtime events on source tables trigger a debounced refresh
```

## Scope boundaries for this pass

- No claim is made that the UI's savings target or desired-surplus controls are persisted; source shows these as local UI state.
- No claim is made that Budgeting's monthly surplus is the canonical surplus used by Goal Planner or Strategy Builder.
- No tests were executed during this documentation pass.
- Recommendations, redesign decisions, and code changes are intentionally outside this evidence inventory.
