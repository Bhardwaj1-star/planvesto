import { apiRequest } from "./client";

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

export async function getLatestMoneywheel(
  planningUnitId: string,
): Promise<MoneywheelResult | null> {
  return apiRequest<MoneywheelResult | null>(
    `/api/moneywheel/latest/${encodeURIComponent(planningUnitId)}`,
  );
}

export async function getMoneywheelHistory(
  planningUnitId: string,
): Promise<MoneywheelResult[]> {
  return apiRequest<MoneywheelResult[]>(
    `/api/moneywheel/history/${encodeURIComponent(planningUnitId)}`,
  );
}

export async function calculateMoneywheel(
  planningUnitId: string,
  financialStateSnapshot: Record<string, unknown>,
): Promise<MoneywheelResult> {
  const response = await apiRequest<MoneywheelResponse>("/api/moneywheel/calculate", {
    method: "POST",
    body: JSON.stringify({
      planning_unit_id: planningUnitId,
      financial_state_snapshot: financialStateSnapshot,
    }),
  });
  return response.result;
}
