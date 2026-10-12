# Moneywheel — Persistence, UI and Integrations

**Baseline:** `d7640029310c8e58d4cdd9a033d7683b5ea10002`.

## Snapshot persistence

`backend/data/moneywheel_repository.py` writes to `moneywheel_snapshots` with planning-unit ID, rule-set version, overall status, ratio payloads, the Financial State snapshot, calculation time and metadata. Repository intent is append-only; it exposes latest and bounded history reads ordered by `calculated_at` descending. Transient connection exceptions are retried in the repository wrapper; this is transport retry behavior, not a business recalculation rule.

Migration `frontend/supabase/migrations/009_moneywheel.sql` defines the table/index/ownership predicate in source. Production migration application and effective RLS were not queried, so do not claim production security state from the migration file alone.

## UI behavior

`frontend/app/investor/moneywheel/page.tsx` obtains planning-unit and latest Financial State context, requests calculation, loads history and renders status-coded ratio cards. Seven display categories map onto the nine canonical keys; a category may contain more than one ratio. Unavailable values display as “Not available”. The UI's grouping and styling do not define calculations or thresholds.

Client helper: `frontend/lib/api/moneywheel.ts`. The helper passes a Financial State snapshot argument for backward compatibility; the backend request route rebuilds its inputs from authoritative server-side data.

## Cross-feature boundaries

- Financial State is the source of current financial metrics.
- Goal Planner provides goal-specific funding context.
- Moneywheel provides diagnostic ratios and snapshots.
- Strategy Builder evaluates strategy paths; a Moneywheel status is not strategy selection.
- Action Plan records execution and actual-state impact; recalculating Moneywheel does not complete an action or update acceptance state.
- Reports may consume Moneywheel snapshots as diagnostic observations, but report presentation is not a second calculation authority.

## Not established

The inspected code does not establish that every ratio is always available, that every UI category has a one-to-one metric, that a refresh mutates accepted-plan state, or that production RLS matches the migration. These require separate verification.
