import { formatCurrency } from "../../../lib/onboarding/commitments/commitments";
import type { Commitment } from "../../../lib/onboarding/commitments/types";

type Props = {
  commitment: Commitment;
  onEdit: () => void;
  onRemove: () => void;
};

export default function CommitmentCard({ commitment, onEdit, onRemove }: Props) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="font-extrabold text-navy-900">{commitment.name}</h3>
          <p className="mt-1 text-sm font-semibold text-teal-700">
            {formatCurrency(Number(commitment.amount))}
          </p>
        </div>
        <div className="flex shrink-0 gap-3 text-sm font-bold">
          <button
            type="button"
            onClick={onEdit}
            className="text-teal-700 underline decoration-teal-200 underline-offset-4 hover:text-teal-800"
          >
            Edit
          </button>
          <button
            type="button"
            onClick={onRemove}
            className="text-slate-500 underline decoration-slate-200 underline-offset-4 hover:text-red-600"
          >
            Remove
          </button>
        </div>
      </div>
    </article>
  );
}
