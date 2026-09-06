import { formatCurrency, annualizeIncome } from "../../../lib/onboarding/income/income";
import type { IncomeSource } from "../../../lib/onboarding/income/types";

type Props = { source: IncomeSource; onEdit: () => void; onRemove: () => void };

export default function IncomeSourceCard({ source, onEdit, onRemove }: Props) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="font-extrabold text-navy-900">{source.incomeType}</h3>
          <p className="mt-1 text-sm text-slate-500">{source.frequency}</p>
        </div>
        <div className="flex shrink-0 gap-3 text-sm font-bold">
          <button type="button" onClick={onEdit} className="text-teal-700 underline decoration-teal-200 underline-offset-4 hover:text-teal-800">
            Edit
          </button>
          <button type="button" onClick={onRemove} className="text-slate-500 underline decoration-slate-200 underline-offset-4 hover:text-red-600">
            Remove
          </button>
        </div>
      </div>
      <div className="mt-4 flex flex-wrap items-center gap-2 text-xs font-semibold">
        <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">
          {formatCurrency(annualizeIncome(source))} / year
        </span>
        {source.expectedAnnualGrowth && (
          <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-600">
            Growth {source.expectedAnnualGrowth}%
          </span>
        )}
      </div>
    </article>
  );
}