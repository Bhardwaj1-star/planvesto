-- Database security hardening
-- 1. Keep internal SECURITY DEFINER functions out of the public RPC surface.
-- These functions are invoked by database triggers/event triggers, not by clients.
revoke execute on function public.handle_new_user() from public;
revoke execute on function public.rls_auto_enable() from public;

-- 2. Pin trigger-function search_path so trigger execution cannot resolve
-- objects through a mutable session search_path.
alter function public.prevent_strategy_version_mutation() set search_path = pg_catalog;
alter function public.prevent_strategy_approval_mutation() set search_path = pg_catalog;
alter function public.prevent_primary_transition_mutation() set search_path = pg_catalog;
alter function public.prevent_action_history_mutation() set search_path = pg_catalog;
alter function public.prevent_moneywheel_snapshot_mutation() set search_path = pg_catalog;
alter function public.prevent_financial_state_snapshot_mutation() set search_path = pg_catalog;
alter function public.prevent_financial_decision_mutation() set search_path = pg_catalog;

-- handle_new_user and rls_auto_enable already pin their search_path in the
-- current production definition; keep those definitions unchanged.
