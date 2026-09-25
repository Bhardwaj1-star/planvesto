-- Specialized goal inputs are kept alongside the existing goal record so the
-- current Goal Planner UI/data model remains backward compatible.
ALTER TABLE IF EXISTS public.defined_goals
  ADD COLUMN IF NOT EXISTS specialized_data jsonb NOT NULL DEFAULT '{}'::jsonb;

CREATE INDEX IF NOT EXISTS idx_defined_goals_specialized_data
  ON public.defined_goals USING gin (specialized_data);
