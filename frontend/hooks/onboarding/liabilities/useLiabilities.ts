"use client";

import { useState } from "react";
import { useOnboardingNavigation, useOnboardingStore } from "../../../components/onboarding/OnboardingProvider";
import { createLiabilityId } from "../../../lib/onboarding/liabilities/liabilities";
import { emptyLiability, type Liability, type LiabilityErrors } from "../../../lib/onboarding/liabilities/types";
import { validateLiability } from "../../../lib/onboarding/liabilities/validation";

export function useLiabilities() {
  const { liabilities, setLiabilities, saveLiabilities } = useOnboardingStore();
  const { completeStep, goNext, goPrevious } = useOnboardingNavigation(6);
  const [draft, setDraft] = useState<Liability>({ id: createLiabilityId(), ...emptyLiability });
  const [editingLiabilityId, setEditingLiabilityId] = useState<string | null>(null);
  const [errors, setErrors] = useState<LiabilityErrors>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  function startAdding() {
    setDraft({ id: createLiabilityId(), ...emptyLiability });
    setEditingLiabilityId(null);
    setErrors({});
    setIsSubmitted(false);
  }

  function startEditing(liability: Liability) {
    setDraft({ ...liability });
    setEditingLiabilityId(liability.id);
    setErrors({});
    setIsSubmitted(false);
  }

  function cancelEditing() {
    startAdding();
  }

  function updateDraft(changes: Partial<Liability>) {
    const nextDraft = { ...draft, ...changes };
    setDraft(nextDraft);
    setIsComplete(false);
    if (isSubmitted) setErrors(validateLiability(nextDraft));
  }

  async function saveLiability(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const nextErrors = validateLiability(draft);
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) {
      document.getElementById(Object.keys(nextErrors)[0])?.focus();
      return false;
    }

    const nextLiabilities = editingLiabilityId
      ? liabilities.map((liability) => liability.id === editingLiabilityId ? draft : liability)
      : [...liabilities, draft];
    setLiabilities(nextLiabilities);
    try {
      const data = await saveLiabilities(nextLiabilities);
      setLiabilities(data.liabilities);
    } catch {
      return false;
    }
    startAdding();
    return true;
  }

  async function removeLiability(id: string) {
    const nextLiabilities = liabilities.filter((liability) => liability.id !== id);
    setLiabilities(nextLiabilities);
    try {
      const data = await saveLiabilities(nextLiabilities);
      setLiabilities(data.liabilities);
    } catch {
      return;
    }
    if (editingLiabilityId === id) startAdding();
    setIsComplete(false);
  }

  async function handleContinue(event: React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const liabilityErrors = liabilities.map((liability) => validateLiability(liability));
    const invalidIndex = liabilityErrors.findIndex((liabilityErrorsForItem) => Object.keys(liabilityErrorsForItem).length > 0);
    if (invalidIndex >= 0) {
      setEditingLiabilityId(liabilities[invalidIndex].id);
      setDraft(liabilities[invalidIndex]);
      setErrors(liabilityErrors[invalidIndex]);
      return;
    }
    try {
      const data = await saveLiabilities(liabilities);
      setLiabilities(data.liabilities);
    } catch {
      return;
    }
    setIsComplete(true);
    completeStep(6);
    goNext();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return {
    liabilities,
    draft,
    editingLiabilityId,
    errors,
    isComplete,
    startEditing,
    updateDraft,
    saveLiability,
    removeLiability,
    cancelEditing,
    handleContinue,
    goPrevious,
  };
}