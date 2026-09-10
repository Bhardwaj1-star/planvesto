create table if not exists public.financial_state_snapshots (
  snapshot_id uuid primary key default gen_random_uuid(),
  planning_unit_id uuid not null references public.planning_units(planning_unit_id) on delete cascade,
  scope text not null check (scope in ('family', 'individual')),
  investor_id uuid null,
  financial_state jsonb not null,
  calculated_at timestamptz not null default now(),
  constraint financial_state_snapshot_individual_owner_check
    check ((scope = 'individual' and investor_id is not null) or (scope = 'family' and investor_id is null))
);

create index if not exists idx_financial_state_snapshots_pu_time
  on public.financial_state_snapshots (planning_unit_id, calculated_at desc);

create index if not exists idx_financial_state_snapshots_scope_investor_time
  on public.financial_state_snapshots (planning_unit_id, scope, investor_id, calculated_at desc);

alter table public.financial_state_snapshots enable row level security;

drop policy if exists "financial_state_snapshot_select_own" on public.financial_state_snapshots;
create policy "financial_state_snapshot_select_own"
  on public.financial_state_snapshots for select
  using (exists (
    select 1 from public.planning_units pu
    where pu.planning_unit_id = financial_state_snapshots.planning_unit_id
      and pu.user_id = auth.uid()
  ));

drop policy if exists "financial_state_snapshot_insert_own" on public.financial_state_snapshots;
create policy "financial_state_snapshot_insert_own"
  on public.financial_state_snapshots for insert
  with check (exists (
    select 1 from public.planning_units pu
    where pu.planning_unit_id = financial_state_snapshots.planning_unit_id
      and pu.user_id = auth.uid()
  ));

create or replace function public.prevent_financial_state_snapshot_mutation()
returns trigger language plpgsql as $$
begin
  raise exception 'financial_state_snapshots are immutable';
end;
$$;

drop trigger if exists financial_state_snapshots_immutable on public.financial_state_snapshots;
create trigger financial_state_snapshots_immutable
  before update or delete on public.financial_state_snapshots
  for each row execute function public.prevent_financial_state_snapshot_mutation();
