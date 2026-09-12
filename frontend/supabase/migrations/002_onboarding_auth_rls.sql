-- Link planning units to Supabase Auth users and enforce ownership for onboarding data.

alter table public.planning_units
  add column if not exists user_id uuid references auth.users(id) on delete cascade;

create index if not exists idx_planning_units_user_id
  on public.planning_units(user_id);

alter table public.planning_units enable row level security;
alter table public.investors enable row level security;
alter table public.dependents enable row level security;
alter table public.income enable row level security;
alter table public.expenses enable row level security;
alter table public.expense_participants enable row level security;
alter table public.assets enable row level security;
alter table public.asset_owners enable row level security;
alter table public.liabilities enable row level security;
alter table public.liability_responsibilities enable row level security;
alter table public.goals enable row level security;
alter table public.goal_funding enable row level security;

drop policy if exists "users can access their planning units" on public.planning_units;
create policy "users can access their planning units"
  on public.planning_units for all
  using (user_id = auth.uid())
  with check (user_id = auth.uid());

drop policy if exists "users can access their investors" on public.investors;
create policy "users can access their investors"
  on public.investors for all
  using (exists (select 1 from public.planning_units where planning_unit_id = investors.planning_unit_id and user_id = auth.uid()))
  with check (exists (select 1 from public.planning_units where planning_unit_id = investors.planning_unit_id and user_id = auth.uid()));

drop policy if exists "users can access their dependents" on public.dependents;
create policy "users can access their dependents"
  on public.dependents for all
  using (exists (select 1 from public.planning_units where planning_unit_id = dependents.planning_unit_id and user_id = auth.uid()))
  with check (exists (select 1 from public.planning_units where planning_unit_id = dependents.planning_unit_id and user_id = auth.uid()));

drop policy if exists "users can access their income" on public.income;
create policy "users can access their income"
  on public.income for all
  using (exists (select 1 from public.planning_units where planning_unit_id = income.planning_unit_id and user_id = auth.uid()))
  with check (exists (select 1 from public.planning_units where planning_unit_id = income.planning_unit_id and user_id = auth.uid()));

drop policy if exists "users can access their expenses" on public.expenses;
create policy "users can access their expenses"
  on public.expenses for all
  using (exists (select 1 from public.planning_units where planning_unit_id = expenses.planning_unit_id and user_id = auth.uid()))
  with check (exists (select 1 from public.planning_units where planning_unit_id = expenses.planning_unit_id and user_id = auth.uid()));

drop policy if exists "users can access their assets" on public.assets;
create policy "users can access their assets"
  on public.assets for all
  using (exists (select 1 from public.planning_units where planning_unit_id = assets.planning_unit_id and user_id = auth.uid()))
  with check (exists (select 1 from public.planning_units where planning_unit_id = assets.planning_unit_id and user_id = auth.uid()));

drop policy if exists "users can access their liabilities" on public.liabilities;
create policy "users can access their liabilities"
  on public.liabilities for all
  using (exists (select 1 from public.planning_units where planning_unit_id = liabilities.planning_unit_id and user_id = auth.uid()))
  with check (exists (select 1 from public.planning_units where planning_unit_id = liabilities.planning_unit_id and user_id = auth.uid()));

drop policy if exists "users can access their goals" on public.goals;
create policy "users can access their goals"
  on public.goals for all
  using (exists (select 1 from public.planning_units where planning_unit_id = goals.planning_unit_id and user_id = auth.uid()))
  with check (exists (select 1 from public.planning_units where planning_unit_id = goals.planning_unit_id and user_id = auth.uid()));

drop policy if exists "users can access their expense participants" on public.expense_participants;
create policy "users can access their expense participants"
  on public.expense_participants for all
  using (exists (
    select 1 from public.expenses
    join public.planning_units using (planning_unit_id)
    where expenses.expense_id = expense_participants.expense_id and planning_units.user_id = auth.uid()
  ))
  with check (exists (
    select 1 from public.expenses
    join public.planning_units using (planning_unit_id)
    where expenses.expense_id = expense_participants.expense_id and planning_units.user_id = auth.uid()
  ));

drop policy if exists "users can access their asset owners" on public.asset_owners;
create policy "users can access their asset owners"
  on public.asset_owners for all
  using (exists (
    select 1 from public.assets
    join public.planning_units using (planning_unit_id)
    where assets.asset_id = asset_owners.asset_id and planning_units.user_id = auth.uid()
  ))
  with check (exists (
    select 1 from public.assets
    join public.planning_units using (planning_unit_id)
    where assets.asset_id = asset_owners.asset_id and planning_units.user_id = auth.uid()
  ));

drop policy if exists "users can access their liability responsibilities" on public.liability_responsibilities;
create policy "users can access their liability responsibilities"
  on public.liability_responsibilities for all
  using (exists (
    select 1 from public.liabilities
    join public.planning_units using (planning_unit_id)
    where liabilities.liability_id = liability_responsibilities.liability_id and planning_units.user_id = auth.uid()
  ))
  with check (exists (
    select 1 from public.liabilities
    join public.planning_units using (planning_unit_id)
    where liabilities.liability_id = liability_responsibilities.liability_id and planning_units.user_id = auth.uid()
  ));

drop policy if exists "users can access their goal funding" on public.goal_funding;
create policy "users can access their goal funding"
  on public.goal_funding for all
  using (exists (
    select 1 from public.goals
    join public.planning_units using (planning_unit_id)
    where goals.goal_id = goal_funding.goal_id and planning_units.user_id = auth.uid()
  ))
  with check (exists (
    select 1 from public.goals
    join public.planning_units using (planning_unit_id)
    where goals.goal_id = goal_funding.goal_id and planning_units.user_id = auth.uid()
  ));
