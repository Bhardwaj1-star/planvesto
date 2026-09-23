import { apiRequest } from "./client";

export type SuitabilityStatus = "Suitable" | "Needs Attention" | "Unsuitable";

export type SuitabilityAssessment = {
  status: SuitabilityStatus;
  diagnostics?: Array<Record<string, unknown>>;
  rule_set_version?: string;
  evaluated_at?: string;
};

export type StrategyApprovalRequest = {
  planning_unit_id: string;
  strategy_run_id: string;
  suitability: SuitabilityAssessment;
  acknowledgement_text?: string | null;
  make_primary?: boolean;
  primary_transition_decision?: "archive_previous" | "keep_previous_approved" | null;
  pending_action_disposition?: "retain_for_reassessment" | "cancel" | null;
};

export type StrategyApprovalResponse = {
  approval_snapshot_id: string | null;
  strategy_id: string;
  strategy_version_id: string;
  strategy_version: number;
  suitability_status: string;
  is_primary: boolean;
  approved_at: string;
};

export function approveStrategy(requestBody: StrategyApprovalRequest) {
  return apiRequest<StrategyApprovalResponse>("/api/strategy/approve", { method: "POST", body: JSON.stringify(requestBody) });
}
