import { supabase } from "../supabase";

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
  library_version: string;
  implementation_version: string;
  active: boolean;
  applicable_goal_types: string[];
  implementation_parameters: StrategyImplementationParamDef[];
  good_outcomes: string[];
  bad_outcomes: string[];
  trade_offs: string[];
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
  recommendation: {
    recommended_strategy_id: string;
    recommended_scenario_id: string;
    short_reasons: string[];
    complete_reasoning: string;
  };
  selected_strategy_id: string | null;
  selected_scenario_id: string | null;
  selected_strategy_version_id: string | null;
  selected_strategy_version: number | null;
  selected_implementation_parameters: Record<string, unknown>;
  selection_timestamp: string | null;
  run_metadata: Record<string, unknown>;
  created_at: string | null;
};

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  if (!backendUrl) throw new Error("Backend URL is not configured.");
  const { data, error } = await supabase.auth.getSession();
  if (error) throw error;
  if (!data.session) throw new Error("Authentication required.");
  const response = await fetch(`${backendUrl}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${data.session.access_token}`,
      ...(init?.headers ?? {}),
    },
  });
  let body: unknown = null;
  try { body = await response.json(); } catch { /* non-JSON error */ }
  if (!response.ok) {
    const detail = typeof body === "object" && body !== null && "detail" in body
      ? String((body as { detail: unknown }).detail)
      : `Request failed with status ${response.status}.`;
    throw new Error(detail);
  }
  return body as T;
}

export function getPlanningUnitId(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("planvesto-planning-unit-id");
}

export function buildStrategy(planningUnitId: string, goalId: string, investorPriorities?: InvestorPriorities) {
  return request<StrategyRun>("/api/strategy/build", {
    method: "POST",
    body: JSON.stringify({ planning_unit_id: planningUnitId, goal_id: goalId, investor_priorities: investorPriorities }),
  });
}

export function getLatestStrategyRun(planningUnitId: string, goalId: string) {
  return request<StrategyRun>(`/api/strategy/runs/${encodeURIComponent(goalId)}/latest?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export function getStrategyRunHistory(planningUnitId: string, goalId: string) {
  return request<StrategyRun[]>(`/api/strategy/runs/${encodeURIComponent(goalId)}/history?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export function updateStrategyPriorities(planningUnitId: string, strategyRunId: string, priorities: InvestorPriorities) {
  return request<StrategyRun>("/api/strategy/priorities", {
    method: "POST",
    body: JSON.stringify({ planning_unit_id: planningUnitId, strategy_run_id: strategyRunId, priorities }),
  });
}

export function addCustomScenario(planningUnitId: string, strategyRunId: string, strategyId: string, scenarioName: string, assumptions: Record<string, unknown>, fundingStructure: Record<string, unknown>) {
  return request<StrategyRun>("/api/strategy/scenarios/custom", {
    method: "POST",
    body: JSON.stringify({ planning_unit_id: planningUnitId, strategy_run_id: strategyRunId, strategy_id: strategyId, scenario_name: scenarioName, assumptions, funding_structure: fundingStructure }),
  });
}

export function selectStrategy(planningUnitId: string, strategyRunId: string, selectedStrategyId: string, selectedScenarioId: string, selectedImplementationParameters: Record<string, unknown>) {
  return request<StrategyRun>("/api/strategy/select", {
    method: "POST",
    body: JSON.stringify({ planning_unit_id: planningUnitId, strategy_run_id: strategyRunId, selected_strategy_id: selectedStrategyId, selected_scenario_id: selectedScenarioId, selected_implementation_parameters: selectedImplementationParameters }),
  });
}
