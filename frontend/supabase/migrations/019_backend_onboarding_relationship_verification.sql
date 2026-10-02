-- 019_backend_onboarding_relationship_verification.sql
-- Read-only post-migration verification.

select
  tc.table_name,
  tc.constraint_name,
  pg_get_constraintdef(pc.oid) as definition
from information_schema.table_constraints tc
join pg_constraint pc
  on pc.conname = tc.constraint_name
 and pc.conrelid = (quote_ident(tc.table_schema)||'.'||quote_ident(tc.table_name))::regclass
where tc.table_schema = 'public'
  and tc.constraint_name in (
    'financial_state_snapshots_investor_id_fkey',
    'profile_runs_investor_id_fkey',
    'strategy_versions_parent_version_fkey',
    'primary_strategy_state_previous_version_fkey',
    'primary_strategy_transitions_previous_version_fkey'
  )
order by tc.table_name, tc.constraint_name;

select
  (select count(*) from public.financial_state_snapshots s
   left join public.investors i on i.investor_id=s.investor_id
   where s.investor_id is not null and i.investor_id is null) as orphan_snapshot_investor,
  (select count(*) from public.profile_runs p
   left join public.investors i on i.investor_id=p.investor_id
   where i.investor_id is null) as orphan_profile_investor,
  (select count(*) from public.strategy_versions v
   left join public.strategy_versions p
     on p.planning_unit_id=v.planning_unit_id
    and p.strategy_id=v.strategy_id
    and p.version=v.parent_version
   where v.parent_version is not null and p.strategy_version_id is null) as orphan_parent_version,
  (select count(*) from public.primary_strategy_state s
   left join public.strategy_versions v on v.strategy_version_id=s.previous_strategy_version_id
   where s.previous_strategy_version_id is not null and v.strategy_version_id is null) as orphan_previous_state_version,
  (select count(*) from public.primary_strategy_transitions t
   left join public.strategy_versions v on v.strategy_version_id=t.previous_strategy_version_id
   where t.previous_strategy_version_id is not null and v.strategy_version_id is null) as orphan_previous_transition_version;
