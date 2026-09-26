import { supabase } from "../supabase";
import type { Database } from "../database.types";
import type { Asset } from "./assets/types";
import type { Expense } from "./expenses/types";
import type { FamilyMember } from "./family-dependents/types";
import { emptyGoalDynamicDetails, type Goal } from "./goals/types";
import type { IncomeSource } from "./income/types";
import type { Liability } from "./liabilities/types";
import type { PersonalInformation } from "./personal-information/model";

export type GoalFundingAllocation = { assetId: string; allocationPercentage: string };
export type GoalPlannerGoal = { id: string; name: string; targetAmount: string; targetDate: string; priority: string; flexibility: string; funding: GoalFundingAllocation[] };
export type GoalPlannerData = { goals: GoalPlannerGoal[]; assets: Array<{ id: string; name: string; currentValue: string }> };
export type OnboardingData = { planningUnitId: string; investorId: string | null; personalInformation: PersonalInformation; familyMembers: FamilyMember[]; incomeSources: IncomeSource[]; expenses: Expense[]; assets: Asset[]; liabilities: Liability[]; goals: Goal[] };
type Tables = Database["public"]["Tables"];
const planningUnitStorageKey = "planvesto-planning-unit-id";
let planningUnitPromise: Promise<string> | null = null;
let planningUnitUserId: string | null = null;

async function getAuthenticatedUser() { const { data, error } = await supabase.auth.getUser(); if (error) throw error; if (!data.user) throw new Error("You must be signed in to access onboarding."); return data.user; }
function isUuid(value: string) { return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value); }
function nullable(value: string) { return value.trim() || null; }
function numeric(value: string): number;
function numeric(value: string, optional: true): number | null;
function numeric(value: string, optional = false) { if (optional && !value.trim()) return null; return Number(value); }
function encodeName(primary: string, description: string) { return description.trim() ? `${primary} - ${description.trim()}` : primary; }
function decodeName(value: string, options: readonly string[]) { const option = options.find((item) => value === item || value.startsWith(`${item} - `)); return { primary: option || "", description: option ? value.slice(option.length).replace(/^ - /, "") : value }; }

async function getPlanningUnitId() {
  const user = await getAuthenticatedUser();
  if (planningUnitPromise && planningUnitUserId === user.id) return planningUnitPromise;
  planningUnitUserId = user.id;
  planningUnitPromise = (async () => {
    const storedId = typeof window !== "undefined" ? window.localStorage.getItem(planningUnitStorageKey) : null;
    if (storedId && isUuid(storedId)) { const { data, error } = await supabase.from("planning_units").select("planning_unit_id").eq("planning_unit_id", storedId).eq("user_id", user.id).maybeSingle(); if (error) throw error; if (data) return data.planning_unit_id; }
    const { data, error } = await supabase.from("planning_units").insert({ user_id: user.id }).select("planning_unit_id").single();
    if (error) throw error; if (typeof window !== "undefined") window.localStorage.setItem(planningUnitStorageKey, data.planning_unit_id); return data.planning_unit_id;
  })();
  try { return await planningUnitPromise; } catch (error) { planningUnitPromise = null; planningUnitUserId = null; throw error; }
}

async function loadRows(planningUnitId: string) {
  const [investors, dependents, income, expenses, assets, liabilities, goals] = await Promise.all([
    supabase.from("investors").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("dependents").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("income").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("expenses").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("assets").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("liabilities").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("goals").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
  ]);
  const result = [investors, dependents, income, expenses, assets, liabilities, goals].find((item) => item.error); if (result?.error) throw result.error;
  const investorRows = investors.data || [];
  const assetOptions = ["Bank / Cash", "Fixed Deposits", "Mutual Funds", "Stocks / Equity", "Bonds / Debt", "EPF / PPF", "NPS", "Gold", "Real Estate", "Business Ownership", "Vehicle", "Other"] as const;
  const liabilityOptions = ["Home Loan", "Car Loan", "Personal Loan", "Education Loan", "Business Loan", "Credit Card", "Other"] as const;
  return {
    planningUnitId,
    investorId: investorRows[0]?.investor_id || null,
    personalInformation: { fullName: investorRows[0]?.full_name || "", dateOfBirth: investorRows[0]?.date_of_birth || "", gender: investorRows[0]?.gender || "", maritalStatus: investorRows[0]?.marital_status || "", mobileNumber: investorRows[0]?.mobile_number || "", address: investorRows[0]?.address || "", city: investorRows[0]?.city || "", state: investorRows[0]?.state || "", country: investorRows[0]?.country || "", occupation: investorRows[0]?.occupation || "" },
    familyMembers: (dependents.data || []).map((row) => ({ id: row.dependent_id, name: row.name, relationship: row.relationship || "", dateOfBirth: row.date_of_birth || "", occupation: row.occupation || "", financialDependency: Boolean(row.financial_dependency), includeInPlanning: Boolean(row.include_in_planning) })),
    incomeSources: (income.data || []).map((row) => ({ id: row.income_id, incomeType: row.income_type as IncomeSource["incomeType"], amount: String(row.amount), frequency: row.frequency as IncomeSource["frequency"], expectedAnnualGrowth: row.growth_assumption === null ? "" : String(row.growth_assumption) })),
    expenses: (expenses.data || []).map((row) => ({ id: row.expense_id, category: row.expense_type as Expense["category"], amount: String(row.amount), frequency: row.frequency as Expense["frequency"] })),
    assets: (assets.data || []).map((row) => { const name = decodeName(row.asset_name, assetOptions); return { id: row.asset_id, assetType: name.primary as Asset["assetType"], description: name.description, currentValue: String(row.current_value), purchaseValue: row.purchase_value === null ? "" : String(row.purchase_value), purchaseDate: row.purchase_date || "" }; }),
    liabilities: (liabilities.data || []).map((row) => { const name = decodeName(row.liability_name, liabilityOptions); return { id: row.liability_id, liabilityType: name.primary as Liability["liabilityType"], description: name.description, outstandingAmount: String(row.outstanding_amount), interestRate: row.interest_rate === null ? "" : String(row.interest_rate), regularPayment: row.emi_amount === null ? "" : String(row.emi_amount), frequency: (row.frequency || "") as Liability["frequency"], endDate: row.end_date || "" }; }),
    goals: (goals.data || []).map((row) => ({ id: row.goal_id, name: row.goal_name, goalType: "" as Goal["goalType"], targetAmount: String(row.target_amount), targetMode: row.target_date ? "Date" as const : "", targetDate: row.target_date || "", targetAge: "", currentSavedAmount: "", monthlyContribution: "", priority: (row.priority || "") as Goal["priority"], flexibility: (row.flexibility || "") as Goal["flexibility"], inflationApplicability: "", notes: "", dynamicDetails: { ...emptyGoalDynamicDetails } })),
  } satisfies OnboardingData;
}

export async function loadOnboardingData(): Promise<OnboardingData> { return loadRows(await getPlanningUnitId()); }
export async function loadGoalPlannerData(): Promise<GoalPlannerData> {
  const planningUnitId = await getPlanningUnitId();
  const [goals, assets] = await Promise.all([supabase.from("goals").select("*").eq("planning_unit_id", planningUnitId).order("created_at"), supabase.from("assets").select("asset_id, asset_name, current_value").eq("planning_unit_id", planningUnitId).order("created_at")]);
  if (goals.error) throw goals.error; if (assets.error) throw assets.error;
  const goalRows = goals.data || []; const goalIds = goalRows.map((goal) => goal.goal_id);
  return { goals: goalRows.map((row) => ({ id: row.goal_id, name: row.goal_name, targetAmount: String(row.target_amount), targetDate: row.target_date || "", priority: row.priority || "", flexibility: row.flexibility || "", funding: [] })), assets: (assets.data || []).map((row) => ({ id: row.asset_id, name: row.asset_name, currentValue: String(row.current_value) })) };
}

export function saveGoals(values: Goal[]) {
  return saveSimpleList(values, "goals", (value, planningUnitId) => ({ planning_unit_id: planningUnitId, goal_name: value.name, target_amount: numeric(value.targetAmount), target_date: nullable(value.targetDate), priority: nullable(value.priority), flexibility: nullable(value.flexibility) }), "goal_id");
}

async function saveSimpleList<T extends { id: string }>(values: T[], table: keyof Tables, map: (value: T, planningUnitId: string) => Record<string, unknown>, idColumn: string) {
  const planningUnitId = await getPlanningUnitId();
  const rows = values.map((value) => ({ ...map(value, planningUnitId), [idColumn]: value.id }));
  const { data, error } = await supabase.from(table).upsert(rows as never, { onConflict: idColumn }).select("*");
  if (error) throw error;
  return { goals: table === "goals" ? (data || []).map((row) => ({ id: row.goal_id, name: row.goal_name, goalType: "" as Goal["goalType"], targetAmount: String(row.target_amount), targetMode: row.target_date ? "Date" as const : "", targetDate: row.target_date || "", targetAge: "", currentSavedAmount: "", monthlyContribution: "", priority: (row.priority || "") as Goal["priority"], flexibility: (row.flexibility || "") as Goal["flexibility"], inflationApplicability: "", notes: "", dynamicDetails: { ...emptyGoalDynamicDetails } })) : [] };
}
