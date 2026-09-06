"use client";

import { useEffect } from "react";
import { useOnboardingNavigation } from "../../../components/onboarding/OnboardingProvider";

export default function OnboardingEntryPage() {
  const { resumeStep, goToStep } = useOnboardingNavigation(1);

  useEffect(() => {
    goToStep(resumeStep);
  }, [goToStep, resumeStep]);

  return null;
}
