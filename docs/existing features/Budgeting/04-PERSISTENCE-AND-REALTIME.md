# Budgeting — Persistence and Realtime Behavior

**Source revision:** `6d2fca0ac37d6dee32c0678047c1df46459b3298`

## 1. Persisted data

Source: [`frontend/supabase/migrations/016_budget_limits.sql`](https://github.com/Bhardwaj1-star/planvesto/blob/main/frontend/supabase/migrations/016_budget_limits.sql)

The migration creates `public.budget_limits` with:

| Column | Definition |
|---|---|
| `budget_limit_id` | UUID primary key, default `gen_random_uuid()` |
| `planning_unit_id` | Required UUID FK to `planning_units`, delete cascade |
| `category` | Required text |
| `classification` | Required text, default `Need`, check limited to Need/Want |
| `budget_monthly` | Required numeric, default 0 |
| `created_at`, `updated_at` | Required timestamps, default now() |

A unique constraint enforces one row per `planning_unit_id, category`.

## 2. Upsert path

`saveBudgetLimits()` iterates through each supplied item and upserts its planning-unit ID, category, classification, monthly amount, and a client-generated `updated_at`. Conflict resolution uses `planning_unit_id,category`.

- Each item is a separate awaited database operation.
- The function throws when an individual upsert returns an error.
- No all-items transaction is visible in this client function.
- A failure after earlier items have succeeded could leave a partially updated set; this is a code-path risk, not a claim that a partial write occurred in production.

## 3. Realtime refresh

`subscribeToBudgetChanges()` creates a channel named `budgeting:<planningUnitId>` and subscribes to all Postgres change events for each of:

- `income`
- `expenses`
- `liabilities`
- `budget_limits`

Each event schedules `onChange` after a 350 ms debounce; a later event clears the prior timer. Cleanup clears the timer and removes the Supabase channel.

The inspected code does not check or surface the return status of `channel.subscribe()`; successful realtime delivery was not tested.

## 4. Schema-missing fallback

During loading, every error from the `budget_limits` query is treated as if no limit rows exist. This can allow the page to render derived categories without stored limits, but can also mask errors other than a missing table. The UI does not distinguish these cases in the inspected data-layer path.

## 5. What was not proven

- No write was made to a live database as part of this audit.
- No concurrent edits, duplicate conflict, partial failure, realtime event, or cleanup scenario was executed.
- Database transaction guarantees beyond the individual Supabase calls were not verified.
