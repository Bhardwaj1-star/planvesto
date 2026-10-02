-- Canonical production DB reconciliation.
-- Existing planning/content data is preserved. This migration only hardens
-- ownership RLS and adds missing FK indexes; no application rows are deleted.

alter policy "Users can view their own budget limits"
  on public.budget_limits to authenticated
  using (planning_unit_id in (
    select pu.planning_unit_id from public.planning_units pu
    where pu.user_id = (select auth.uid())
  ));

alter policy "Users can insert their own budget limits"
  on public.budget_limits to authenticated
  with check (planning_unit_id in (
    select pu.planning_unit_id from public.planning_units pu
    where pu.user_id = (select auth.uid())
  ));

alter policy "Users can update their own budget limits"
  on public.budget_limits to authenticated
  using (planning_unit_id in (
    select pu.planning_unit_id from public.planning_units pu
    where pu.user_id = (select auth.uid())
  ))
  with check (planning_unit_id in (
    select pu.planning_unit_id from public.planning_units pu
    where pu.user_id = (select auth.uid())
  ));

alter policy "Users can delete their own budget limits"
  on public.budget_limits to authenticated
  using (planning_unit_id in (
    select pu.planning_unit_id from public.planning_units pu
    where pu.user_id = (select auth.uid())
  ));

alter policy profile_runs_select_own on public.profile_runs to authenticated
  using (exists (
    select 1 from public.planning_units pu
    where pu.planning_unit_id = profile_runs.planning_unit_id
      and pu.user_id = (select auth.uid())
  ));
alter policy profile_runs_insert_own on public.profile_runs to authenticated
  with check (exists (
    select 1 from public.planning_units pu
    where pu.planning_unit_id = profile_runs.planning_unit_id
      and pu.user_id = (select auth.uid())
  ));

alter policy profile_constraints_select_own on public.profile_constraints to authenticated
  using (exists (
    select 1 from public.profile_runs pr
    join public.planning_units pu on pu.planning_unit_id = pr.planning_unit_id
    where pr.profile_run_id = profile_constraints.profile_run_id
      and pu.user_id = (select auth.uid())
  ));
alter policy profile_constraints_insert_own on public.profile_constraints to authenticated
  with check (exists (
    select 1 from public.profile_runs pr
    join public.planning_units pu on pu.planning_unit_id = pr.planning_unit_id
    where pr.profile_run_id = profile_constraints.profile_run_id
      and pu.user_id = (select auth.uid())
  ));

alter policy profile_conflicts_select_own on public.profile_conflicts to authenticated
  using (exists (
    select 1 from public.profile_runs pr
    join public.planning_units pu on pu.planning_unit_id = pr.planning_unit_id
    where pr.profile_run_id = profile_conflicts.profile_run_id
      and pu.user_id = (select auth.uid())
  ));
alter policy profile_conflicts_insert_own on public.profile_conflicts to authenticated
  with check (exists (
    select 1 from public.profile_runs pr
    join public.planning_units pu on pu.planning_unit_id = pr.planning_unit_id
    where pr.profile_run_id = profile_conflicts.profile_run_id
      and pu.user_id = (select auth.uid())
  ));

create index if not exists idx_article_revisions_topic_id on public.article_revisions(topic_id);
create index if not exists idx_article_revisions_created_by on public.article_revisions(created_by);
create index if not exists idx_editorial_audit_log_actor_id on public.editorial_audit_log(actor_id);
create index if not exists idx_defined_goals_investor_id on public.defined_goals(investor_id);
create index if not exists idx_defined_goal_asset_mappings_asset_id on public.defined_goal_asset_mappings(asset_id);
create index if not exists idx_strategy_runs_defined_goal_id on public.strategy_runs(defined_goal_id);
create index if not exists idx_strategy_approval_snapshots_strategy_version_id on public.strategy_approval_snapshots(strategy_version_id);
create index if not exists idx_strategy_approval_snapshots_goal_id on public.strategy_approval_snapshots(goal_id);
create index if not exists idx_strategy_approval_snapshots_defined_goal_id on public.strategy_approval_snapshots(defined_goal_id);
create index if not exists idx_primary_strategy_state_strategy_version_id on public.primary_strategy_state(strategy_version_id);
create index if not exists idx_primary_strategy_state_approval_snapshot_id on public.primary_strategy_state(approval_snapshot_id);
create index if not exists idx_primary_strategy_transitions_new_strategy_version_id on public.primary_strategy_transitions(new_strategy_version_id);
create index if not exists idx_primary_strategy_transitions_approval_snapshot_id on public.primary_strategy_transitions(approval_snapshot_id);
create index if not exists idx_action_plan_items_strategy_version_id on public.action_plan_items(strategy_version_id);
create index if not exists idx_insurance_policies_asset_id on public.insurance_policies(asset_id);
create index if not exists idx_insurance_policies_expense_id on public.insurance_policies(expense_id);
create index if not exists idx_profile_runs_financial_snapshot_id on public.profile_runs(financial_snapshot_id);
