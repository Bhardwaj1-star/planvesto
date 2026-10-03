"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { supabase } from "../../../lib/supabase";
import {
  goalFlexibilities,
  goalTypes,
  type Goal,
  type GoalErrors,
  type GoalDynamicDetails,
} from "../../../lib/onboarding/goals/types";

type Props = {
  goal: Goal;
  errors: GoalErrors;
  isEditing: boolean;
  onChange: (changes: Partial<Goal>) => void;
  onSave: (event: React.FormEvent<HTMLFormElement>) => boolean | Promise<boolean>;
  onCancel: () => void;
};

type LiabilityOption = {
  id: string;
  name: string;
  outstandingAmount: number;
  interestRate: number | null;
  emi: number | null;
  endDate: string | null;
};

function fieldClasses(hasError = false) {
  return `form-field w-full rounded-xl border bg-white px-4 py-3 text-sm text-navy-900 placeholder:text-slate-400 ${hasError ? "border-red-300" : "border-slate-200"}`;
}

function ErrorMessage({ id, message }: { id: string; message?: string }) {
  return message ? <p id={id} className="mt-1.5 text-xs font-medium text-red-600" role="alert">{message}</p> : null;
}

function ChoiceGroup({ label, name, value, options, error, onChange }: { label: string; name: string; value: string; options: readonly string[]; error?: string; onChange: (value: string) => void }) {
  return (
    <fieldset>
      <legend className="mb-2 text-xs font-semibold text-navy-900">{label}</legend>
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
        {options.map((option) => (
          <label key={option} className={`flex cursor-pointer items-center gap-2 rounded-lg border bg-white px-3 py-2.5 text-xs font-semibold ${value === option ? "border-teal-500 ring-2 ring-teal-50" : "border-slate-200"}`}>
            <input type="radio" name={name} value={option} checked={value === option} onChange={() => onChange(option)} className="h-3.5 w-3.5 accent-teal-600" />
            {option}
          </label>
        ))}
      </div>
      <ErrorMessage id={`${name}-error`} message={error} />
    </fieldset>
  );
}

function TextField({ id, label, value, onChange, placeholder, type = "text", error }: { id: string; label: string; value: string; onChange: (value: string) => void; placeholder?: string; type?: string; error?: string }) {
  return (
    <div>
      <label htmlFor={id} className="mb-1.5 block text-xs font-semibold text-navy-900">{label}</label>
      <input id={id} type={type} value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} className={fieldClasses(Boolean(error))} />
      <ErrorMessage id={`${id}-error`} message={error} />
    </div>
  );
}

function updateDetails(goal: Goal, changes: Partial<GoalDynamicDetails>, onChange: Props["onChange"]) {
  onChange({ dynamicDetails: { ...goal.dynamicDetails, ...changes } });
}

export default function GoalForm({ goal, errors, isEditing, onChange, onSave, onCancel }: Props) {
  const isProfile = usePathname() === "/investor/profile";
  const [profileOpen, setProfileOpen] = useState(false);
  const [liabilities, setLiabilities] = useState<LiabilityOption[]>([]);
  const details = goal.dynamicDetails;

  useEffect(() => {
    if (goal.goalType !== "Debt Freedom") return;
    let active = true;
    async function loadLiabilities() {
      const planningUnitId = typeof window !== "undefined" ? window.localStorage.getItem("planvesto-planning-unit-id") : null;
      if (!planningUnitId) return;
      const { data } = await supabase.from("liabilities").select("liability_id, liability_name, outstanding_amount, interest_rate, emi_amount, end_date").eq("planning_unit_id", planningUnitId).order("created_at");
      if (!active) return;
      setLiabilities((data || []).map((row) => ({
        id: row.liability_id,
        name: row.liability_name,
        outstandingAmount: Number(row.outstanding_amount || 0),
        interestRate: row.interest_rate == null ? null : Number(row.interest_rate),
        emi: row.emi_amount == null ? null : Number(row.emi_amount),
        endDate: row.end_date || null,
      })));
    }
    loadLiabilities();
    return () => { active = false; };
  }, [goal.goalType]);

  const isOther = goal.goalType === "Other";
  const isRetirement = goal.goalType === "Retirement";
  const isFinancialFreedom = goal.goalType === "Financial Independence";
  const isDebt = goal.goalType === "Debt Freedom";
  const needsTodayCost = !isRetirement && !isFinancialFreedom && !isDebt;

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    const saved = await onSave(event);
    if (saved && isProfile) setProfileOpen(false);
  }

  if (isProfile && !isEditing && !profileOpen) {
    return <div className="flex justify-start"><button type="button" onClick={() => setProfileOpen(true)} className="inline-flex items-center justify-center rounded-xl border border-teal-600 bg-white px-5 py-3 text-sm font-bold text-teal-700 shadow-sm hover:bg-teal-50">+ Add new goal</button></div>;
  }

  return (
    <form noValidate onSubmit={handleSubmit} className="rounded-2xl border border-teal-200 bg-teal-50/50 p-5 shadow-sm sm:p-6">
      <div className="mb-5 flex items-start justify-between gap-4 border-b border-teal-100 pb-4">
        <div>
          <p className="text-[11px] font-bold uppercase tracking-[0.14em] text-teal-700">{isEditing ? "Edit goal" : "New goal"}</p>
          <h2 className="mt-1.5 text-lg font-extrabold text-navy-900">{goal.goalType ? "Shape your goal" : "Select a goal"}</h2>
          <p className="mt-1 text-xs text-slate-500">{goal.goalType ? "We&apos;ll ask only for the information relevant to this goal." : "Start by selecting the goal you are planning for."}</p>
        </div>
        <button type="button" onClick={onCancel} className="text-xs font-bold text-slate-500 underline underline-offset-4">Cancel</button>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5">
        <label htmlFor="goalType" className="mb-1.5 block text-xs font-semibold text-navy-900">Goal</label>
        <select
          id="goalType"
          value={goal.goalType}
          onChange={(e) => onChange({ goalType: e.target.value as Goal["goalType"], name: e.target.value === "Other" ? "" : e.target.value })}
          className={`${fieldClasses(Boolean(errors.goalType))} appearance-none`}
        >
          <option value="">Select a goal</option>
          {goalTypes.map((name) => <option key={name} value={name}>{name}</option>)}
        </select>
        <ErrorMessage id="goalType-error" message={errors.goalType} />
      </div>

      {goal.goalType && <>
        <div className="mt-4 rounded-2xl border border-teal-100 bg-teal-50/30 p-4 sm:p-5">
          <h3 className="text-sm font-extrabold text-navy-900">Goal details</h3>
          <div className="mt-4 grid gap-4 sm:grid-cols-2">
            {isOther && <TextField id="otherGoalName" label="Goal Name" value={details.otherGoalName} onChange={(value) => updateDetails(goal, { otherGoalName: value }, onChange)} placeholder="e.g. Family milestone" error={errors["otherGoalName"]} />}

            {isRetirement && <>
              <TextField id="lifeExpectancy" label="Life Expectancy" value={details.lifeExpectancy} onChange={(value) => updateDetails(goal, { lifeExpectancy: value }, onChange)} type="number" placeholder="e.g. 85" error={errors["lifeExpectancy"]} />
              <TextField id="desiredLifestyleMonthlyExpense" label="Desired Lifestyle Monthly Expense" value={details.desiredLifestyleMonthlyExpense} onChange={(value) => updateDetails(goal, { desiredLifestyleMonthlyExpense: value }, onChange)} type="number" placeholder="₹ per month" error={errors["desiredLifestyleMonthlyExpense"]} />
            </>}

            {goal.goalType === "Financial Independence" && <TextField id="desiredPassiveIncomeAmount" label="Desired Passive Income Amount" value={details.desiredPassiveIncomeAmount} onChange={(value) => updateDetails(goal, { desiredPassiveIncomeAmount: value }, onChange)} type="number" placeholder="₹ per month" error={errors["desiredPassiveIncomeAmount"]} />}

            {goal.goalType === "Education" && <ChoiceGroup label="For Whom" name="educationForWhom" value={details.educationForWhom} options={["Self", "Spouse", "Children"]} error={errors["educationForWhom"]} onChange={(value) => updateDetails(goal, { educationForWhom: value as GoalDynamicDetails["educationForWhom"] }, onChange)} />}

            {goal.goalType === "Marriage" && <ChoiceGroup label="For Whom" name="marriageForWhom" value={details.marriageForWhom} options={["Self", "Spouse", "Child", "Other"]} error={errors["marriageForWhom"]} onChange={(value) => updateDetails(goal, { marriageForWhom: value as GoalDynamicDetails["marriageForWhom"] }, onChange)} />}

            {goal.goalType === "Home" && <TextField id="preferredLocation" label="Preferred Location" value={details.preferredLocation} onChange={(value) => updateDetails(goal, { preferredLocation: value }, onChange)} placeholder="City / area" error={errors["preferredLocation"]} />}

            {goal.goalType === "Vehicle" && <>
              <TextField id="vehicleType" label="Vehicle Type" value={details.vehicleType} onChange={(value) => updateDetails(goal, { vehicleType: value }, onChange)} placeholder="e.g. SUV, Sedan, Bike" error={errors["vehicleType"]} />
              <ChoiceGroup label="Condition" name="vehicleCondition" value={details.vehicleCondition} options={["New", "Used"]} error={errors["vehicleCondition"]} onChange={(value) => updateDetails(goal, { vehicleCondition: value as GoalDynamicDetails["vehicleCondition"] }, onChange)} />
            </>}

            {goal.goalType === "Travel & Experiences" && <>
              <TextField id="vacationFrequency" label="Frequency" value={details.vacationFrequency} onChange={(value) => updateDetails(goal, { vacationFrequency: value }, onChange)} placeholder="e.g. Once a year" error={errors["vacationFrequency"]} />
              <ChoiceGroup label="Travel Type" name="vacationType" value={details.vacationType} options={["Domestic", "International"]} error={errors["vacationType"]} onChange={(value) => updateDetails(goal, { vacationType: value as GoalDynamicDetails["vacationType"] }, onChange)} />
            </>}

            {goal.goalType === "Wealth Creation" && <TextField id="targetWealthCorpus" label="Target Wealth / Corpus" value={details.targetWealthCorpus} onChange={(value) => updateDetails(goal, { targetWealthCorpus: value }, onChange)} type="number" placeholder="₹" error={errors["targetWealthCorpus"]} />}

            {isDebt && <div className="sm:col-span-2">
              <label htmlFor="selectedLiabilityId" className="mb-1.5 block text-xs font-semibold text-navy-900">Select Liability / Debt</label>
              <select id="selectedLiabilityId" value={details.selectedLiabilityId} onChange={(e) => updateDetails(goal, { selectedLiabilityId: e.target.value }, onChange)} className={`${fieldClasses(Boolean(errors["selectedLiabilityId"]))} appearance-none`}>
                <option value="">Select an existing liability</option>
                {liabilities.map((liability) => <option key={liability.id} value={liability.id}>{liability.name} · ₹{liability.outstandingAmount.toLocaleString("en-IN")}</option>)}
              </select>
              <ErrorMessage id="selectedLiabilityId-error" message={errors["selectedLiabilityId"]} />
              {details.selectedLiabilityId && (() => {
                const selected = liabilities.find((item) => item.id === details.selectedLiabilityId);
                return selected ? <p className="mt-2 text-xs text-slate-500">Outstanding ₹{selected.outstandingAmount.toLocaleString("en-IN")}{selected.interestRate != null ? ` · ${selected.interestRate}% interest` : ""}{selected.emi != null ? ` · EMI ₹${selected.emi.toLocaleString("en-IN")}` : ""}</p> : null;
              })()}
            </div>}

            {goal.goalType === "Legacy & Giving" && <TextField id="philanthropyContributionAmount" label="Contribution Amount" value={details.philanthropyContributionAmount} onChange={(value) => updateDetails(goal, { philanthropyContributionAmount: value }, onChange)} type="number" placeholder="₹" error={errors["philanthropyContributionAmount"]} />}

            {needsTodayCost && <TextField id="targetAmount" label="Today&apos;s Cost" value={goal.targetAmount} onChange={(value) => onChange({ targetAmount: value })} type="number" placeholder="₹" error={errors.targetAmount} />}

            <div>
              <label htmlFor="targetDate" className="mb-1.5 block text-xs font-semibold text-navy-900">Target Month &amp; Year</label>
              <input id="targetDate" type="month" min={new Date().toISOString().slice(0, 7)} value={goal.targetDate.slice(0, 7)} onChange={(e) => onChange({ targetMode: "Date", targetDate: e.target.value ? `${e.target.value}-01` : "" })} className={fieldClasses(Boolean(errors.targetDate || errors.targetMode))} />
              <ErrorMessage id="targetDate-error" message={errors.targetDate || errors.targetMode} />
            </div>

            <ChoiceGroup label="Flexibility" name="flexibility" value={goal.flexibility} options={goalFlexibilities} error={errors.flexibility} onChange={(value) => onChange({ flexibility: value as Goal["flexibility"] })} />

            {isOther && <>
              <TextField id="otherGoalDescription" label="Goal Description" value={details.otherGoalDescription} onChange={(value) => updateDetails(goal, { otherGoalDescription: value }, onChange)} placeholder="Describe the goal" error={errors["otherGoalDescription"]} />
              <TextField id="otherAdditionalDetails" label="Relevant Additional Details" value={details.otherAdditionalDetails} onChange={(value) => updateDetails(goal, { otherAdditionalDetails: value }, onChange)} placeholder="Anything else we should know?" error={errors["otherAdditionalDetails"]} />
            </>}
          </div>
        </div>

        <div className="mt-5 flex justify-end">
          <button type="submit" className="rounded-xl bg-teal-700 px-5 py-2.5 text-xs font-bold text-white">{isEditing ? "Save changes" : "Add goal"}</button>
        </div>
      </>}
    </form>
  );
}
