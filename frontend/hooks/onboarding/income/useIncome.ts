"use client";

import { useState } from "react";
import { useOnboardingNavigation, useOnboardingStore } from "../../../components/onboarding/OnboardingProvider";
import { createIncomeSourceId } from "../../../lib/onboarding/income/income";
import { emptyIncomeSource, type IncomeSource, type IncomeSourceErrors } from "../../../lib/onboarding/income/types";
import { validateIncomeSource } from "../../../lib/onboarding/income/validation";

export function useIncome() {
  const { incomeSources: sources, setIncomeSources: setSources, saveIncomeSources } = useOnboardingStore();
  const { completeStep, goNext, goPrevious } = useOnboardingNavigation(3);
  const [draft, setDraft] = useState<IncomeSource>({ id: createIncomeSourceId(), ...emptyIncomeSource });
  const [editingSourceId, setEditingSourceId] = useState<string | null>(null);
  const [errors, setErrors] = useState<IncomeSourceErrors>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  function startAdding() {
    setDraft({ id: createIncomeSourceId(), ...emptyIncomeSource });
    setEditingSourceId(null);
    setErrors({});
    setIsSubmitted(false);
  }

  function startEditing(source: IncomeSource) {
    setDraft({ ...source });
    setEditingSourceId(source.id);
    setErrors({});
    setIsSubmitted(false);
  }

  function cancelEditing() {
    startAdding();
  }

  function updateDraft(changes: Partial<IncomeSource>) {
    const nextDraft = { ...draft, ...changes };
    setDraft(nextDraft);
    setIsComplete(false);
    if (isSubmitted) setErrors(validateIncomeSource(nextDraft));
  }

  async function saveSource(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const nextErrors = validateIncomeSource(draft);
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) {
      const firstInvalidField = Object.keys(nextErrors)[0];
      document.getElementById(firstInvalidField)?.focus();
      return false;
    }

    const nextSources = editingSourceId
      ? sources.map((source) => source.id === editingSourceId ? draft : source)
      : [...sources, draft];
    setSources(nextSources);
    try {
      const data = await saveIncomeSources(nextSources);
      setSources(data.incomeSources);
    } catch {
      return false;
    }
    startAdding();
    return true;
  }

  async function removeSource(id: string) {
    const nextSources = sources.filter((source) => source.id !== id);
    setSources(nextSources);
    try {
      const data = await saveIncomeSources(nextSources);
      setSources(data.incomeSources);
    } catch {
      return;
    }
    if (editingSourceId === id) startAdding();
    setIsComplete(false);
  }

  async function handleContinue(event: React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const sourceErrors = sources.map((source) => validateIncomeSource(source));
    const invalidIndex = sourceErrors.findIndex((sourceErrorsForSource) => Object.keys(sourceErrorsForSource).length > 0);
    if (invalidIndex >= 0) {
      setEditingSourceId(sources[invalidIndex].id);
      setDraft(sources[invalidIndex]);
      setErrors(sourceErrors[invalidIndex]);
      return;
    }
    try {
      const data = await saveIncomeSources(sources);
      setSources(data.incomeSources);
    } catch {
      return;
    }
    setIsComplete(true);
    completeStep(3);
    goNext();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return {
    sources,
    draft,
    editingSourceId,
    errors,
    isComplete,
    startEditing,
    updateDraft,
    saveSource,
    removeSource,
    cancelEditing,
    handleContinue,
    goPrevious,
  };
}