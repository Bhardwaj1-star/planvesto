-- ============================================================================
-- Migration 016: Budget Limits Table
-- Stores user-defined budget limits per expense category per planning unit.
-- Actual spend is derived from the existing expenses + liabilities tables.
-- ============================================================================

create table if not exists public.budget_limits (
  budget_limit_id uuid primary key default gen_random_uuid(),
  planning_unit_id uuid not null references public.planning_units(planning_unit_id) on delete cascade,
  category text not null,
  classification text not null default 'Need' check (classification in ('Need', 'Want')),
  budget_monthly numeric not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  -- One budget limit per category per planning unit
  unique (planning_unit_id, category)
);

-- Enable RLS
alter table public.budget_limits enable row level security;

-- RLS Policies: mirror the pattern used by other onboarding tables
create policy "Users can view their own budget limits"
  on public.budget_limits for select
  using (
    planning_unit_id in (
      select planning_unit_id from public.planning_units where user_id = auth.uid()
    )
  );

create policy "Users can insert their own budget limits"
  on public.budget_limits for insert
  with check (
    planning_unit_id in (
      select planning_unit_id from public.planning_units where user_id = auth.uid()
    )
  );

create policy "Users can update their own budget limits"
  on public.budget_limits for update
  using (
    planning_unit_id in (
      select planning_unit_id from public.planning_units where user_id = auth.uid()
    )
  );

create policy "Users can delete their own budget limits"
  on public.budget_limits for delete
  using (
    planning_unit_id in (
      select planning_unit_id from public.planning_units where user_id = auth.uid()
    )
  );

-- Enable realtime for this table
alter publication supabase_realtime add table public.budget_limits;
