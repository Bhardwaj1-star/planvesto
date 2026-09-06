alter table public.strategy_results
add column if not exists annual_return numeric(8,4) not null default 0;