import type { Goal, GoalErrors } from "./types";

function isValidDate(value: string) {
  const date = new Date(`${value}T00:00:00`);
  return !Number.isNaN(date.getTime()) && date.toISOString().slice(0, 10) === value;
}

function required(errors: GoalErrors, field: string, value: string, message: string) {
  if (!value.trim()) errors[field] = message;
}

export function validateGoal(goal: Goal): GoalErrors {
  const errors: GoalErrors = {};
  const targetAmount = Number(goal.targetAmount);
  const today = new Date().toISOString().slice(0, 10);
  const details = goal.dynamicDetails;

  if (!goal.goalType) errors.goalType = "Select a goal type.";
  if (goal.goalType === "Others") required(errors, "otherGoalName", details.otherGoalName, "Enter a name for this goal.");

  const noTodayCost = goal.goalType === "Retirement / Financial Freedom" || goal.goalType === "Debt Repayment";
  if (!noTodayCost) {
    if (!goal.targetAmount) errors.targetAmount = "Enter today's cost.";
    else if (!Number.isFinite(targetAmount) || targetAmount <= 0) errors.targetAmount = "Enter an amount greater than zero.";
  }

  if (!goal.targetMode) errors.targetMode = "Choose a target date.";
  else if (goal.targetMode === "Date") {
    if (!goal.targetDate) errors.targetDate = "Enter the target date.";
    else if (!isValidDate(goal.targetDate)) errors.targetDate = "Enter a valid target date.";
    else if (goal.targetDate < today) errors.targetDate = "Target date cannot be in the past.";
  }

  if (!goal.flexibility) errors.flexibility = "Select whether the goal is fixed or flexible.";

  switch (goal.goalType) {
    case "Retirement / Financial Freedom":
      required(errors, "lifeExpectancy", details.lifeExpectancy, "Enter life expectancy.");
      required(errors, "desiredLifestyleMonthlyExpense", details.desiredLifestyleMonthlyExpense, "Enter the desired monthly expense.");
      break;
    case "Passive Income":
      required(errors, "desiredPassiveIncomeAmount", details.desiredPassiveIncomeAmount, "Enter the desired passive income amount.");
      break;
    case "Education":
      required(errors, "educationForWhom", details.educationForWhom, "Select who the education goal is for.");
      break;
    case "Marriage":
      required(errors, "marriageForWhom", details.marriageForWhom, "Select who the marriage goal is for.");
      break;
    case "Dream Home":
      required(errors, "preferredLocation", details.preferredLocation, "Enter a preferred location.");
      break;
    case "Vehicle":
      required(errors, "vehicleType", details.vehicleType, "Enter the vehicle type.");
      required(errors, "vehicleCondition", details.vehicleCondition, "Select new or used.");
      break;
    case "Vacation":
      required(errors, "vacationFrequency", details.vacationFrequency, "Enter the vacation frequency.");
      required(errors, "vacationType", details.vacationType, "Select domestic or international.");
      break;
    case "Wealth Creation":
      required(errors, "targetWealthCorpus", details.targetWealthCorpus, "Enter the target wealth/corpus.");
      break;
    case "Debt Repayment":
      required(errors, "selectedLiabilityId", details.selectedLiabilityId, "Select a liability to repay.");
      break;
    case "Philanthropy":
      required(errors, "philanthropyContributionAmount", details.philanthropyContributionAmount, "Enter the contribution amount.");
      break;
  }

  return errors;
}
