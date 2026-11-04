create table if not exists public.goal_funding_assessments (
    assessment_id uuid primary key default gen_random_uuid(),
    planning_unit_id uuid not null,
    goal_id uuid not null,
    defined_goal_id uuid not null,
    defined_goal_version integer not null check (defined_goal_version > 0),
    version integer not null check (version > 0),
    status text not null check (status in ('insufficient_evidence', 'ready_for_investor_review')),
    entry_route text not null check (entry_route in ('steps_1_to_3_then_step_4', 'step_4_direct')),
    goal_handoff jsonb not null default '{}'::jsonb,
    self_money jsonb not null,
    self_money_financing jsonb not null,
    comparison jsonb not null default '{}'::jsonb,
    investor_decision text null check (investor_decision in ('self_money', 'self_money_financing')),
    investor_decision_confirmed boolean not null default false,
    decision_notes text null,
    created_at timestamptz not null default now(),
    constraint goal_funding_assessment_goal_fk
        foreign key (planning_unit_id, goal_id)
        references public.goals(planning_unit_id, goal_id) on delete cascade,
    constraint goal_funding_assessment_defined_goal_fk
        foreign key (planning_unit_id, goal_id, defined_goal_id, defined_goal_version)
        references public.defined_goals(planning_unit_id, goal_id, defined_goal_id, version) on delete cascade,
    unique (planning_unit_id, goal_id, version)
);

create index if not exists idx_goal_funding_assessments_latest
    on public.goal_funding_assessments (planning_unit_id, goal_id, version desc);

alter table public.goal_funding_assessments enable row level security;

drop policy if exists "users can access their goal funding assessments" on public.goal_funding_assessments;
drop policy if exists "goal_funding_assessments_select_own" on public.goal_funding_assessments;
drop policy if exists "goal_funding_assessments_insert_own" on public.goal_funding_assessments;

create policy "goal_funding_assessments_select_own"
    on public.goal_funding_assessments for select
    using (exists (
        select 1 from public.planning_units pu
        where pu.planning_unit_id = goal_funding_assessments.planning_unit_id
          and pu.user_id = auth.uid()
    ));

create policy "goal_funding_assessments_insert_own"
    on public.goal_funding_assessments for insert
    with check (exists (
        select 1 from public.planning_units pu
        where pu.planning_unit_id = goal_funding_assessments.planning_unit_id
          and pu.user_id = auth.uid()
    ));

create or replace function public.prevent_goal_funding_assessment_mutation()
returns trigger language plpgsql as $$
begin
    raise exception 'goal_funding_assessments are immutable snapshots';
end;
$$;

drop trigger if exists goal_funding_assessments_immutable on public.goal_funding_assessments;
create trigger goal_funding_assessments_immutable
before update or delete on public.goal_funding_assessments
for each row execute function public.prevent_goal_funding_assessment_mutation();

comment on table public.goal_funding_assessments is
'Immutable Goal Funding assessments for Self Money and Self Money + Financing. Does not execute transactions or mutate Accepted Plans.';
