import { supabase } from "../supabase";

export type SuitabilityStatus = "Suitable" | "Needs Attention" | "Unsuitable";

export type SuitabilityAssessment = {
  status: SuitabilityStatus;
  diagnostics: Array<Record<string, unknown>>;
  rule_set_version: string;
  evaluated_at: string;
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

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  if (!backendUrl) throw new Error("Backend URL is not configured.");
  const { data, error } = await supabase.auth.getSession();
  if (error) throw error;
  if (!data.session) throw new Error("Authentication required.");

  const response = await fetch(`${backendUrl}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${data.session.access_token}`,
      ...(init?.headers ?? {}),
    },
  });

  let body: unknown = null;
  try { body = await response.json(); } catch { /* non-JSON error */ }
  if (!response.ok) {
    const detail = typeof body === "object" && body !== null && "detail" in body
      ? String((body as { detail: unknown }).detail)
      : `Request failed with status ${response.status}.`;
    throw new Error(detail);
  }
  return body as T;
}

export function approveStrategy(requestBody: StrategyApprovalRequest) {
  return request<StrategyApprovalResponse>("/api/strategy/approve", {
    method: "POST",
    body: JSON.stringify(requestBody),
  });
}
