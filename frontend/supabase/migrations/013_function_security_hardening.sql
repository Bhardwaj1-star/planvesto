-- Security hardening: remove SECURITY DEFINER RPC exposure and pin trigger function search_path.
revoke execute on function public.handle_new_user() from public;
revoke execute on function public.rls_auto_enable() from public;
alter function public.prevent_strategy_version_mutation() set search_path = pg_catalog;
alter function public.prevent_strategy_approval_mutation() set search_path = pg_catalog;
alter function public.prevent_primary_transition_mutation() set search_path = pg_catalog;
alter function public.prevent_action_history_mutation() set search_path = pg_catalog;
alter function public.prevent_moneywheel_snapshot_mutation() set search_path = pg_catalog;
alter function public.prevent_financial_state_snapshot_mutation() set search_path = pg_catalog;
alter function public.prevent_financial_decision_mutation() set search_path = pg_catalog;
