alter table public.defined_goals
  add constraint defined_goals_authority_context_unique
  unique (planning_unit_id, goal_id, defined_goal_id, version);

alter table public.goals
  add constraint goals_authority_context_unique
  unique (planning_unit_id, goal_id);

alter table public.strategy_runs
  add constraint strategy_runs_authority_context_unique
  unique (
    planning_unit_id,
    goal_id,
    defined_goal_id,
    defined_goal_version,
    strategy_run_id
  );

alter table public.strategy_versions
  add column if not exists goal_id uuid references public.goals(goal_id) on delete cascade,
  add column if not exists defined_goal_id uuid references public.defined_goals(defined_goal_id) on delete restrict,
  add column if not exists defined_goal_version integer check (defined_goal_version is null or defined_goal_version >= 1),
  add column if not exists architecture jsonb,
  add column if not exists decision_snapshot jsonb not null default '{}'::jsonb,
  add column if not exists source_strategy_run_id uuid,
  add constraint strategy_versions_goal_context_complete check (
    (goal_id is null and defined_goal_id is null and defined_goal_version is null)
    or (goal_id is not null and defined_goal_id is not null and defined_goal_version is not null)
  ),
  add constraint strategy_versions_finalized_context_complete check (
    goal_id is null
    or (
      architecture is not null
      and source_strategy_run_id is not null
      and architecture ->> 'primary_strategy_id' = strategy_id
      and decision_snapshot #>> '{recommendation,recommended_strategy_id}' = strategy_id
      and decision_snapshot #>> '{recommendation,recommended_scenario_id}'
        = decision_snapshot ->> 'selected_scenario_id'
      and decision_snapshot -> 'scenarios' @> jsonb_build_array(
        jsonb_build_object(
          'scenario_id',
          decision_snapshot ->> 'selected_scenario_id'
        )
      )
    )
  ),
  add constraint strategy_versions_defined_goal_context_fk
    foreign key (planning_unit_id, goal_id, defined_goal_id, defined_goal_version)
    references public.defined_goals (planning_unit_id, goal_id, defined_goal_id, version),
  add constraint strategy_versions_goal_planning_unit_fk
    foreign key (planning_unit_id, goal_id)
    references public.goals (planning_unit_id, goal_id),
  add constraint strategy_versions_source_run_context_fk
    foreign key (
      planning_unit_id,
      goal_id,
      defined_goal_id,
      defined_goal_version,
      source_strategy_run_id
    )
    references public.strategy_runs (
      planning_unit_id,
      goal_id,
      defined_goal_id,
      defined_goal_version,
      strategy_run_id
    )
    on delete restrict,
  add constraint strategy_versions_authority_context_unique
    unique (planning_unit_id, goal_id, defined_goal_id, defined_goal_version, strategy_version_id);

create table if not exists public.goal_strategy_selections (
  planning_unit_id uuid not null references public.planning_units(planning_unit_id) on delete cascade,
  goal_id uuid not null references public.goals(goal_id) on delete cascade,
  defined_goal_id uuid not null,
  defined_goal_version integer not null check (defined_goal_version >= 1),
  strategy_version_id uuid not null,
  selected_at timestamptz not null default now(),
  primary key (planning_unit_id, goal_id),
  constraint goal_strategy_selections_defined_goal_fk
    foreign key (planning_unit_id, goal_id, defined_goal_id, defined_goal_version)
    references public.defined_goals (planning_unit_id, goal_id, defined_goal_id, version),
  constraint goal_strategy_selections_strategy_version_fk
    foreign key (
      planning_unit_id, goal_id, defined_goal_id, defined_goal_version, strategy_version_id
    )
    references public.strategy_versions (
      planning_unit_id, goal_id, defined_goal_id, defined_goal_version, strategy_version_id
    )
);

alter table public.goal_strategy_selections enable row level security;

drop policy if exists "goal_strategy_selections_select_own" on public.goal_strategy_selections;
create policy "goal_strategy_selections_select_own"
  on public.goal_strategy_selections for select
  using (exists (
    select 1 from public.planning_units pu
    where pu.planning_unit_id = goal_strategy_selections.planning_unit_id
      and pu.user_id = auth.uid()
  ));

drop policy if exists "goal_strategy_selections_insert_own" on public.goal_strategy_selections;
create policy "goal_strategy_selections_insert_own"
  on public.goal_strategy_selections for insert
  with check (exists (
    select 1 from public.planning_units pu
    where pu.planning_unit_id = goal_strategy_selections.planning_unit_id
      and pu.user_id = auth.uid()
  ));

drop policy if exists "goal_strategy_selections_update_own" on public.goal_strategy_selections;
create policy "goal_strategy_selections_update_own"
  on public.goal_strategy_selections for update
  using (exists (
    select 1 from public.planning_units pu
    where pu.planning_unit_id = goal_strategy_selections.planning_unit_id
      and pu.user_id = auth.uid()
  ))
  with check (exists (
    select 1 from public.planning_units pu
    where pu.planning_unit_id = goal_strategy_selections.planning_unit_id
      and pu.user_id = auth.uid()
  ));
