-- =========================================================
-- PLANVESTO — FINANCIAL PLANNING DATABASE
-- PostgreSQL / Supabase
-- =========================================================

-- UUID generation
create extension if not exists pgcrypto;


-- =========================================================
-- 1. PLANNING UNITS
-- =========================================================

create table planning_units (
    planning_unit_id uuid primary key default gen_random_uuid(),

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);


-- =========================================================
-- 2. INVESTORS / PLANNING PARTICIPANTS
-- =========================================================

create table investors (
    investor_id uuid primary key default gen_random_uuid(),

    planning_unit_id uuid not null,

    full_name text not null,
    date_of_birth date,
    gender text,
    marital_status text,

    mobile_number text,
    address text,
    city text,
    state text,
    country text,

    occupation text,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint fk_investor_planning_unit
        foreign key (planning_unit_id)
        references planning_units(planning_unit_id)
        on delete cascade
);


-- =========================================================
-- 3. DEPENDENTS
-- =========================================================

create table dependents (
    dependent_id uuid primary key default gen_random_uuid(),

    planning_unit_id uuid not null,

    name text not null,
    relationship text,
    date_of_birth date,
    occupation text,
    financial_dependency boolean,

    -- If TRUE, this dependent is to be included
    -- as a planning participant.
    include_in_planning boolean not null default false,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint fk_dependent_planning_unit
        foreign key (planning_unit_id)
        references planning_units(planning_unit_id)
        on delete cascade
);


-- =========================================================
-- 4. INCOME
-- =========================================================

create table income (
    income_id uuid primary key default gen_random_uuid(),

    planning_unit_id uuid not null,
    investor_id uuid not null,

    income_type text not null,
    amount numeric(15,2) not null,
    frequency text not null,
    growth_assumption numeric(8,4),

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint income_amount_non_negative
        check (amount >= 0),

    constraint fk_income_planning_unit
        foreign key (planning_unit_id)
        references planning_units(planning_unit_id)
        on delete cascade,

    constraint fk_income_investor
        foreign key (investor_id)
        references investors(investor_id)
        on delete cascade
);


-- =========================================================
-- 5. EXPENSES
-- =========================================================

create table expenses (
    expense_id uuid primary key default gen_random_uuid(),

    planning_unit_id uuid not null,

    expense_type text not null,
    amount numeric(15,2) not null,
    frequency text not null,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint expense_amount_non_negative
        check (amount >= 0),

    constraint fk_expense_planning_unit
        foreign key (planning_unit_id)
        references planning_units(planning_unit_id)
        on delete cascade
);


-- =========================================================
-- 6. EXPENSE PARTICIPANTS
-- =========================================================

create table expense_participants (
    expense_participant_id uuid primary key default gen_random_uuid(),

    expense_id uuid not null,
    investor_id uuid not null,

    participation_percentage numeric(6,3) not null,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint expense_participation_range
        check (
            participation_percentage >= 0
            and participation_percentage <= 100
        ),

    constraint fk_expense_participant_expense
        foreign key (expense_id)
        references expenses(expense_id)
        on delete cascade,

    constraint fk_expense_participant_investor
        foreign key (investor_id)
        references investors(investor_id)
        on delete cascade,

    constraint unique_expense_participant
        unique (expense_id, investor_id)
);


-- =========================================================
-- 7. ASSETS
-- =========================================================

create table assets (
    asset_id uuid primary key default gen_random_uuid(),

    planning_unit_id uuid not null,

    asset_name text not null,
    current_value numeric(15,2) not null,
    purchase_value numeric(15,2),
    purchase_date date,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint asset_current_value_non_negative
        check (current_value >= 0),

    constraint asset_purchase_value_non_negative
        check (
            purchase_value is null
            or purchase_value >= 0
        ),

    constraint fk_asset_planning_unit
        foreign key (planning_unit_id)
        references planning_units(planning_unit_id)
        on delete cascade
);


-- =========================================================
-- 8. ASSET OWNERS
-- =========================================================

create table asset_owners (
    asset_owner_id uuid primary key default gen_random_uuid(),

    asset_id uuid not null,
    investor_id uuid not null,

    ownership_percentage numeric(6,3) not null,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint asset_ownership_range
        check (
            ownership_percentage >= 0
            and ownership_percentage <= 100
        ),

    constraint fk_asset_owner_asset
        foreign key (asset_id)
        references assets(asset_id)
        on delete cascade,

    constraint fk_asset_owner_investor
        foreign key (investor_id)
        references investors(investor_id)
        on delete cascade,

    constraint unique_asset_owner
        unique (asset_id, investor_id)
);


-- =========================================================
-- 9. LIABILITIES
-- =========================================================

create table liabilities (
    liability_id uuid primary key default gen_random_uuid(),

    planning_unit_id uuid not null,

    liability_name text not null,
    outstanding_amount numeric(15,2) not null,
    interest_rate numeric(8,4),
    emi_amount numeric(15,2),
    frequency text,
    end_date date,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint liability_outstanding_non_negative
        check (outstanding_amount >= 0),

    constraint liability_emi_non_negative
        check (
            emi_amount is null
            or emi_amount >= 0
        ),

    constraint fk_liability_planning_unit
        foreign key (planning_unit_id)
        references planning_units(planning_unit_id)
        on delete cascade
);


-- =========================================================
-- 10. LIABILITY RESPONSIBILITIES
-- =========================================================

create table liability_responsibilities (
    liability_responsibility_id uuid primary key default gen_random_uuid(),

    liability_id uuid not null,
    investor_id uuid not null,

    responsibility_percentage numeric(6,3) not null,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint liability_responsibility_range
        check (
            responsibility_percentage >= 0
            and responsibility_percentage <= 100
        ),

    constraint fk_liability_responsibility_liability
        foreign key (liability_id)
        references liabilities(liability_id)
        on delete cascade,

    constraint fk_liability_responsibility_investor
        foreign key (investor_id)
        references investors(investor_id)
        on delete cascade,

    constraint unique_liability_responsibility
        unique (liability_id, investor_id)
);


-- =========================================================
-- 11. COMMITMENTS
-- =========================================================

create table commitments (
    commitment_id uuid primary key default gen_random_uuid(),

    planning_unit_id uuid not null,

    commitment_name text not null,
    amount numeric(15,2) not null,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint commitment_amount_non_negative
        check (amount >= 0),

    constraint fk_commitment_planning_unit
        foreign key (planning_unit_id)
        references planning_units(planning_unit_id)
        on delete cascade
);


-- =========================================================
-- 12. COMMITMENT PARTICIPANTS
-- =========================================================

create table commitment_participants (
    commitment_participant_id uuid primary key default gen_random_uuid(),

    commitment_id uuid not null,
    investor_id uuid not null,

    participation_percentage numeric(6,3) not null,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint commitment_participation_range
        check (
            participation_percentage >= 0
            and participation_percentage <= 100
        ),

    constraint fk_commitment_participant_commitment
        foreign key (commitment_id)
        references commitments(commitment_id)
        on delete cascade,

    constraint fk_commitment_participant_investor
        foreign key (investor_id)
        references investors(investor_id)
        on delete cascade,

    constraint unique_commitment_participant
        unique (commitment_id, investor_id)
);


-- =========================================================
-- 13. GOALS
-- =========================================================

create table goals (
    goal_id uuid primary key default gen_random_uuid(),

    planning_unit_id uuid not null,

    goal_name text not null,
    target_amount numeric(15,2) not null,
    target_date date,
    priority text,
    flexibility text,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint goal_target_amount_non_negative
        check (target_amount >= 0),

    constraint fk_goal_planning_unit
        foreign key (planning_unit_id)
        references planning_units(planning_unit_id)
        on delete cascade
);


-- =========================================================
-- 14. GOAL FUNDING
-- =========================================================

create table goal_funding (
    goal_funding_id uuid primary key default gen_random_uuid(),

    goal_id uuid not null,
    asset_id uuid not null,

    allocation_percentage numeric(6,3) not null,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint goal_allocation_range
        check (
            allocation_percentage >= 0
            and allocation_percentage <= 100
        ),

    constraint fk_goal_funding_goal
        foreign key (goal_id)
        references goals(goal_id)
        on delete cascade,

    constraint fk_goal_funding_asset
        foreign key (asset_id)
        references assets(asset_id)
        on delete cascade,

    constraint unique_goal_asset
        unique (goal_id, asset_id)
);


-- =========================================================
-- INDEXES
-- =========================================================

create index idx_investors_planning_unit
    on investors(planning_unit_id);

create index idx_dependents_planning_unit
    on dependents(planning_unit_id);

create index idx_income_planning_unit
    on income(planning_unit_id);

create index idx_income_investor
    on income(investor_id);

create index idx_expenses_planning_unit
    on expenses(planning_unit_id);

create index idx_expense_participants_expense
    on expense_participants(expense_id);

create index idx_expense_participants_investor
    on expense_participants(investor_id);

create index idx_assets_planning_unit
    on assets(planning_unit_id);

create index idx_asset_owners_asset
    on asset_owners(asset_id);

create index idx_asset_owners_investor
    on asset_owners(investor_id);

create index idx_liabilities_planning_unit
    on liabilities(planning_unit_id);

create index idx_liability_responsibilities_liability
    on liability_responsibilities(liability_id);

create index idx_liability_responsibilities_investor
    on liability_responsibilities(investor_id);

create index idx_commitments_planning_unit
    on commitments(planning_unit_id);

create index idx_commitment_participants_commitment
    on commitment_participants(commitment_id);

create index idx_commitment_participants_investor
    on commitment_participants(investor_id);

create index idx_goals_planning_unit
    on goals(planning_unit_id);

create index idx_goal_funding_goal
    on goal_funding(goal_id);

create index idx_goal_funding_asset
    on goal_funding(asset_id);