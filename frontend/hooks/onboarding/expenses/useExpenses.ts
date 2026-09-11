"use client";

import { useState } from "react";
import { useOnboardingNavigation, useOnboardingStore } from "../../../components/onboarding/OnboardingProvider";
import { createExpenseId } from "../../../lib/onboarding/expenses/expenses";
import { emptyExpense, type Expense, type ExpenseErrors } from "../../../lib/onboarding/expenses/types";
import { validateExpense } from "../../../lib/onboarding/expenses/validation";

export function useExpenses() {
  const { expenses, setExpenses, saveExpenses } = useOnboardingStore();
  const { completeStep, goNext, goPrevious } = useOnboardingNavigation(4);
  const [draft, setDraft] = useState<Expense>({ id: createExpenseId(), ...emptyExpense });
  const [editingExpenseId, setEditingExpenseId] = useState<string | null>(null);
  const [errors, setErrors] = useState<ExpenseErrors>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  function startAdding() {
    setDraft({ id: createExpenseId(), ...emptyExpense });
    setEditingExpenseId(null);
    setErrors({});
    setIsSubmitted(false);
  }

  function startEditing(expense: Expense) {
    setDraft({ ...expense });
    setEditingExpenseId(expense.id);
    setErrors({});
    setIsSubmitted(false);
  }

  function cancelEditing() {
    startAdding();
  }

  function updateDraft(changes: Partial<Expense>) {
    const nextDraft = { ...draft, ...changes };
    setDraft(nextDraft);
    setIsComplete(false);
    if (isSubmitted) setErrors(validateExpense(nextDraft));
  }

  async function saveExpense(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const nextErrors = validateExpense(draft);
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) {
      document.getElementById(Object.keys(nextErrors)[0])?.focus();
      return false;
    }

    const nextExpenses = editingExpenseId
      ? expenses.map((expense) => expense.id === editingExpenseId ? draft : expense)
      : [...expenses, draft];
    setExpenses(nextExpenses);
    try {
      const data = await saveExpenses(nextExpenses);
      setExpenses(data.expenses);
    } catch {
      return false;
    }
    startAdding();
    return true;
  }

  async function removeExpense(id: string) {
    const nextExpenses = expenses.filter((expense) => expense.id !== id);
    setExpenses(nextExpenses);
    try {
      const data = await saveExpenses(nextExpenses);
      setExpenses(data.expenses);
    } catch {
      return;
    }
    if (editingExpenseId === id) startAdding();
    setIsComplete(false);
  }

  async function handleContinue(event: React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault();
    setIsSubmitted(true);
    const expenseErrors = expenses.map((expense) => validateExpense(expense));
    const invalidIndex = expenseErrors.findIndex((expenseErrorsForItem) => Object.keys(expenseErrorsForItem).length > 0);
    if (invalidIndex >= 0) {
      setEditingExpenseId(expenses[invalidIndex].id);
      setDraft(expenses[invalidIndex]);
      setErrors(expenseErrors[invalidIndex]);
      return;
    }
    try {
      const data = await saveExpenses(expenses);
      setExpenses(data.expenses);
    } catch {
      return;
    }
    setIsComplete(true);
    completeStep(4);
    goNext();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return {
    expenses,
    draft,
    editingExpenseId,
    errors,
    isComplete,
    startEditing,
    updateDraft,
    saveExpense,
    removeExpense,
    cancelEditing,
    handleContinue,
    goPrevious,
  };
}