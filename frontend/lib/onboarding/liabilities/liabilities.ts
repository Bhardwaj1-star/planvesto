import type { Liability, LiabilityType } from "./types";
import { formatINR } from "@/lib/format";

export function createLiabilityId() { return `liability-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`; }
export function getTotalOutstandingDebt(liabilities: Liability[]) { return liabilities.reduce((total, liability) => total + Number(liability.outstandingAmount), 0); }
export function getTotalMonthlyDebtPayments(liabilities: Liability[]) { return liabilities.reduce((total, liability) => total + Number(liability.regularPayment), 0); }
export function getDebtBreakdown(liabilities: Liability[]) { return liabilities.reduce<Partial<Record<LiabilityType, number>>>((breakdown, liability) => { if (liability.liabilityType) breakdown[liability.liabilityType] = (breakdown[liability.liabilityType] ?? 0) + Number(liability.outstandingAmount); return breakdown; }, {}); }
export function formatCurrency(amount: number) { return formatINR(amount); }
