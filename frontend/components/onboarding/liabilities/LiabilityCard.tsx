import { formatCurrency } from "../../../lib/onboarding/liabilities/liabilities";
import type { Liability } from "../../../lib/onboarding/liabilities/types";

type Props = { liability: Liability; onEdit: () => void; onRemove: () => void };

export default function LiabilityCard({ liability, onEdit, onRemove }: Props) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="font-extrabold text-navy-900">{liability.liabilityType}</h3>
          <p className="mt-1 text-sm text-slate-500">{liability.description}</p>
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
      <div className="mt-4 flex flex-wrap gap-2 text-xs font-semibold">
        <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">
          {formatCurrency(Number(liability.outstandingAmount))} outstanding
        </span>
        {liability.regularPayment && (
          <span className="rounded-full bg-amber-50 px-3 py-1 text-amber-800">
            {formatCurrency(Number(liability.regularPayment))} / {liability.frequency ? liability.frequency.toLowerCase() : "payment"}
          </span>
        )}
        {liability.interestRate && (
          <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-600">
            {liability.interestRate}% interest
          </span>
        )}
        {liability.endDate && (
          <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-600">
            Ends {liability.endDate}
          </span>
        )}
      </div>
    </article>
  );
}