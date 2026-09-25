-- Goal Planner specialized goal types
-- Backward-compatible: existing goals remain valid.

alter table public.goals
  add column if not exists goal_type text not null default 'one_time',
  add column if not exists goal_details jsonb not null default '{}'::jsonb;

alter table public.goals
  drop constraint if exists goals_goal_type_check;

alter table public.goals
  add constraint goals_goal_type_check
  check (goal_type in (
    'one_time',
    'retirement',
    'education',
    'travel',
    'home_purchase',
    'vehicle_purchase',
    'emergency_fund',
    'debt_repayment'
  ));

create index if not exists idx_goals_goal_type
  on public.goals (planning_unit_id, goal_type);
