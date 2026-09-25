"use client";

import { useState } from "react";
import { usePersonalInformationForm } from "../../hooks/onboarding/personal-information/usePersonalInformationForm";
import { useFamilyDependents } from "../../hooks/onboarding/family-dependents/useFamilyDependents";
import { useIncome } from "../../hooks/onboarding/income/useIncome";
import { useExpenses } from "../../hooks/onboarding/expenses/useExpenses";
import { useAssets } from "../../hooks/onboarding/assets/useAssets";
import { useLiabilities } from "../../hooks/onboarding/liabilities/useLiabilities";
import { useGoals } from "../../hooks/onboarding/goals/useGoals";
import FamilySummary from "../onboarding/family-dependents/FamilySummary";
import FamilyMemberForm from "../onboarding/family-dependents/FamilyMemberForm";
import IncomeSummary from "../onboarding/income/IncomeSummary";
import IncomeSourceForm from "../onboarding/income/IncomeSourceForm";
import ExpenseSummary from "../onboarding/expenses/ExpenseSummary";
import ExpenseCategoryForm from "../onboarding/expenses/ExpenseCategoryForm";
import AssetSummary from "../onboarding/assets/AssetSummary";
import AssetForm from "../onboarding/assets/AssetForm";
import LiabilitySummary from "../onboarding/liabilities/LiabilitySummary";
import LiabilityForm from "../onboarding/liabilities/LiabilityForm";
import GoalSummary from "../onboarding/goals/GoalSummary";
import GoalForm from "../onboarding/goals/GoalForm";
import InsuranceSection from "../onboarding/insurance/InsuranceSection";
import { genderSelectOptions, maritalStatusSelectOptions } from "../../lib/onboarding/personal-information/model";

type FinancialCategory = "personal" | "income" | "expenses" | "assets" | "liabilities" | "goals" | "insurance";

export default function FinancialInformationSection({ initialCategory = "personal" }: { initialCategory?: FinancialCategory }) {
  const [activeCategory, setActiveCategory] = useState<FinancialCategory>(initialCategory);
  const personal = usePersonalInformationForm();
  const family = useFamilyDependents();
  const income = useIncome();
  const expenses = useExpenses();
  const assets = useAssets();
  const liabilities = useLiabilities();
  const goals = useGoals();
  const today = new Date().toISOString().slice(0, 10);
  const categories = [
    { id: "personal", label: "Personal Information", count: family.members.length ? `${family.members.length} family` : undefined },
    { id: "income", label: "Income", count: income.sources.length ? `${income.sources.length} sources` : undefined },
    { id: "expenses", label: "Expenses", count: expenses.expenses.length ? `${expenses.expenses.length} items` : undefined },
    { id: "assets", label: "Assets", count: assets.assets.length ? `${assets.assets.length} assets` : undefined },
    { id: "liabilities", label: "Liabilities", count: liabilities.liabilities.length ? `${liabilities.liabilities.length} loans` : undefined },
    { id: "goals", label: "Goals", count: goals.goals.length ? `${goals.goals.length} goals` : undefined },
    { id: "insurance", label: "Insurance" },
  ] as const;
  function fieldClasses(hasError = false) { return `form-field w-full rounded-xl border bg-white px-3 py-2.5 text-sm text-navy-900 placeholder:text-slate-400 focus:border-teal-500 focus:outline-none focus:ring-4 focus:ring-teal-50 ${hasError ? "border-red-300" : "border-slate-200"}`; }
  return <div className="space-y-4">
    <div className="flex flex-wrap gap-1.5 border-b border-slate-200 pb-3">
      {categories.map((cat) => <button key={cat.id} type="button" onClick={() => setActiveCategory(cat.id as FinancialCategory)} className={`flex items-center gap-1.5 rounded-lg px-3 py-2 text-[11px] font-bold transition ${activeCategory === cat.id ? "bg-navy-900 text-white" : "border border-slate-200 bg-white text-slate-700 hover:bg-slate-50"}`}><span>{cat.label}</span>{cat.count && <span className={`rounded-full px-1.5 py-0.5 text-[9px] ${activeCategory === cat.id ? "bg-teal-400 text-navy-900" : "bg-slate-100 text-slate-600"}`}>{cat.count}</span>}</button>)}
    </div>

    {activeCategory === "personal" && <div className="space-y-4">
      <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5">
        <div className="mb-4 border-b border-slate-100 pb-3"><h3 className="text-lg font-extrabold text-navy-900">Personal Information &amp; Household</h3><p className="mt-0.5 text-xs text-slate-500">Update identity, profession, residence and household details.</p></div>
        <form noValidate onSubmit={personal.handleSubmit} className="space-y-4">
          <div className="grid gap-3 sm:grid-cols-2">
            <div><label htmlFor="p-fullName" className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Full Name</label><input id="p-fullName" type="text" value={personal.values.fullName} onChange={(e) => personal.handleChange({ name: "fullName", value: e.target.value })} onBlur={() => personal.handleBlur("fullName")} placeholder="Full Name" className={fieldClasses(Boolean(personal.errors.fullName))} />{personal.errors.fullName && <p className="mt-1 text-[11px] text-red-600">{personal.errors.fullName}</p>}</div>
            <div><label htmlFor="p-dateOfBirth" className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Date of Birth</label><input id="p-dateOfBirth" type="date" max={today} value={personal.values.dateOfBirth} onChange={(e) => personal.handleChange({ name: "dateOfBirth", value: e.target.value })} onBlur={() => personal.handleBlur("dateOfBirth")} className={fieldClasses(Boolean(personal.errors.dateOfBirth))} />{personal.errors.dateOfBirth && <p className="mt-1 text-[11px] text-red-600">{personal.errors.dateOfBirth}</p>}</div>
            <div><label htmlFor="p-gender" className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Gender</label><select id="p-gender" value={personal.values.gender} onChange={(e) => personal.handleChange({ name: "gender", value: e.target.value })} onBlur={() => personal.handleBlur("gender")} className={`${fieldClasses(Boolean(personal.errors.gender))} appearance-none`}><option value="">Select gender</option>{genderSelectOptions.map((opt) => <option key={opt.value} value={opt.value}>{opt.label}</option>)}</select></div>
            <div><label htmlFor="p-maritalStatus" className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Marital Status</label><select id="p-maritalStatus" value={personal.values.maritalStatus} onChange={(e) => personal.handleChange({ name: "maritalStatus", value: e.target.value })} onBlur={() => personal.handleBlur("maritalStatus")} className={`${fieldClasses(Boolean(personal.errors.maritalStatus))} appearance-none`}><option value="">Select marital status</option>{maritalStatusSelectOptions.map((opt) => <option key={opt.value} value={opt.value}>{opt.label}</option>)}</select></div>
            <div className="sm:col-span-2"><label htmlFor="p-mobileNumber" className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Mobile Number <span className="font-normal text-slate-400">(optional)</span></label><input id="p-mobileNumber" type="tel" value={personal.values.mobileNumber} onChange={(e) => personal.handleChange({ name: "mobileNumber", value: e.target.value })} onBlur={() => personal.handleBlur("mobileNumber")} placeholder="+91 98765 43210" className={fieldClasses(Boolean(personal.errors.mobileNumber))} /></div>
          </div>
          <div className="border-t border-slate-100 pt-3"><label htmlFor="p-occupation" className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Occupation / Profession</label><input id="p-occupation" type="text" value={personal.values.occupation} onChange={(e) => personal.handleChange({ name: "occupation", value: e.target.value })} onBlur={() => personal.handleBlur("occupation")} placeholder="e.g. Entrepreneur" className={fieldClasses(Boolean(personal.errors.occupation))} />{personal.errors.occupation && <p className="mt-1 text-[11px] text-red-600">{personal.errors.occupation}</p>}</div>
          <div className="grid gap-3 border-t border-slate-100 pt-3 sm:grid-cols-2">
            <div className="sm:col-span-2"><label htmlFor="p-address" className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Street Address</label><input id="p-address" type="text" value={personal.values.address} onChange={(e) => personal.handleChange({ name: "address", value: e.target.value })} onBlur={() => personal.handleBlur("address")} placeholder="Street address" className={fieldClasses(Boolean(personal.errors.address))} />{personal.errors.address && <p className="mt-1 text-[11px] text-red-600">{personal.errors.address}</p>}</div>
            <div><label htmlFor="p-city" className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">City</label><input id="p-city" type="text" value={personal.values.city} onChange={(e) => personal.handleChange({ name: "city", value: e.target.value })} onBlur={() => personal.handleBlur("city")} placeholder="City" className={fieldClasses(Boolean(personal.errors.city))} />{personal.errors.city && <p className="mt-1 text-[11px] text-red-600">{personal.errors.city}</p>}</div>
            <div><label htmlFor="p-state" className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">State / Province</label><input id="p-state" type="text" value={personal.values.state} onChange={(e) => personal.handleChange({ name: "state", value: e.target.value })} onBlur={() => personal.handleBlur("state")} placeholder="State or Province" className={fieldClasses(Boolean(personal.errors.state))} />{personal.errors.state && <p className="mt-1 text-[11px] text-red-600">{personal.errors.state}</p>}</div>
            <div className="sm:col-span-2"><label htmlFor="p-country" className="mb-1 block text-[11px] font-bold uppercase tracking-wider text-slate-500">Country</label><input id="p-country" type="text" value={personal.values.country} onChange={(e) => personal.handleChange({ name: "country", value: e.target.value })} onBlur={() => personal.handleBlur("country")} placeholder="Country" className={fieldClasses(Boolean(personal.errors.country))} />{personal.errors.country && <p className="mt-1 text-[11px] text-red-600">{personal.errors.country}</p>}</div>
          </div>
          <div className="flex items-center justify-between border-t border-slate-100 pt-3"><span className="text-[11px] text-slate-500">Changes save instantly.</span><button type="submit" className="rounded-lg bg-navy-900 px-4 py-2 text-[11px] font-bold uppercase tracking-wider text-white hover:bg-navy-800">Save Personal Info</button></div>
        </form>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5 space-y-4"><div><h3 className="text-lg font-extrabold text-navy-900">Family &amp; Dependents</h3><p className="mt-0.5 text-xs text-slate-500">People you support today or plan to support.</p></div><FamilySummary members={family.members} onEdit={family.startEditing} onRemove={family.removeMember} /><FamilyMemberForm member={family.draft} errors={family.errors} isEditing={Boolean(family.editingMemberId)} onChange={family.updateDraft} onSave={family.saveMember} onCancel={family.cancelEditing} /></div>
    </div>}
    {activeCategory === "income" && <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5 space-y-4"><div className="border-b border-slate-100 pb-3"><h3 className="text-lg font-extrabold text-navy-900">Income Sources</h3><p className="mt-0.5 text-xs text-slate-500">Manage salaries, business income and predictable inflows.</p></div><IncomeSummary sources={income.sources} onEdit={income.startEditing} onRemove={income.removeSource} /><IncomeSourceForm source={income.draft} errors={income.errors} isEditing={Boolean(income.editingSourceId)} onChange={income.updateDraft} onSave={income.saveSource} onCancel={income.cancelEditing} /></div>}
    {activeCategory === "expenses" && <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5 space-y-4"><div className="border-b border-slate-100 pb-3"><h3 className="text-lg font-extrabold text-navy-900">Expenses &amp; Lifestyle Costs</h3><p className="mt-0.5 text-xs text-slate-500">Manage living costs and discretionary spending.</p></div><ExpenseSummary expenses={expenses.expenses} onEdit={expenses.startEditing} onRemove={expenses.removeExpense} /><ExpenseCategoryForm expense={expenses.draft} errors={expenses.errors} isEditing={Boolean(expenses.editingExpenseId)} onChange={expenses.updateDraft} onSave={expenses.saveExpense} onCancel={expenses.cancelEditing} /></div>}
    {activeCategory === "assets" && <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5 space-y-4"><div className="border-b border-slate-100 pb-3"><h3 className="text-lg font-extrabold text-navy-900">Assets &amp; Investments</h3><p className="mt-0.5 text-xs text-slate-500">Savings, funds, equity, gold, real estate and reserves.</p></div><AssetSummary assets={assets.assets} onEdit={assets.startEditing} onRemove={assets.removeAsset} /><AssetForm asset={assets.draft} errors={assets.errors} isEditing={Boolean(assets.editingAssetId)} onChange={assets.updateDraft} onSave={assets.saveAsset} onCancel={assets.cancelEditing} /></div>}
    {activeCategory === "liabilities" && <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5 space-y-4"><div className="border-b border-slate-100 pb-3"><h3 className="text-lg font-extrabold text-navy-900">Liabilities &amp; Debt</h3><p className="mt-0.5 text-xs text-slate-500">Home loans, car loans, personal debt, credit lines and EMIs.</p></div><LiabilitySummary liabilities={liabilities.liabilities} onEdit={liabilities.startEditing} onRemove={liabilities.removeLiability} /><LiabilityForm liability={liabilities.draft} errors={liabilities.errors} isEditing={Boolean(liabilities.editingLiabilityId)} onChange={liabilities.updateDraft} onSave={liabilities.saveLiability} onCancel={liabilities.cancelEditing} /></div>}
    {activeCategory === "goals" && <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5 space-y-4"><div className="border-b border-slate-100 pb-3"><h3 className="text-lg font-extrabold text-navy-900">Goals &amp; Life Milestones</h3><p className="mt-0.5 text-xs text-slate-500">Target amounts, time horizons and planning assumptions.</p></div>{goals.goals.length > 0 && <GoalSummary goals={goals.goals} onEdit={goals.startEditing} onRemove={goals.removeGoal} />}{goals.isFormOpen ? <GoalForm goal={goals.draft} errors={goals.errors} isEditing={Boolean(goals.editingGoalId)} onChange={goals.updateDraft} onSave={goals.saveGoal} onCancel={goals.cancelEditing} /> : <button type="button" onClick={goals.startAdding} className="inline-flex items-center rounded-xl border border-teal-600 bg-white px-5 py-3 text-sm font-bold text-teal-700 hover:bg-teal-50">+ Add new goal</button>}</div>}
    {activeCategory === "insurance" && <InsuranceSection />}
  </div>;
}
