"use client";

import IncomeSourceForm from "./IncomeSourceForm";
import IncomeSummary from "./IncomeSummary";
import { useIncome } from "../../../hooks/onboarding/income/useIncome";
import OnboardingShell from "../OnboardingShell";

export default function IncomeForm() {
  const income = useIncome();

  return (
    <OnboardingShell
      currentStep={2}
      title="How does money come into your life?"
      subtitle="Understanding your income sources helps us determine your earnings power and savings capacity."
      stepContext="Income & Earning Stability"
      badge={income.sources.length > 0 ? `${income.sources.length} source${income.sources.length > 1 ? "s" : ""}` : undefined}
    >
      <div className="space-y-6">
        <IncomeSummary
          sources={income.sources}
          onEdit={income.startEditing}
          onRemove={income.removeSource}
        />

        <IncomeSourceForm
          source={income.draft}
          errors={income.errors}
          isEditing={Boolean(income.editingSourceId)}
          onChange={income.updateDraft}
          onSave={income.saveSource}
          onCancel={income.cancelEditing}
        />

        {/* Consistent Action Bar */}
        <div className="flex flex-col-reverse items-stretch gap-4 pt-4 sm:flex-row sm:items-center sm:justify-between border-t border-slate-200/80">
          <button
            type="button"
            onClick={income.goPrevious}
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-700 shadow-sm transition hover:bg-slate-50 hover:text-navy-900"
          >
            <span aria-hidden="true">&larr;</span>
            Back to Personal Information
          </button>

          <button
            type="button"
            onClick={income.handleContinue}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-7 py-3.5 text-sm font-bold text-white shadow-sm transition hover:bg-navy-800 focus:outline-none focus:ring-4 focus:ring-teal-100 disabled:cursor-not-allowed disabled:opacity-60"
          >
            Continue to Expenses
            <span aria-hidden="true">&rarr;</span>
          </button>
        </div>

        {income.isComplete && (
          <p className="rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700" role="status">
            Income information is complete for this session.
          </p>
        )}
      </div>
    </OnboardingShell>
  );
}