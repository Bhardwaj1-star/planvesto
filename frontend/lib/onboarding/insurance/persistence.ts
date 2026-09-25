import { supabase } from "../../supabase";
import { getPlanningUnitId } from "../../api/client";
import type { InsurancePolicy, InsurancePolicyDraft } from "./types";

const table = () => supabase.from("insurance_policies");

function numeric(value: string | number | null | undefined): number | null {
  if (value == null) return null;
  const trimmed = String(value).trim();
  if (!trimmed) return null;
  const num = Number(trimmed);
  return isNaN(num) ? null : num;
}

function nullable(value: string | null | undefined): string | null {
  if (!value) return null;
  const trimmed = value.trim();
  return trimmed || null;
}

async function planningUnitId(): Promise<string> {
  const { data: sessionData, error: sessionErr } = await supabase.auth.getSession();
  if (sessionErr) throw sessionErr;
  if (!sessionData.session) throw new Error("Authentication required.");
  const userId = sessionData.session.user.id;

  const storedId = getPlanningUnitId();
  if (storedId) {
    const { data } = await supabase
      .from("planning_units")
      .select("planning_unit_id")
      .eq("planning_unit_id", storedId)
      .eq("user_id", userId)
      .maybeSingle();
    if (data?.planning_unit_id) return data.planning_unit_id;
  }

  const { data: existing } = await supabase
    .from("planning_units")
    .select("planning_unit_id")
    .eq("user_id", userId)
    .order("created_at", { ascending: false })
    .limit(1)
    .maybeSingle();

  if (existing?.planning_unit_id) {
    if (typeof window !== "undefined") {
      window.localStorage.setItem("planvesto-planning-unit-id", existing.planning_unit_id);
    }
    return existing.planning_unit_id;
  }

  const { data: created, error: createErr } = await supabase
    .from("planning_units")
    .insert({ user_id: userId })
    .select("planning_unit_id")
    .single();
  if (createErr) throw createErr;
  if (typeof window !== "undefined") {
    window.localStorage.setItem("planvesto-planning-unit-id", created.planning_unit_id);
  }
  return created.planning_unit_id;
}

function mapRow(row: {
  policy_id: string;
  policy_name: string;
  insurer: string | null;
  policy_number: string | null;
  policy_type: string | null;
  premium: number | null;
  premium_frequency: string | null;
  sum_assured: number | null;
  current_value: number | null;
  maturity_date: string | null;
  maturity_value: number | null;
  source: string;
}): InsurancePolicy {
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

async function syncAsset(policy: InsurancePolicyDraft, policyId: string, linkedAssetId: string | null): Promise<string | null> {
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

async function syncExpense(policy: InsurancePolicyDraft, linkedExpenseId: string | null): Promise<string | null> {
  const id = await planningUnitId();
  const premium = numeric(policy.premium);

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
    frequency: policy.premiumFrequency || "Monthly",
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
    const { data } = await table().select("asset_id, expense_id").eq("policy_id", policy.id).eq("planning_unit_id", id).maybeSingle();
    if (data) {
      linkedAssetId = data.asset_id;
      linkedExpenseId = data.expense_id;
    }
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

export async function removeInsurancePolicy(policyId: string): Promise<InsurancePolicy[]> {
  const id = await planningUnitId();
  const { data, error } = await table().select("asset_id, expense_id").eq("policy_id", policyId).eq("planning_unit_id", id).maybeSingle();
  if (error) throw error;
  if (data?.asset_id) {
    const { error: assetError } = await supabase.from("assets").delete().eq("asset_id", data.asset_id).eq("planning_unit_id", id);
    if (assetError) throw assetError;
  }
  if (data?.expense_id) {
    const { error: expenseError } = await supabase.from("expenses").delete().eq("expense_id", data.expense_id).eq("planning_unit_id", id);
    if (expenseError) throw expenseError;
  }
  const { error: policyError } = await table().delete().eq("policy_id", policyId).eq("planning_unit_id", id);
  if (policyError) throw policyError;
  return loadInsurancePolicies();
}
