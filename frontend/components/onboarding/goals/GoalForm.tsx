"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";
import {
  goalFlexibilities,
  goalPriorities,
  goalTypes,
  type Goal,
  type GoalErrors,
} from "../../../lib/onboarding/goals/types";

type Props = {
  goal: Goal;
  errors: GoalErrors;
  isEditing: boolean;
  onChange: (changes: Partial<Goal>) => void;
  onSave: (event: React.FormEvent<HTMLFormElement>) => boolean | Promise<boolean>;
  onCancel: () => void;
};

const PRESET_GOAL_NAMES = [
  "Retirement",
  "Child Education",
  "Child Marriage",
  "Dream Home",
  "Vehicle",
  "Travel",
  "Wealth Creation",
  "Emergency Fund",
  "Other",
] as const;

function fieldClasses(hasError = false) {
  return `form-field w-full rounded-xl border bg-white px-4 py-3 text-sm text-navy-900 placeholder:text-slate-400 ${hasError ? "border-red-300" : "border-slate-200"}`;
}

function ErrorMessage({ id, message }: { id: string; message?: string }) {
  return message ? <p id={id} className="mt-1.5 text-xs font-medium text-red-600" role="alert">{message}</p> : null;
}

function ChoiceGroup({
  label,
  name,
  value,
  options,
  error,
  onChange,
}: {
  label: string;
  name: string;
  value: string;
  options: readonly string[];
  error?: string;
  onChange: (value: string) => void;
}) {
  return (
    <fieldset>
      <legend className="mb-2 text-xs font-semibold text-navy-900">{label}</legend>
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
        {options.map((option) => (
          <label
            key={option}
            className={`flex cursor-pointer items-center gap-2 rounded-lg border bg-white px-3 py-2.5 text-xs font-semibold ${value === option ? "border-teal-500 ring-2 ring-teal-50" : "border-slate-200"}`}
          >
            <input
              type="radio"
              name={name}
              value={option}
              checked={value === option}
              onChange={() => onChange(option)}
              className="h-3.5 w-3.5 accent-teal-600"
            />
            {option}
          </label>
        ))}
      </div>
      <ErrorMessage id={`${name}-error`} message={error} />
    </fieldset>
  );
}

export default function GoalForm({ goal, errors, isEditing, onChange, onSave, onCancel }: Props) {
  const isProfile = usePathname() === "/investor/profile";
  const [profileOpen, setProfileOpen] = useState(false);
  const presetValue = PRESET_GOAL_NAMES.includes(goal.name as (typeof PRESET_GOAL_NAMES)[number])
    ? goal.name
    : goal.name
      ? "Other"
      : "";

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    const saved = await onSave(event);
    if (saved && isProfile) setProfileOpen(false);
  }

  if (isProfile && !isEditing && !profileOpen) {
    return (
      <div className="flex justify-start">
        <button type="button" onClick={() => setProfileOpen(true)} className="inline-flex items-center justify-center rounded-xl border border-teal-600 bg-white px-5 py-3 text-sm font-bold text-teal-700 shadow-sm hover:bg-teal-50">
          + Add new goal
        </button>
      </div>
    );
  }

  return (
    <form noValidate onSubmit={handleSubmit} className="rounded-2xl border border-teal-200 bg-teal-50/50 p-5 shadow-sm sm:p-6">
      <div className="mb-5 flex items-start justify-between gap-4 border-b border-teal-100 pb-4">
        <div>
          <p className="text-[11px] font-bold uppercase tracking-[0.14em] text-teal-700">{isEditing ? "Edit goal" : "New goal"}</p>
          <h2 className="mt-1.5 text-lg font-extrabold text-navy-900">Give this goal a shape</h2>
          <p className="mt-1 text-xs text-slate-500">Tell us what you are planning for. We&apos;ll use this information later to build your plan.</p>
        </div>
        <button type="button" onClick={onCancel} className="text-xs font-bold text-slate-500 underline underline-offset-4">Cancel</button>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label htmlFor="goalPreset" className="mb-1.5 block text-xs font-semibold text-navy-900">Goal</label>
          <select
            id="goalPreset"
            value={presetValue}
            onChange={(e) => {
              const value = e.target.value;
              if (value === "Other") {
                onChange({ name: "", goalType: "Other" });
              } else {
                const mappedType = value === "Dream Home" ? "Home Purchase" : value;
                onChange({ name: value, goalType: mappedType as Goal["goalType"] });
              }
            }}
            className={`${fieldClasses(Boolean(errors.name || errors.goalType))} appearance-none`}
          >
            <option value="">Select a goal</option>
            {PRESET_GOAL_NAMES.map((name) => <option key={name} value={name}>{name}</option>)}
          </select>
          <ErrorMessage id="goalPreset-error" message={errors.name || errors.goalType} />
        </div>

        {presetValue === "Other" && (
          <div>
            <label htmlFor="name" className="mb-1.5 block text-xs font-semibold text-navy-900">Goal name</label>
            <input id="name" value={goal.name} onChange={(e) => onChange({ name: e.target.value, goalType: "Other" })} placeholder="e.g. A family milestone" className={fieldClasses(Boolean(errors.name))} />
            <ErrorMessage id="name-error" message={errors.name} />
          </div>
        )}

        <div>
          <label htmlFor="targetAmount" className="mb-1.5 block text-xs font-semibold text-navy-900">Today&apos;s cost</label>
          <div className="relative"><span className="pointer-events-none absolute left-4 top-2.5 text-sm text-slate-400">₹</span><input id="targetAmount" type="number" min="0.01" step="0.01" inputMode="decimal" value={goal.targetAmount} onChange={(e) => onChange({ targetAmount: e.target.value })} placeholder="0.00" className={`${fieldClasses(Boolean(errors.targetAmount))} pl-8`} /></div>
          <ErrorMessage id="targetAmount-error" message={errors.targetAmount} />
        </div>

        <div>
          <label htmlFor="targetDate" className="mb-1.5 block text-xs font-semibold text-navy-900">Target month &amp; year</label>
          <input
            id="targetDate"
            type="month"
            min={new Date().toISOString().slice(0, 7)}
            value={goal.targetDate.slice(0, 7)}
            onChange={(e) => onChange({ targetMode: "Date", targetDate: e.target.value ? `${e.target.value}-01` : "" })}
            className={fieldClasses(Boolean(errors.targetDate || errors.targetMode))}
          />
          <ErrorMessage id="targetDate-error" message={errors.targetDate || errors.targetMode} />
        </div>

        <ChoiceGroup label="Priority" name="priority" value={goal.priority} options={goalPriorities} error={errors.priority} onChange={(value) => onChange({ priority: value as Goal["priority"] })} />
        <ChoiceGroup label="Flexibility" name="flexibility" value={goal.flexibility} options={goalFlexibilities} error={errors.flexibility} onChange={(value) => onChange({ flexibility: value as Goal["flexibility"] })} />
      </div>

      <input type="hidden" value={goal.targetMode || "Date"} readOnly />

      <div className="mt-5 flex justify-end">
        <button type="submit" className="rounded-xl bg-teal-700 px-5 py-2.5 text-xs font-bold text-white shadow-sm">{isEditing ? "Save changes" : "Add goal"}</button>
      </div>
    </form>
  );
}
