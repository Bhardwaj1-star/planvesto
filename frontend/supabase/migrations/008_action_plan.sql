create table if not exists public.action_plan_items (
  action_id uuid primary key default gen_random_uuid(),
  planning_unit_id uuid not null references public.planning_units(planning_unit_id) on delete cascade,
  strategy_version_id uuid not null references public.strategy_versions(strategy_version_id),
  title text not null,
  description text,
  priority text not null default 'medium' check (priority in ('high','medium','low')),
  deadline timestamptz,
  status text not null default 'planned' check (status in ('planned','confirmed','completed','cancelled')),
  planned_impact jsonb not null default '{}'::jsonb,
  actual_impact jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.action_decision_history (
  decision_id uuid primary key default gen_random_uuid(),
  planning_unit_id uuid not null references public.planning_units(planning_unit_id) on delete cascade,
  action_id uuid not null,
  decision text not null check (decision in ('add','modify','delete','complete','cancel')),
  before_state jsonb not null default '{}'::jsonb,
  after_state jsonb not null default '{}'::jsonb,
  impact_preview jsonb not null,
  confirmed_at timestamptz not null default now(),
  historical boolean not null default true
);

create index if not exists idx_action_plan_items_pu on public.action_plan_items(planning_unit_id);
create index if not exists idx_action_history_pu on public.action_decision_history(planning_unit_id, confirmed_at desc);

alter table public.action_plan_items enable row level security;
alter table public.action_decision_history enable row level security;

create policy "action_plan_select_own" on public.action_plan_items for select using (exists (select 1 from public.planning_units pu where pu.planning_unit_id = action_plan_items.planning_unit_id and pu.user_id = auth.uid()));
create policy "action_plan_insert_own" on public.action_plan_items for insert with check (exists (select 1 from public.planning_units pu where pu.planning_unit_id = action_plan_items.planning_unit_id and pu.user_id = auth.uid()));
create policy "action_plan_update_own" on public.action_plan_items for update using (exists (select 1 from public.planning_units pu where pu.planning_unit_id = action_plan_items.planning_unit_id and pu.user_id = auth.uid())) with check (exists (select 1 from public.planning_units pu where pu.planning_unit_id = action_plan_items.planning_unit_id and pu.user_id = auth.uid()));
create policy "action_history_select_own" on public.action_decision_history for select using (exists (select 1 from public.planning_units pu where pu.planning_unit_id = action_decision_history.planning_unit_id and pu.user_id = auth.uid()));
create policy "action_history_insert_own" on public.action_decision_history for insert with check (exists (select 1 from public.planning_units pu where pu.planning_unit_id = action_decision_history.planning_unit_id and pu.user_id = auth.uid()));

create or replace function public.prevent_action_history_mutation() returns trigger language plpgsql as $$ begin raise exception 'action_decision_history is immutable'; end; $$;
drop trigger if exists action_decision_history_immutable on public.action_decision_history;
create trigger action_decision_history_immutable before update or delete on public.action_decision_history for each row execute function public.prevent_action_history_mutation();
