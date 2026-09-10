create table if not exists public.strategy_approval_snapshots (
  approval_snapshot_id uuid primary key default gen_random_uuid(),
  planning_unit_id uuid not null references public.planning_units(planning_unit_id) on delete cascade,
  strategy_id text not null,
  strategy_version_id uuid not null references public.strategy_versions(strategy_version_id),
  strategy_version integer not null check (strategy_version >= 1),
  goal_id uuid not null references public.goals(goal_id),
  defined_goal_id uuid not null references public.defined_goals(defined_goal_id),
  defined_goal_version integer not null check (defined_goal_version >= 1),
  strategy_snapshot jsonb not null,
  suitability jsonb not null,
  acknowledgement_type text not null default 'none' check (acknowledgement_type in ('none', 'needs_attention', 'unsuitable')),
  acknowledgement_text text,
  acknowledged_at timestamptz,
  approved_at timestamptz not null default now(),
  is_primary boolean not null default false
);

create index if not exists idx_strategy_approval_pu
  on public.strategy_approval_snapshots (planning_unit_id, approved_at desc);

create index if not exists idx_strategy_approval_strategy
  on public.strategy_approval_snapshots (planning_unit_id, strategy_id, strategy_version);

create unique index if not exists idx_strategy_approval_primary
  on public.strategy_approval_snapshots (planning_unit_id)
  where is_primary = true;

alter table public.strategy_approval_snapshots enable row level security;

drop policy if exists "strategy_approval_select_own" on public.strategy_approval_snapshots;
create policy "strategy_approval_select_own"
  on public.strategy_approval_snapshots for select
  using (
    exists (
      select 1 from public.planning_units pu
      where pu.planning_unit_id = strategy_approval_snapshots.planning_unit_id
        and pu.user_id = auth.uid()
    )
  );

drop policy if exists "strategy_approval_insert_own" on public.strategy_approval_snapshots;
create policy "strategy_approval_insert_own"
  on public.strategy_approval_snapshots for insert
  with check (
    exists (
      select 1 from public.planning_units pu
      where pu.planning_unit_id = strategy_approval_snapshots.planning_unit_id
        and pu.user_id = auth.uid()
    )
  );

create or replace function public.prevent_strategy_approval_mutation()
returns trigger
language plpgsql
as $$
begin
  raise exception 'strategy_approval_snapshots are immutable';
end;
$$;

drop trigger if exists strategy_approval_snapshots_immutable on public.strategy_approval_snapshots;
create trigger strategy_approval_snapshots_immutable
before update or delete on public.strategy_approval_snapshots
for each row execute function public.prevent_strategy_approval_mutation();
