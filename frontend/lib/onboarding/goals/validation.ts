import type { Goal, GoalErrors } from "./types";

function isValidDate(value: string) {
  const date = new Date(`${value}T00:00:00`);
  return !Number.isNaN(date.getTime()) && date.toISOString().slice(0, 10) === value;
}

export function validateGoal(goal: Goal): GoalErrors {
  const errors: GoalErrors = {};
  const targetAmount = Number(goal.targetAmount);
  const currentSavedAmount = Number(goal.currentSavedAmount);
  const monthlyContribution = Number(goal.monthlyContribution);
  const targetAge = Number(goal.targetAge);
  const today = new Date().toISOString().slice(0, 10);

  if (!goal.name.trim()) errors.name = "Enter a name for this goal.";
  if (!goal.goalType) errors.goalType = "Select a goal type.";
  if (!goal.targetAmount) {
    errors.targetAmount = "Enter the target amount in today's value.";
  } else if (!Number.isFinite(targetAmount) || targetAmount <= 0) {
    errors.targetAmount = "Enter an amount greater than zero.";
  }
  if (!goal.targetMode) {
    errors.targetMode = "Choose a target date or target age.";
  } else if (goal.targetMode === "Date") {
    if (!goal.targetDate) errors.targetDate = "Enter the target date.";
    else if (!isValidDate(goal.targetDate)) errors.targetDate = "Enter a valid target date.";
    else if (goal.targetDate < today) errors.targetDate = "Target date cannot be in the past.";
  } else if (!goal.targetAge) {
    errors.targetAge = "Enter the target age.";
  } else if (!Number.isInteger(targetAge) || targetAge < 1 || targetAge > 120) {
    errors.targetAge = "Enter a target age between 1 and 120.";
  }
  if (goal.currentSavedAmount && (!Number.isFinite(currentSavedAmount) || currentSavedAmount < 0)) {
    errors.currentSavedAmount = "Enter zero or a positive amount.";
  }
  if (goal.monthlyContribution && (!Number.isFinite(monthlyContribution) || monthlyContribution < 0)) {
    errors.monthlyContribution = "Enter zero or a positive amount.";
  }
  if (!goal.priority) errors.priority = "Select the goal priority.";
  if (!goal.flexibility) errors.flexibility = "Select whether the goal is fixed or flexible.";
  if (!goal.inflationApplicability) errors.inflationApplicability = "Select whether inflation applies.";

  return errors;
}