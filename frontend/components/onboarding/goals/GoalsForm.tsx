"use client";

import GoalForm from "./GoalForm";
import GoalSummary from "./GoalSummary";
import { useGoals } from "../../../hooks/onboarding/goals/useGoals";
import OnboardingShell from "../OnboardingShell";

export default function GoalsForm() {
  const goals = useGoals();

  return (
    <OnboardingShell
      currentStep={6}
      title="What are you planning your money for?"
      subtitle="Financial planning connects your balance sheet and cash flow to life milestones, family security, and future aspirations."
      stepContext="Goals & Life Aspirations"
      badge={goals.goals.length > 0 ? `${goals.goals.length} goal${goals.goals.length > 1 ? "s" : ""} added` : undefined}
    >
      <div className="space-y-6">
        {(goals.goals.length > 0 || !goals.isFormOpen) && (
          <GoalSummary
            goals={goals.goals}
            onEdit={goals.startEditing}
            onRemove={goals.removeGoal}
          />
        )}

        {goals.isFormOpen ? (
          <GoalForm
            goal={goals.draft}
            errors={goals.errors}
            isEditing={Boolean(goals.editingGoalId)}
            onChange={goals.updateDraft}
            onSave={goals.saveGoal}
            onCancel={goals.cancelEditing}
          />
        ) : (
          <div className="flex justify-start">
            <button
              type="button"
              onClick={goals.startAdding}
              className="inline-flex items-center justify-center gap-2 rounded-xl border border-teal-600 bg-white px-5 py-3 text-sm font-bold text-teal-700 shadow-sm transition hover:bg-teal-50 focus:outline-none focus:ring-4 focus:ring-teal-100"
            >
              <span aria-hidden="true" className="text-base font-extrabold">+</span>
              Add Goal
            </button>
          </div>
        )}

        {/* Consistent Action Bar */}
        <div className="flex flex-col-reverse items-stretch gap-4 pt-4 sm:flex-row sm:items-center sm:justify-between border-t border-slate-200/80">
          <button
            type="button"
            onClick={goals.goPrevious}
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-700 shadow-sm transition hover:bg-slate-50 hover:text-navy-900"
          >
            <span aria-hidden="true">&larr;</span>
            Back to Liabilities
          </button>

          <button
            type="button"
            onClick={goals.handleContinue}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-teal-700 px-7 py-3.5 text-sm font-bold text-white shadow-sm transition hover:bg-teal-800 focus:outline-none focus:ring-4 focus:ring-teal-100 disabled:cursor-not-allowed disabled:opacity-60"
          >
            Complete Onboarding &amp; View Plan
            <span aria-hidden="true">&rarr;</span>
          </button>
        </div>

        {goals.isComplete && (
          <p className="rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700" role="status">
            All onboarding steps complete! Navigating to your financial state...
          </p>
        )}
      </div>
    </OnboardingShell>
  );
}