-- Planvesto Strategy Builder
-- Initial database schema

create extension if not exists "pgcrypto";


-- =========================================================
-- INVESTORS
-- =========================================================

create table if not exists public.investors (
    id uuid primary key default gen_random_uuid(),

    user_id uuid not null
        references auth.users(id)
        on delete cascade,

    name text,
    email text,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint investors_user_id_unique unique (user_id)
);


-- =========================================================
-- STRATEGY INPUTS
-- =========================================================

create table if not exists public.strategy_inputs (
    id uuid primary key default gen_random_uuid(),

    investor_id uuid not null
        references public.investors(id)
        on delete cascade,

    goal_amount numeric(18,2) not null,
    time_horizon_years integer not null,
    current_corpus numeric(18,2) not null default 0,
    monthly_investment numeric(18,2) not null default 0,
    existing_investments numeric(18,2) not null default 0,
    expected_annual_return numeric(8,4) not null,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint strategy_inputs_goal_positive
        check (goal_amount > 0),

    constraint strategy_inputs_horizon_positive
        check (time_horizon_years > 0),

    constraint strategy_inputs_current_corpus_nonnegative
        check (current_corpus >= 0),

    constraint strategy_inputs_monthly_investment_nonnegative
        check (monthly_investment >= 0),

    constraint strategy_inputs_existing_investments_nonnegative
        check (existing_investments >= 0),

    constraint strategy_inputs_return_valid
        check (
            expected_annual_return >= 0
            and expected_annual_return <= 100
        )
);


-- =========================================================
-- STRATEGY RESULTS
-- =========================================================

create table if not exists public.strategy_results (
    id uuid primary key default gen_random_uuid(),

    investor_id uuid not null
        references public.investors(id)
        on delete cascade,

    strategy_input_id uuid not null
        references public.strategy_inputs(id)
        on delete cascade,

    strategy_id text not null,
    strategy_name text not null,

    monthly_investment numeric(18,2) not null default 0,
    time_horizon_years integer not null,
    initial_capital numeric(18,2) not null default 0,
    projected_corpus numeric(18,2) not null default 0,
    funding_gap numeric(18,2) not null default 0,
    total_contribution numeric(18,2) not null default 0,

    created_at timestamptz not null default now(),

    constraint strategy_results_monthly_nonnegative
        check (monthly_investment >= 0),

    constraint strategy_results_horizon_positive
        check (time_horizon_years > 0),

    constraint strategy_results_initial_capital_nonnegative
        check (initial_capital >= 0),

    constraint strategy_results_projected_corpus_nonnegative
        check (projected_corpus >= 0),

    constraint strategy_results_funding_gap_nonnegative
        check (funding_gap >= 0),

    constraint strategy_results_total_contribution_nonnegative
        check (total_contribution >= 0)
);


-- =========================================================
-- INDEXES
-- =========================================================

create index if not exists idx_investors_user_id
    on public.investors(user_id);

create index if not exists idx_strategy_inputs_investor_id
    on public.strategy_inputs(investor_id);

create index if not exists idx_strategy_results_investor_id
    on public.strategy_results(investor_id);

create index if not exists idx_strategy_results_input_id
    on public.strategy_results(strategy_input_id);


-- =========================================================
-- ROW LEVEL SECURITY
-- =========================================================

alter table public.investors enable row level security;
alter table public.strategy_inputs enable row level security;
alter table public.strategy_results enable row level security;


-- =========================================================
-- INVESTOR POLICIES
-- =========================================================

drop policy if exists "Users can view their own investor profile"
on public.investors;

create policy "Users can view their own investor profile"
on public.investors
for select
to authenticated
using (user_id = auth.uid());


drop policy if exists "Users can create their own investor profile"
on public.investors;

create policy "Users can create their own investor profile"
on public.investors
for insert
to authenticated
with check (user_id = auth.uid());


drop policy if exists "Users can update their own investor profile"
on public.investors;

create policy "Users can update their own investor profile"
on public.investors
for update
to authenticated
using (user_id = auth.uid())
with check (user_id = auth.uid());


-- =========================================================
-- STRATEGY INPUT POLICIES
-- =========================================================

drop policy if exists "Users can view their own strategy inputs"
on public.strategy_inputs;

create policy "Users can view their own strategy inputs"
on public.strategy_inputs
for select
to authenticated
using (
    exists (
        select 1
        from public.investors i
        where i.id = strategy_inputs.investor_id
        and i.user_id = auth.uid()
    )
);


drop policy if exists "Users can create their own strategy inputs"
on public.strategy_inputs;

create policy "Users can create their own strategy inputs"
on public.strategy_inputs
for insert
to authenticated
with check (
    exists (
        select 1
        from public.investors i
        where i.id = strategy_inputs.investor_id
        and i.user_id = auth.uid()
    )
);


drop policy if exists "Users can update their own strategy inputs"
on public.strategy_inputs;

create policy "Users can update their own strategy inputs"
on public.strategy_inputs
for update
to authenticated
using (
    exists (
        select 1
        from public.investors i
        where i.id = strategy_inputs.investor_id
        and i.user_id = auth.uid()
    )
)
with check (
    exists (
        select 1
        from public.investors i
        where i.id = strategy_inputs.investor_id
        and i.user_id = auth.uid()
    )
);


-- =========================================================
-- STRATEGY RESULT POLICIES
-- =========================================================

drop policy if exists "Users can view their own strategy results"
on public.strategy_results;

create policy "Users can view their own strategy results"
on public.strategy_results
for select
to authenticated
using (
    exists (
        select 1
        from public.investors i
        where i.id = strategy_results.investor_id
        and i.user_id = auth.uid()
    )
);


drop policy if exists "Users can create their own strategy results"
on public.strategy_results;

create policy "Users can create their own strategy results"
on public.strategy_results
for insert
to authenticated
with check (
    exists (
        select 1
        from public.investors i
        where i.id = strategy_results.investor_id
        and i.user_id = auth.uid()
    )
);