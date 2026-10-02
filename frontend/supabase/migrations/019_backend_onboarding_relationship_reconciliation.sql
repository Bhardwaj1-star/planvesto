-- 019_backend_onboarding_relationship_reconciliation.sql
-- Canonical DB hardening derived from backend repositories/models and onboarding persistence.
-- No application data is deleted or rewritten.

begin;

-- 1. FinancialState snapshot -> Investor
-- Individual snapshots already require investor_id; enforce that the investor exists.
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'financial_state_snapshots_investor_id_fkey'
      and conrelid = 'public.financial_state_snapshots'::regclass
  ) then
    alter table public.financial_state_snapshots
      add constraint financial_state_snapshots_investor_id_fkey
      foreign key (investor_id)
      references public.investors(investor_id)
      on delete set null;
  end if;
end $$;

create index if not exists idx_financial_state_snapshots_investor
  on public.financial_state_snapshots (investor_id, calculated_at desc);

-- 2. Profile run -> Investor
-- profile_runs are versioned investor-profile snapshots and must belong to a real investor.
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'profile_runs_investor_id_fkey'
      and conrelid = 'public.profile_runs'::regclass
  ) then
    alter table public.profile_runs
      add constraint profile_runs_investor_id_fkey
      foreign key (investor_id)
      references public.investors(investor_id)
      on delete cascade;
  end if;
end $$;

create index if not exists idx_profile_runs_investor
  on public.profile_runs (investor_id, created_at desc);

-- 3. Strategy version parent lineage
-- parent_version is scoped by planning_unit + strategy_id, so enforce that scope.
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'strategy_versions_parent_version_fkey'
      and conrelid = 'public.strategy_versions'::regclass
  ) then
    alter table public.strategy_versions
      add constraint strategy_versions_parent_version_fkey
      foreign key (planning_unit_id, strategy_id, parent_version)
      references public.strategy_versions(planning_unit_id, strategy_id, version)
      on delete restrict;
  end if;
end $$;

-- 4. Primary strategy current-state previous version lineage.
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'primary_strategy_state_previous_version_fkey'
      and conrelid = 'public.primary_strategy_state'::regclass
  ) then
    alter table public.primary_strategy_state
      add constraint primary_strategy_state_previous_version_fkey
      foreign key (previous_strategy_version_id)
      references public.strategy_versions(strategy_version_id)
      on delete set null;
  end if;
end $$;

create index if not exists idx_primary_strategy_state_previous_version
  on public.primary_strategy_state (previous_strategy_version_id);

-- 5. Primary strategy transition previous version lineage.
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'primary_strategy_transitions_previous_version_fkey'
      and conrelid = 'public.primary_strategy_transitions'::regclass
  ) then
    alter table public.primary_strategy_transitions
      add constraint primary_strategy_transitions_previous_version_fkey
      foreign key (previous_strategy_version_id)
      references public.strategy_versions(strategy_version_id)
      on delete set null;
  end if;
end $$;

create index if not exists idx_primary_strategy_transitions_previous_version
  on public.primary_strategy_transitions (previous_strategy_version_id);

commit;
