import type { Liability, LiabilityErrors } from "./types";

export function validateLiability(liability: Liability): LiabilityErrors {
  const errors: LiabilityErrors = {};
  const outstandingAmount = Number(liability.outstandingAmount);
  const interestRate = Number(liability.interestRate);
  const regularPayment = Number(liability.regularPayment);

  if (!liability.liabilityType) errors.liabilityType = "Select a liability type.";
  if (!liability.description.trim()) errors.description = "Enter a lender or description.";
  if (!liability.outstandingAmount) {
    errors.outstandingAmount = "Enter the current outstanding amount.";
  } else if (!Number.isFinite(outstandingAmount) || outstandingAmount <= 0) {
    errors.outstandingAmount = "Enter an amount greater than zero.";
  }
  if (liability.interestRate && (!Number.isFinite(interestRate) || interestRate < 0 || interestRate > 100)) {
    errors.interestRate = "Enter a percentage between 0 and 100.";
  }
  if (liability.regularPayment && (!Number.isFinite(regularPayment) || regularPayment <= 0)) {
    errors.regularPayment = "Enter a payment greater than zero.";
  }

  return errors;
}