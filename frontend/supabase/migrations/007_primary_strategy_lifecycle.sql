-- Approval snapshots are historical records; multiple snapshots may have been Primary over time.
drop index if exists public.idx_strategy_approval_primary;

create table if not exists public.primary_strategy_state (
  planning_unit_id uuid primary key references public.planning_units(planning_unit_id) on delete cascade,
  strategy_id text not null,
  strategy_version_id uuid not null references public.strategy_versions(strategy_version_id),
  approval_snapshot_id uuid not null references public.strategy_approval_snapshots(approval_snapshot_id),
  status text not null default 'primary' check (status = 'primary'),
  previous_strategy_id text,
  previous_strategy_version_id uuid,
  pending_action_disposition text check (pending_action_disposition is null or pending_action_disposition in ('retain_for_reassessment', 'cancel')),
  transition_metadata jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists public.primary_strategy_transitions (
  transition_id uuid primary key default gen_random_uuid(),
  planning_unit_id uuid not null references public.planning_units(planning_unit_id) on delete cascade,
  previous_strategy_id text,
  previous_strategy_version_id uuid,
  new_strategy_id text not null,
  new_strategy_version_id uuid not null references public.strategy_versions(strategy_version_id),
  approval_snapshot_id uuid not null references public.strategy_approval_snapshots(approval_snapshot_id),
  transition_decision text not null check (transition_decision in ('set_initial_primary', 'archive_previous', 'keep_previous_approved')),
  pending_action_disposition text check (pending_action_disposition is null or pending_action_disposition in ('retain_for_reassessment', 'cancel')),
  transitioned_at timestamptz not null default now()
);

create index if not exists idx_primary_strategy_transitions_pu on public.primary_strategy_transitions (planning_unit_id, transitioned_at desc);

alter table public.primary_strategy_state enable row level security;
alter table public.primary_strategy_transitions enable row level security;

drop policy if exists "primary_state_select_own" on public.primary_strategy_state;
create policy "primary_state_select_own" on public.primary_strategy_state for select using (exists (select 1 from public.planning_units pu where pu.planning_unit_id = primary_strategy_state.planning_unit_id and pu.user_id = auth.uid()));
drop policy if exists "primary_state_insert_own" on public.primary_strategy_state;
create policy "primary_state_insert_own" on public.primary_strategy_state for insert with check (exists (select 1 from public.planning_units pu where pu.planning_unit_id = primary_strategy_state.planning_unit_id and pu.user_id = auth.uid()));
drop policy if exists "primary_state_update_own" on public.primary_strategy_state;
create policy "primary_state_update_own" on public.primary_strategy_state for update using (exists (select 1 from public.planning_units pu where pu.planning_unit_id = primary_strategy_state.planning_unit_id and pu.user_id = auth.uid())) with check (exists (select 1 from public.planning_units pu where pu.planning_unit_id = primary_strategy_state.planning_unit_id and pu.user_id = auth.uid()));

drop policy if exists "primary_transition_select_own" on public.primary_strategy_transitions;
create policy "primary_transition_select_own" on public.primary_strategy_transitions for select using (exists (select 1 from public.planning_units pu where pu.planning_unit_id = primary_strategy_transitions.planning_unit_id and pu.user_id = auth.uid()));
drop policy if exists "primary_transition_insert_own" on public.primary_strategy_transitions;
create policy "primary_transition_insert_own" on public.primary_strategy_transitions for insert with check (exists (select 1 from public.planning_units pu where pu.planning_unit_id = primary_strategy_transitions.planning_unit_id and pu.user_id = auth.uid()));

create or replace function public.prevent_primary_transition_mutation()
returns trigger language plpgsql as $$
begin
  raise exception 'primary_strategy_transitions are immutable';
end;
$$;

drop trigger if exists primary_strategy_transitions_immutable on public.primary_strategy_transitions;
create trigger primary_strategy_transitions_immutable before update or delete on public.primary_strategy_transitions for each row execute function public.prevent_primary_transition_mutation();
