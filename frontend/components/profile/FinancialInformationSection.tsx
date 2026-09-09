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

import {
  genderSelectOptions,
  maritalStatusSelectOptions,
  type PersonalInformationField,
  type SelectOption,
} from "../../lib/onboarding/personal-information/model";

type FinancialCategory =
  | "personal"
  | "income"
  | "expenses"
  | "assets"
  | "liabilities"
  | "goals";

export default function FinancialInformationSection({
  initialCategory = "personal",
}: {
  initialCategory?: FinancialCategory;
}) {
  const [activeCategory, setActiveCategory] = useState<FinancialCategory>(initialCategory);

  // Hooks for each of the 6 structured categories
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
  ] as const;

  function fieldClasses(hasError = false) {
    return `form-field w-full rounded-xl border bg-white px-4 py-3 text-sm text-navy-900 placeholder:text-slate-400 focus:border-teal-500 focus:outline-none focus:ring-4 focus:ring-teal-50 ${
      hasError ? "border-red-300" : "border-slate-200"
    }`;
  }

  return (
    <div className="space-y-6">
      {/* Category Pills Bar */}
      <div className="flex flex-wrap gap-2 border-b border-slate-200 pb-4">
        {categories.map((cat) => {
          const isActive = activeCategory === cat.id;
          return (
            <button
              key={cat.id}
              type="button"
              onClick={() => setActiveCategory(cat.id as FinancialCategory)}
              className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-xs font-bold transition shadow-xs ${
                isActive
                  ? "bg-navy-900 text-white shadow-sm"
                  : "bg-white text-slate-700 hover:bg-slate-100 hover:text-navy-900 border border-slate-200/80"
              }`}
            >
              <span>{cat.label}</span>
              {cat.count && (
                <span
                  className={`rounded-full px-2 py-0.5 text-[10px] font-bold ${
                    isActive ? "bg-teal-400 text-navy-900" : "bg-slate-100 text-slate-600"
                  }`}
                >
                  {cat.count}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* ==================================================================== */}
      {/* 1. PERSONAL INFORMATION & HOUSEHOLD                                  */}
      {/* ==================================================================== */}
      {activeCategory === "personal" && (
        <div className="space-y-8">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
            <div className="mb-6 border-b border-slate-100 pb-5">
              <h3 className="text-xl font-extrabold text-navy-900">Personal Information &amp; Household</h3>
              <p className="mt-1 text-sm text-slate-500">
                Update your identity details, professional context, residence, and family members.
              </p>
            </div>

            <form noValidate onSubmit={personal.handleSubmit} className="space-y-6">
              {/* Identity Details */}
              <div className="grid gap-5 sm:grid-cols-2">
                <div>
                  <label htmlFor="p-fullName" className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">
                    Full Name
                  </label>
                  <input
                    id="p-fullName"
                    type="text"
                    value={personal.values.fullName}
                    onChange={(e) => personal.handleChange({ name: "fullName", value: e.target.value })}
                    onBlur={() => personal.handleBlur("fullName")}
                    placeholder="Full Name"
                    className={fieldClasses(Boolean(personal.errors.fullName))}
                  />
                  {personal.errors.fullName && <p className="mt-1 text-xs text-red-600">{personal.errors.fullName}</p>}
                </div>

                <div>
                  <label htmlFor="p-dateOfBirth" className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">
                    Date of Birth
                  </label>
                  <input
                    id="p-dateOfBirth"
                    type="date"
                    max={today}
                    value={personal.values.dateOfBirth}
                    onChange={(e) => personal.handleChange({ name: "dateOfBirth", value: e.target.value })}
                    onBlur={() => personal.handleBlur("dateOfBirth")}
                    className={fieldClasses(Boolean(personal.errors.dateOfBirth))}
                  />
                  {personal.errors.dateOfBirth && <p className="mt-1 text-xs text-red-600">{personal.errors.dateOfBirth}</p>}
                </div>

                <div>
                  <label htmlFor="p-gender" className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">
                    Gender
                  </label>
                  <select
                    id="p-gender"
                    value={personal.values.gender}
                    onChange={(e) => personal.handleChange({ name: "gender", value: e.target.value })}
                    onBlur={() => personal.handleBlur("gender")}
                    className={`${fieldClasses(Boolean(personal.errors.gender))} appearance-none`}
                  >
                    <option value="">Select gender</option>
                    {genderSelectOptions.map((opt) => (
                      <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="p-maritalStatus" className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">
                    Marital Status
                  </label>
                  <select
                    id="p-maritalStatus"
                    value={personal.values.maritalStatus}
                    onChange={(e) => personal.handleChange({ name: "maritalStatus", value: e.target.value })}
                    onBlur={() => personal.handleBlur("maritalStatus")}
                    className={`${fieldClasses(Boolean(personal.errors.maritalStatus))} appearance-none`}
                  >
                    <option value="">Select marital status</option>
                    {maritalStatusSelectOptions.map((opt) => (
                      <option key={opt.value} value={opt.value}>{opt.label}</option>
                    ))}
                  </select>
                </div>

                <div className="sm:col-span-2">
                  <label htmlFor="p-mobileNumber" className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">
                    Mobile Number <span className="font-normal text-slate-400">(optional)</span>
                  </label>
                  <input
                    id="p-mobileNumber"
                    type="tel"
                    value={personal.values.mobileNumber}
                    onChange={(e) => personal.handleChange({ name: "mobileNumber", value: e.target.value })}
                    onBlur={() => personal.handleBlur("mobileNumber")}
                    placeholder="+1 555 123 4567"
                    className={fieldClasses(Boolean(personal.errors.mobileNumber))}
                  />
                </div>
              </div>

              {/* Work & Profession */}
              <div className="pt-4 border-t border-slate-100">
                <label htmlFor="p-occupation" className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">
                  Occupation / Profession
                </label>
                <input
                  id="p-occupation"
                  type="text"
                  value={personal.values.occupation}
                  onChange={(e) => personal.handleChange({ name: "occupation", value: e.target.value })}
                  onBlur={() => personal.handleBlur("occupation")}
                  placeholder="e.g. Senior Software Architect"
                  className={fieldClasses(Boolean(personal.errors.occupation))}
                />
                {personal.errors.occupation && <p className="mt-1 text-xs text-red-600">{personal.errors.occupation}</p>}
              </div>

              {/* Residence */}
              <div className="pt-4 border-t border-slate-100 grid gap-5 sm:grid-cols-2">
                <div className="sm:col-span-2">
                  <label htmlFor="p-address" className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">
                    Street Address
                  </label>
                  <input
                    id="p-address"
                    type="text"
                    value={personal.values.address}
                    onChange={(e) => personal.handleChange({ name: "address", value: e.target.value })}
                    onBlur={() => personal.handleBlur("address")}
                    placeholder="123 Financial Ave, Suite 400"
                    className={fieldClasses(Boolean(personal.errors.address))}
                  />
                  {personal.errors.address && <p className="mt-1 text-xs text-red-600">{personal.errors.address}</p>}
                </div>

                <div>
                  <label htmlFor="p-city" className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">
                    City
                  </label>
                  <input
                    id="p-city"
                    type="text"
                    value={personal.values.city}
                    onChange={(e) => personal.handleChange({ name: "city", value: e.target.value })}
                    onBlur={() => personal.handleBlur("city")}
                    placeholder="City"
                    className={fieldClasses(Boolean(personal.errors.city))}
                  />
                  {personal.errors.city && <p className="mt-1 text-xs text-red-600">{personal.errors.city}</p>}
                </div>

                <div>
                  <label htmlFor="p-state" className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">
                    State / Province
                  </label>
                  <input
                    id="p-state"
                    type="text"
                    value={personal.values.state}
                    onChange={(e) => personal.handleChange({ name: "state", value: e.target.value })}
                    onBlur={() => personal.handleBlur("state")}
                    placeholder="State or Province"
                    className={fieldClasses(Boolean(personal.errors.state))}
                  />
                  {personal.errors.state && <p className="mt-1 text-xs text-red-600">{personal.errors.state}</p>}
                </div>

                <div className="sm:col-span-2">
                  <label htmlFor="p-country" className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-500">
                    Country
                  </label>
                  <input
                    id="p-country"
                    type="text"
                    value={personal.values.country}
                    onChange={(e) => personal.handleChange({ name: "country", value: e.target.value })}
                    onBlur={() => personal.handleBlur("country")}
                    placeholder="Country"
                    className={fieldClasses(Boolean(personal.errors.country))}
                  />
                  {personal.errors.country && <p className="mt-1 text-xs text-red-600">{personal.errors.country}</p>}
                </div>
              </div>

              {/* Submit Personal Info */}
              <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                <span className="text-xs text-slate-500 font-medium">Updates are instantly saved to your profile.</span>
                <button
                  type="submit"
                  className="rounded-xl bg-navy-900 px-6 py-2.5 text-xs font-bold uppercase tracking-wider text-white shadow-sm hover:bg-navy-800 transition"
                >
                  Save Personal Info
                </button>
              </div>
            </form>
          </div>

          {/* Family & Dependents Card */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8 space-y-6">
            <div>
              <h3 className="text-xl font-extrabold text-navy-900">Family &amp; Dependents</h3>
              <p className="mt-1 text-sm text-slate-500">
                People you support today or plan to support in your financial life.
              </p>
            </div>

            <FamilySummary
              members={family.members}
              onEdit={family.startEditing}
              onRemove={family.removeMember}
            />

            <FamilyMemberForm
              member={family.draft}
              errors={family.errors}
              isEditing={Boolean(family.editingMemberId)}
              onChange={family.updateDraft}
              onSave={family.saveMember}
              onCancel={family.cancelEditing}
            />
          </div>
        </div>
      )}

      {/* ==================================================================== */}
      {/* 2. INCOME                                                            */}
      {/* ==================================================================== */}
      {activeCategory === "income" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8 space-y-6">
          <div className="border-b border-slate-100 pb-5">
            <h3 className="text-xl font-extrabold text-navy-900">Income Sources</h3>
            <p className="mt-1 text-sm text-slate-500">
              Manage your salaries, business income, investments, and predictable inflows.
            </p>
          </div>

          <IncomeSummary
            sources={income.sources}
            onEdit={income.startEditing}
            onRemove={income.removeSource}
          />

          <IncomeSourceForm
            source={income.draft}
            errors={income.errors}
            isEditing={Boolean(income.editingSourceId)}
            onChange={income.updateDraft}
            onSave={income.saveSource}
            onCancel={income.cancelEditing}
          />
        </div>
      )}

      {/* ==================================================================== */}
      {/* 3. EXPENSES                                                          */}
      {/* ==================================================================== */}
      {activeCategory === "expenses" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8 space-y-6">
          <div className="border-b border-slate-100 pb-5">
            <h3 className="text-xl font-extrabold text-navy-900">Expenses &amp; Lifestyle Costs</h3>
            <p className="mt-1 text-sm text-slate-500">
              Manage living costs, utilities, discretionary lifestyle spending, and family expenses.
            </p>
          </div>

          <ExpenseSummary
            expenses={expenses.expenses}
            onEdit={expenses.startEditing}
            onRemove={expenses.removeExpense}
          />

          <ExpenseCategoryForm
            expense={expenses.draft}
            errors={expenses.errors}
            isEditing={Boolean(expenses.editingExpenseId)}
            onChange={expenses.updateDraft}
            onSave={expenses.saveExpense}
            onCancel={expenses.cancelEditing}
          />
        </div>
      )}

      {/* ==================================================================== */}
      {/* 4. ASSETS                                                            */}
      {/* ==================================================================== */}
      {activeCategory === "assets" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8 space-y-6">
          <div className="border-b border-slate-100 pb-5">
            <h3 className="text-xl font-extrabold text-navy-900">Assets &amp; Investments</h3>
            <p className="mt-1 text-sm text-slate-500">
              Current savings, mutual funds, equity portfolios, gold, real estate, and emergency reserves.
            </p>
          </div>

          <AssetSummary
            assets={assets.assets}
            onEdit={assets.startEditing}
            onRemove={assets.removeAsset}
          />

          <AssetForm
            asset={assets.draft}
            errors={assets.errors}
            isEditing={Boolean(assets.editingAssetId)}
            onChange={assets.updateDraft}
            onSave={assets.saveAsset}
            onCancel={assets.cancelEditing}
          />
        </div>
      )}

      {/* ==================================================================== */}
      {/* 5. LIABILITIES                                                       */}
      {/* ==================================================================== */}
      {activeCategory === "liabilities" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8 space-y-6">
          <div className="border-b border-slate-100 pb-5">
            <h3 className="text-xl font-extrabold text-navy-900">Liabilities &amp; Debt</h3>
            <p className="mt-1 text-sm text-slate-500">
              Outstanding home loans, car loans, personal debts, credit lines, and EMIs.
            </p>
          </div>

          <LiabilitySummary
            liabilities={liabilities.liabilities}
            onEdit={liabilities.startEditing}
            onRemove={liabilities.removeLiability}
          />

          <LiabilityForm
            liability={liabilities.draft}
            errors={liabilities.errors}
            isEditing={Boolean(liabilities.editingLiabilityId)}
            onChange={liabilities.updateDraft}
            onSave={liabilities.saveLiability}
            onCancel={liabilities.cancelEditing}
          />
        </div>
      )}

      {/* ==================================================================== */}
      {/* 6. GOALS                                                             */}
      {/* ==================================================================== */}
      {activeCategory === "goals" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8 space-y-6">
          <div className="border-b border-slate-100 pb-5">
            <h3 className="text-xl font-extrabold text-navy-900">Goals &amp; Life Milestones</h3>
            <p className="mt-1 text-sm text-slate-500">
              Target amounts, time horizons, priorities, and flexible assumptions for your financial future.
            </p>
          </div>

          {(goals.goals.length > 0 || !goals.isFormOpen) && (
            <GoalSummary
              goals={goals.goals}
              onEdit={goals.startEditing}
              onRemove={goals.removeGoal}
            />
          )}

          {goals.isFormOpen ? (
            <GoalForm
              goal={goals.draft}
              errors={goals.errors}
              isEditing={Boolean(goals.editingGoalId)}
              onChange={goals.updateDraft}
              onSave={goals.saveGoal}
              onCancel={goals.cancelEditing}
            />
          ) : (
            <div className="flex justify-start">
              <button
                type="button"
                onClick={goals.startAdding}
                className="inline-flex items-center justify-center gap-2 rounded-xl border border-teal-600 bg-white px-5 py-3 text-sm font-bold text-teal-700 shadow-sm transition hover:bg-teal-50 focus:outline-none focus:ring-4 focus:ring-teal-100"
              >
                <span aria-hidden="true" className="text-base font-extrabold">+</span>
                Add Goal
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
