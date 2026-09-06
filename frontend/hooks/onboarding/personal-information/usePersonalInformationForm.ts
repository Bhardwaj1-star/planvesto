"use client";

import { useState } from "react";
import {
  initialPersonalInformation,
  type PersonalInformation,
  type PersonalInformationErrors,
  type PersonalInformationField,
  } from "../../../lib/onboarding/personal-information/model";
import { validatePersonalInformation } from "../../../lib/onboarding/personal-information/validation";
import { useOnboardingNavigation, useOnboardingStore } from "../../../components/onboarding/OnboardingProvider";

type FieldChange = {
  name: PersonalInformationField;
  value: string;
};

export function usePersonalInformationForm() {
  const { personalInformation: values, setPersonalInformation, savePersonalInformation } = useOnboardingStore();
  const { completeStep, goNext } = useOnboardingNavigation(1);
  const [errors, setErrors] = useState<PersonalInformationErrors>({});
  const [touched, setTouched] = useState<Partial<Record<PersonalInformationField, boolean>>>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  function handleChange({ name, value }: FieldChange) {
    const nextValues = { ...values, [name]: value };
    setPersonalInformation(nextValues);
    setIsComplete(false);

    if (touched[name] || isSubmitted) {
      setErrors(validatePersonalInformation(nextValues));
    }
  }

  function handleBlur(name: PersonalInformationField) {
    const nextTouched = { ...touched, [name]: true };
    setTouched(nextTouched);
    setErrors(validatePersonalInformation(values));
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    setTouched({
      fullName: true,
      dateOfBirth: true,
      gender: true,
      maritalStatus: true,
      mobileNumber: true,
      address: true,
      city: true,
      state: true,
      country: true,
      occupation: true,
    });

    const nextErrors = validatePersonalInformation(values);
    setErrors(nextErrors);

    if (Object.keys(nextErrors).length > 0) {
      const firstInvalidField = Object.keys(nextErrors)[0] as PersonalInformationField;
      document.getElementById(firstInvalidField)?.focus();
      return;
    }

    const data = await savePersonalInformation(values);
    setPersonalInformation(data.personalInformation);
    setIsComplete(true);
    completeStep(1);
    goNext();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return {
    values,
    errors,
    touched,
    handleChange,
    handleBlur,
    handleSubmit,
    isComplete,
  };
}
