alter table public.assets
  add column if not exists monthly_contribution_amount numeric(15,2) not null default 0,
  add column if not exists monthly_contribution_frequency text not null default 'Monthly';

alter table public.assets
  drop constraint if exists assets_monthly_contribution_amount_non_negative;

alter table public.assets
  add constraint assets_monthly_contribution_amount_non_negative
  check (monthly_contribution_amount >= 0);

alter table public.assets
  drop constraint if exists assets_monthly_contribution_frequency_check;

alter table public.assets
  add constraint assets_monthly_contribution_frequency_check
  check (monthly_contribution_frequency in ('Monthly', 'Annual'));
