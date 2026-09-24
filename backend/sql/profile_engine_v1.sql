-- Profile Engine v1
-- Apply through the Planvesto Supabase project migration workflow.
-- The backend uses the service role after API-level ownership verification.
-- RLS is enabled so these tables are not directly exposed to client roles by default.

create table if not exists public.profile_runs (
    profile_run_id uuid primary key default gen_random_uuid(),
    planning_unit_id text not null,
    investor_id text not null,
    version integer not null check (version > 0),
    profile_version text not null,
    engine_version text not null,
    financial_snapshot_id text null,
    input_snapshot jsonb not null default '{}'::jsonb,
    profile_result jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now(),
    unique (planning_unit_id, investor_id, version)
);

create table if not exists public.profile_constraints (
    profile_constraint_id uuid primary key default gen_random_uuid(),
    profile_run_id uuid not null references public.profile_runs(profile_run_id) on delete cascade,
    key text not null,
    value jsonb not null,
    unit text null,
    kind text not null check (kind in ('hard', 'soft')),
    source text not null check (source in ('financial_state', 'observed_behavior', 'declared_constraint', 'preference')),
    evidence jsonb not null default '[]'::jsonb,
    confidence numeric(5,4) not null check (confidence >= 0 and confidence <= 1),
    priority_rank integer null check (priority_rank is null or priority_rank > 0),
    valid_from timestamptz null,
    valid_until timestamptz null,
    created_at timestamptz not null default now()
);

create table if not exists public.profile_conflicts (
    profile_conflict_id uuid primary key default gen_random_uuid(),
    profile_run_id uuid not null references public.profile_runs(profile_run_id) on delete cascade,
    key text not null,
    status text not null check (status in ('unresolved', 'resolved')),
    reason text not null,
    sources jsonb not null default '[]'::jsonb,
    hard_constraint_present boolean not null default false,
    created_at timestamptz not null default now()
);

create index if not exists idx_profile_runs_lookup
    on public.profile_runs (planning_unit_id, investor_id, version desc);
create index if not exists idx_profile_constraints_run
    on public.profile_constraints (profile_run_id);
create index if not exists idx_profile_conflicts_run
    on public.profile_conflicts (profile_run_id);

alter table public.profile_runs enable row level security;
alter table public.profile_constraints enable row level security;
alter table public.profile_conflicts enable row level security;
