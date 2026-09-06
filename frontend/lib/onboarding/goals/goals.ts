import type { Goal } from "./types";

export function createGoalId() {
  return `goal-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

export function getTotalCurrentGoalFunding(goals: Goal[]) {
  return goals.reduce((total, goal) => total + Number(goal.currentSavedAmount || 0), 0);
}

export function getTotalMonthlyGoalContributions(goals: Goal[]) {
  return goals.reduce((total, goal) => total + Number(goal.monthlyContribution || 0), 0);
}

export function getCriticalGoalCount(goals: Goal[]) {
  return goals.filter((goal) => goal.priority === "Critical").length;
}

export function formatCurrency(amount: number) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(amount);
}

export function getGoalTarget(goal: Goal) {
  return goal.targetMode === "Age" ? `By age ${goal.targetAge}` : goal.targetDate || "Target not set";
}