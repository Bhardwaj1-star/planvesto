import type { Goal } from "./types";

export function createGoalId() {
  return `goal-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
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
  return goal.targetDate || "Target not set";
}