-- Goal Planner v2: type-driven goal definitions.
-- Existing goals remain compatible; generic one-time goals continue to work.

ALTER TABLE public.goals
    ADD COLUMN IF NOT EXISTS goal_type TEXT NOT NULL DEFAULT 'Other',
    ADD COLUMN IF NOT EXISTS goal_details JSONB NOT NULL DEFAULT '{}'::jsonb;

ALTER TABLE public.goals
    ALTER COLUMN target_amount DROP NOT NULL;

ALTER TABLE public.goals
    ADD CONSTRAINT goals_target_amount_non_negative_v2
    CHECK (target_amount IS NULL OR target_amount >= 0);

ALTER TABLE public.goals
    ADD CONSTRAINT goals_goal_type_check_v2
    CHECK (goal_type IN (
        'Emergency Fund',
        'Child Education',
        'Child Marriage',
        'Home Purchase',
        'Vehicle',
        'Retirement',
        'Travel',
        'Business',
        'Wealth Creation',
        'Other'
    ));

CREATE INDEX IF NOT EXISTS idx_goals_planning_unit_goal_type
    ON public.goals(planning_unit_id, goal_type);

COMMENT ON COLUMN public.goals.goal_type IS
    'Goal Planner calculation model. Specialized types may derive target_amount.';

COMMENT ON COLUMN public.goals.goal_details IS
    'Type-specific inputs used by the Goal Planner calculation engine.';
