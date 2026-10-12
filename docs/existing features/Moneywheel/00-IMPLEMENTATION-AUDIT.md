# Moneywheel — Implementation Audit

**Audited baseline:** `55d8b40235087b7c1f0052d4736303665fb5e41e`  
**Status:** Source inspection only; production state not independently verified. No application code changed.

## Source evidence
UI: `frontend/app/investor/moneywheel/page.tsx`; client: `frontend/lib/api/moneywheel.ts`; API/service: `backend/api/moneywheel.py`, `backend/services/moneywheel_service.py`; engine/rules: `backend/engines/moneywheel/engine.py`, `backend/rules/moneywheel.py`; repository/migration: `backend/data/moneywheel_repository.py`, `frontend/supabase/migrations/009_moneywheel.sql`.

## Calculation and ratio rules
The page loads current Financial State, requests calculation and history. The service describes Moneywheel as based on authoritative Financial State and source classifications. The rules module defines nine canonical ratio keys with formula descriptions, units and status bands: `excellent`, `healthy`, `attention`, `critical`. Unknown keys are rejected. The UI describes seven financial dimensions while counting nine available ratios; these are different presentation groupings.

## Inputs, persistence and decision boundary
The repository describes snapshots as append-only; client API exposes calculate/latest/history. Migration 009 defines snapshot persistence, an index by planning unit/calculation time and an ownership predicate. Production migration status and effective RLS were not queried.

Moneywheel is diagnostic evidence, not a final decision-maker. A ratio status or debt existence alone does not select Debt Reduction or Credit Utilisation. Goal Planner contextualizes goal funding; Strategy Builder evaluates candidate paths; Action Plan executes an accepted path. Refreshed ratios do not automatically replace an accepted plan. Proposed debt metrics must not be described as implemented without engine/rule evidence.

## Verification gaps
Repository search surfaced `backend/tests/test_moneywheel_service.py`; it was not run. Verify nine keys/formulas/units/thresholds, unknown keys, missing inputs/zero denominators, ownership, snapshot ordering/limits, production RLS, UI grouping, proposed metric implementation status and that diagnostics do not mutate selection/acceptance state.