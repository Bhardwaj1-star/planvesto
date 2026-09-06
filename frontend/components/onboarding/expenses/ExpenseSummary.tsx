import { formatCurrency, getAnnualExpenses } from "../../../lib/onboarding/expenses/expenses";
import type { Expense } from "../../../lib/onboarding/expenses/types";
import ExpenseCategoryCard from "./ExpenseCategoryCard";

type Props = { expenses: Expense[]; onEdit: (expense: Expense) => void; onRemove: (id: string) => void };

export default function ExpenseSummary({ expenses, onEdit, onRemove }: Props) {
  const annualExpenses = getAnnualExpenses(expenses);
  if (expenses.length === 0) {
    return (
      <div className="rounded-[28px] border border-dashed border-slate-300 bg-white px-6 py-10 text-center sm:px-8">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-teal-50 text-teal-700" aria-hidden="true">
          $
        </div>
        <h2 className="mt-4 text-lg font-extrabold text-navy-900">No expenses added yet</h2>
        <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
          Add your regular spending so your plan can reflect sustainable cash flow. You can continue without adding an expense right now.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="grid gap-3 sm:grid-cols-2">
        <div className="rounded-2xl border border-navy-900 bg-navy-900 p-5 text-white">
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-200">Total annual expenses</p>
          <p className="mt-2 text-2xl font-extrabold">{formatCurrency(annualExpenses)}</p>
        </div>
        <div className="rounded-2xl border border-teal-200 bg-teal-50 p-5 text-navy-900">
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-700">Total monthly expenses</p>
          <p className="mt-2 text-2xl font-extrabold">{formatCurrency(annualExpenses / 12)}</p>
          <p className="mt-1 text-xs text-slate-500">Annual expenses divided by 12</p>
        </div>
      </div>
      <div className="space-y-3">
        {expenses.map((expense) => (
          <ExpenseCategoryCard key={expense.id} expense={expense} onEdit={() => onEdit(expense)} onRemove={() => onRemove(expense.id)} />
        ))}
      </div>
    </div>
  );
}