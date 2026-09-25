create table if not exists public.profile_runs (
  profile_run_id uuid primary key default gen_random_uuid(),
  planning_unit_id uuid not null references public.planning_units(planning_unit_id) on delete cascade,
  investor_id uuid not null,
  version integer not null check (version > 0),
  engine_version text not null,
  profile_version text not null,
  financial_snapshot_id uuid null references public.financial_state_snapshots(snapshot_id),
  input_snapshot jsonb not null default '{}'::jsonb,
  profile_result jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique (planning_unit_id, investor_id, version)
);

create index if not exists idx_profile_runs_owner_version on public.profile_runs (planning_unit_id, investor_id, version desc);

create table if not exists public.profile_constraints (
  profile_constraint_id uuid primary key default gen_random_uuid(),
  profile_run_id uuid not null references public.profile_runs(profile_run_id) on delete cascade,
  key text not null,
  value jsonb not null,
  unit text null,
  kind text not null check (kind in ('hard', 'soft')),
  source text not null check (source in ('financial_state', 'observed_behavior', 'declared_constraint', 'preference')),
  evidence jsonb not null default '[]'::jsonb,
  confidence numeric(5,4) not null check (confidence >= 0 and confidence <= 1),
  priority_rank integer null check (priority_rank is null or priority_rank > 0),
  valid_from timestamptz null,
  valid_until timestamptz null,
  created_at timestamptz not null default now()
);

create index if not exists idx_profile_constraints_run on public.profile_constraints(profile_run_id);

create table if not exists public.profile_conflicts (
  profile_conflict_id uuid primary key default gen_random_uuid(),
  profile_run_id uuid not null references public.profile_runs(profile_run_id) on delete cascade,
  key text not null,
  status text not null check (status in ('unresolved', 'resolved')),
  reason text not null,
  sources jsonb not null default '[]'::jsonb,
  hard_constraint_present boolean not null default false,
  created_at timestamptz not null default now()
);

create index if not exists idx_profile_conflicts_run on public.profile_conflicts(profile_run_id);

alter table public.profile_runs enable row level security;
alter table public.profile_constraints enable row level security;
alter table public.profile_conflicts enable row level security;

drop policy if exists "profile_runs_select_own" on public.profile_runs;
drop policy if exists "profile_runs_insert_own" on public.profile_runs;
drop policy if exists "profile_constraints_select_own" on public.profile_constraints;
drop policy if exists "profile_constraints_insert_own" on public.profile_constraints;
drop policy if exists "profile_conflicts_select_own" on public.profile_conflicts;
drop policy if exists "profile_conflicts_insert_own" on public.profile_conflicts;

create policy "profile_runs_select_own" on public.profile_runs for select using (
  exists (select 1 from public.planning_units pu where pu.planning_unit_id = profile_runs.planning_unit_id and pu.user_id = (select auth.uid()))
);
create policy "profile_runs_insert_own" on public.profile_runs for insert with check (
  exists (select 1 from public.planning_units pu where pu.planning_unit_id = profile_runs.planning_unit_id and pu.user_id = (select auth.uid()))
);
create policy "profile_constraints_select_own" on public.profile_constraints for select using (
  exists (select 1 from public.profile_runs pr join public.planning_units pu on pu.planning_unit_id = pr.planning_unit_id where pr.profile_run_id = profile_constraints.profile_run_id and pu.user_id = (select auth.uid()))
);
create policy "profile_constraints_insert_own" on public.profile_constraints for insert with check (
  exists (select 1 from public.profile_runs pr join public.planning_units pu on pu.planning_unit_id = pr.planning_unit_id where pr.profile_run_id = profile_constraints.profile_run_id and pu.user_id = (select auth.uid()))
);
create policy "profile_conflicts_select_own" on public.profile_conflicts for select using (
  exists (select 1 from public.profile_runs pr join public.planning_units pu on pu.planning_unit_id = pr.planning_unit_id where pr.profile_run_id = profile_conflicts.profile_run_id and pu.user_id = (select auth.uid()))
);
create policy "profile_conflicts_insert_own" on public.profile_conflicts for insert with check (
  exists (select 1 from public.profile_runs pr join public.planning_units pu on pu.planning_unit_id = pr.planning_unit_id where pr.profile_run_id = profile_conflicts.profile_run_id and pu.user_id = (select auth.uid()))
);

create or replace function public.prevent_profile_mutation()
returns trigger
language plpgsql
set search_path = pg_catalog, public
as $$
begin
  raise exception 'profile snapshots are immutable';
end;
$$;

drop trigger if exists profile_runs_immutable on public.profile_runs;
create trigger profile_runs_immutable before update or delete on public.profile_runs for each row execute function public.prevent_profile_mutation();
drop trigger if exists profile_constraints_immutable on public.profile_constraints;
create trigger profile_constraints_immutable before update or delete on public.profile_constraints for each row execute function public.prevent_profile_mutation();
drop trigger if exists profile_conflicts_immutable on public.profile_conflicts;
create trigger profile_conflicts_immutable before update or delete on public.profile_conflicts for each row execute function public.prevent_profile_mutation();
