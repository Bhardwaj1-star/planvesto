import type { IncomeSource, IncomeSourceErrors } from "./types";

export function validateIncomeSource(source: IncomeSource): IncomeSourceErrors {
  const errors: IncomeSourceErrors = {};
  const amount = Number(source.amount);
  const growth = Number(source.expectedAnnualGrowth);

  if (!source.incomeType) errors.incomeType = "Select an income type.";
  if (!source.amount) {
    errors.amount = "Enter an income amount.";
  } else if (!Number.isFinite(amount) || amount <= 0) {
    errors.amount = "Enter an amount greater than zero.";
  }
  if (!source.frequency) errors.frequency = "Select how often this income arrives.";
  if (source.expectedAnnualGrowth.trim()) {
    if (!Number.isFinite(growth) || growth < -100 || growth > 100) {
      errors.expectedAnnualGrowth = "Enter a percentage between -100 and 100.";
    }
  }

  return errors;
}