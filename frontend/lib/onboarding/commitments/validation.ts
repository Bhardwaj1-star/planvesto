import type { Commitment, CommitmentErrors } from "./types";

export function validateCommitment(commitment: Commitment): CommitmentErrors {
  const errors: CommitmentErrors = {};
  const amount = Number(commitment.amount);

  if (!commitment.name.trim()) {
    errors.name = "Enter a commitment name or description.";
  }
  if (!commitment.amount) {
    errors.amount = "Enter the commitment amount.";
  } else if (!Number.isFinite(amount) || amount <= 0) {
    errors.amount = "Enter an amount greater than zero.";
  }

  return errors;
}
