import { supabase } from "../supabase";

export type StrategyEditResult = {
  strategy_id: string;
  strategy_version_id: string;
  strategy_version: number;
  parent_version: number;
  suitability_reassessment_required: boolean;
  approval_snapshot_required: boolean;
  primary_replacement_required: boolean;
};

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function editStrategy(input: { planning_unit_id: string; strategy_id: string; parent_version: number; implementation_parameters: Record<string, unknown> }) {
  if (!backendUrl) throw new Error("Backend URL is not configured.");
  const { data, error } = await supabase.auth.getSession();
  if (error) throw error;
  if (!data.session) throw new Error("Authentication required.");
  const response = await fetch(`${backendUrl}/api/strategy/edit`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${data.session.access_token}` },
    body: JSON.stringify(input),
  });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = typeof body === "object" && body !== null && "detail" in body ? String((body as { detail: unknown }).detail) : `Request failed with status ${response.status}.`;
    throw new Error(detail);
  }
  return body as StrategyEditResult;
}
