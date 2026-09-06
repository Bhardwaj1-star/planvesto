import type { Commitment } from "./types";

export function createCommitmentId() {
  return `commitment-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

export function getTotalCommitments(commitments: Commitment[]) {
  return commitments.reduce((total, commitment) => total + Number(commitment.amount), 0);
}

export function formatCurrency(amount: number) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(amount);
}
