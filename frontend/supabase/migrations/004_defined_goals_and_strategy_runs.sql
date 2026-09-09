-- =========================================================
-- Migration 004: DefinedGoal Versioning & Strategy Runs
-- =========================================================

-- 1. DEFINED GOALS (Immutable snapshots of goal planning state)
CREATE TABLE IF NOT EXISTS public.defined_goals (
    defined_goal_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    goal_id UUID NOT NULL REFERENCES public.goals(goal_id) ON DELETE CASCADE,
    planning_unit_id UUID NOT NULL REFERENCES public.planning_units(planning_unit_id) ON DELETE CASCADE,
    investor_id UUID REFERENCES public.investors(investor_id) ON DELETE SET NULL,
    version INTEGER NOT NULL DEFAULT 1,
    is_latest BOOLEAN NOT NULL DEFAULT TRUE,
    goal_type TEXT NOT NULL,
    goal_name TEXT NOT NULL,
    today_cost NUMERIC(15,2) NOT NULL,
    inflation_rate NUMERIC(6,4) NOT NULL,
    inflation_source TEXT NOT NULL DEFAULT 'default',
    target_month INTEGER NOT NULL,
    target_year INTEGER NOT NULL,
    duration_years NUMERIC(6,3) NOT NULL,
    future_target NUMERIC(15,2) NOT NULL,
    priority TEXT NOT NULL,
    flexibility TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Active',
    projected_mapped_asset_value NUMERIC(15,2) NOT NULL DEFAULT 0,
    funding_gap NUMERIC(15,2) NOT NULL,
    funding_status TEXT NOT NULL,
    version_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT unique_goal_version UNIQUE (goal_id, version)
);

-- 2. DEFINED GOAL ASSET MAPPINGS (Immutable asset allocation snapshot for each DefinedGoal version)
CREATE TABLE IF NOT EXISTS public.defined_goal_asset_mappings (
    mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    defined_goal_id UUID NOT NULL REFERENCES public.defined_goals(defined_goal_id) ON DELETE CASCADE,
    asset_id UUID NOT NULL REFERENCES public.assets(asset_id) ON DELETE CASCADE,
    allocation_type TEXT NOT NULL,
    allocation_value NUMERIC(15,2) NOT NULL,
    allocated_amount NUMERIC(15,2) NOT NULL,
    allocated_percentage NUMERIC(6,3) NOT NULL,
    expected_return NUMERIC(6,4) NOT NULL,
    return_frequency TEXT NOT NULL DEFAULT 'annual',
    projected_value NUMERIC(15,2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3. STRATEGY RUNS (Execution records of Strategy Builder)
CREATE TABLE IF NOT EXISTS public.strategy_runs (
    strategy_run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    planning_unit_id UUID NOT NULL REFERENCES public.planning_units(planning_unit_id) ON DELETE CASCADE,
    goal_id UUID NOT NULL REFERENCES public.goals(goal_id) ON DELETE CASCADE,
    defined_goal_id UUID NOT NULL REFERENCES public.defined_goals(defined_goal_id) ON DELETE CASCADE,
    defined_goal_version INTEGER NOT NULL,
    run_version INTEGER NOT NULL DEFAULT 1,
    is_latest BOOLEAN NOT NULL DEFAULT TRUE,
    status TEXT NOT NULL DEFAULT 'completed',
    investor_priorities JSONB NOT NULL DEFAULT '{}'::jsonb,
    applicable_strategies JSONB NOT NULL DEFAULT '[]'::jsonb,
    scenarios JSONB NOT NULL DEFAULT '[]'::jsonb,
    comparison_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
    ranking_snapshot JSONB NOT NULL DEFAULT '[]'::jsonb,
    recommendation JSONB NOT NULL DEFAULT '{}'::jsonb,
    selected_strategy_id TEXT,
    selected_scenario_id TEXT,
    selected_implementation_parameters JSONB NOT NULL DEFAULT '{}'::jsonb,
    selection_timestamp TIMESTAMPTZ,
    run_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT unique_goal_run_version UNIQUE (goal_id, run_version)
);

-- 4. STRATEGY SCENARIOS (Separate persistence for baseline vs investor-customized/modified scenarios)
CREATE TABLE IF NOT EXISTS public.strategy_scenarios (
    scenario_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strategy_run_id UUID NOT NULL REFERENCES public.strategy_runs(strategy_run_id) ON DELETE CASCADE,
    strategy_id TEXT NOT NULL,
    scenario_type TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    assumptions JSONB NOT NULL DEFAULT '{}'::jsonb,
    funding_structure JSONB NOT NULL DEFAULT '{}'::jsonb,
    metrics JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_investor_modified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 5. INDEXES
CREATE INDEX IF NOT EXISTS idx_defined_goals_pu ON public.defined_goals(planning_unit_id);
CREATE INDEX IF NOT EXISTS idx_defined_goals_goal_latest ON public.defined_goals(goal_id, is_latest);
CREATE INDEX IF NOT EXISTS idx_defined_goal_asset_mappings_goal ON public.defined_goal_asset_mappings(defined_goal_id);
CREATE INDEX IF NOT EXISTS idx_strategy_runs_pu ON public.strategy_runs(planning_unit_id);
CREATE INDEX IF NOT EXISTS idx_strategy_runs_goal_latest ON public.strategy_runs(goal_id, is_latest);
CREATE INDEX IF NOT EXISTS idx_strategy_scenarios_run ON public.strategy_scenarios(strategy_run_id);

-- 6. ROW LEVEL SECURITY
ALTER TABLE public.defined_goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.defined_goal_asset_mappings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.strategy_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.strategy_scenarios ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "users can access their defined goals" ON public.defined_goals;
CREATE POLICY "users can access their defined goals"
  ON public.defined_goals FOR ALL
  USING (EXISTS (SELECT 1 FROM public.planning_units WHERE planning_unit_id = defined_goals.planning_unit_id AND user_id = auth.uid()))
  WITH CHECK (EXISTS (SELECT 1 FROM public.planning_units WHERE planning_unit_id = defined_goals.planning_unit_id AND user_id = auth.uid()));

DROP POLICY IF EXISTS "users can access their defined goal asset mappings" ON public.defined_goal_asset_mappings;
CREATE POLICY "users can access their defined goal asset mappings"
  ON public.defined_goal_asset_mappings FOR ALL
  USING (EXISTS (SELECT 1 FROM public.defined_goals JOIN public.planning_units USING (planning_unit_id) WHERE defined_goals.defined_goal_id = defined_goal_asset_mappings.defined_goal_id AND planning_units.user_id = auth.uid()))
  WITH CHECK (EXISTS (SELECT 1 FROM public.defined_goals JOIN public.planning_units USING (planning_unit_id) WHERE defined_goals.defined_goal_id = defined_goal_asset_mappings.defined_goal_id AND planning_units.user_id = auth.uid()));

DROP POLICY IF EXISTS "users can access their strategy runs" ON public.strategy_runs;
CREATE POLICY "users can access their strategy runs"
  ON public.strategy_runs FOR ALL
  USING (EXISTS (SELECT 1 FROM public.planning_units WHERE planning_unit_id = strategy_runs.planning_unit_id AND user_id = auth.uid()))
  WITH CHECK (EXISTS (SELECT 1 FROM public.planning_units WHERE planning_unit_id = strategy_runs.planning_unit_id AND user_id = auth.uid()));

DROP POLICY IF EXISTS "users can access their strategy scenarios" ON public.strategy_scenarios;
CREATE POLICY "users can access their strategy scenarios"
  ON public.strategy_scenarios FOR ALL
  USING (EXISTS (SELECT 1 FROM public.strategy_runs JOIN public.planning_units USING (planning_unit_id) WHERE strategy_runs.strategy_run_id = strategy_scenarios.strategy_run_id AND planning_units.user_id = auth.uid()))
  WITH CHECK (EXISTS (SELECT 1 FROM public.strategy_runs JOIN public.planning_units USING (planning_unit_id) WHERE strategy_runs.strategy_run_id = strategy_scenarios.strategy_run_id AND planning_units.user_id = auth.uid()));
