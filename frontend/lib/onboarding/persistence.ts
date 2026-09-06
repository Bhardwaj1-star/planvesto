import { supabase } from "../supabase";
import type { Database } from "../database.types";
import type { Asset } from "./assets/types";
import type { Expense } from "./expenses/types";
import type { FamilyMember } from "./family-dependents/types";
import type { Goal } from "./goals/types";
import type { IncomeSource } from "./income/types";
import type { Liability } from "./liabilities/types";
import type { PersonalInformation } from "./personal-information/model";

import type { Commitment } from "./commitments/types";

export type { Commitment };

export type GoalFundingAllocation = {
  assetId: string;
  allocationPercentage: string;
};

export type GoalPlannerGoal = {
  id: string;
  name: string;
  targetAmount: string;
  targetDate: string;
  priority: string;
  flexibility: string;
  funding: GoalFundingAllocation[];
};

export type GoalPlannerData = {
  goals: GoalPlannerGoal[];
  assets: Array<{ id: string; name: string; currentValue: string }>;
};

export type OnboardingData = {
  planningUnitId: string;
  investorId: string | null;
  personalInformation: PersonalInformation;
  familyMembers: FamilyMember[];
  incomeSources: IncomeSource[];
  expenses: Expense[];
  assets: Asset[];
  liabilities: Liability[];
  commitments: Commitment[];
  goals: Goal[];
};

type Tables = Database["public"]["Tables"];
const planningUnitStorageKey = "planvesto-planning-unit-id";
let planningUnitPromise: Promise<string> | null = null;
let planningUnitUserId: string | null = null;

async function getAuthenticatedUser() {
  const { data, error } = await supabase.auth.getUser();
  if (error) throw error;
  if (!data.user) throw new Error("You must be signed in to access onboarding.");
  return data.user;
}

function isUuid(value: string) {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value);
}

function nullable(value: string) {
  return value.trim() || null;
}

function numeric(value: string): number;
function numeric(value: string, optional: true): number | null;
function numeric(value: string, optional = false) {
  if (optional && !value.trim()) return null;
  return Number(value);
}

function encodeName(primary: string, description: string) {
  return description.trim() ? `${primary} - ${description.trim()}` : primary;
}

function decodeName(value: string, options: readonly string[]) {
  const option = options.find((item) => value === item || value.startsWith(`${item} - `));
  return { primary: option || "", description: option ? value.slice(option.length).replace(/^ - /, "") : value };
}

async function getPlanningUnitId() {
  const user = await getAuthenticatedUser();
  if (planningUnitPromise && planningUnitUserId === user.id) return planningUnitPromise;

  planningUnitUserId = user.id;
  planningUnitPromise = (async () => {
  const storedId = typeof window !== "undefined" ? window.localStorage.getItem(planningUnitStorageKey) : null;
  if (storedId && isUuid(storedId)) {
    const { data, error } = await supabase.from("planning_units").select("planning_unit_id").eq("planning_unit_id", storedId).eq("user_id", user.id).maybeSingle();
    if (error) throw error;
    if (data) return data.planning_unit_id;
  }

  const { data, error } = await supabase.from("planning_units").insert({ user_id: user.id }).select("planning_unit_id").single();
  if (error) throw error;
  if (typeof window !== "undefined") window.localStorage.setItem(planningUnitStorageKey, data.planning_unit_id);
  return data.planning_unit_id;
  })();

  try {
    return await planningUnitPromise;
  } catch (error) {
    planningUnitPromise = null;
    planningUnitUserId = null;
    throw error;
  }
}

async function loadRows(planningUnitId: string) {
  const [investors, dependents, income, expenses, assets, liabilities, commitments, goals] = await Promise.all([
    supabase.from("investors").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("dependents").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("income").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("expenses").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("assets").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("liabilities").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("commitments").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("goals").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
  ]);
  const result = [investors, dependents, income, expenses, assets, liabilities, commitments, goals].find((item) => item.error);
  if (result?.error) throw result.error;

  const investorRows = investors.data || [];
  const personal = investorRows[0];
  const assetOptions = ["Bank / Cash", "Fixed Deposits", "Mutual Funds", "Stocks / Equity", "Bonds / Debt", "EPF / PPF", "NPS", "Gold", "Real Estate", "Business Ownership", "Vehicle", "Other"] as const;
  const liabilityOptions = ["Home Loan", "Car Loan", "Personal Loan", "Education Loan", "Business Loan", "Credit Card", "Other"] as const;

  return {
    planningUnitId,
    investorId: personal?.investor_id || null,
    personalInformation: {
      fullName: personal?.full_name || "",
      dateOfBirth: personal?.date_of_birth || "",
      gender: personal?.gender || "",
      maritalStatus: personal?.marital_status || "",
      mobileNumber: personal?.mobile_number || "",
      address: personal?.address || "",
      city: personal?.city || "",
      state: personal?.state || "",
      country: personal?.country || "",
      occupation: personal?.occupation || "",
    },
    familyMembers: (dependents.data || []).map((row) => ({
      id: row.dependent_id,
      name: row.name,
      relationship: row.relationship || "",
      dateOfBirth: row.date_of_birth || "",
      occupation: row.occupation || "",
      financialDependency: Boolean(row.financial_dependency),
      includeInPlanning: Boolean(row.include_in_planning),
    })),
    incomeSources: (income.data || []).map((row) => ({
      id: row.income_id,
      incomeType: row.income_type as IncomeSource["incomeType"],
      amount: String(row.amount),
      frequency: row.frequency as IncomeSource["frequency"],
      expectedAnnualGrowth: row.growth_assumption === null ? "" : String(row.growth_assumption),
    })),
    expenses: (expenses.data || []).map((row) => ({
      id: row.expense_id,
      category: row.expense_type as Expense["category"],
      amount: String(row.amount),
      frequency: row.frequency as Expense["frequency"],
    })),
    assets: (assets.data || []).map((row) => {
      const name = decodeName(row.asset_name, assetOptions);
      return {
        id: row.asset_id,
        assetType: name.primary as Asset["assetType"],
        description: name.description,
        currentValue: String(row.current_value),
        purchaseValue: row.purchase_value === null ? "" : String(row.purchase_value),
        purchaseDate: row.purchase_date || "",
      };
    }),
    liabilities: (liabilities.data || []).map((row) => {
      const name = decodeName(row.liability_name, liabilityOptions);
      return {
        id: row.liability_id,
        liabilityType: name.primary as Liability["liabilityType"],
        description: name.description,
        outstandingAmount: String(row.outstanding_amount),
        interestRate: row.interest_rate === null ? "" : String(row.interest_rate),
        regularPayment: row.emi_amount === null ? "" : String(row.emi_amount),
        frequency: (row.frequency || "") as Liability["frequency"],
        endDate: row.end_date || "",
      };
    }),
    commitments: (commitments.data || []).map((row) => ({ id: row.commitment_id, name: row.commitment_name, amount: String(row.amount) })),
    goals: (goals.data || []).map((row) => ({
      id: row.goal_id,
      name: row.goal_name,
      goalType: "",
      targetAmount: String(row.target_amount),
      targetMode: row.target_date ? "Date" : "",
      targetDate: row.target_date || "",
      targetAge: "",
      currentSavedAmount: "",
      monthlyContribution: "",
      priority: (row.priority || "") as Goal["priority"],
      flexibility: (row.flexibility || "") as Goal["flexibility"],
      inflationApplicability: "",
      notes: "",
    })),
  } satisfies OnboardingData;
}

export async function loadOnboardingData(): Promise<OnboardingData> {
  return loadRows(await getPlanningUnitId());
}

export async function loadGoalPlannerData(): Promise<GoalPlannerData> {
  const planningUnitId = await getPlanningUnitId();
  const [goals, assets] = await Promise.all([
    supabase.from("goals").select("*").eq("planning_unit_id", planningUnitId).order("created_at"),
    supabase.from("assets").select("asset_id, asset_name, current_value").eq("planning_unit_id", planningUnitId).order("created_at"),
  ]);
  if (goals.error) throw goals.error;
  if (assets.error) throw assets.error;

  const goalIds = (goals.data || []).map((goal) => goal.goal_id);
  const funding = goalIds.length
    ? await supabase.from("goal_funding").select("goal_id, asset_id, allocation_percentage").in("goal_id", goalIds)
    : { data: [], error: null };
  if (funding.error) throw funding.error;

  return {
    goals: (goals.data || []).map((goal) => ({
      id: goal.goal_id,
      name: goal.goal_name,
      targetAmount: String(goal.target_amount),
      targetDate: goal.target_date ? goal.target_date.slice(0, 7) : "",
      priority: goal.priority || "",
      flexibility: goal.flexibility || "",
      funding: (funding.data || [])
        .filter((row) => row.goal_id === goal.goal_id)
        .map((row) => ({ assetId: row.asset_id, allocationPercentage: String(row.allocation_percentage) })),
    })),
    assets: (assets.data || []).map((asset) => ({ id: asset.asset_id, name: asset.asset_name, currentValue: String(asset.current_value) })),
  };
}

export async function saveGoalPlannerData(values: GoalPlannerGoal[]): Promise<GoalPlannerData> {
  const planningUnitId = await getPlanningUnitId();
  const { data: existingGoals, error: existingError } = await supabase.from("goals").select("goal_id").eq("planning_unit_id", planningUnitId);
  if (existingError) throw existingError;
  const existingIds = (existingGoals || []).map((goal) => goal.goal_id);
  const retainedIds = values.filter((goal) => isUuid(goal.id)).map((goal) => goal.id);
  const removedIds = existingIds.filter((id) => !retainedIds.includes(id));

  if (removedIds.length) {
    const { error } = await supabase.from("goals").delete().in("goal_id", removedIds).eq("planning_unit_id", planningUnitId);
    if (error) throw error;
  }

  for (const value of values) {
    const payload: Tables["goals"]["Insert"] = {
      planning_unit_id: planningUnitId,
      goal_name: value.name,
      target_amount: numeric(value.targetAmount),
      target_date: value.targetDate ? `${value.targetDate}-01` : null,
      priority: nullable(value.priority),
      flexibility: nullable(value.flexibility),
    };
    const result = isUuid(value.id)
      ? await supabase.from("goals").update(payload).eq("goal_id", value.id).eq("planning_unit_id", planningUnitId).select("goal_id").single()
      : await supabase.from("goals").insert(payload).select("goal_id").single();
    if (result.error) throw result.error;

    const goalId = result.data.goal_id;
    const { error: deleteFundingError } = await supabase.from("goal_funding").delete().eq("goal_id", goalId);
    if (deleteFundingError) throw deleteFundingError;
    const fundingRows: Tables["goal_funding"]["Insert"][] = value.funding
      .filter((allocation) => isUuid(allocation.assetId) && allocationPercentageIsValid(allocation.allocationPercentage))
      .map((allocation) => ({
        goal_id: goalId,
        asset_id: allocation.assetId,
        allocation_percentage: Number(allocation.allocationPercentage),
      }));
    if (fundingRows.length) {
      const { error } = await supabase.from("goal_funding").insert(fundingRows);
      if (error) throw error;
    }
  }

  return loadGoalPlannerData();
}

function allocationPercentageIsValid(value: string) {
  const percentage = Number(value);
  return Number.isFinite(percentage) && percentage >= 0 && percentage <= 100;
}

export async function savePersonalInformation(value: PersonalInformation) {
  const planningUnitId = await getPlanningUnitId();
  const { data: existing, error: existingError } = await supabase.from("investors").select("investor_id").eq("planning_unit_id", planningUnitId).order("created_at").limit(1).maybeSingle();
  if (existingError) throw existingError;
  const payload: Tables["investors"]["Insert"] = {
    planning_unit_id: planningUnitId,
    full_name: value.fullName,
    date_of_birth: nullable(value.dateOfBirth),
    gender: nullable(value.gender),
    marital_status: nullable(value.maritalStatus),
    mobile_number: nullable(value.mobileNumber),
    address: nullable(value.address),
    city: nullable(value.city),
    state: nullable(value.state),
    country: nullable(value.country),
    occupation: nullable(value.occupation),
  };
  const request = existing
    ? supabase.from("investors").update(payload).eq("investor_id", existing.investor_id).eq("planning_unit_id", planningUnitId)
    : supabase.from("investors").insert(payload);
  const { error } = await request;
  if (error) throw error;
  return loadRows(planningUnitId);
}

export async function saveFamilyMembers(values: FamilyMember[]) {
  const planningUnitId = await getPlanningUnitId();
  const { data: existing, error: existingError } = await supabase.from("dependents").select("dependent_id").eq("planning_unit_id", planningUnitId);
  if (existingError) throw existingError;
  const ids = values.filter((value) => isUuid(value.id)).map((value) => value.id);
  const removed = (existing || []).map((row) => row.dependent_id).filter((id) => !ids.includes(id));
  if (removed.length) {
    const { error } = await supabase.from("dependents").delete().in("dependent_id", removed).eq("planning_unit_id", planningUnitId);
    if (error) throw error;
  }
  for (const value of values) {
    const payload: Tables["dependents"]["Insert"] = {
      planning_unit_id: planningUnitId,
      name: value.name,
      relationship: nullable(value.relationship),
      date_of_birth: nullable(value.dateOfBirth),
      occupation: nullable(value.occupation),
      financial_dependency: Boolean(value.financialDependency),
      include_in_planning: Boolean(value.includeInPlanning),
    };
    const request = isUuid(value.id)
      ? supabase.from("dependents").update(payload).eq("dependent_id", value.id).eq("planning_unit_id", planningUnitId)
      : supabase.from("dependents").insert(payload);
    const { error } = await request;
    if (error) throw error;
  }
  return loadRows(planningUnitId);
}

export async function saveIncomeSources(values: IncomeSource[]) {
  const planningUnitId = await getPlanningUnitId();
  const { data: investor, error: investorError } = await supabase.from("investors").select("investor_id").eq("planning_unit_id", planningUnitId).order("created_at").limit(1).maybeSingle();
  if (investorError) throw investorError;
  if (!investor) throw new Error("Complete personal information before saving income.");
  const { data: existing, error: existingError } = await supabase.from("income").select("income_id").eq("planning_unit_id", planningUnitId);
  if (existingError) throw existingError;
  const ids = values.filter((value) => isUuid(value.id)).map((value) => value.id);
  const removed = (existing || []).map((row) => row.income_id).filter((id) => !ids.includes(id));
  if (removed.length) {
    const { error } = await supabase.from("income").delete().in("income_id", removed).eq("planning_unit_id", planningUnitId);
    if (error) throw error;
  }
  for (const value of values) {
    const payload: Tables["income"]["Insert"] = {
      planning_unit_id: planningUnitId,
      investor_id: investor.investor_id,
      income_type: value.incomeType,
      amount: numeric(value.amount),
      frequency: value.frequency,
      growth_assumption: numeric(value.expectedAnnualGrowth, true),
    };
    const request = isUuid(value.id)
      ? supabase.from("income").update(payload).eq("income_id", value.id).eq("planning_unit_id", planningUnitId)
      : supabase.from("income").insert(payload);
    const { error } = await request;
    if (error) throw error;
  }
  return loadRows(planningUnitId);
}

async function saveSimpleList<T extends { id: string }>(
  values: T[],
  table: "expenses" | "assets" | "liabilities" | "commitments" | "goals",
  toInsert: (value: T, planningUnitId: string) => Tables[typeof table]["Insert"],
  idColumn: "expense_id" | "asset_id" | "liability_id" | "commitment_id" | "goal_id",
) {
  const planningUnitId = await getPlanningUnitId();
  const { data: existing, error: existingError } = await supabase.from(table).select(idColumn).eq("planning_unit_id", planningUnitId);
  if (existingError) throw existingError;
  const ids = values.filter((value) => isUuid(value.id)).map((value) => value.id);
  const removed = (existing || []).map((row) => (row as unknown as Record<string, string>)[idColumn]).filter((id) => !ids.includes(id));
  if (removed.length) {
    const { error } = await supabase.from(table).delete().in(idColumn, removed).eq("planning_unit_id", planningUnitId);
    if (error) throw error;
  }
  for (const value of values) {
    const payload = toInsert(value, planningUnitId);
    const request = isUuid(value.id)
      ? supabase.from(table).update(payload).eq(idColumn, value.id).eq("planning_unit_id", planningUnitId)
      : supabase.from(table).insert(payload as never);
    const { error } = await request;
    if (error) throw error;
  }
  return loadRows(planningUnitId);
}

export function saveExpenses(values: Expense[]) {
  return saveSimpleList(values, "expenses", (value, planningUnitId) => ({ planning_unit_id: planningUnitId, expense_type: value.category, amount: numeric(value.amount), frequency: value.frequency }), "expense_id");
}

export function saveAssets(values: Asset[]) {
  return saveSimpleList(values, "assets", (value, planningUnitId) => ({ planning_unit_id: planningUnitId, asset_name: encodeName(value.assetType, value.description), current_value: numeric(value.currentValue), purchase_value: numeric(value.purchaseValue, true), purchase_date: nullable(value.purchaseDate) }), "asset_id");
}

export function saveLiabilities(values: Liability[]) {
  return saveSimpleList(values, "liabilities", (value, planningUnitId) => ({ planning_unit_id: planningUnitId, liability_name: encodeName(value.liabilityType, value.description), outstanding_amount: numeric(value.outstandingAmount), interest_rate: numeric(value.interestRate, true), emi_amount: numeric(value.regularPayment, true), frequency: nullable(value.frequency), end_date: nullable(value.endDate) }), "liability_id");
}

export function saveCommitments(values: Commitment[]) {
  return saveSimpleList(values, "commitments", (value, planningUnitId) => ({ planning_unit_id: planningUnitId, commitment_name: value.name, amount: numeric(value.amount) }), "commitment_id");
}

export function saveGoals(values: Goal[]) {
  return saveSimpleList(values, "goals", (value, planningUnitId) => ({ planning_unit_id: planningUnitId, goal_name: value.name, target_amount: numeric(value.targetAmount), target_date: nullable(value.targetDate), priority: nullable(value.priority), flexibility: nullable(value.flexibility) }), "goal_id");
}