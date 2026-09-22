import { supabase } from "../supabase";

export type ActionStatus = "planned" | "confirmed" | "completed" | "cancelled";
export type ActionDecision = "add" | "modify" | "delete" | "complete" | "cancel";

export type ActionPlanItem = {
  action_id: string | null;
  planning_unit_id: string;
  strategy_version_id: string;
  title: string;
  description: string | null;
  priority: "high" | "medium" | "low";
  deadline: string | null;
  status: ActionStatus;
  planned_impact: Record<string, unknown>;
  actual_impact: Record<string, unknown>;
  created_at: string;
};

export type ActionImpactPreview = {
  action: Record<string, unknown>;
  financial_state_impact: Record<string, unknown>;
  goal_impacts: Array<Record<string, unknown>>;
  strategy_impact: Record<string, unknown>;
  financial_health_impact: Record<string, unknown>;
  alternatives: Array<Record<string, unknown>>;
  cause_explanation: string | null;
};

export type ActionDecisionRecord = {
  decision_id: string | null;
  planning_unit_id: string;
  action_id: string;
  decision: ActionDecision;
  before_state: Record<string, unknown>;
  after_state: Record<string, unknown>;
  impact_preview: ActionImpactPreview;
  confirmed_at: string;
  historical: boolean;
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
  try { body = await response.json(); } catch {}
  if (!response.ok) {
    const detail = typeof body === "object" && body !== null && "detail" in body
      ? String((body as { detail: unknown }).detail)
      : `Request failed with status ${response.status}.`;
    throw new Error(detail);
  }
  return body as T;
}

export function getPlanningUnitId(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("planvesto-planning-unit-id");
}

export function getActions(planningUnitId: string) {
  return request<ActionPlanItem[]>(`/api/action-plan/actions?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export function generateStrategyActions(planningUnitId: string, strategyVersionId: string) {
  return request<ActionPlanItem[]>(
    `/api/action-plan/actions/generate?planning_unit_id=${encodeURIComponent(planningUnitId)}&strategy_version_id=${encodeURIComponent(strategyVersionId)}`,
    { method: "POST" },
  );
}

export function getAction(planningUnitId: string, actionId: string) {
  return request<ActionPlanItem>(`/api/action-plan/actions/${encodeURIComponent(actionId)}?planning_unit_id=${encodeURIComponent(planningUnitId)}`);
}

export function getDecisionHistory(planningUnitId: string, actionId?: string) {
  const query = actionId ? `&action_id=${encodeURIComponent(actionId)}` : "";
  return request<ActionDecisionRecord[]>(`/api/action-plan/decisions?planning_unit_id=${encodeURIComponent(planningUnitId)}${query}`);
}

export function confirmActionDecision(
  planningUnitId: string,
  action: ActionPlanItem,
  decision: ActionDecision,
  afterState: Record<string, unknown> = {},
  impactPreview?: Partial<ActionImpactPreview>,
) {
  const preview: ActionImpactPreview = {
    action: { action_id: action.action_id, title: action.title, decision },
    financial_state_impact: {},
    goal_impacts: [],
    strategy_impact: {},
    financial_health_impact: {},
    alternatives: [],
    cause_explanation: null,
    ...impactPreview,
  };
  return request<{ decision_id: string | null; action_id: string; decision: string; confirmed_at: string; historical: boolean }>("/api/action-plan/decisions", {
    method: "POST",
    body: JSON.stringify({ planning_unit_id: planningUnitId, action_id: action.action_id, decision, impact_preview: preview, after_state: afterState }),
  });
}

export function createAction(input: {
  planning_unit_id: string;
  strategy_version_id: string;
  title: string;
  description?: string | null;
  priority?: "high" | "medium" | "low";
  deadline?: string | null;
  planned_impact?: Record<string, unknown>;
}) {
  return request<ActionPlanItem>("/api/action-plan/actions", { method: "POST", body: JSON.stringify(input) });
}

export function completeAction(
  planningUnitId: string,
  actionId: string,
  completionPreview?: Partial<ActionImpactPreview>,
) {
  const preview: ActionImpactPreview = {
    action: { action_id: actionId, decision: "complete" },
    financial_state_impact: {},
    goal_impacts: [],
    strategy_impact: {},
    financial_health_impact: {},
    alternatives: [],
    cause_explanation: null,
    ...completionPreview,
  };
  return request<ActionPlanItem>(
    "/api/action-plan/actions/" + encodeURIComponent(actionId) + "/complete",
    {
      method: "POST",
      body: JSON.stringify({ planning_unit_id: planningUnitId, action_id: actionId, completion_preview: preview }),
    },
  );
}
