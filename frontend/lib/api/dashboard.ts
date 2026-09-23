import { apiRequest, getPlanningUnitId } from "./client";

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

export async function getDashboard(): Promise<DashboardData> {
  const planningUnitId = getPlanningUnitId();
  if (!planningUnitId) throw new Error("Planning unit is not configured.");

  return apiRequest<DashboardData>(
    `/api/dashboard?planning_unit_id=${encodeURIComponent(planningUnitId)}`,
  );
}
