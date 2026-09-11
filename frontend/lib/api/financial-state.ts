import { supabase } from "../supabase";

export type Metric = {
  value: number | null;
  available: boolean;
  reason: string | null;
};

export type BreakdownItem = {
  type: string;
  monthly: number;
  annual: number;
};

export type AssetBreakdownItem = {
  asset_id: string;
  name: string;
  current_value: number;
  ownership_applied: number;
  liquidity: string | null;
};

export type LiabilityBreakdownItem = {
  liability_id: string;
  name: string;
  outstanding_amount: number;
  responsibility_applied: number;
  classification: string | null;
};

export type FinancialState = {
  scope: "family" | "individual" | string;
  planning_unit_id: string;
  investor_id: string | null;
  income_monthly: Metric;
  income_annual: Metric;
  income_breakdown: BreakdownItem[];
  expenses_monthly: Metric;
  expenses_annual: Metric;
  expense_breakdown: BreakdownItem[];
  investable_surplus_monthly: Metric;
  investable_surplus_annual: Metric;
  cash_flow_ratio: Metric;
  savings_investment_rate: Metric;
  total_assets: Metric;
  asset_breakdown: AssetBreakdownItem[];
  asset_allocation?: Record<string, unknown> | null;
  liquidity_breakdown?: Record<string, unknown> | null;
  total_liabilities: Metric;
  liability_breakdown: LiabilityBreakdownItem[];
  liability_allocation?: Record<string, unknown> | null;
  emi_burden_monthly: Metric;
  net_worth: Metric;
  safety_reserve_months: Metric;
  safety_reserve_required_amount: Metric;
  snapshot_id?: string;
  created_at?: string;
};

export type FinancialStateHistory = FinancialState[];

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  if (!backendUrl) {
    throw new Error("Backend URL is not configured.");
  }

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

export function getPlanningUnitId(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("planvesto-planning-unit-id");
}

export async function buildFinancialState(
  planningUnitId: string,
  scope: "family" | "individual" = "family",
  investorId?: string | null,
): Promise<FinancialState> {
  return request<FinancialState>("/api/financial-state/build", {
    method: "POST",
    body: JSON.stringify({
      planning_unit_id: planningUnitId,
      scope,
      investor_id: investorId ?? null,
    }),
  });
}

export async function getLatestFinancialState(
  planningUnitId: string,
): Promise<FinancialState> {
  return request<FinancialState>(
    `/api/financial-state/latest/${encodeURIComponent(planningUnitId)}`,
  );
}

export async function getFinancialStateHistory(
  planningUnitId: string,
): Promise<FinancialStateHistory> {
  return request<FinancialStateHistory>(
    `/api/financial-state/history/${encodeURIComponent(planningUnitId)}`,
  );
}
