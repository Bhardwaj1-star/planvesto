import { apiRequest } from "./client";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface PathProjectionRow {
  year_index: number;
  calendar_year: number;
  opening_balance: number;
  annual_contributions: number;
  investment_growth: number;
  financing_disbursement: number;
  annual_debt_repayment: number;
  goal_withdrawal: number;
  closing_balance: number;
}

export interface SelfMoneyPathResult {
  goal_id: string;
  total_own_contributions: number;
  projected_corpus_at_goal: number;
  goal_amount_funded: number;
  remaining_corpus: number;
  is_fully_funded: boolean;
  explanation: string;
  yearly_projections: PathProjectionRow[];
}

export interface FinancingPathResult extends SelfMoneyPathResult {
  down_payment: number;
  financing_amount: number;
  loan_interest_rate_pct: number;
  loan_tenure_months: number;
  monthly_emi: number;
  total_interest_cost: number;
  total_repayment: number;
  emi_affordable: boolean;
}

export interface FundingComparisonMatrix {
  goal_id: string;
  own_money_outflow_difference: number;
  financing_cost_drag: number;
  remaining_corpus_difference: number;
  trade_off_summary: string;
  investor_decision_prompt: string;
}

export interface GoalFundingAssessment {
  planning_unit_id: string;
  goal_id: string;
  self_money_path: SelfMoneyPathResult;
  financing_path?: FinancingPathResult;
  comparison_matrix?: FundingComparisonMatrix;
}

export interface FinancingOption {
  down_payment: number;
  loan_annual_interest_rate_pct: number;
  loan_tenure_months: number;
}

// ---------------------------------------------------------------------------
// Request params
// ---------------------------------------------------------------------------

export interface AssessGoalFundingParams {
  target_amount: number;
  horizon_years: number;
  start_calendar_year: number;
  initial_allocated_assets: number;
  required_monthly_sip: number;
  expected_annual_return_pct: number;
  available_monthly_surplus: number;
  financing_option?: FinancingOption;
}

// ---------------------------------------------------------------------------
// API function
// ---------------------------------------------------------------------------

export async function assessGoalFunding(
  planningUnitId: string,
  goalId: string,
  params: AssessGoalFundingParams,
): Promise<GoalFundingAssessment> {
  return apiRequest<GoalFundingAssessment>("/api/goal-funding/assess", {
    method: "POST",
    body: JSON.stringify({
      planning_unit_id: planningUnitId,
      goal_id: goalId,
      ...params,
    }),
  });
}
