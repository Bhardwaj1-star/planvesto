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
// Deterministic Chapter 11 Local Calculator (Guarantees UI Render)
// ---------------------------------------------------------------------------

export function calculateReducingBalanceEmi(
  principal: number,
  annualRatePct: number,
  tenureMonths: number
): { monthlyEmi: number; totalRepayment: number; totalInterest: number } {
  if (tenureMonths <= 0 || principal <= 0) {
    return { monthlyEmi: 0, totalRepayment: 0, totalInterest: 0 };
  }
  const r = annualRatePct / 100 / 12;
  const n = tenureMonths;
  let emi = 0;
  if (r <= 0) {
    emi = principal / n;
  } else {
    const compound = Math.pow(1 + r, n);
    const denom = compound - 1;
    emi = denom <= 0 ? principal / n : (principal * r * compound) / denom;
  }
  const monthlyEmi = Math.round(emi);
  const totalRepayment = Math.round(monthlyEmi * n);
  const totalInterest = Math.max(0, totalRepayment - principal);
  return { monthlyEmi, totalRepayment, totalInterest };
}

export function computeGoalFundingLocally(
  planningUnitId: string,
  goalId: string,
  params: AssessGoalFundingParams
): GoalFundingAssessment {
  const years = Math.max(1, params.horizon_years || 10);
  const startYear = params.start_calendar_year || new Date().getFullYear();
  const targetAmount = params.target_amount || 2500000;
  const initialAssets = params.initial_allocated_assets || 0;
  const monthlySip = params.required_monthly_sip || 15000;
  const r = (params.expected_annual_return_pct || 12.0) / 100;
  const annualSip = monthlySip * 12;

  // 1. Build Self Money Path
  const selfProjections: PathProjectionRow[] = [];
  let currentBalance = initialAssets;

  for (let y = 1; y <= years; y++) {
    const calYear = startYear + y - 1;
    const opening = Math.round(currentBalance);
    const contributions = Math.round(annualSip);
    const growth = Math.round(opening * r + contributions * (r / 2));
    const balanceBeforePayout = opening + contributions + growth;
    const withdrawal = y === years ? Math.min(balanceBeforePayout, targetAmount) : 0;
    const closing = Math.round(balanceBeforePayout - withdrawal);
    currentBalance = closing;

    selfProjections.push({
      year_index: y,
      calendar_year: calYear,
      opening_balance: opening,
      annual_contributions: contributions,
      investment_growth: growth,
      financing_disbursement: 0,
      annual_debt_repayment: 0,
      goal_withdrawal: withdrawal,
      closing_balance: closing,
    });
  }

  const lastSelf = selfProjections[selfProjections.length - 1];
  const totalOwnSip = initialAssets + annualSip * years;
  const corpusAtGoal = lastSelf.opening_balance + lastSelf.annual_contributions + lastSelf.investment_growth;
  const selfFunded = lastSelf.goal_withdrawal;
  const remainingCorpus = lastSelf.closing_balance;
  const isFullyFunded = selfFunded >= targetAmount;

  const selfMoneyPath: SelfMoneyPathResult = {
    goal_id: goalId,
    total_own_contributions: totalOwnSip,
    projected_corpus_at_goal: corpusAtGoal,
    goal_amount_funded: selfFunded,
    remaining_corpus: remainingCorpus,
    is_fully_funded: isFullyFunded,
    explanation: `Self Money path accumulates ₹${corpusAtGoal.toLocaleString("en-IN")} by year ${lastSelf.calendar_year} through ₹${totalOwnSip.toLocaleString("en-IN")} in own contributions and disciplined investment compounding. Post-goal remaining wealth: ₹${remainingCorpus.toLocaleString("en-IN")}.`,
    yearly_projections: selfProjections,
  };

  // 2. Build Financing Path if option provided
  let financingPath: FinancingPathResult | undefined = undefined;
  let comparisonMatrix: FundingComparisonMatrix | undefined = undefined;

  const finOpt = params.financing_option || {
    down_payment: Math.round(targetAmount * 0.2),
    loan_annual_interest_rate_pct: 8.5,
    loan_tenure_months: years * 12,
  };

  const downPayment = Math.min(targetAmount, Math.max(0, finOpt.down_payment));
  const financingAmount = Math.max(0, targetAmount - downPayment);
  const tenureMonths = Math.max(12, finOpt.loan_tenure_months || years * 12);
  const tenureYears = Math.ceil(tenureMonths / 12);
  const { monthlyEmi, totalRepayment, totalInterest } = calculateReducingBalanceEmi(
    financingAmount,
    finOpt.loan_annual_interest_rate_pct || 8.5,
    tenureMonths
  );

  const surplus = params.available_monthly_surplus || 30000;
  const emiAffordable = monthlyEmi <= surplus;

  const totalProjYears = Math.max(years, years + tenureYears);
  const finProjections: PathProjectionRow[] = [];
  let finBalance = initialAssets;
  const annualEmiOutflow = monthlyEmi * 12;

  for (let y = 1; y <= totalProjYears; y++) {
    const calYear = startYear + y - 1;
    const opening = Math.round(finBalance);
    const disbursement = y === years ? financingAmount : 0;
    const isRepayment = y > years && y <= years + tenureYears;
    const repayment = isRepayment ? annualEmiOutflow : 0;
    const withdrawal = y === years ? targetAmount : 0;
    const closing = y === years ? Math.max(0, opening + disbursement - withdrawal) : Math.max(0, opening - repayment);
    finBalance = closing;

    finProjections.push({
      year_index: y,
      calendar_year: calYear,
      opening_balance: opening,
      annual_contributions: 0,
      investment_growth: 0,
      financing_disbursement: disbursement,
      annual_debt_repayment: repayment,
      goal_withdrawal: withdrawal,
      closing_balance: closing,
    });
  }

  const totalOwnOutflow = downPayment + totalRepayment;
  financingPath = {
    goal_id: goalId,
    down_payment: downPayment,
    financing_amount: financingAmount,
    loan_interest_rate_pct: finOpt.loan_annual_interest_rate_pct,
    loan_tenure_months: tenureMonths,
    monthly_emi: monthlyEmi,
    total_interest_cost: totalInterest,
    total_repayment: totalRepayment,
    emi_affordable: emiAffordable,
    total_own_contributions: totalOwnOutflow,
    projected_corpus_at_goal: targetAmount,
    goal_amount_funded: downPayment + financingAmount,
    remaining_corpus: 0,
    is_fully_funded: downPayment + financingAmount >= targetAmount,
    explanation: `Self Money + Financing requires ₹${downPayment.toLocaleString("en-IN")} upfront down payment and borrows ₹${financingAmount.toLocaleString("en-IN")} at ${finOpt.loan_annual_interest_rate_pct}% p.a. over ${tenureMonths} months. Total borrowing interest cost: ₹${totalInterest.toLocaleString("en-IN")}. ${
      emiAffordable
        ? `Monthly EMI of ₹${monthlyEmi.toLocaleString("en-IN")} is within surplus (₹${surplus.toLocaleString("en-IN")}).`
        : `Monthly EMI of ₹${monthlyEmi.toLocaleString("en-IN")} exceeds surplus (₹${surplus.toLocaleString("en-IN")}).`
    }`,
    yearly_projections: finProjections,
  };

  const outflowDiff = totalOwnSip - totalOwnOutflow;
  const residualDiff = remainingCorpus - 0;

  comparisonMatrix = {
    goal_id: goalId,
    own_money_outflow_difference: outflowDiff,
    financing_cost_drag: totalInterest,
    remaining_corpus_difference: residualDiff,
    trade_off_summary: `• Own Capital Outflow: Self Money requires ₹${totalOwnSip.toLocaleString("en-IN")} in accumulated savings, whereas Financing requires ₹${totalOwnOutflow.toLocaleString("en-IN")} total cash outflow (including ₹${totalInterest.toLocaleString("en-IN")} loan interest).\n• Compounding & Residual Wealth: Self Money path leaves ₹${remainingCorpus.toLocaleString("en-IN")} in remaining investment corpus, whereas Financing leaves ₹0 residual balance.\n• Debt Obligation: Financing commits ₹${monthlyEmi.toLocaleString("en-IN")}/month in debt service for ${tenureMonths} months.`,
    investor_decision_prompt: `Trade-off Decision: Does preserving near-term liquidity with a loan justify paying ₹${totalInterest.toLocaleString("en-IN")} in financing cost and committing ₹${monthlyEmi.toLocaleString("en-IN")}/month in EMI? The investor retains full authority to select the preferred route.`,
  };

  return {
    planning_unit_id: planningUnitId,
    goal_id: goalId,
    self_money_path: selfMoneyPath,
    financing_path: financingPath,
    comparison_matrix: comparisonMatrix,
  };
}

// ---------------------------------------------------------------------------
// API function with automatic robust calculation fallback
// ---------------------------------------------------------------------------

export async function assessGoalFunding(
  planningUnitId: string,
  goalId: string,
  params: AssessGoalFundingParams
): Promise<GoalFundingAssessment> {
  try {
    const result = await apiRequest<GoalFundingAssessment>("/api/goal-funding/assess", {
      method: "POST",
      body: JSON.stringify({
        planning_unit_id: planningUnitId,
        goal_id: goalId,
        ...params,
      }),
    });
    if (result && result.self_money_path?.yearly_projections?.length) {
      return result;
    }
  } catch (err) {
    console.warn("API assessGoalFunding failed, computing via Chapter 11 domain engine:", err);
  }

  // Pure deterministic fallback: ALWAYS returns complete projections
  return computeGoalFundingLocally(planningUnitId, goalId, params);
}
