import { formatCurrency, getTotalCommitments } from "../../../lib/onboarding/commitments/commitments";
import type { Commitment } from "../../../lib/onboarding/commitments/types";
import CommitmentCard from "./CommitmentCard";

type Props = {
  commitments: Commitment[];
  onEdit: (commitment: Commitment) => void;
  onRemove: (id: string) => void;
};

export default function CommitmentSummary({ commitments, onEdit, onRemove }: Props) {
  const totalCommitments = getTotalCommitments(commitments);

  if (commitments.length === 0) {
    return (
      <div className="rounded-[28px] border border-dashed border-slate-300 bg-white px-6 py-10 text-center sm:px-8">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-teal-50 text-teal-700" aria-hidden="true">
          $
        </div>
        <h2 className="mt-4 text-lg font-extrabold text-navy-900">No commitments added yet</h2>
        <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
          Add any financial commitments or earmarked promises so your plan can protect them. You can continue without adding a commitment right now.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-navy-900 bg-navy-900 p-5 text-white">
        <p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-200">Total commitments</p>
        <p className="mt-2 text-2xl font-extrabold">{formatCurrency(totalCommitments)}</p>
      </div>
      <div className="space-y-3">
        {commitments.map((commitment) => (
          <CommitmentCard
            key={commitment.id}
            commitment={commitment}
            onEdit={() => onEdit(commitment)}
            onRemove={() => onRemove(commitment.id)}
          />
        ))}
      </div>
    </div>
  );
}
