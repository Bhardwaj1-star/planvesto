import { supabase } from "../supabase";

export type MoneywheelStatus =
  | "excellent"
  | "healthy"
  | "attention"
  | "critical"
  | "unavailable";

export type MoneywheelRatio = {
  key: string;
  name: string;
  value: number | null;
  unit: string;
  status: MoneywheelStatus;
  formula: string;
  explanation: string;
  available: boolean;
};

export type MoneywheelResult = {
  planning_unit_id: string;
  overall_status: "excellent" | "healthy" | "attention" | "critical" | "incomplete" | null;
  ratios: MoneywheelRatio[];
  rule_set_version: string;
  calculated_at: string;
  metadata: Record<string, unknown>;
};

export type MoneywheelResponse = {
  result: MoneywheelResult;
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
  try {
    body = await response.json();
  } catch {
    // Keep non-JSON server errors generic.
  }

  if (!response.ok) {
    const detail =
      typeof body === "object" && body !== null && "detail" in body
        ? String((body as { detail: unknown }).detail)
        : `Request failed with status ${response.status}.`;
    throw new Error(detail);
  }

  return body as T;
}

export async function getLatestMoneywheel(
  planningUnitId: string,
): Promise<MoneywheelResult | null> {
  return request<MoneywheelResult | null>(
    `/api/moneywheel/latest/${encodeURIComponent(planningUnitId)}`,
  );
}

export async function getMoneywheelHistory(
  planningUnitId: string,
): Promise<MoneywheelResult[]> {
  return request<MoneywheelResult[]>(
    `/api/moneywheel/history/${encodeURIComponent(planningUnitId)}`,
  );
}

export async function calculateMoneywheel(
  planningUnitId: string,
  financialStateSnapshot: Record<string, unknown>,
): Promise<MoneywheelResult> {
  const response = await request<MoneywheelResponse>("/api/moneywheel/calculate", {
    method: "POST",
    body: JSON.stringify({
      planning_unit_id: planningUnitId,
      financial_state_snapshot: financialStateSnapshot,
    }),
  });
  return response.result;
}
