import type { Expense, ExpenseErrors } from "./types";

export function validateExpense(expense: Expense): ExpenseErrors {
  const errors: ExpenseErrors = {};
  const amount = Number(expense.amount);

  if (!expense.category) errors.category = "Select an expense category.";
  if (!expense.amount) {
    errors.amount = "Enter an expense amount.";
  } else if (!Number.isFinite(amount) || amount <= 0) {
    errors.amount = "Enter an amount greater than zero.";
  }
  if (!expense.frequency) errors.frequency = "Select how often this expense occurs.";

  return errors;
}