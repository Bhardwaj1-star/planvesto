"use client";

import { useState } from "react";
import { useOnboardingNavigation, useOnboardingStore } from "../../../components/onboarding/OnboardingProvider";
import { createCommitmentId } from "../../../lib/onboarding/commitments/commitments";
import { emptyCommitment, type Commitment, type CommitmentErrors } from "../../../lib/onboarding/commitments/types";
import { validateCommitment } from "../../../lib/onboarding/commitments/validation";

export function useCommitments() {
  const { commitments, setCommitments, saveCommitments } = useOnboardingStore();
  const { completeStep, goNext, goPrevious } = useOnboardingNavigation(7);
  const [draft, setDraft] = useState<Commitment>({ id: createCommitmentId(), ...emptyCommitment });
  const [editingCommitmentId, setEditingCommitmentId] = useState<string | null>(null);
  const [errors, setErrors] = useState<CommitmentErrors>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  function startAdding() {
    setDraft({ id: createCommitmentId(), ...emptyCommitment });
    setEditingCommitmentId(null);
    setErrors({});
    setIsSubmitted(false);
  }

  function startEditing(commitment: Commitment) {
    setDraft({ ...commitment });
    setEditingCommitmentId(commitment.id);
    setErrors({});
    setIsSubmitted(false);
  }

  function cancelEditing() {
    startAdding();
  }

  function updateDraft(changes: Partial<Commitment>) {
    const nextDraft = { ...draft, ...changes };
    setDraft(nextDraft);
    setIsComplete(false);
    if (isSubmitted) setErrors(validateCommitment(nextDraft));
  }

  async function saveCommitment(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const nextErrors = validateCommitment(draft);
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) {
      document.getElementById(Object.keys(nextErrors)[0])?.focus();
      return false;
    }

    const nextCommitments = editingCommitmentId
      ? commitments.map((item) => (item.id === editingCommitmentId ? draft : item))
      : [...commitments, draft];
    setCommitments(nextCommitments);
    try {
      const data = await saveCommitments(nextCommitments);
      setCommitments(data.commitments);
    } catch {
      return false;
    }
    startAdding();
    return true;
  }

  async function removeCommitment(id: string) {
    const nextCommitments = commitments.filter((item) => item.id !== id);
    setCommitments(nextCommitments);
    try {
      const data = await saveCommitments(nextCommitments);
      setCommitments(data.commitments);
    } catch {
      return;
    }
    if (editingCommitmentId === id) startAdding();
    setIsComplete(false);
  }

  async function handleContinue(event: React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const itemErrors = commitments.map((item) => validateCommitment(item));
    const invalidIndex = itemErrors.findIndex((errs) => Object.keys(errs).length > 0);
    if (invalidIndex >= 0) {
      setEditingCommitmentId(commitments[invalidIndex].id);
      setDraft(commitments[invalidIndex]);
      setErrors(itemErrors[invalidIndex]);
      return;
    }
    try {
      const data = await saveCommitments(commitments);
      setCommitments(data.commitments);
    } catch {
      return;
    }
    setIsComplete(true);
    completeStep(7);
    goNext();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return {
    commitments,
    draft,
    editingCommitmentId,
    errors,
    isComplete,
    startEditing,
    updateDraft,
    saveCommitment,
    removeCommitment,
    cancelEditing,
    handleContinue,
    goPrevious,
  };
}
