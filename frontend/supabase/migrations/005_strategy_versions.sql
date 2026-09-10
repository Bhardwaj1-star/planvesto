create table if not exists public.strategy_versions (
  strategy_version_id uuid primary key default gen_random_uuid(),
  planning_unit_id uuid not null references public.planning_units(planning_unit_id) on delete cascade,
  strategy_id text not null,
  version integer not null check (version >= 1),
  parent_version integer check (parent_version is null or parent_version >= 1),
  source text not null check (source in ('library', 'investor_edit')),
  library_version text not null,
  implementation_version text not null,
  implementation_parameters jsonb not null default '{}'::jsonb,
  status text not null default 'draft' check (status in ('draft', 'approved', 'primary', 'archived', 'needs_review', 'provisional')),
  created_at timestamptz not null default now(),
  constraint strategy_versions_unique_version unique (planning_unit_id, strategy_id, version),
  constraint strategy_versions_parent_required check (source = 'library' or parent_version is not null)
);

create index if not exists idx_strategy_versions_planning_strategy
  on public.strategy_versions (planning_unit_id, strategy_id, version desc);
create index if not exists idx_strategy_versions_planning_unit
  on public.strategy_versions (planning_unit_id);

alter table public.strategy_versions enable row level security;

drop policy if exists "strategy_versions_select_own" on public.strategy_versions;
create policy "strategy_versions_select_own"
  on public.strategy_versions for select
  using (exists (select 1 from public.planning_units pu where pu.planning_unit_id = strategy_versions.planning_unit_id and pu.user_id = auth.uid()));

drop policy if exists "strategy_versions_insert_own" on public.strategy_versions;
create policy "strategy_versions_insert_own"
  on public.strategy_versions for insert
  with check (exists (select 1 from public.planning_units pu where pu.planning_unit_id = strategy_versions.planning_unit_id and pu.user_id = auth.uid()));

create or replace function public.prevent_strategy_version_mutation()
returns trigger language plpgsql as $$
begin
  raise exception 'strategy_versions are immutable';
end;
$$;

drop trigger if exists strategy_versions_immutable on public.strategy_versions;
create trigger strategy_versions_immutable
before update or delete on public.strategy_versions
for each row execute function public.prevent_strategy_version_mutation();

alter table public.strategy_runs
  add column if not exists selected_strategy_version_id uuid,
  add column if not exists selected_strategy_version integer;

create index if not exists idx_strategy_runs_selected_strategy_version
  on public.strategy_runs (selected_strategy_version_id);
