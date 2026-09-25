import { supabase } from "@/lib/supabase";

export type InsurancePolicyInput = {
  planningUnitId: string;
  policyName: string;
  insurer?: string;
  policyNumber?: string;
  policyType?: string;
  premium?: number;
  premiumFrequency?: string;
  sumAssured?: number;
  currentValue?: number;
  maturityDate?: string;
  maturityValue?: number;
  source?: "manual" | "pdf";
};

export async function saveInsurancePolicy(input: InsurancePolicyInput) {
  const { data, error } = await supabase
    .from("insurance_policies")
    .insert({
      planning_unit_id: input.planningUnitId,
      policy_name: input.policyName,
      insurer: input.insurer ?? null,
      policy_number: input.policyNumber ?? null,
      policy_type: input.policyType ?? null,
      premium: input.premium ?? null,
      premium_frequency: input.premiumFrequency ?? null,
      sum_assured: input.sumAssured ?? null,
      current_value: input.currentValue ?? null,
      maturity_date: input.maturityDate ?? null,
      maturity_value: input.maturityValue ?? null,
      source: input.source ?? "manual",
    })
    .select()
    .single();

  if (error) throw error;
  return data;
}

export async function getInsurancePolicies(planningUnitId: string) {
  const { data, error } = await supabase
    .from("insurance_policies")
    .select("*")
    .eq("planning_unit_id", planningUnitId)
    .order("created_at", { ascending: false });

  if (error) throw error;
  return data ?? [];
}
