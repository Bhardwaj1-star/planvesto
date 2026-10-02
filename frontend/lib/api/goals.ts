import { apiRequest } from "./client";
import type { DefinedGoal } from "../onboarding/goals/types";

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

export function getGoals(planningUnitId: string) {
  return apiRequest<GoalSummary[]>(`/api/goals?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export function getLatestDefinedGoal(planningUnitId: string, goalId: string) {
  return apiRequest<DefinedGoal>(`/api/goals/${encodeURIComponent(goalId)}/defined/latest?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export function getDefinedGoalVersions(planningUnitId: string, goalId: string) {
  return apiRequest<DefinedGoalVersionSummary[]>(`/api/goals/${encodeURIComponent(goalId)}/defined/versions?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export function getDefinedGoalVersion(planningUnitId: string, goalId: string, version: number) {
  return apiRequest<Record<string, unknown>>(`/api/goals/${encodeURIComponent(goalId)}/defined/versions/${version}?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export { getPlanningUnitId } from "./client";
