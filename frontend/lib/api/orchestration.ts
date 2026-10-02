import { apiRequest, getPlanningUnitId } from "./client";

export type GoalPriorityLevel = "critical" | "high" | "medium" | "low";
export type FundingStatusType =
  | "fully_funded"
  | "partially_funded"
  | "unfunded"
  | "within_surplus"
  | "surplus_shortfall"
  | "requires_review";
export type FeasibilityStatusType = "feasible" | "constrained" | "infeasible";

export type WorkflowNextAction = {
  label: string;
  route: string;
};

export type WorkflowMissingData = {
  label: string;
  route: string | null;
};

export type WorkflowBlocker = {
  key: string;
  reason: string | null;
  missing_data: WorkflowMissingData[];
  next_action: WorkflowNextAction | null;
};

export type WorkflowReadiness = {
  status: "ready" | "blocked";
  process_route: string;
  blockers: WorkflowBlocker[];
  next_action: WorkflowNextAction | null;
  return_to: string;
};

export interface GoalResolution {
  goal_id: string;
  goal_name: string;
  goal_type: string;
  client_priority: GoalPriorityLevel;
  resolved_priority: GoalPriorityLevel;
  target_date: string | null;
  required_monthly_contribution: number;
  allocated_monthly_contribution: number;
  shortfall: number;
  funding_status: FundingStatusType;
  feasibility_status: FeasibilityStatusType;
  recommended_strategy_id: string | null;
  recommended_strategy_name: string | null;
  override_applied: boolean;
  override_reason: string | null;
  reasons: string[];
  notes: string[];
}

export interface MultiGoalPlanResult {
  planning_unit_id: string | null;
  financial_state: Record<string, unknown>;
  total_available_surplus: number | null;
  total_required_contribution: number;
  total_allocated_contribution: number;
  monthly_gap: number | null;
  overall_funding_status: FundingStatusType;
  goals: GoalResolution[];
  competing_resources_detected: boolean;
  trade_offs: string[];
  action_plan: Array<{
    sequence: number;
    goal_id: string;
    goal_name: string;
    action: string;
    monthly_contribution: number;
    required_contribution: number;
    target_date: string | null;
    funding_status: string;
  }>;
  audit_trail: Array<{
    goal_id: string;
    goal_name: string;
    client_priority: string;
    resolved_priority: string;
    override_applied: boolean;
    override_reason: string | null;
    required_monthly_contribution: number;
    allocated_monthly_contribution: number;
    funding_status: string;
    allocation_reasoning: string;
  }>;
  planning_notes: string[];
}

export interface MultiGoalPlanRequest {
  planning_unit_id: string;
  rule_overrides?: Record<string, { resolved_priority?: GoalPriorityLevel; reason?: string }>;
}

export interface PlanningOrchestrationRequest {
  planning_unit_id: string;
  investor_id?: string;
  goal_version_ids: string[];
  strategy_version_id?: string;
  scope?: "family" | "individual";
}

/**
 * Triggers backend multi-goal orchestration across competing goals and resources.
 * Calls POST /api/orchestration/plan
 */
export async function buildMultiGoalOrchestrationPlan(
  planningUnitId: string,
  ruleOverrides?: Record<string, { resolved_priority?: GoalPriorityLevel; reason?: string }>
): Promise<MultiGoalPlanResult> {
  return apiRequest<MultiGoalPlanResult>("/api/orchestration/plan", {
    method: "POST",
    body: JSON.stringify({
      planning_unit_id: planningUnitId,
      rule_overrides: ruleOverrides,
    }),
  });
}

/**
 * Builds planning context combining financial state, selected goals, and strategy modules.
 * Calls POST /api/orchestration/context
 */
export async function buildPlanningContext(
  request: PlanningOrchestrationRequest
): Promise<Record<string, unknown>> {
  return apiRequest<Record<string, unknown>>("/api/orchestration/context", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export { getPlanningUnitId };
