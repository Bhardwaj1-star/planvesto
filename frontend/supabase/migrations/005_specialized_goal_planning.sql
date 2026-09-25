-- Specialized Goal Planning
-- Keeps the existing goals model intact while allowing goal-type-specific inputs.

ALTER TABLE public.goals
  ADD COLUMN IF NOT EXISTS goal_parameters JSONB NOT NULL DEFAULT '{}'::jsonb;

ALTER TABLE public.defined_goals
  ADD COLUMN IF NOT EXISTS goal_parameters JSONB NOT NULL DEFAULT '{}'::jsonb;

COMMENT ON COLUMN public.goals.goal_parameters IS
  'Goal-type-specific planning inputs. Keys are controlled by the Goal Planner contract.';

COMMENT ON COLUMN public.defined_goals.goal_parameters IS
  'Snapshot of goal-type-specific planning inputs used for this DefinedGoal version.';

CREATE INDEX IF NOT EXISTS idx_goals_goal_type
  ON public.goals (goal_type);

CREATE INDEX IF NOT EXISTS idx_defined_goals_goal_type
  ON public.defined_goals (goal_type);
