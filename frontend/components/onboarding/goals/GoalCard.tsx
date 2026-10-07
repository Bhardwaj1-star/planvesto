import { formatCurrency, getGoalTarget } from "../../../lib/onboarding/goals/goals";
import type { Goal } from "../../../lib/onboarding/goals/types";

type Props = { goal: Goal; onEdit: () => void; onRemove: () => void };

export default function GoalCard({ goal, onEdit, onRemove }: Props) {
  return (
    <article className="rounded-2xl border border-teal-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="font-extrabold text-navy-900">{goal.name}</h3>
          <p className="mt-1 text-sm text-slate-500">{goal.goalType} · {getGoalTarget(goal)}</p>
        </div>
        <div className="flex shrink-0 gap-3 text-sm font-bold">
          <button type="button" onClick={onEdit} className="text-teal-700 underline decoration-teal-200 underline-offset-4 hover:text-teal-800">Edit</button>
          <button type="button" onClick={onRemove} className="text-slate-500 underline decoration-slate-200 underline-offset-4 hover:text-red-600">Cancel Goal</button>
        </div>
      </div>
      <div className="mt-4 flex flex-wrap gap-2 text-xs font-semibold">
        <span className={`rounded-full px-3 py-1 ${goal.flexibility === "Fixed" ? "bg-amber-50 text-amber-800" : "bg-slate-100 text-slate-600"}`}>{goal.flexibility}</span>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">Target {formatCurrency(Number(goal.targetAmount))}</span>
      </div>
    </article>
  );
}