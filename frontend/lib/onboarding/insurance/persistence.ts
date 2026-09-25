import { supabase } from "../../supabase";
import { getPlanningUnitId } from "../../api/client";
import type { InsurancePolicy, InsurancePolicyDraft } from "./types";

const table = () => (supabase.from("insurance_policies") as any);

function numeric(value: string) {
  const trimmed = value.trim();
  return trimmed ? Number(trimmed) : null;
}

function nullable(value: string) {
  return value.trim() || null;
}

async function planningUnitId() {
  const id = getPlanningUnitId();
  if (!id) throw new Error("Financial planning unit is not available. Please reload your profile.");
  const { data: session, error } = await supabase.auth.getSession();
  if (error) throw error;
  if (!session.session) throw new Error("Authentication required.");
  return id;
}

function mapRow(row: any): InsurancePolicy {
  return {
    id: row.policy_id,
    policyName: row.policy_name || "",
    insurer: row.insurer || "",
    policyNumber: row.policy_number || "",
    policyType: row.policy_type || "",
    premium: row.premium == null ? "" : String(row.premium),
    premiumFrequency: (row.premium_frequency || "Monthly") as InsurancePolicy["premiumFrequency"],
    sumAssured: row.sum_assured == null ? "" : String(row.sum_assured),
    currentValue: row.current_value == null ? "" : String(row.current_value),
    maturityDate: row.maturity_date || "",
    maturityValue: row.maturity_value == null ? "" : String(row.maturity_value),
    source: row.source === "pdf" ? "pdf" : "manual",
  };
}

export async function loadInsurancePolicies(): Promise<InsurancePolicy[]> {
  const id = await planningUnitId();
  const { data, error } = await table().select("*").eq("planning_unit_id", id).order("created_at");
  if (error) throw error;
  return (data || []).map(mapRow);
}

async function syncAsset(policy: InsurancePolicyDraft, policyId: string, linkedAssetId: string | null) {
  const id = await planningUnitId();
  const currentValue = numeric(policy.currentValue);
  const name = `Insurance - ${policy.policyName.trim()}`;

  if (!currentValue || currentValue <= 0) {
    if (linkedAssetId) {
      const { error } = await supabase.from("assets").delete().eq("asset_id", linkedAssetId).eq("planning_unit_id", id);
      if (error) throw error;
    }
    return null;
  }

  const payload = {
    planning_unit_id: id,
    asset_name: name,
    current_value: currentValue,
    purchase_value: null,
    purchase_date: null,
  };
  if (linkedAssetId) {
    const { data, error } = await supabase.from("assets").update(payload).eq("asset_id", linkedAssetId).eq("planning_unit_id", id).select("asset_id").single();
    if (error) throw error;
    return data.asset_id;
  }
  const { data, error } = await supabase.from("assets").insert(payload).select("asset_id").single();
  if (error) throw error;
  return data.asset_id;
}

async function syncExpense(policy: InsurancePolicyDraft, linkedExpenseId: string | null) {
  const id = await planningUnitId();
  const premium = numeric(policy.premium);
  const name = `Insurance - ${policy.policyName.trim()}`;

  if (!premium || premium <= 0) {
    if (linkedExpenseId) {
      const { error } = await supabase.from("expenses").delete().eq("expense_id", linkedExpenseId).eq("planning_unit_id", id);
      if (error) throw error;
    }
    return null;
  }

  const payload = {
    planning_unit_id: id,
    expense_type: "Insurance",
    amount: premium,
    frequency: policy.premiumFrequency,
  };
  if (linkedExpenseId) {
    const { data, error } = await supabase.from("expenses").update(payload).eq("expense_id", linkedExpenseId).eq("planning_unit_id", id).select("expense_id").single();
    if (error) throw error;
    return data.expense_id;
  }
  const { data, error } = await supabase.from("expenses").insert(payload).select("expense_id").single();
  if (error) throw error;
  return data.expense_id;
}

export async function saveInsurancePolicy(policy: InsurancePolicyDraft): Promise<InsurancePolicy[]> {
  const id = await planningUnitId();
  if (!policy.policyName.trim()) throw new Error("Policy name is required.");

  let linkedAssetId: string | null = null;
  let linkedExpenseId: string | null = null;
  if (policy.id) {
    const { data, error } = await table().select("asset_id, expense_id").eq("policy_id", policy.id).eq("planning_unit_id", id).single();
    if (error) throw error;
    linkedAssetId = data.asset_id;
    linkedExpenseId = data.expense_id;
  }

  linkedAssetId = await syncAsset(policy, policy.id || "", linkedAssetId);
  linkedExpenseId = await syncExpense(policy, linkedExpenseId);

  const payload = {
    planning_unit_id: id,
    policy_name: policy.policyName.trim(),
    insurer: nullable(policy.insurer),
    policy_number: nullable(policy.policyNumber),
    policy_type: nullable(policy.policyType),
    premium: numeric(policy.premium),
    premium_frequency: nullable(policy.premiumFrequency),
    sum_assured: numeric(policy.sumAssured),
    current_value: numeric(policy.currentValue),
    maturity_date: nullable(policy.maturityDate),
    maturity_value: numeric(policy.maturityValue),
    asset_id: linkedAssetId,
    expense_id: linkedExpenseId,
    source: policy.source || "manual",
    updated_at: new Date().toISOString(),
  };

  const result = policy.id
    ? await table().update(payload).eq("policy_id", policy.id).eq("planning_unit_id", id)
    : await table().insert(payload);
  if (result.error) throw result.error;
  return loadInsurancePolicies();
}

export async function removeInsurancePolicy(policyId: string) {
  const id = await planningUnitId();
  const { data, error } = await table().select("asset_id, expense_id").eq("policy_id", policyId).eq("planning_unit_id", id).single();
  if (error) throw error;
  if (data.asset_id) {
    const { error: assetError } = await supabase.from("assets").delete().eq("asset_id", data.asset_id).eq("planning_unit_id", id);
    if (assetError) throw assetError;
  }
  if (data.expense_id) {
    const { error: expenseError } = await supabase.from("expenses").delete().eq("expense_id", data.expense_id).eq("planning_unit_id", id);
    if (expenseError) throw expenseError;
  }
  const { error: policyError } = await table().delete().eq("policy_id", policyId).eq("planning_unit_id", id);
  if (policyError) throw policyError;
  return loadInsurancePolicies();
}
