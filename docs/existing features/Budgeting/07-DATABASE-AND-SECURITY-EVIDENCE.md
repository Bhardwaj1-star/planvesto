# Budgeting — Database and Security Evidence

**Source revision:** `6d2fca0ac37d6dee32c0678047c1df46459b3298`

## 1. Budget limit table

The repository migration `frontend/supabase/migrations/016_budget_limits.sql` creates `public.budget_limits`, its unique category-per-planning-unit constraint, timestamps, and a foreign key to `planning_units` with cascade delete.

## 2. Initial row-level security policies

Migration 016 enables RLS and defines select, insert, update and delete policies based on whether the row's `planning_unit_id` belongs to a `planning_units` row whose `user_id = auth.uid()`.

The initial policy text does not explicitly include a `TO authenticated` role clause. Later migrations in the repository alter these policies.

## 3. Later hardening and reconciliation evidence

The source tree includes:
- `frontend/supabase/migrations/017_reconcile_post_hardening_rls.sql`
- `frontend/supabase/migrations/018_production_database_reconciliation.sql`
- `frontend/supabase/migrations/20261002202600_reconcile_budget_and_profile_rls.sql`

These files contain subsequent policy alterations for Budgeting's `budget_limits` table, including authenticated-role targeting and planning-unit ownership predicates. They are repository migration evidence only; this audit did not connect to the live database to establish which migrations have been applied, in what order, or whether production policies match the checked-in source.

## 4. Client-side access and trust boundary

The frontend queries Supabase directly. Reading `planning_unit_id` from localStorage selects a scope but does not authorize access. The database's effective RLS policy and authenticated session are essential to the security boundary.

The page/data layer does not call a Budgeting-specific backend route that performs the ownership checks visible in `backend/api/financial_state.py`. This difference should not be interpreted as a vulnerability without verifying the effective database policies and Supabase client/session configuration.

## 5. Unverified database facts

- Effective live RLS policy definitions and role grants.
- Migration application status and order in the target environment.
- Actual foreign keys, indexes, triggers and publication configuration in production.
- Whether realtime publication permissions and client subscriptions work for the authenticated user.
- Whether all source tables use equivalent ownership constraints.

No live database mutation or security test was performed.
