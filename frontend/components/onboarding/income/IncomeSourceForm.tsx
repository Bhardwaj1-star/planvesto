"use client";

import { incomeFrequencies, incomeTypes, type IncomeSource, type IncomeSourceErrors } from "../../../lib/onboarding/income/types";

type Props = {
  source: IncomeSource;
  errors: IncomeSourceErrors;
  isEditing: boolean;
  onChange: (changes: Partial<IncomeSource>) => void;
  onSave: (event: React.FormEvent<HTMLFormElement>) => boolean | Promise<boolean>;
  onCancel: () => void;
};

function fieldClasses(hasError = false) {
  return `form-field w-full rounded-xl border bg-white px-4 py-3.5 text-sm text-navy-900 placeholder:text-slate-400 ${hasError ? "border-red-300" : "border-slate-200"}`;
}

function ErrorMessage({ id, message }: { id: string; message?: string }) {
  return message ? <p id={id} className="mt-2 text-xs font-medium text-red-600" role="alert">{message}</p> : null;
}

export default function IncomeSourceForm({ source, errors, isEditing, onChange, onSave, onCancel }: Props) {
  return (
    <form noValidate onSubmit={onSave} className="rounded-[28px] border border-teal-200 bg-teal-50/50 p-6 shadow-soft sm:p-8">
      <div className="mb-6 flex items-start justify-between gap-4 border-b border-teal-100 pb-5">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-700">{isEditing ? "Edit income" : "New income source"}</p>
          <h2 className="mt-2 text-xl font-extrabold text-navy-900">Describe this income</h2>
        </div>
        {isEditing && (
          <button type="button" onClick={onCancel} className="text-sm font-bold text-slate-500 underline decoration-slate-300 underline-offset-4 hover:text-navy-900">
            Cancel
          </button>
        )}
      </div>
      <div className="grid gap-5 sm:grid-cols-2">
        <div>
          <label htmlFor="incomeType" className="mb-2 block text-sm font-semibold text-navy-900">Income type</label>
          <select
            id="incomeType"
            value={source.incomeType}
            onChange={(event) => onChange({ incomeType: event.target.value as IncomeSource["incomeType"] })}
            aria-invalid={Boolean(errors.incomeType)}
            aria-describedby={errors.incomeType ? "incomeType-error" : undefined}
            className={`${fieldClasses(Boolean(errors.incomeType))} appearance-none`}
          >
            <option value="">Select an income type</option>
            {incomeTypes.map((type) => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
          <ErrorMessage id="incomeType-error" message={errors.incomeType} />
        </div>
        <div>
          <label htmlFor="amount" className="mb-2 block text-sm font-semibold text-navy-900">Amount</label>
          <div className="relative">
            <span className="pointer-events-none absolute left-4 top-3.5 text-sm text-slate-400">$</span>
            <input
              id="amount"
              type="number"
              min="0.01"
              step="0.01"
              inputMode="decimal"
              value={source.amount}
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
        <fieldset>
          <legend className="mb-3 text-sm font-semibold text-navy-900">Frequency</legend>
          <div className="grid grid-cols-2 gap-3">
            {incomeFrequencies.map((frequency) => (
              <label
                key={frequency}
                className={`flex cursor-pointer items-center gap-3 rounded-xl border bg-white px-4 py-3 text-sm font-semibold ${
                  source.frequency === frequency ? "border-teal-500 ring-4 ring-teal-50" : "border-slate-200"
                }`}
              >
                <input
                  type="radio"
                  name="frequency"
                  value={frequency}
                  checked={source.frequency === frequency}
                  onChange={() => onChange({ frequency })}
                  className="h-4 w-4 accent-teal-600"
                />
                {frequency}
              </label>
            ))}
          </div>
          <ErrorMessage id="frequency-error" message={errors.frequency} />
        </fieldset>
        <div>
          <label htmlFor="expectedAnnualGrowth" className="mb-2 block text-sm font-semibold text-navy-900">
            Expected annual growth <span className="font-normal text-slate-400">(optional)</span>
          </label>
          <div className="relative">
            <input
              id="expectedAnnualGrowth"
              type="number"
              min="-100"
              max="100"
              step="0.1"
              inputMode="decimal"
              value={source.expectedAnnualGrowth}
              onChange={(event) => onChange({ expectedAnnualGrowth: event.target.value })}
              onKeyDown={(event) => ["e", "E", "+"].includes(event.key) && event.preventDefault()}
              aria-invalid={Boolean(errors.expectedAnnualGrowth)}
              aria-describedby={errors.expectedAnnualGrowth ? "expectedAnnualGrowth-error" : undefined}
              placeholder="e.g. 3"
              className={`${fieldClasses(Boolean(errors.expectedAnnualGrowth))} pr-9`}
            />
            <span className="pointer-events-none absolute right-4 top-3.5 text-sm text-slate-400">%</span>
          </div>
          <p className="mt-2 text-xs text-slate-500">Leave blank or use 0 if you do not expect this source to grow.</p>
          <ErrorMessage id="expectedAnnualGrowth-error" message={errors.expectedAnnualGrowth} />
        </div>
      </div>
      <div className="mt-7 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">{isEditing && <button type="button" onClick={onCancel} className="rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-navy-900 transition hover:border-slate-300">Cancel</button>}<button type="submit" className="rounded-xl bg-teal-700 px-5 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-teal-800 focus:outline-none focus:ring-4 focus:ring-teal-100">{isEditing ? "Save changes" : "Add income source"}</button></div>
    </form>
  );
}