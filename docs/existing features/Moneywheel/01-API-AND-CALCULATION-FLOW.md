# Moneywheel — API and Calculation Flow

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002` · Source inspection only.

## API boundary

Router: `backend/api/moneywheel.py`, prefix `/api/moneywheel`. The route authenticates the caller and verifies planning-unit ownership before calculating or reading stored snapshots. The calculate request includes `planning_unit_id`; the request schema retains `financial_state_snapshot` for compatibility, but the API deliberately ignores that client-supplied snapshot and rebuilds input from server-owned Financial State. This prevents a caller's submitted numbers from becoming calculation authority.

The route family exposes calculation plus latest/history retrieval. Frontend helpers in `frontend/lib/api/moneywheel.ts` call:
- `POST /api/moneywheel/calculate`
- `GET /api/moneywheel/latest/{planning_unit_id}`
- `GET /api/moneywheel/history/{planning_unit_id}`

Confirm exact status/error behavior against the current router before changing clients; this document does not claim live deployment.

## Service and input assembly

`MoneywheelService` coordinates Financial State, goal-derived inputs, the adapter, engine and repository. `MoneywheelFinancialStateAdapter` maps FinancialState fields such as monthly income/surplus, expenses, liquid assets, debt payments, assets, liabilities, financial assets and insurance sum assured into `MoneywheelInput`.

Goal-dependent inputs are separate from the Financial State adapter: current funding, goal target, projected funding, future target and duration require goal context. Do not assume all nine ratios can be calculated from Financial State alone.

## Engine

`MoneywheelEngine.build()` creates the canonical nine ratio results using canonical calculation functions in `engines/calculation/canonical.py`, then attaches rule-set version, calculation time and metadata. Missing numerator/denominator or a zero denominator produces an unavailable result with a reason. Non-finite outputs are also unavailable. A result can therefore be partially available rather than fabricated as a complete score.

## Ownership and responsibility

Moneywheel reports metrics; it does not infer investor acceptance or select a strategy. Goal Planner owns goal funding/feasibility; Strategy Builder evaluates candidate strategies; Action Plan tracks implementation. A ratio may inform a decision, but the ratio status alone is not a decision rule for changing an accepted plan.
