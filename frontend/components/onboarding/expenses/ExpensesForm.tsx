"use client";

import ExpenseCategoryForm from "./ExpenseCategoryForm";
import ExpenseSummary from "./ExpenseSummary";
import { useExpenses } from "../../../hooks/onboarding/expenses/useExpenses";
import OnboardingShell from "../OnboardingShell";

export default function ExpensesForm() {
  const expenses = useExpenses();

  return (
    <OnboardingShell
      currentStep={3}
      title="Where does your money go?"
      subtitle="Understanding your living costs and discretionary spending establishes your true investable surplus."
      stepContext="Expenses & Lifestyle Costs"
      badge={expenses.expenses.length > 0 ? `${expenses.expenses.length} categor${expenses.expenses.length > 1 ? "ies" : "y"} added` : undefined}
    >
      <div className="space-y-6">
        <ExpenseSummary
          expenses={expenses.expenses}
          onEdit={expenses.startEditing}
          onRemove={expenses.removeExpense}
        />

        <ExpenseCategoryForm
          expense={expenses.draft}
          errors={expenses.errors}
          isEditing={Boolean(expenses.editingExpenseId)}
          onChange={expenses.updateDraft}
          onSave={expenses.saveExpense}
          onCancel={expenses.cancelEditing}
        />

        {/* Consistent Action Bar */}
        <div className="flex flex-col-reverse items-stretch gap-4 pt-4 sm:flex-row sm:items-center sm:justify-between border-t border-slate-200/80">
          <button
            type="button"
            onClick={expenses.goPrevious}
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-700 shadow-sm transition hover:bg-slate-50 hover:text-navy-900"
          >
            <span aria-hidden="true">&larr;</span>
            Back to Income
          </button>

          <button
            type="button"
            onClick={expenses.handleContinue}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-7 py-3.5 text-sm font-bold text-white shadow-sm transition hover:bg-navy-800 focus:outline-none focus:ring-4 focus:ring-teal-100 disabled:cursor-not-allowed disabled:opacity-60"
          >
            Continue to Assets
            <span aria-hidden="true">&rarr;</span>
          </button>
        </div>

        {expenses.isComplete && (
          <p className="rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700" role="status">
            Expense information is complete for this session.
          </p>
        )}
      </div>
    </OnboardingShell>
  );
}