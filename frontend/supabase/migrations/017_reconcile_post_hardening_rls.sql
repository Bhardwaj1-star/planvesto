-- Migration 017: Reconcile post-hardening RLS policies.
-- Keeps ownership semantics unchanged while aligning tables added after the
-- original security-hardening migration with the authenticated-only baseline.

alter policy "Users can view their own budget limits"
  on public.budget_limits to authenticated
  using (
    planning_unit_id in (
      select planning_unit_id from public.planning_units
      where user_id = (select auth.uid())
    )
  );

alter policy "Users can insert their own budget limits"
  on public.budget_limits to authenticated
  with check (
    planning_unit_id in (
      select planning_unit_id from public.planning_units
      where user_id = (select auth.uid())
    )
  );

alter policy "Users can update their own budget limits"
  on public.budget_limits to authenticated
  using (
    planning_unit_id in (
      select planning_unit_id from public.planning_units
      where user_id = (select auth.uid())
    )
  )
  with check (
    planning_unit_id in (
      select planning_unit_id from public.planning_units
      where user_id = (select auth.uid())
    )
  );

alter policy "Users can delete their own budget limits"
  on public.budget_limits to authenticated
  using (
    planning_unit_id in (
      select planning_unit_id from public.planning_units
      where user_id = (select auth.uid())
    )
  );

alter policy "users can access their insurance policies"
  on public.insurance_policies to authenticated
  using (
    exists (
      select 1
      from public.planning_units
      where planning_units.planning_unit_id = insurance_policies.planning_unit_id
        and planning_units.user_id = (select auth.uid())
    )
  )
  with check (
    exists (
      select 1
      from public.planning_units
      where planning_units.planning_unit_id = insurance_policies.planning_unit_id
        and planning_units.user_id = (select auth.uid())
    )
  );

alter policy "profile_runs_select_own"
  on public.profile_runs to authenticated
  using (
    exists (
      select 1 from public.planning_units pu
      where pu.planning_unit_id = profile_runs.planning_unit_id
        and pu.user_id = (select auth.uid())
    )
  );

alter policy "profile_runs_insert_own"
  on public.profile_runs to authenticated
  with check (
    exists (
      select 1 from public.planning_units pu
      where pu.planning_unit_id = profile_runs.planning_unit_id
        and pu.user_id = (select auth.uid())
    )
  );

alter policy "profile_constraints_select_own"
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

alter policy "profile_constraints_insert_own"
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

alter policy "profile_conflicts_select_own"
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

alter policy "profile_conflicts_insert_own"
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
