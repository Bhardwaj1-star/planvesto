"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useOnboardingNavigation, useOnboardingStore } from "../../../components/onboarding/OnboardingProvider";
import { createGoalId } from "../../../lib/onboarding/goals/goals";
import { emptyGoal, type Goal, type GoalErrors } from "../../../lib/onboarding/goals/types";
import { validateGoal } from "../../../lib/onboarding/goals/validation";

export function useGoals() {
  const { goals, setGoals, saveGoals } = useOnboardingStore();
  const { completeStep, goPrevious } = useOnboardingNavigation(7);
  const router = useRouter();
  const [draft, setDraft] = useState<Goal>({ id: createGoalId(), ...emptyGoal });
  const [isAdding, setIsAdding] = useState(goals.length === 0);
  const [editingGoalId, setEditingGoalId] = useState<string | null>(null);
  const [errors, setErrors] = useState<GoalErrors>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  function startAdding() { setDraft({ id: createGoalId(), ...emptyGoal }); setEditingGoalId(null); setIsAdding(true); setErrors({}); setIsSubmitted(false); }
  function startEditing(goal: Goal) { setDraft({ ...goal }); setEditingGoalId(goal.id); setIsAdding(true); setErrors({}); setIsSubmitted(false); }
  function cancelEditing() { setDraft({ id: createGoalId(), ...emptyGoal }); setEditingGoalId(null); setIsAdding(false); setErrors({}); setIsSubmitted(false); }
  function updateDraft(changes: Partial<Goal>) { const nextDraft = { ...draft, ...changes }; setDraft(nextDraft); setIsComplete(false); if (isSubmitted) setErrors(validateGoal(nextDraft)); }

  async function saveGoal(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); setIsSubmitted(true); const nextErrors = validateGoal(draft); setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) { document.getElementById(Object.keys(nextErrors)[0])?.focus(); return false; }
    const nextGoals = editingGoalId ? goals.map((goal) => goal.id === editingGoalId ? draft : goal) : [...goals, draft];
    try { await saveGoals(nextGoals); setGoals(nextGoals); } catch { return false; }
    setDraft({ id: createGoalId(), ...emptyGoal }); setEditingGoalId(null); setIsAdding(false); setErrors({}); setIsSubmitted(false); return true;
  }

  async function removeGoal(id: string) {
    const nextGoals = goals.filter((goal) => goal.id !== id); setGoals(nextGoals);
    try { await saveGoals(nextGoals); } catch { return; }
    if (editingGoalId === id) cancelEditing(); setIsComplete(false);
  }

  async function handleContinue(event: React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault(); setIsSubmitted(true);
    const hasEnteredDraft = Boolean(draft.name.trim() || draft.dynamicDetails.otherGoalName.trim() || draft.targetAmount || draft.goalType || draft.targetDate || draft.targetAge || editingGoalId || goals.length === 0);
    let goalsToSave = goals;
    if (hasEnteredDraft) {
      const nextErrors = validateGoal(draft); setErrors(nextErrors);
      if (Object.keys(nextErrors).length > 0) { document.getElementById(Object.keys(nextErrors)[0])?.focus(); return; }
      goalsToSave = editingGoalId ? goals.map((goal) => (goal.id === editingGoalId ? draft : goal)) : [...goals, draft];
    }
    try { await saveGoals(goalsToSave); setGoals(goalsToSave); } catch { return; }
    setDraft({ id: createGoalId(), ...emptyGoal }); setEditingGoalId(null); setIsAdding(false); setErrors({}); setIsSubmitted(false); setIsComplete(true); completeStep(7); router.push("/investor/financial-state");
  }

  return { goals, draft, editingGoalId, isAdding, isFormOpen: isAdding || Boolean(editingGoalId), errors, isComplete, startAdding, startEditing, updateDraft, saveGoal, removeGoal, cancelEditing, handleContinue, goPrevious };
}
