-- PLANVESTO — PROFILE ENGINE
-- Immutable, versioned investor profiles.

create table if not exists public.profile_runs (
    profile_run_id uuid primary key default gen_random_uuid(),
    planning_unit_id uuid not null references public.planning_units(planning_unit_id) on delete cascade,
    investor_id uuid not null references public.investors(investor_id) on delete cascade,
    version integer not null,
    engine_version text not null,
    questionnaire_version text not null,
    financial_snapshot_id uuid null references public.financial_state_snapshots(snapshot_id) on delete set null,
    completeness numeric(6,4) not null check (completeness >= 0 and completeness <= 1),
    input_snapshot jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now(),
    constraint unique_profile_version unique (planning_unit_id, investor_id, version)
);

create table if not exists public.profile_dimensions (
    profile_dimension_id uuid primary key default gen_random_uuid(),
    profile_run_id uuid not null references public.profile_runs(profile_run_id) on delete cascade,
    dimension_key text not null,
    score numeric(8,4) not null check (score >= 0 and score <= 100),
    band text not null,
    confidence numeric(6,4) not null check (confidence >= 0 and confidence <= 1),
    components jsonb not null default '{}'::jsonb,
    explanations jsonb not null default '[]'::jsonb,
    created_at timestamptz not null default now(),
    constraint unique_profile_dimension unique (profile_run_id, dimension_key)
);

create index if not exists idx_profile_runs_investor_version
    on public.profile_runs(planning_unit_id, investor_id, version desc);
create index if not exists idx_profile_dimensions_run
    on public.profile_dimensions(profile_run_id);

alter table public.profile_runs enable row level security;
alter table public.profile_dimensions enable row level security;

drop policy if exists "profile_runs_select_own" on public.profile_runs;
create policy "profile_runs_select_own" on public.profile_runs for select using (
    exists (select 1 from public.planning_units pu where pu.planning_unit_id = profile_runs.planning_unit_id and pu.user_id = auth.uid())
);

drop policy if exists "profile_runs_insert_own" on public.profile_runs;
create policy "profile_runs_insert_own" on public.profile_runs for insert with check (
    exists (select 1 from public.planning_units pu where pu.planning_unit_id = profile_runs.planning_unit_id and pu.user_id = auth.uid())
);

drop policy if exists "profile_dimensions_select_own" on public.profile_dimensions;
create policy "profile_dimensions_select_own" on public.profile_dimensions for select using (
    exists (
        select 1 from public.profile_runs pr join public.planning_units pu using (planning_unit_id)
        where pr.profile_run_id = profile_dimensions.profile_run_id and pu.user_id = auth.uid()
    )
);

drop policy if exists "profile_dimensions_insert_own" on public.profile_dimensions;
create policy "profile_dimensions_insert_own" on public.profile_dimensions for insert with check (
    exists (
        select 1 from public.profile_runs pr join public.planning_units pu using (planning_unit_id)
        where pr.profile_run_id = profile_dimensions.profile_run_id and pu.user_id = auth.uid()
    )
);

create or replace function public.prevent_profile_mutation()
returns trigger language plpgsql as $$
begin
    raise exception 'profile history is immutable';
end;
$$;

drop trigger if exists profile_runs_immutable on public.profile_runs;
create trigger profile_runs_immutable before update or delete on public.profile_runs
for each row execute function public.prevent_profile_mutation();

drop trigger if exists profile_dimensions_immutable on public.profile_dimensions;
create trigger profile_dimensions_immutable before update or delete on public.profile_dimensions
for each row execute function public.prevent_profile_mutation();
