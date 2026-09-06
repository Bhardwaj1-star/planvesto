"use client";

import { liabilityFrequencies, liabilityTypes, type Liability, type LiabilityErrors } from "../../../lib/onboarding/liabilities/types";

type Props = {
  liability: Liability;
  errors: LiabilityErrors;
  isEditing: boolean;
  onChange: (changes: Partial<Liability>) => void;
  onSave: (event: React.FormEvent<HTMLFormElement>) => boolean | Promise<boolean>;
  onCancel: () => void;
};

function fieldClasses(hasError = false) {
  return `form-field w-full rounded-xl border bg-white px-4 py-3.5 text-sm text-navy-900 placeholder:text-slate-400 ${hasError ? "border-red-300" : "border-slate-200"}`;
}

function ErrorMessage({ id, message }: { id: string; message?: string }) {
  return message ? <p id={id} className="mt-2 text-xs font-medium text-red-600" role="alert">{message}</p> : null;
}

export default function LiabilityForm({ liability, errors, isEditing, onChange, onSave, onCancel }: Props) {
  return (
    <form noValidate onSubmit={onSave} className="rounded-[28px] border border-teal-200 bg-teal-50/50 p-6 shadow-soft sm:p-8">
      <div className="mb-6 flex items-start justify-between gap-4 border-b border-teal-100 pb-5">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-700">{isEditing ? "Edit liability" : "New liability"}</p>
          <h2 className="mt-2 text-xl font-extrabold text-navy-900">Describe what you owe</h2>
        </div>
        {isEditing && (
          <button type="button" onClick={onCancel} className="text-sm font-bold text-slate-500 underline decoration-slate-300 underline-offset-4 hover:text-navy-900">
            Cancel
          </button>
        )}
      </div>
      <div className="grid gap-5 sm:grid-cols-2">
        <div>
          <label htmlFor="liabilityType" className="mb-2 block text-sm font-semibold text-navy-900">Liability type</label>
          <select
            id="liabilityType"
            value={liability.liabilityType}
            onChange={(event) => onChange({ liabilityType: event.target.value as Liability["liabilityType"] })}
            aria-invalid={Boolean(errors.liabilityType)}
            aria-describedby={errors.liabilityType ? "liabilityType-error" : undefined}
            className={`${fieldClasses(Boolean(errors.liabilityType))} appearance-none`}
          >
            <option value="">Select a liability type</option>
            {liabilityTypes.map((type) => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
          <ErrorMessage id="liabilityType-error" message={errors.liabilityType} />
        </div>
        <div>
          <label htmlFor="description" className="mb-2 block text-sm font-semibold text-navy-900">Lender / description</label>
          <input
            id="description"
            value={liability.description}
            onChange={(event) => onChange({ description: event.target.value })}
            aria-invalid={Boolean(errors.description)}
            aria-describedby={errors.description ? "description-error" : undefined}
            placeholder="e.g. Home loan with ABC Bank"
            className={fieldClasses(Boolean(errors.description))}
          />
          <ErrorMessage id="description-error" message={errors.description} />
        </div>
        <div>
          <label htmlFor="outstandingAmount" className="mb-2 block text-sm font-semibold text-navy-900">Current outstanding amount</label>
          <div className="relative">
            <span className="pointer-events-none absolute left-4 top-3.5 text-sm text-slate-400">$</span>
            <input
              id="outstandingAmount"
              type="number"
              min="0.01"
              step="0.01"
              inputMode="decimal"
              value={liability.outstandingAmount}
              onChange={(event) => onChange({ outstandingAmount: event.target.value })}
              onKeyDown={(event) => ["e", "E", "+", "-"].includes(event.key) && event.preventDefault()}
              aria-invalid={Boolean(errors.outstandingAmount)}
              aria-describedby={errors.outstandingAmount ? "outstandingAmount-error" : undefined}
              placeholder="0.00"
              className={`${fieldClasses(Boolean(errors.outstandingAmount))} pl-8`}
            />
          </div>
          <ErrorMessage id="outstandingAmount-error" message={errors.outstandingAmount} />
        </div>
        <div>
          <label htmlFor="interestRate" className="mb-2 block text-sm font-semibold text-navy-900">
            Interest rate <span className="font-normal text-slate-400">(optional)</span>
          </label>
          <div className="relative">
            <input
              id="interestRate"
              type="number"
              min="0"
              max="100"
              step="0.01"
              inputMode="decimal"
              value={liability.interestRate}
              onChange={(event) => onChange({ interestRate: event.target.value })}
              onKeyDown={(event) => ["e", "E", "+", "-"].includes(event.key) && event.preventDefault()}
              aria-invalid={Boolean(errors.interestRate)}
              aria-describedby={errors.interestRate ? "interestRate-error" : undefined}
              placeholder="e.g. 8.5"
              className={`${fieldClasses(Boolean(errors.interestRate))} pr-9`}
            />
            <span className="pointer-events-none absolute right-4 top-3.5 text-sm text-slate-400">%</span>
          </div>
          <ErrorMessage id="interestRate-error" message={errors.interestRate} />
        </div>
        <div>
          <label htmlFor="regularPayment" className="mb-2 block text-sm font-semibold text-navy-900">
            EMI / regular payment <span className="font-normal text-slate-400">(optional)</span>
          </label>
          <div className="relative">
            <span className="pointer-events-none absolute left-4 top-3.5 text-sm text-slate-400">$</span>
            <input
              id="regularPayment"
              type="number"
              min="0.01"
              step="0.01"
              inputMode="decimal"
              value={liability.regularPayment}
              onChange={(event) => onChange({ regularPayment: event.target.value })}
              onKeyDown={(event) => ["e", "E", "+", "-"].includes(event.key) && event.preventDefault()}
              aria-invalid={Boolean(errors.regularPayment)}
              aria-describedby={errors.regularPayment ? "regularPayment-error" : undefined}
              placeholder="0.00"
              className={`${fieldClasses(Boolean(errors.regularPayment))} pl-8`}
            />
          </div>
          <ErrorMessage id="regularPayment-error" message={errors.regularPayment} />
        </div>
        <div>
          <label htmlFor="endDate" className="mb-2 block text-sm font-semibold text-navy-900">
            End date <span className="font-normal text-slate-400">(optional)</span>
          </label>
          <input
            id="endDate"
            type="date"
            value={liability.endDate}
            onChange={(event) => onChange({ endDate: event.target.value })}
            aria-invalid={Boolean(errors.endDate)}
            aria-describedby={errors.endDate ? "endDate-error" : undefined}
            className={fieldClasses(Boolean(errors.endDate))}
          />
          <ErrorMessage id="endDate-error" message={errors.endDate} />
        </div>
        <fieldset className="sm:col-span-2">
          <legend className="mb-3 text-sm font-semibold text-navy-900">Payment frequency</legend>
          <div className="grid grid-cols-3 gap-3">
            {liabilityFrequencies.map((frequency) => (
              <label
                key={frequency}
                className={`flex cursor-pointer items-center gap-3 rounded-xl border bg-white px-4 py-3 text-sm font-semibold ${
                  liability.frequency === frequency ? "border-teal-500 ring-4 ring-teal-50" : "border-slate-200"
                }`}
              >
                <input
                  type="radio"
                  name="liability-frequency"
                  value={frequency}
                  checked={liability.frequency === frequency}
                  onChange={() => onChange({ frequency })}
                  className="h-4 w-4 accent-teal-600"
                />
                {frequency}
              </label>
            ))}
          </div>
          <ErrorMessage id="frequency-error" message={errors.frequency} />
        </fieldset>
      </div>
      <div className="mt-7 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">{isEditing && <button type="button" onClick={onCancel} className="rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-navy-900 transition hover:border-slate-300">Cancel</button>}<button type="submit" className="rounded-xl bg-teal-700 px-5 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-teal-800 focus:outline-none focus:ring-4 focus:ring-teal-100">{isEditing ? "Save changes" : "Add liability"}</button></div>
    </form>
  );
}