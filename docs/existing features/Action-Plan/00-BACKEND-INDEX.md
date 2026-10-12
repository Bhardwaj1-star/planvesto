# Action Plan — Backend Evidence Index

**Branch:** `main` · **Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`  
**Status:** Source inspection only; no tests run or production database queried.

## Component documents

| Document | Scope |
|---|---|
| [01 — API, models and action generation](01-API-MODELS-AND-GENERATION.md) | Routes, approval gate, request/response contracts |
| [02 — Lifecycle, decisions and impact comparison](02-LIFECYCLE-DECISIONS-AND-IMPACT.md) | State transitions, actual Financial State and variance |
| [03 — Persistence, UI and integration boundaries](03-PERSISTENCE-UI-AND-INTEGRATIONS.md) | Repository tables, page behavior and authority |
| [04 — Tests and evidence gaps](04-TESTS-AND-EVIDENCE-GAPS.md) | Lifecycle and partial-failure verification |

## Runtime path

```text
/investor/action-plan
  -> frontend/lib/api/action-plan.ts
  -> /api/action-plan
  -> auth + ownership/version checks
  -> ActionPlanService / StrategyActionGenerator
  -> action_plan_items + action_decision_history
  -> on actual completion: Financial State snapshot + variance analysis
```

## Primary sources

`frontend/app/investor/action-plan/page.tsx`, `frontend/lib/api/action-plan.ts`, `backend/api/action_plan.py`, `backend/services/action_plan_service.py`, `backend/services/strategy_action_generator.py`, `backend/data/action_plan_repository.py`, `backend/models/action_plan.py`, `backend/schemas/action_plan.py`, `backend/rules/action_plan.py`, `backend/engines/action_plan/impact_engine.py`.

Action Plan is execution tracking for an approved Strategy Version; a generated/planned action is not itself investor acceptance of the strategy. Component-specific evidence and verification gaps are documented in the files above.