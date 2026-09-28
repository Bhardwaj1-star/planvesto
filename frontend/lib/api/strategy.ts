import { apiRequest, apiRequestBlob } from "./client";

export type InvestorPriorities = {
  safety: number;
  liquidity: number;
  growth: number;
  flexibility: number;
};

export type StrategyImplementationParamDef = {
  name: string;
  label: string;
  param_type: "currency" | "percentage" | "integer" | "choice";
  description: string;
  default_value: unknown;
  editable: boolean;
  min_value?: number | null;
  max_value?: number | null;
  choices?: string[];
};

export type StrategyDefinition = {
  strategy_id: string;
  name: string;
  tagline: string;
  description: string;
  strategy_family: string;
  strategic_objective: string;
  core_mechanism: string;
  principles: string[];
  constraints: string[];
  dependencies: string[];
  required_inputs: string[];
  applicable_goal_characteristics: string[];
  applicable_goal_types: string[];
  technique_ids: string[];
  strategic_levers: string[];
  compatible_strategy_ids: string[];
  conflicting_strategy_ids: string[];
  library_version: string;
  implementation_version: string;
  active: boolean;
  implementation_parameters: StrategyImplementationParamDef[];
  good_outcomes: string[];
  bad_outcomes: string[];
  trade_offs: string[];
  baseline_safety_score: number;
  baseline_liquidity_score: number;
  baseline_growth_score: number;
  baseline_flexibility_score: number;
};

export type StrategyArchitecture = {
  architecture_id: string;
  primary_strategy_id: string;
  supporting_strategy_ids: string[];
  technique_ids: string[];
  rationale: string[];
  trade_offs: string[];
  feasibility_status: "feasible" | "conditional" | "infeasible";
  constraints: string[];
};

export type Scenario = {
  scenario_id: string;
  strategy_id: string;
  scenario_type: "baseline" | "modified" | "custom";
  scenario_name: string;
  assumptions: Record<string, unknown>;
  funding_structure: Record<string, unknown>;
  metrics: Record<string, unknown>;
  trade_off_notes: string;
  is_investor_modified: boolean;
};

export type StrategyRankingItem = {
  rank: number;
  strategy_id: string;
  scenario_id: string;
  strategy_name: string;
  scenario_name: string;
  composite_score: number;
  dimension_scores: Record<string, number>;
  is_recommended: boolean;
  evidence_scores?: Record<string, unknown>;
  is_eligible?: boolean;
  ineligible_reasons?: string[];
};

export type StrategyRecommendation = {
  recommended_strategy_id: string;
  recommended_scenario_id: string;
  short_reasons: string[];
  complete_reasoning: string;
  architecture: StrategyArchitecture | null;
  alternative_architecture_ids: string[];
  feasibility_status: "feasible" | "conditional" | "infeasible";
  constraints: string[];
};

export type StrategyRun = {
  strategy_run_id: string | null;
  planning_unit_id: string;
  goal_id: string;
  defined_goal_id: string;
  defined_goal_version: number;
  run_version: number;
  is_latest: boolean;
  status: string;
  applicable_strategies: StrategyDefinition[];
  scenarios: Scenario[];
  investor_priorities: InvestorPriorities;
  comparison_matrix: Record<string, unknown>;
  rankings: StrategyRankingItem[];
  recommendation: StrategyRecommendation;
  architectures: StrategyArchitecture[];
  selected_strategy_id: string | null;
  selected_scenario_id: string | null;
  selected_strategy_version_id: string | null;
  selected_strategy_version: number | null;
  selected_implementation_parameters: Record<string, unknown>;
  selected_architecture: StrategyArchitecture | null;
  selection_timestamp: string | null;
  approval_status: "not_selected" | "selected" | "approved" | "rejected" | "superseded";
  run_metadata: Record<string, unknown>;
  created_at: string | null;
};

export { getPlanningUnitId } from "./client";

function limitToTopTwoStrategies(run: StrategyRun): StrategyRun {
  const strategyIds: string[] = [];
  for (const ranking of [...run.rankings].sort((a, b) => a.rank - b.rank)) {
    if (!strategyIds.includes(ranking.strategy_id)) strategyIds.push(ranking.strategy_id);
    if (strategyIds.length === 2) break;
  }
  if (!strategyIds.length) return run;
  const allowed = new Set(strategyIds);
  return {
    ...run,
    applicable_strategies: run.applicable_strategies.filter((strategy) => allowed.has(strategy.strategy_id)),
    rankings: run.rankings.filter((ranking) => allowed.has(ranking.strategy_id)),
  };
}

export async function buildStrategy(planningUnitId: string, goalId: string, investorPriorities?: InvestorPriorities) {
  const run = await apiRequest<StrategyRun>("/api/strategy/build", {
    method: "POST",
    body: JSON.stringify({
      planning_unit_id: planningUnitId,
      goal_id: goalId,
      investor_priorities: investorPriorities ?? { safety: 0.25, liquidity: 0.25, growth: 0.25, flexibility: 0.25 },
    }),
  });
  return limitToTopTwoStrategies(run);
}

export async function getLatestStrategyRun(planningUnitId: string, goalId: string) {
  const run = await apiRequest<StrategyRun>(`/api/strategy/runs/${encodeURIComponent(goalId)}/latest?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
  return limitToTopTwoStrategies(run);
}

export function getStrategyRunHistory(planningUnitId: string, goalId: string) {
  return apiRequest<StrategyRun[]>(`/api/strategy/runs/${encodeURIComponent(goalId)}/history?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export async function updateStrategyPriorities(planningUnitId: string, strategyRunId: string, priorities: InvestorPriorities) {
  const run = await apiRequest<StrategyRun>("/api/strategy/priorities", {
    method: "POST",
    body: JSON.stringify({ planning_unit_id: planningUnitId, strategy_run_id: strategyRunId, priorities }),
  });
  return limitToTopTwoStrategies(run);
}

export function addCustomScenario(planningUnitId: string, strategyRunId: string, strategyId: string, scenarioName: string, assumptions: Record<string, unknown>, fundingStructure: Record<string, unknown>) {
  return apiRequest<StrategyRun>("/api/strategy/scenarios/custom", {
    method: "POST",
    body: JSON.stringify({ planning_unit_id: planningUnitId, strategy_run_id: strategyRunId, strategy_id: strategyId, scenario_name: scenarioName, assumptions, funding_structure: fundingStructure }),
  });
}

export function selectStrategy(
  planningUnitId: string,
  strategyRunId: string,
  selectedStrategyId: string,
  selectedScenarioId: string,
  selectedImplementationParameters: Record<string, unknown>,
  selectedArchitectureId?: string,
) {
  return apiRequest<StrategyRun>("/api/strategy/select", {
    method: "POST",
    body: JSON.stringify({
      planning_unit_id: planningUnitId,
      strategy_run_id: strategyRunId,
      selected_strategy_id: selectedStrategyId,
      selected_scenario_id: selectedScenarioId,
      selected_architecture_id: selectedArchitectureId ?? null,
      selected_implementation_parameters: selectedImplementationParameters,
    }),
  });
}

export type ReportSection = {
  id: string;
  title: string;
  description?: string;
  columns?: string[];
  rows?: unknown[][];
  narratives?: Record<string, unknown>;
  data?: unknown;
};

export type RetirementReportData = {
  title: string;
  sections: ReportSection[];
};

export function getRetirementReport(planningUnitId: string, strategyRunId: string): Promise<RetirementReportData> {
  return apiRequest<RetirementReportData>(
    `/api/strategy/runs/${encodeURIComponent(strategyRunId)}/retirement-report?planning_unit_id=${encodeURIComponent(planningUnitId)}`
  );
}

export function downloadRetirementReportPdf(planningUnitId: string, strategyRunId: string): Promise<Blob> {
  return apiRequestBlob(
    `/api/strategy/runs/${encodeURIComponent(strategyRunId)}/retirement-report.pdf?planning_unit_id=${encodeURIComponent(planningUnitId)}`
  );
}