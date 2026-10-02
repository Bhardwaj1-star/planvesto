-- Reconcile production RLS hardening for budget/profile persistence tables.
-- These tables contain authenticated user planning data and must not expose public-role policies.

alter policy "Users can view their own budget limits"
  on public.budget_limits to authenticated
  using (
    planning_unit_id in (
      select pu.planning_unit_id
      from public.planning_units pu
      where pu.user_id = (select auth.uid())
    )
  );

alter policy "Users can insert their own budget limits"
  on public.budget_limits to authenticated
  with check (
    planning_unit_id in (
      select pu.planning_unit_id
      from public.planning_units pu
      where pu.user_id = (select auth.uid())
    )
  );

alter policy "Users can update their own budget limits"
  on public.budget_limits to authenticated
  using (
    planning_unit_id in (
      select pu.planning_unit_id
      from public.planning_units pu
      where pu.user_id = (select auth.uid())
    )
  )
  with check (
    planning_unit_id in (
      select pu.planning_unit_id
      from public.planning_units pu
      where pu.user_id = (select auth.uid())
    )
  );

alter policy "Users can delete their own budget limits"
  on public.budget_limits to authenticated
  using (
    planning_unit_id in (
      select pu.planning_unit_id
      from public.planning_units pu
      where pu.user_id = (select auth.uid())
    )
  );

alter policy profile_runs_select_own
  on public.profile_runs to authenticated
  using (
    exists (
      select 1
      from public.planning_units pu
      where pu.planning_unit_id = profile_runs.planning_unit_id
        and pu.user_id = (select auth.uid())
    )
  );

alter policy profile_runs_insert_own
  on public.profile_runs to authenticated
  with check (
    exists (
      select 1
      from public.planning_units pu
      where pu.planning_unit_id = profile_runs.planning_unit_id
        and pu.user_id = (select auth.uid())
    )
  );

alter policy profile_constraints_select_own
  on public.profile_constraints to authenticated
  using (
    exists (
      select 1
      from public.profile_runs pr
      join public.planning_units pu on pu.planning_unit_id = pr.planning_unit_id
      where pr.profile_run_id = profile_constraints.profile_run_id
        and pu.user_id = (select auth.uid())
    )
  );

alter policy profile_constraints_insert_own
  on public.profile_constraints to authenticated
  with check (
    exists (
      select 1
      from public.profile_runs pr
      join public.planning_units pu on pu.planning_unit_id = pr.planning_unit_id
      where pr.profile_run_id = profile_constraints.profile_run_id
        and pu.user_id = (select auth.uid())
    )
  );

alter policy profile_conflicts_select_own
  on public.profile_conflicts to authenticated
  using (
    exists (
      select 1
      from public.profile_runs pr
      join public.planning_units pu on pu.planning_unit_id = pr.planning_unit_id
      where pr.profile_run_id = profile_conflicts.profile_run_id
        and pu.user_id = (select auth.uid())
    )
  );

alter policy profile_conflicts_insert_own
  on public.profile_conflicts to authenticated
  with check (
    exists (
      select 1
      from public.profile_runs pr
      join public.planning_units pu on pu.planning_unit_id = pr.planning_unit_id
      where pr.profile_run_id = profile_conflicts.profile_run_id
        and pu.user_id = (select auth.uid())
    )
  );
