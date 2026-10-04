"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import InsuranceSection from "./InsuranceSection";
import OnboardingShell from "../OnboardingShell";
import { useOnboardingNavigation } from "../OnboardingProvider";

export default function InsuranceForm() {
  const router = useRouter();
  const { completeStep, goPrevious } = useOnboardingNavigation(7);
  const [isComplete, setIsComplete] = useState(false);

  function handleContinue() {
    completeStep(7);
    setIsComplete(true);
    router.push("/investor/onboarding/goals");
  }

  return (
    <OnboardingShell
      currentStep={7}
      title="How are you protected?"
      subtitle="Add your existing insurance policies so your financial picture includes protection, premiums, and policy-linked value."
      stepContext="Insurance & Protection"
    >
      <div className="space-y-6">
        <InsuranceSection />

        <div className="flex flex-col-reverse items-stretch gap-4 border-t border-slate-200/80 pt-4 sm:flex-row sm:items-center sm:justify-between">
          <button
            type="button"
            onClick={goPrevious}
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-700 shadow-sm transition hover:bg-slate-50"
          >
            <span aria-hidden="true">&larr;</span>
            Back to Liabilities
          </button>

          <button
            type="button"
            onClick={handleContinue}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-7 py-3.5 text-sm font-bold text-white shadow-sm transition hover:bg-navy-800"
          >
            Continue to Goals
            <span aria-hidden="true">&rarr;</span>
          </button>
        </div>

        {isComplete && (
          <p className="rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700" role="status">
            Insurance information is complete for this session.
          </p>
        )}
      </div>
    </OnboardingShell>
  );
}