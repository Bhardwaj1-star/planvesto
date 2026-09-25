import type { IncomeSource } from "./types";
import { formatINR } from "@/lib/format";

export function createIncomeSourceId() { return `income-source-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`; }
export function annualizeIncome(source: IncomeSource) { const amount = Number(source.amount); return source.frequency === "Monthly" ? amount * 12 : amount; }
export function getAnnualIncome(sources: IncomeSource[]) { return sources.reduce((total, source) => total + annualizeIncome(source), 0); }
export function formatCurrency(amount: number) { return formatINR(amount); }
