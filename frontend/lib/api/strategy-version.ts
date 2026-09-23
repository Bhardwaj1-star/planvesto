import { apiRequest } from "./client";

export type StrategyVersion = {
  strategy_version_id: string | null;
  planning_unit_id: string;
  strategy_id: string;
  version: number;
  parent_version: number | null;
  source: "library" | "investor_edit";
  library_version: string;
  implementation_version: string;
  implementation_parameters: Record<string, unknown>;
  status: "draft" | "approved" | "primary" | "archived" | "needs_review" | "provisional";
  created_at: string;
};

export function getStrategyVersionById(planningUnitId: string, strategyVersionId: string) {
  return apiRequest<StrategyVersion>(
    `/api/strategy/versions/by-id/${encodeURIComponent(strategyVersionId)}?planning_unit_id=${encodeURIComponent(planningUnitId)}`,
  );
}

export function getStrategyVersionHistory(planningUnitId: string, strategyId: string) {
  return apiRequest<StrategyVersion[]>(`/api/strategy/versions/${encodeURIComponent(strategyId)}?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export function getCurrentPrimaryStrategy(planningUnitId: string) {
  return apiRequest<{
    planning_unit_id: string;
    strategy_id: string;
    strategy_version_id: string;
    approval_snapshot_id: string;
    status: string;
    previous_strategy_id: string | null;
    previous_strategy_version_id: string | null;
    pending_action_disposition: string | null;
    transition_metadata: Record<string, unknown>;
    updated_at: string;
  } | null>(`/api/strategy/primary?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}
