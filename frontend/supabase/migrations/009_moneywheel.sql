create table if not exists public.moneywheel_snapshots (
  snapshot_id uuid primary key default gen_random_uuid(),
  planning_unit_id uuid not null references public.planning_units(planning_unit_id) on delete cascade,
  rule_set_version text not null,
  overall_status text not null check (overall_status in ('excellent', 'healthy', 'attention', 'critical', 'incomplete')),
  ratios jsonb not null,
  financial_state_snapshot jsonb not null default '{}'::jsonb,
  calculated_at timestamptz not null default now(),
  metadata jsonb not null default '{}'::jsonb
);

create index if not exists idx_moneywheel_snapshots_pu_time
  on public.moneywheel_snapshots (planning_unit_id, calculated_at desc);

alter table public.moneywheel_snapshots enable row level security;

drop policy if exists "moneywheel_snapshot_select_own" on public.moneywheel_snapshots;
create policy "moneywheel_snapshot_select_own"
  on public.moneywheel_snapshots for select
  using (exists (
    select 1 from public.planning_units pu
    where pu.planning_unit_id = moneywheel_snapshots.planning_unit_id
      and pu.user_id = auth.uid()
  ));

drop policy if exists "moneywheel_snapshot_insert_own" on public.moneywheel_snapshots;
create policy "moneywheel_snapshot_insert_own"
  on public.moneywheel_snapshots for insert
  with check (exists (
    select 1 from public.planning_units pu
    where pu.planning_unit_id = moneywheel_snapshots.planning_unit_id
      and pu.user_id = auth.uid()
  ));

create or replace function public.prevent_moneywheel_snapshot_mutation()
returns trigger language plpgsql as $$
begin
  raise exception 'moneywheel_snapshots are immutable';
end;
$$;

drop trigger if exists moneywheel_snapshots_immutable on public.moneywheel_snapshots;
create trigger moneywheel_snapshots_immutable
  before update or delete on public.moneywheel_snapshots
  for each row execute function public.prevent_moneywheel_snapshot_mutation();
