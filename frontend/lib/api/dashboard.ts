import { supabase } from "../supabase";
import { getPlanningUnitId } from "./financial-state";

export type DashboardMetric = {
  value: number | null;
  available: boolean;
  reason: string | null;
};

export type DashboardAsset = {
  asset_id: string;
  name: string;
  current_value: number;
};

export type DashboardLiability = {
  liability_id: string;
  name: string;
  outstanding_amount: number;
};

export type DashboardGoal = {
  goal_id: string;
  goal_name: string;
  goal_type: string;
  target_amount: number;
  target_date: string | null;
  priority: string | null;
  flexibility: string | null;
  funding_status: string | null;
  funding_gap: number | null;
  projected_mapped_asset_value: number | null;
  coverage_percentage: number | null;
  image_key: string;
};

export type DashboardData = {
  planning_unit_id: string;
  scope: string;
  financial_state: {
    net_worth: DashboardMetric;
    total_assets: DashboardMetric;
    asset_breakdown: DashboardAsset[];
    total_liabilities: DashboardMetric;
    liability_breakdown: DashboardLiability[];
    income_monthly: DashboardMetric;
    income_annual: DashboardMetric;
    expenses_monthly: DashboardMetric;
    expenses_annual: DashboardMetric;
    investable_surplus_monthly: DashboardMetric;
    investable_surplus_annual: DashboardMetric;
  };
  goals: DashboardGoal[];
};

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function getDashboard(): Promise<DashboardData> {
  if (!backendUrl) throw new Error("Backend URL is not configured.");
  const planningUnitId = getPlanningUnitId();
  if (!planningUnitId) throw new Error("Planning unit is not configured.");

  const { data, error } = await supabase.auth.getSession();
  if (error) throw error;
  if (!data.session) throw new Error("Authentication required.");

  const response = await fetch(
    `${backendUrl}/api/dashboard?planning_unit_id=${encodeURIComponent(planningUnitId)}`,
    { headers: { Authorization: `Bearer ${data.session.access_token}` } },
  );

  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = body && typeof body === "object" && "detail" in body
      ? String((body as { detail: unknown }).detail)
      : `Request failed with status ${response.status}.`;
    throw new Error(detail);
  }
  return body as DashboardData;
}
