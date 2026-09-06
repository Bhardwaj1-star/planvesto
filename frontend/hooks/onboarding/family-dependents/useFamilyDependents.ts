"use client";

import { useState } from "react";
import { useOnboardingNavigation, useOnboardingStore } from "../../../components/onboarding/OnboardingProvider";
import { createFamilyMemberId } from "../../../lib/onboarding/family-dependents/familyDependents";
import { emptyFamilyMember, type FamilyMember, type FamilyMemberErrors } from "../../../lib/onboarding/family-dependents/types";
import { validateFamilyMember } from "../../../lib/onboarding/family-dependents/validation";

export function useFamilyDependents() {
  const { familyMembers: members, setFamilyMembers: setMembers, saveFamilyMembers } = useOnboardingStore();
  const { completeStep, goNext, goPrevious } = useOnboardingNavigation(2);
  const [draft, setDraft] = useState<FamilyMember>({ id: createFamilyMemberId(), ...emptyFamilyMember });
  const [editingMemberId, setEditingMemberId] = useState<string | null>(null);
  const [errors, setErrors] = useState<FamilyMemberErrors>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  function startAdding() {
    setDraft({ id: createFamilyMemberId(), ...emptyFamilyMember });
    setEditingMemberId(null);
    setErrors({});
    setIsSubmitted(false);
  }

  function startEditing(member: FamilyMember) {
    setDraft({ ...member });
    setEditingMemberId(member.id);
    setErrors({});
    setIsSubmitted(false);
  }

  function cancelEditing() {
    startAdding();
  }

  function updateDraft(changes: Partial<FamilyMember>) {
    const nextDraft = { ...draft, ...changes };
    setDraft(nextDraft);
    setIsComplete(false);
    if (isSubmitted) setErrors(validateFamilyMember(nextDraft));
  }

  async function saveMember(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const nextErrors = validateFamilyMember(draft);
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) {
      const firstInvalidField = Object.keys(nextErrors)[0];
      document.getElementById(firstInvalidField)?.focus();
      return false;
    }

    const nextMembers = editingMemberId
      ? members.map((member) => member.id === editingMemberId ? draft : member)
      : [...members, draft];
    setMembers(nextMembers);
    try {
      const data = await saveFamilyMembers(nextMembers);
      setMembers(data.familyMembers);
    } catch {
      return false;
    }
    startAdding();
    return true;
  }

  async function removeMember(id: string) {
    const nextMembers = members.filter((member) => member.id !== id);
    setMembers(nextMembers);
    try {
      const data = await saveFamilyMembers(nextMembers);
      setMembers(data.familyMembers);
    } catch {
      return;
    }
    if (editingMemberId === id) startAdding();
    setIsComplete(false);
  }

  async function handleContinue(event: React.FormEvent | React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const memberErrors = members.map((member) => validateFamilyMember(member));
    const invalidIndex = memberErrors.findIndex((memberErrorsForMember) => Object.keys(memberErrorsForMember).length > 0);
    if (invalidIndex >= 0) {
      setEditingMemberId(members[invalidIndex].id);
      setDraft(members[invalidIndex]);
      setErrors(memberErrors[invalidIndex]);
      return;
    }
    try {
      const data = await saveFamilyMembers(members);
      setMembers(data.familyMembers);
    } catch {
      return;
    }
    setIsComplete(true);
    completeStep(2);
    goNext();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return {
    members,
    draft,
    editingMemberId,
    errors,
    isComplete,
    startAdding,
    startEditing,
    cancelEditing,
    updateDraft,
    saveMember,
    removeMember,
    handleContinue,
    goPrevious,
  };
}