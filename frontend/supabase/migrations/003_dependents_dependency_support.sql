-- Migration 003: Add support for dependencyLevel, dependencyAreas, and dependencyDuration
-- to the dependents table, preserving all existing rows.

alter table public.dependents
  add column if not exists dependency_level text check (dependency_level in ('Fully', 'Partially', 'None')),
  add column if not exists dependency_areas text[] default '{}'::text[],
  add column if not exists dependency_duration integer;

-- Safely backfill existing rows:
-- If financial_dependency is true and dependency_level is null, backfill 'Fully'
-- If financial_dependency is false and dependency_level is null, backfill 'None'
update public.dependents
set dependency_level = case
  when financial_dependency = true then 'Fully'
  when financial_dependency = false then 'None'
  else dependency_level
end
where dependency_level is null and financial_dependency is not null;

-- Ensure dependency_areas default array for existing null rows
update public.dependents
set dependency_areas = '{}'::text[]
where dependency_areas is null;
