# Moneywheel — Backend Evidence Index

**Repository:** `Bhardwaj1-star/planvesto` · **Branch:** `main`  
**Audited baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`  
**Purpose:** Code-derived map of Moneywheel's current calculation, API, persistence and UI boundaries. Source inspection only; no tests run and no production database state verified.

## Component documents

| Document | Responsibility |
|---|---|
| [01 — API and calculation flow](01-API-AND-CALCULATION-FLOW.md) | Authenticated endpoints, server-owned Financial State, service orchestration |
| [02 — Ratio contracts and classification rules](02-RATIO-CONTRACTS-AND-RULES.md) | Nine ratio keys, formulas, availability and status bands |
| [03 — Persistence, UI and integration boundaries](03-PERSISTENCE-UI-AND-INTEGRATIONS.md) | Snapshot history, frontend groupings, Goal Planner/Action Plan boundary |
| [04 — Tests and evidence gaps](04-TESTS-AND-EVIDENCE-GAPS.md) | Existing test files and unverified behavior |

## Runtime path

```text
Moneywheel page
  -> frontend/lib/api/moneywheel.ts
  -> authenticated /api/moneywheel endpoints
  -> MoneywheelService
  -> current Financial State + GoalRepository context
  -> FinancialStateAdapter -> MoneywheelInput
  -> MoneywheelEngine + rules/moneywheel.py
  -> append-only moneywheel_snapshots
  -> latest/history responses
```

## Evidence rules

- Source files establish the inspected implementation; names or UI copy alone do not.
- A successful calculation response does not prove production migration/RLS state.
- Missing inputs or zero denominators must remain unavailable; they are not evidence of a healthy ratio.
- Moneywheel is diagnostic output. It does not choose a strategy, approve a plan or mark an action accepted.
- The existing [implementation audit](00-IMPLEMENTATION-AUDIT.md) is retained as a concise overview; the linked documents break its claims into component boundaries.

## Main source paths

`backend/api/moneywheel.py`, `backend/services/moneywheel_service.py`, `backend/engines/moneywheel/engine.py`, `backend/engines/moneywheel/financial_state_adapter.py`, `backend/rules/moneywheel.py`, `backend/models/moneywheel.py`, `backend/data/moneywheel_repository.py`, `frontend/app/investor/moneywheel/page.tsx`, `frontend/lib/api/moneywheel.ts`, `frontend/supabase/migrations/009_moneywheel.sql`.
