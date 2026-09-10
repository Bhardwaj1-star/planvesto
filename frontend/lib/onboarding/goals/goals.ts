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

export function formatINR(amount: number) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatCurrency(amount: number) {
  return formatINR(amount);
}

const MONTH_NAMES = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

export function formatTargetMonthYear(month: number, year: number) {
  const monthName = MONTH_NAMES[month - 1] || `Month ${month}`;
  return `${monthName} ${year}`;
}

export function getGoalTarget(goal: Goal) {
  return goal.targetMode === "Age" ? `By age ${goal.targetAge}` : goal.targetDate || "Target not set";
}