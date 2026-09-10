import { supabase } from "../supabase";

export type GoalSummary = {
  goal_id: string;
  planning_unit_id: string;
  goal_name: string;
  target_amount: number;
  target_date: string | null;
  priority: string | null;
  flexibility: string | null;
};

export type DefinedGoalVersionSummary = {
  defined_goal_id: string;
  goal_id: string;
  version: number;
  is_latest: boolean;
  today_cost: number;
  future_target: number;
  projected_mapped_asset_value: number;
  funding_gap: number;
  funding_status: string;
  created_at: string;
};

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

async function request<T>(path: string): Promise<T> {
  if (!backendUrl) throw new Error("Backend URL is not configured.");
  const { data, error } = await supabase.auth.getSession();
  if (error) throw error;
  if (!data.session) throw new Error("Authentication required.");
  const response = await fetch(`${backendUrl}${path}`, {
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${data.session.access_token}` },
  });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof body === "object" && body !== null && "detail" in body ? String((body as { detail: unknown }).detail) : `Request failed with status ${response.status}.`;
    throw new Error(detail);
  }
  return body as T;
}

export function getGoals(planningUnitId: string) {
  return request<GoalSummary[]>(`/api/goals?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export function getLatestDefinedGoal(planningUnitId: string, goalId: string) {
  return request<Record<string, unknown>>(`/api/goals/${encodeURIComponent(goalId)}/defined/latest?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export function getDefinedGoalVersions(planningUnitId: string, goalId: string) {
  return request<DefinedGoalVersionSummary[]>(`/api/goals/${encodeURIComponent(goalId)}/defined/versions?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export function getDefinedGoalVersion(planningUnitId: string, goalId: string, version: number) {
  return request<Record<string, unknown>>(`/api/goals/${encodeURIComponent(goalId)}/defined/versions/${version}?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export { getPlanningUnitId } from "./strategy";
