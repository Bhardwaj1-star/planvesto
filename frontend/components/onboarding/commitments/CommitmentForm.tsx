"use client";

import type { Commitment, CommitmentErrors } from "../../../lib/onboarding/commitments/types";

type Props = {
  commitment: Commitment;
  errors: CommitmentErrors;
  isEditing: boolean;
  onChange: (changes: Partial<Commitment>) => void;
  onSave: (event: React.FormEvent<HTMLFormElement>) => boolean | Promise<boolean>;
  onCancel: () => void;
};

function fieldClasses(hasError = false) {
  return `form-field w-full rounded-xl border bg-white px-4 py-3.5 text-sm text-navy-900 placeholder:text-slate-400 ${
    hasError ? "border-red-300" : "border-slate-200"
  }`;
}

function ErrorMessage({ id, message }: { id: string; message?: string }) {
  return message ? <p id={id} className="mt-2 text-xs font-medium text-red-600" role="alert">{message}</p> : null;
}

export default function CommitmentForm({ commitment, errors, isEditing, onChange, onSave, onCancel }: Props) {
  return (
    <form noValidate onSubmit={onSave} className="rounded-[28px] border border-teal-200 bg-teal-50/50 p-6 shadow-soft sm:p-8">
      <div className="mb-6 flex items-start justify-between gap-4 border-b border-teal-100 pb-5">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-700">
            {isEditing ? "Edit commitment" : "New commitment"}
          </p>
          <h2 className="mt-2 text-xl font-extrabold text-navy-900">Describe this commitment</h2>
        </div>
        {isEditing && (
          <button
            type="button"
            onClick={onCancel}
            className="text-sm font-bold text-slate-500 underline decoration-slate-300 underline-offset-4 hover:text-navy-900"
          >
            Cancel
          </button>
        )}
      </div>
      <div className="grid gap-5 sm:grid-cols-2">
        <div>
          <label htmlFor="name" className="mb-2 block text-sm font-semibold text-navy-900">
            Commitment name / description
          </label>
          <input
            id="name"
            value={commitment.name}
            onChange={(event) => onChange({ name: event.target.value })}
            aria-invalid={Boolean(errors.name)}
            aria-describedby={errors.name ? "name-error" : undefined}
            placeholder="e.g. Children higher education, Family support"
            className={fieldClasses(Boolean(errors.name))}
          />
          <ErrorMessage id="name-error" message={errors.name} />
        </div>
        <div>
          <label htmlFor="amount" className="mb-2 block text-sm font-semibold text-navy-900">
            Amount
          </label>
          <div className="relative">
            <span className="pointer-events-none absolute left-4 top-3.5 text-sm text-slate-400">$</span>
            <input
              id="amount"
              type="number"
              min="0.01"
              step="0.01"
              inputMode="decimal"
              value={commitment.amount}
              onChange={(event) => onChange({ amount: event.target.value })}
              onKeyDown={(event) => ["e", "E", "+", "-"].includes(event.key) && event.preventDefault()}
              aria-invalid={Boolean(errors.amount)}
              aria-describedby={errors.amount ? "amount-error" : undefined}
              placeholder="0.00"
              className={`${fieldClasses(Boolean(errors.amount))} pl-8`}
            />
          </div>
          <ErrorMessage id="amount-error" message={errors.amount} />
        </div>
      </div>
      <div className="mt-7 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
        {isEditing && (
          <button
            type="button"
            onClick={onCancel}
            className="rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-navy-900 transition hover:border-slate-300"
          >
            Cancel
          </button>
        )}
        <button
          type="submit"
          className="rounded-xl bg-teal-700 px-5 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-teal-800 focus:outline-none focus:ring-4 focus:ring-teal-100"
        >
          {isEditing ? "Save changes" : "Add commitment"}
        </button>
      </div>
    </form>
  );
}
