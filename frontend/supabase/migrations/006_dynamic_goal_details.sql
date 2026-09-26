-- Store goal type and goal-specific onboarding answers without duplicating columns per goal type.
alter table public.goals
  add column if not exists goal_type text,
  add column if not exists dynamic_details jsonb not null default '{}'::jsonb;

create index if not exists idx_goals_goal_type on public.goals(goal_type);
