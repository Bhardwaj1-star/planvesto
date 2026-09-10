create table if not exists public.diary_entries (
  id uuid primary key default gen_random_uuid(),
  planning_unit_id uuid not null references public.planning_units(planning_unit_id) on delete cascade,
  date date not null,
  title text,
  content text not null,
  tags jsonb not null default '[]'::jsonb,
  prompts jsonb not null default '[]'::jsonb,
  follow_up_note text,
  is_important boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.financial_decision_history (
  id uuid primary key default gen_random_uuid(),
  planning_unit_id uuid not null references public.planning_units(planning_unit_id) on delete cascade,
  date date not null,
  title text not null,
  summary text not null,
  category text not null check (category in ('Strategy','Investment','Debt','Goal','Allocation','General')),
  source text not null,
  source_id uuid,
  metrics jsonb not null default '{}'::jsonb,
  notes text,
  created_at timestamptz not null default now(),
  historical boolean not null default true
);

create index if not exists idx_diary_entries_pu_date on public.diary_entries(planning_unit_id, date desc);
create index if not exists idx_financial_decisions_pu_date on public.financial_decision_history(planning_unit_id, date desc);

alter table public.diary_entries enable row level security;
alter table public.financial_decision_history enable row level security;

create policy "diary_entries_select_own" on public.diary_entries for select using (exists (select 1 from public.planning_units pu where pu.planning_unit_id = diary_entries.planning_unit_id and pu.user_id = auth.uid()));
create policy "diary_entries_insert_own" on public.diary_entries for insert with check (exists (select 1 from public.planning_units pu where pu.planning_unit_id = diary_entries.planning_unit_id and pu.user_id = auth.uid()));
create policy "diary_entries_update_own" on public.diary_entries for update using (exists (select 1 from public.planning_units pu where pu.planning_unit_id = diary_entries.planning_unit_id and pu.user_id = auth.uid())) with check (exists (select 1 from public.planning_units pu where pu.planning_unit_id = diary_entries.planning_unit_id and pu.user_id = auth.uid()));
create policy "diary_entries_delete_own" on public.diary_entries for delete using (exists (select 1 from public.planning_units pu where pu.planning_unit_id = diary_entries.planning_unit_id and pu.user_id = auth.uid()));

create policy "financial_decisions_select_own" on public.financial_decision_history for select using (exists (select 1 from public.planning_units pu where pu.planning_unit_id = financial_decision_history.planning_unit_id and pu.user_id = auth.uid()));
create policy "financial_decisions_insert_own" on public.financial_decision_history for insert with check (exists (select 1 from public.planning_units pu where pu.planning_unit_id = financial_decision_history.planning_unit_id and pu.user_id = auth.uid()));

create or replace function public.prevent_financial_decision_mutation() returns trigger language plpgsql as $$ begin raise exception 'financial_decision_history is immutable'; end; $$;
drop trigger if exists financial_decision_history_immutable on public.financial_decision_history;
create trigger financial_decision_history_immutable before update or delete on public.financial_decision_history for each row execute function public.prevent_financial_decision_mutation();
