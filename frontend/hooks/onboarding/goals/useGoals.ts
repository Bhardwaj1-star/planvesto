"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useOnboardingNavigation, useOnboardingStore } from "../../../components/onboarding/OnboardingProvider";
import { createGoalId } from "../../../lib/onboarding/goals/goals";
import { emptyGoal, type Goal, type GoalErrors } from "../../../lib/onboarding/goals/types";
import { validateGoal } from "../../../lib/onboarding/goals/validation";

export function useGoals() {
  const { goals, setGoals, saveGoals } = useOnboardingStore();
  const { completeStep, goPrevious } = useOnboardingNavigation(8);
  const router = useRouter();
  const [draft, setDraft] = useState<Goal>({ id: createGoalId(), ...emptyGoal });
  const [editingGoalId, setEditingGoalId] = useState<string | null>(null);
  const [errors, setErrors] = useState<GoalErrors>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  function startAdding() {
    setDraft({ id: createGoalId(), ...emptyGoal });
    setEditingGoalId(null);
    setErrors({});
    setIsSubmitted(false);
  }

  function startEditing(goal: Goal) {
    setDraft({ ...goal });
    setEditingGoalId(goal.id);
    setErrors({});
    setIsSubmitted(false);
  }

  function cancelEditing() {
    startAdding();
  }

  function updateDraft(changes: Partial<Goal>) {
    const nextDraft = { ...draft, ...changes };
    setDraft(nextDraft);
    setIsComplete(false);
    if (isSubmitted) setErrors(validateGoal(nextDraft));
  }

  async function saveGoal(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const nextErrors = validateGoal(draft);
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) {
      document.getElementById(Object.keys(nextErrors)[0])?.focus();
      return false;
    }

    const nextGoals = editingGoalId
      ? goals.map((goal) => goal.id === editingGoalId ? draft : goal)
      : [...goals, draft];
    setGoals(nextGoals);
    try {
      const data = await saveGoals(nextGoals);
      setGoals(data.goals);
    } catch {
      return false;
    }
    startAdding();
    return true;
  }

  async function removeGoal(id: string) {
    const nextGoals = goals.filter((goal) => goal.id !== id);
    setGoals(nextGoals);
    try {
      const data = await saveGoals(nextGoals);
      setGoals(data.goals);
    } catch {
      return;
    }
    if (editingGoalId === id) startAdding();
    setIsComplete(false);
  }

  async function handleContinue(event: React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const goalErrors = goals.map((goal) => validateGoal(goal));
    const invalidIndex = goalErrors.findIndex((goalErrorsForItem) => Object.keys(goalErrorsForItem).length > 0);
    if (invalidIndex >= 0) {
      setEditingGoalId(goals[invalidIndex].id);
      setDraft(goals[invalidIndex]);
      setErrors(goalErrors[invalidIndex]);
      return;
    }
    try {
      const data = await saveGoals(goals);
      setGoals(data.goals);
    } catch {
      return;
    }
    setIsComplete(true);
    completeStep(8);
    router.push("/investor/financial-state");
  }

  return {
    goals,
    draft,
    editingGoalId,
    errors,
    isComplete,
    startEditing,
    updateDraft,
    saveGoal,
    removeGoal,
    cancelEditing,
    handleContinue,
    goPrevious,
  };
}