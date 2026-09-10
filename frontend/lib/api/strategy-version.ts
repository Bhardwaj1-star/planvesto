import { supabase } from "../supabase";

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

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

async function request<T>(path: string): Promise<T> {
  if (!backendUrl) throw new Error("Backend URL is not configured.");
  const { data, error } = await supabase.auth.getSession();
  if (error) throw error;
  if (!data.session) throw new Error("Authentication required.");
  const response = await fetch(`${backendUrl}${path}`, {
    headers: {
      Authorization: `Bearer ${data.session.access_token}`,
      "Content-Type": "application/json",
    },
  });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof body === "object" && body !== null && "detail" in body
      ? String((body as { detail: unknown }).detail)
      : `Request failed with status ${response.status}.`;
    throw new Error(detail);
  }
  return body as T;
}

export function getStrategyVersionHistory(planningUnitId: string, strategyId: string) {
  return request<StrategyVersion[]>(`/api/strategy/versions/${encodeURIComponent(strategyId)}?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export function getCurrentPrimaryStrategy(planningUnitId: string) {
  return request<{
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
