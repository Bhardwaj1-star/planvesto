import type { Expense } from "./types";
import { formatINR } from "@/lib/format";

export function createExpenseId() { return `expense-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`; }
export function annualizeExpense(expense: Expense) { const amount = Number(expense.amount); return expense.frequency === "Monthly" ? amount * 12 : amount; }
export function getAnnualExpenses(expenses: Expense[]) { return expenses.reduce((total, expense) => total + annualizeExpense(expense), 0); }
export function formatCurrency(amount: number) { return formatINR(amount); }
