import { apiRequest } from "./client";

export type StrategyEditResult = {
  strategy_id: string;
  strategy_version_id: string;
  strategy_version: number;
  parent_version: number;
  suitability_reassessment_required: boolean;
  approval_snapshot_required: boolean;
  primary_replacement_required: boolean;
};

export async function editStrategy(input: { planning_unit_id: string; strategy_id: string; parent_version: number; implementation_parameters: Record<string, unknown> }) {
  return apiRequest<StrategyEditResult>("/api/strategy/edit", {
    method: "POST",
    body: JSON.stringify(input),
  });
}
