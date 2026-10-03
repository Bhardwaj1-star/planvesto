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
export type StrategyDefinition = { strategy_id: string; name: string; tagline: string; description: string; strategy_family: string; strategic_objective: string; core_mechanism: string; principles: string[]; constraints: string[]; dependencies: string[]; required_inputs: string[]; applicable_goal_characteristics: string[]; applicable_goal_types: string[]; technique_ids: string[]; strategic_levers: string[]; compatible_strategy_ids: string[]; conflicting_strategy_ids: string[]; library_version: string; implementation_version: string; active: boolean; implementation_parameters: StrategyImplementationParamDef[]; good_outcomes: string[]; bad_outcomes: string[]; trade_offs: string[]; baseline_safety_score: number; baseline_liquidity_score: number; baseline_growth_score: number; baseline_flexibility_score: number; };
export type StrategyArchitecture = { architecture_id: string; primary_strategy_id: string; supporting_strategy_ids: string[]; technique_ids: string[]; rationale: string[]; trade_offs: string[]; feasibility_status: "feasible" | "conditional" | "infeasible"; constraints: string[]; };
export type Scenario = { scenario_id: string; strategy_id: string; scenario_type: "baseline" | "modified" | "custom"; scenario_name: string; assumptions: Record<string, unknown>; funding_structure: Record<string, unknown>; metrics: Record<string, unknown>; trade_off_notes: string; is_investor_modified: boolean; };
export type StrategyRankingItem = { rank: number; strategy_id: string; scenario_id: string; strategy_name: string; scenario_name: string; composite_score: number; dimension_scores: Record<string, number>; is_recommended: boolean; evidence_scores?: Record<string, unknown>; is_eligible?: boolean; ineligible_reasons?: string[]; };
export type StrategyRecommendation = { recommended_strategy_id: string; recommended_scenario_id: string; short_reasons: string[]; complete_reasoning: string; architecture: StrategyArchitecture | null; alternative_architecture_ids: string[]; feasibility_status: "feasible" | "conditional" | "infeasible"; constraints: string[]; };
export type StrategyRun = { strategy_run_id: string | null; planning_unit_id: string; goal_id: string; defined_goal_id: string; defined_goal_version: number; run_version: number; is_latest: boolean; status: string; applicable_strategies: StrategyDefinition[]; scenarios: Scenario[]; investor_priorities: InvestorPriorities; comparison_matrix: Record<string, unknown>; rankings: StrategyRankingItem[]; recommendation: StrategyRecommendation; architectures: StrategyArchitecture[]; selected_strategy_id: string | null; selected_scenario_id: string | null; selected_strategy_version_id: string | null; selected_strategy_version: number | null; selected_implementation_parameters: Record<string, unknown>; selected_architecture: StrategyArchitecture | null; selection_timestamp: string | null; approval_status?: string | null; run_metadata: Record<string, unknown>; created_at: string | null; };

export { getPlanningUnitId } from "./client";
function limitToTopTwoStrategies(run: StrategyRun): StrategyRun { const ids: string[] = []; for (const ranking of [...run.rankings].sort((a,b)=>a.rank-b.rank)) { if (!ids.includes(ranking.strategy_id)) ids.push(ranking.strategy_id); if (ids.length===2) break; } if (!ids.length) return run; const allowed=new Set(ids); return {...run, applicable_strategies:run.applicable_strategies.filter(s=>allowed.has(s.strategy_id)), rankings:run.rankings.filter(r=>allowed.has(r.strategy_id))}; }
export async function buildStrategy(planningUnitId:string,goalId:string,investorPriorities?:InvestorPriorities){const run=await apiRequest<StrategyRun>("/api/strategy/build",{method:"POST",body:JSON.stringify({planning_unit_id:planningUnitId,goal_id:goalId,investor_priorities:investorPriorities??{safety:.25,liquidity:.25,growth:.25,flexibility:.25}})});return limitToTopTwoStrategies(run);}
export async function getLatestStrategyRun(planningUnitId:string,goalId:string){const run=await apiRequest<StrategyRun>(`/api/strategy/runs/${encodeURIComponent(goalId)}/latest?planning_unit_id=${encodeURIComponent(planningUnitId)}`);return limitToTopTwoStrategies(run);}
export async function getStrategyRunById(planningUnitId:string,strategyRunId:string){return apiRequest<StrategyRun>(`/api/strategy/runs/by-id/${encodeURIComponent(strategyRunId)}?planning_unit_id=${encodeURIComponent(planningUnitId)}`);}
export function previewImplementation(planningUnitId:string,strategyRunId:string,selectedStrategyId:string,selectedScenarioId:string,implementationParameters:Record<string,unknown>,assumptions:Record<string,unknown>,fundingStructure:Record<string,unknown>,selectedArchitectureId?:string){return apiRequest<StrategyRun>("/api/strategy/implementation/preview",{method:"POST",body:JSON.stringify({planning_unit_id:planningUnitId,strategy_run_id:strategyRunId,selected_strategy_id:selectedStrategyId,selected_scenario_id:selectedScenarioId,selected_architecture_id:selectedArchitectureId??null,implementation_parameters:implementationParameters,assumptions,funding_structure:fundingStructure})});}
export function finalizeImplementation(planningUnitId:string,strategyRunId:string,definedGoalVersion:number,selectedStrategyId:string,selectedScenarioId:string,implementationParameters:Record<string,unknown>,assumptions:Record<string,unknown>,fundingStructure:Record<string,unknown>,selectedArchitectureId?:string){return apiRequest<StrategyRun>("/api/strategy/implementation/finalize",{method:"POST",body:JSON.stringify({planning_unit_id:planningUnitId,strategy_run_id:strategyRunId,defined_goal_version:definedGoalVersion,selected_strategy_id:selectedStrategyId,selected_scenario_id:selectedScenarioId,selected_architecture_id:selectedArchitectureId??null,implementation_parameters:implementationParameters,assumptions,funding_structure:fundingStructure})});}
export function getStrategyRunHistory(planningUnitId:string,goalId:string){return apiRequest<StrategyRun[]>(`/api/strategy/runs/${encodeURIComponent(goalId)}/history?planning_unit_id=${encodeURIComponent(planningUnitId)}`);}
export async function updateStrategyPriorities(planningUnitId:string,strategyRunId:string,priorities:InvestorPriorities){const run=await apiRequest<StrategyRun>("/api/strategy/priorities",{method:"POST",body:JSON.stringify({planning_unit_id:planningUnitId,strategy_run_id:strategyRunId,priorities})});return limitToTopTwoStrategies(run);}
export function addCustomScenario(planningUnitId:string,strategyRunId:string,strategyId:string,scenarioName:string,assumptions:Record<string,unknown>,fundingStructure:Record<string,unknown>){return apiRequest<StrategyRun>("/api/strategy/scenarios/custom",{method:"POST",body:JSON.stringify({planning_unit_id:planningUnitId,strategy_run_id:strategyRunId,strategy_id:strategyId,scenario_name:scenarioName,assumptions,funding_structure:fundingStructure})});}
export function selectStrategy(planningUnitId:string,strategyRunId:string,selectedStrategyId:string,selectedScenarioId:string,selectedImplementationParameters:Record<string,unknown>,selectedArchitectureId?:string){return apiRequest<StrategyRun>("/api/strategy/select",{method:"POST",body:JSON.stringify({planning_unit_id:planningUnitId,strategy_run_id:strategyRunId,selected_strategy_id:selectedStrategyId,selected_scenario_id:selectedScenarioId,selected_architecture_id:selectedArchitectureId??null,selected_implementation_parameters:selectedImplementationParameters})});}
export function saveStrategyChanges(planningUnitId:string,strategyRunId:string,selectedStrategyId:string,selectedScenarioId:string,selectedImplementationParameters:Record<string,unknown>,selectedArchitectureId?:string){return selectStrategy(planningUnitId,strategyRunId,selectedStrategyId,selectedScenarioId,selectedImplementationParameters,selectedArchitectureId);}
export type ReportSection={id:string;title:string;description?:string;columns?:string[];rows?:unknown[][];narratives?:Record<string,unknown>;data?:unknown};
export type RetirementReportData={title:string;sections:ReportSection[]};
export function getRetirementReport(planningUnitId:string,strategyRunId:string):Promise<RetirementReportData>{return apiRequest<RetirementReportData>(`/api/strategy/runs/${encodeURIComponent(strategyRunId)}/retirement-report?planning_unit_id=${encodeURIComponent(planningUnitId)}`);}
export function downloadRetirementReportPdf(planningUnitId:string,strategyRunId:string):Promise<Blob>{return apiRequestBlob(`/api/strategy/runs/${encodeURIComponent(strategyRunId)}/retirement-report.pdf?planning_unit_id=${encodeURIComponent(planningUnitId)}`);}
export type CashFlowTrajectoryItem = {
  year_index: number;
  year: number;
  opening_balance: number;
  annual_contribution: number;
  growth: number;
  closing_balance: number;
  inflation_adjusted_target?: number;
};

export type ProductBucketItem = {
  bucket_id?: string;
  bucket_name?: string;
  bucket?: string;
  role?: string;
  horizon_years?: number;
  allocation_pct?: number;
  allocation?: string | number;
  instruments: string | string[] | Record<string, unknown>;
  rationale?: string;
  strategic_rule?: string;
};

export type ContributionRuleItem = {
  rule_id: string;
  name: string;
  trigger: string;
  execution: string;
};

export type ActionTimelineItem = {
  timeline: string;
  action: string;
  owner: string;
  milestone: string;
};

export type ContingencyItem = {
  risk_event: string;
  immediate_action: string;
  planning_change: string;
  what_not_to_do: string;
};

export type GoalStrategyReport = {
  report_type: string;
  goal_id?: string;
  goal_name?: string;
  goal_type?: string | null;
  goal?: {
    id: string;
    name: string;
    type?: string | null;
    priority?: string | null;
    flexibility?: string | null;
    status?: string | null;
    duration_years?: number | null;
    target_year?: number | null;
    target_month?: number | null;
  };
  goal_details?: Record<string, unknown>;
  mapped_assets?: Array<{
    asset_name?: string;
    allocation?: number;
    allocation_percentage?: number;
    expected_return?: number;
    projected_value?: number;
  }>;
  strategy_run_id: string;
  strategy: {
    name?: string | null;
    objective?: string | null;
    selected_strategy_id?: string | null;
    selected_strategy_name?: string | null;
    rationale?: string | null;
    trade_offs?: string[];
    architecture?: Record<string, unknown>;
  };
  recommendation?: Record<string, unknown>;
  selected_strategy_id?: string | null;
  approval_status?: string | null;
  goal_calculation: Record<string, unknown>;
  financial_state: Record<string, unknown>;
  cash_flow_trajectory?: CashFlowTrajectoryItem[];
  product_architecture?: ProductBucketItem[];
  contribution_rules?: ContributionRuleItem[];
  action_plan_timeline?: ActionTimelineItem[];
  contingency_matrix?: ContingencyItem[];
};

export function getGoalStrategyReport(planningUnitId:string,strategyRunId:string):Promise<GoalStrategyReport>{return apiRequest<GoalStrategyReport>(`/api/strategy/runs/${encodeURIComponent(strategyRunId)}/report?planning_unit_id=${encodeURIComponent(planningUnitId)}`);}
export function downloadGoalStrategyReportPdf(planningUnitId:string,strategyRunId:string):Promise<Blob>{return apiRequestBlob(`/api/strategy/runs/${encodeURIComponent(strategyRunId)}/report.pdf?planning_unit_id=${encodeURIComponent(planningUnitId)}`);}
export function getGoalStrategyReportByStrategyVersion(planningUnitId:string,strategyVersionId:string):Promise<GoalStrategyReport>{return apiRequest<GoalStrategyReport>(`/api/strategy/strategy-versions/${encodeURIComponent(strategyVersionId)}/report?planning_unit_id=${encodeURIComponent(planningUnitId)}`);}
export function downloadGoalStrategyReportPdfByStrategyVersion(planningUnitId:string,strategyVersionId:string):Promise<Blob>{return apiRequestBlob(`/api/strategy/strategy-versions/${encodeURIComponent(strategyVersionId)}/report.pdf?planning_unit_id=${encodeURIComponent(planningUnitId)}`);}

export function buildBasketReport(planningUnitId: string, goalIds: string[], basketName?: string): Promise<Record<string, unknown>> {
  return apiRequest<Record<string, unknown>>("/api/basket-report", {
    method: "POST",
    body: JSON.stringify({
      planning_unit_id: planningUnitId,
      goal_ids: goalIds,
      basket_name: basketName,
    }),
  });
}

export function downloadBasketReportPdf(planningUnitId: string, goalIds: string[], basketName?: string): Promise<Blob> {
  return apiRequestBlob("/api/basket-report/pdf", {
    method: "POST",
    body: JSON.stringify({
      planning_unit_id: planningUnitId,
      goal_ids: goalIds,
      basket_name: basketName,
    }),
  });
}

export type RatioConstraintEvaluation = {
  rule_id: string;
  rule_name: string;
  category: string;
  current_ratio: number | null;
  target_threshold: number;
  condition: string;
  status: "pass" | "conditional" | "fail";
  mandatory_minimum_reserve?: number;
  max_allowable_debt_service?: number;
  minimum_savings_required?: number;
  reason: string;
  corrective_action?: string | null;
};

export type ResourceAllocationSummary = {
  total_monthly_surplus: number;
  foundation_allocation: {
    emergency_fund_monthly: number;
    debt_reduction_monthly: number;
    mandatory_savings_monthly: number;
  };
  discretionary_surplus_monthly: number;
  goal_allocations: Array<{
    goal_id: string;
    goal_name: string;
    requested_amount: number;
    allocated_amount: number;
    shortfall: number;
    funding_percentage: number;
    priority_rank: number;
    client_priority?: string;
    resolved_priority?: string;
    override_applied: boolean;
    override_reason?: string | null;
  }>;
  total_allocated_monthly: number;
  unallocated_surplus: number;
};

export type ConsolidatedActionItem = {
  action_id: string;
  category: "foundation" | "goal" | "protection";
  title: string;
  description: string;
  priority: "high" | "medium" | "low";
  target_type: string;
  target_id?: string | null;
  monthly_commitment: number;
  lump_sum_commitment: number;
  deadline?: string | null;
  status: string;
};

export type ConsolidatedFinancialPlan = {
  plan_id?: string;
  planning_unit_id: string;
  created_at?: string;
  investor_priorities?: InvestorPriorities;
  summary: {
    total_goals_count: number;
    fully_funded_goals_count: number;
    partially_funded_goals_count: number;
    total_funding_gap: number;
    total_monthly_commitment: number;
  };
  ratio_constraints?: RatioConstraintEvaluation[];
  resource_allocation: ResourceAllocationSummary;
  goal_plans: Array<{
    goal_id: string;
    goal_name: string;
    goal_type: string;
    target_amount: number;
    target_date?: string | null;
    strategy_run_id: string;
    strategy_name: string;
    recommended_strategy_name: string;
    monthly_allocation: number;
    funding_gap: number;
    is_feasible: boolean;
  }>;
  action_plan: {
    actions: ConsolidatedActionItem[];
    total_actions: number;
  };
  goals?: Array<Record<string, unknown>>;
  consolidated_funding?: {
    required_monthly_contribution: number;
    allocated_monthly_contribution: number;
    available_monthly_surplus: number | null;
    monthly_gap: number | null;
    funding_status: string;
    competition_detected: boolean;
  };
  actions?: Array<Record<string, unknown>>;
  trade_offs?: string[];
  audit_trail?: Array<Record<string, unknown>>;
  planning_notes?: string[];
};

export function getCompleteFinancialPlan(planningUnitId: string): Promise<ConsolidatedFinancialPlan> {
  return apiRequest<ConsolidatedFinancialPlan>(`/api/strategy/financial-plan?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export function buildCompleteFinancialPlan(planningUnitId: string, priorities?: InvestorPriorities): Promise<ConsolidatedFinancialPlan> {
  return apiRequest<ConsolidatedFinancialPlan>("/api/strategy/financial-plan/build", {
    method: "POST",
    body: JSON.stringify({
      planning_unit_id: planningUnitId,
      investor_priorities: priorities ?? { safety: 0.25, liquidity: 0.25, growth: 0.25, flexibility: 0.25 },
    }),
  });
}

export function downloadCompleteFinancialPlanPdf(planningUnitId: string): Promise<Blob> {
  return apiRequestBlob(`/api/strategy/financial-plan.pdf?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}
