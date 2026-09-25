-- Insurance policies are the source of truth for protection + investment-linked insurance.
-- A policy may optionally materialize one asset (current/surrender value) and one
-- expense (premium). The linked rows prevent double-counting elsewhere.

create table if not exists public.insurance_policies (
    policy_id uuid primary key default gen_random_uuid(),
    planning_unit_id uuid not null,
    policy_name text not null,
    insurer text,
    policy_number text,
    policy_type text,
    premium numeric(15,2),
    premium_frequency text,
    sum_assured numeric(15,2),
    current_value numeric(15,2),
    maturity_date date,
    maturity_value numeric(15,2),
    asset_id uuid,
    expense_id uuid,
    source text not null default 'manual',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint fk_insurance_policy_planning_unit
        foreign key (planning_unit_id)
        references public.planning_units(planning_unit_id)
        on delete cascade,
    constraint fk_insurance_policy_asset
        foreign key (asset_id)
        references public.assets(asset_id)
        on delete set null,
    constraint fk_insurance_policy_expense
        foreign key (expense_id)
        references public.expenses(expense_id)
        on delete set null,
    constraint insurance_premium_non_negative
        check (premium is null or premium >= 0),
    constraint insurance_sum_assured_non_negative
        check (sum_assured is null or sum_assured >= 0),
    constraint insurance_current_value_non_negative
        check (current_value is null or current_value >= 0),
    constraint insurance_maturity_value_non_negative
        check (maturity_value is null or maturity_value >= 0)
);

create index if not exists idx_insurance_policies_planning_unit
    on public.insurance_policies(planning_unit_id);

alter table public.insurance_policies enable row level security;

drop policy if exists "users can access their insurance policies" on public.insurance_policies;
create policy "users can access their insurance policies"
  on public.insurance_policies for all
  using (exists (
    select 1 from public.planning_units
    where planning_units.planning_unit_id = insurance_policies.planning_unit_id
      and planning_units.user_id = auth.uid()
  ))
  with check (exists (
    select 1 from public.planning_units
    where planning_units.planning_unit_id = insurance_policies.planning_unit_id
      and planning_units.user_id = auth.uid()
  ));
