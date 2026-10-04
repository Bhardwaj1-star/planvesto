import { apiRequest } from "./client";
import type { StrategyVersion } from "./strategy";

export type { StrategyVersion } from "./strategy";

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
