"use client";

import { useState, useMemo, useEffect, useCallback } from "react";
import Link from "next/link";
import InvestorHeader from "../../../components/InvestorHeader";
import {
  loadBudgetData,
  saveBudgetLimits,
  subscribeToBudgetChanges,
  type BudgetItem,
  type BudgetData,
  type NeedWantClassification,
} from "../../../lib/api/budgeting";

// ============================================================================
// HELPER
// ============================================================================

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(amount);
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export default function InvestorBudgetingPage() {
  // Period Selector: Monthly vs Annual
  const [period, setPeriod] = useState<"Monthly" | "Annual">("Monthly");

  // Multiplier for display toggle (presentation only)
  const multiplier = period === "Annual" ? 12 : 1;

  // Data loading states
  const [budgetData, setBudgetData] = useState<BudgetData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  // Local Budget Editing State
  const [isEditingBudget, setIsEditingBudget] = useState(false);
  const [editDraftItems, setEditDraftItems] = useState<BudgetItem[]>([]);
  const [editSuccessNotice, setEditSuccessNotice] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  // Budget Targets Controls (UI state only)
  const [targetType, setTargetType] = useState<"percentage" | "amount">("percentage");
  const [savingsTargetInput, setSavingsTargetInput] = useState("30");
  const [desiredSurplusInput, setDesiredSurplusInput] = useState("65000");

  // ========================================================================
  // DATA FETCHING
  // ========================================================================

  const fetchData = useCallback(async () => {
    try {
      setLoadError(null);
      const data = await loadBudgetData();
      if (data) {
        setBudgetData(data);
      } else {
        setBudgetData(null);
      }
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Failed to load budget data";
      setLoadError(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Initial load
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Realtime subscription
  useEffect(() => {
    if (!budgetData?.planningUnitId) return;
    const cleanup = subscribeToBudgetChanges(budgetData.planningUnitId, () => {
      fetchData();
    });
    return cleanup;
  }, [budgetData?.planningUnitId, fetchData]);

  // ========================================================================
  // EDITING HANDLERS
  // ========================================================================

  const expensesList = budgetData?.items ?? [];

  const handleStartEditing = () => {
    setEditDraftItems([...expensesList]);
    setIsEditingBudget(true);
  };

  const handleEditCategoryChange = (
    id: string,
    field: "budgetMonthly" | "classification",
    value: string | NeedWantClassification
  ) => {
    setEditDraftItems((prev) =>
      prev.map((item) => {
        if (item.id !== id) return item;
        if (field === "budgetMonthly") {
          return { ...item, budgetMonthly: Number(value) || 0 };
        }
        if (field === "classification") {
          return { ...item, classification: value as NeedWantClassification };
        }
        return item;
      })
    );
  };

  const handleSaveBudgetEdits = async () => {
    if (!budgetData?.planningUnitId) return;
    setIsSaving(true);
    try {
      await saveBudgetLimits(
        budgetData.planningUnitId,
        editDraftItems.map((item) => ({
          category: item.category,
          classification: item.classification,
          budgetMonthly: item.budgetMonthly,
        }))
      );
      setIsEditingBudget(false);
      setEditSuccessNotice(true);
      setTimeout(() => setEditSuccessNotice(false), 4000);
      // Refresh data after save
      await fetchData();
    } catch (err) {
      console.error("Failed to save budget limits:", err);
    } finally {
      setIsSaving(false);
    }
  };

  const handleResetBudget = () => {
    setEditDraftItems([...expensesList]);
    setIsEditingBudget(false);
  };

  // Need vs Want calculations based on real items
  const { needsTotal, wantsTotal, needsPercent, wantsPercent } = useMemo(() => {
    const items = isEditingBudget ? editDraftItems : expensesList;
    let n = 0;
    let w = 0;
    items.forEach((item) => {
      if (item.classification === "Need") n += item.actualMonthly;
      else w += item.actualMonthly;
    });
    const total = n + w;
    return {
      needsTotal: n * multiplier,
      wantsTotal: w * multiplier,
      needsPercent: total > 0 ? Math.round((n / total) * 100) : 0,
      wantsPercent: total > 0 ? Math.round((w / total) * 100) : 0,
    };
  }, [expensesList, editDraftItems, isEditingBudget, multiplier]);

  // ==========================================================================
  // RENDER: LOADING STATE
  // ==========================================================================
  if (isLoading) {
    return (
      <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10" aria-busy="true">
        <div className="mx-auto max-w-6xl space-y-6">
          <div className="h-8 w-64 animate-pulse rounded-lg bg-slate-200" />
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            <div className="h-28 animate-pulse rounded-2xl bg-white shadow-sm" />
            <div className="h-28 animate-pulse rounded-2xl bg-white shadow-sm" />
            <div className="h-28 animate-pulse rounded-2xl bg-white shadow-sm" />
            <div className="h-28 animate-pulse rounded-2xl bg-white shadow-sm" />
          </div>
          <div className="h-32 animate-pulse rounded-3xl bg-white shadow-sm" />
          <div className="h-72 animate-pulse rounded-3xl bg-white shadow-sm" />
        </div>
      </main>
    );
  }

  // ==========================================================================
  // RENDER: ERROR STATE
  // ==========================================================================
  if (loadError) {
    return (
      <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
        <div className="mx-auto max-w-2xl rounded-3xl border border-red-200 bg-white p-8 text-center shadow-sm">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-red-50 text-red-600">
            <svg className="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h2 className="mt-4 text-xl font-bold text-slate-900">Unable to Load Budget Data</h2>
          <p className="mt-2 text-sm text-slate-600">
            We encountered a temporary issue while fetching your cash flow and expense metrics. Please try again.
          </p>
          <button
            onClick={() => { setIsLoading(true); fetchData(); }}
            className="mt-6 inline-flex items-center rounded-xl bg-navy-900 px-6 py-2.5 text-sm font-semibold text-white transition hover:bg-navy-800"
          >
            Retry Loading Budget
          </button>
        </div>
      </main>
    );
  }

  // ==========================================================================
  // RENDER: EMPTY STATE (no income, no expenses, no data)
  // ==========================================================================
  if (!budgetData || (budgetData.items.length === 0 && budgetData.overview.totalIncomeMonthly === 0)) {
    return (
      <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
        <div className="mx-auto max-w-2xl rounded-3xl border border-slate-200 bg-white p-10 text-center shadow-sm">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-teal-50 text-teal-700">
            <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="mt-4 text-2xl font-black text-slate-950">No Budget Configured Yet</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-600 max-w-md mx-auto">
            Set up your expense limits and target cash flows to track where your money goes, prevent lifestyle creep, and protect your investments.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            <Link
              href="/investor/onboarding/expenses"
              className="inline-flex items-center rounded-xl bg-teal-700 px-6 py-3 text-sm font-bold text-white transition hover:bg-teal-800"
            >
              Add Expenses & Income →
            </Link>
            <Link
              href="/investor/financial-state"
              className="inline-flex items-center rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
            >
              Review Financial State
            </Link>
          </div>
        </div>
      </main>
    );
  }

  // ==========================================================================
  // RENDER: NORMAL POPULATED STATE
  // ==========================================================================
  const overview = budgetData.overview;
  const totalIncome = overview.totalIncomeMonthly * multiplier;
  const totalExpenses = overview.totalExpensesMonthly * multiplier;
  const surplus = overview.surplusMonthly * multiplier;
  const savingsTarget = overview.savingsTargetMonthly * multiplier;
  const expensePercent = totalIncome > 0 ? Math.round((totalExpenses / totalIncome) * 100) : 0;
  const displayItems = isEditingBudget ? editDraftItems : expensesList;

  return (
    <main className="min-h-screen bg-[#f6f8fb] text-slate-900 pb-20">
      <InvestorHeader
        eyebrow="Cash Flow Management"
        title="Budgeting"
        description="Manage your expenses, monitor variances, and plan future cash flow targets."
      >
        <div className="inline-flex rounded-xl bg-slate-100 p-1 border border-slate-200">
          <button
            type="button"
            onClick={() => setPeriod("Monthly")}
            className={`rounded-lg px-3.5 py-1.5 text-xs font-bold transition ${
              period === "Monthly"
                ? "bg-white text-navy-900 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Monthly
          </button>
          <button
            type="button"
            onClick={() => setPeriod("Annual")}
            className={`rounded-lg px-3.5 py-1.5 text-xs font-bold transition ${
              period === "Annual"
                ? "bg-white text-navy-900 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Annual
          </button>
        </div>
      </InvestorHeader>

      {/* Supporting Banner */}
      <div className="border-b border-teal-200 bg-teal-50/60 px-6 py-2.5 text-xs text-teal-900">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4">
          <p className="flex items-center gap-2">
            <span className="flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-teal-200 text-teal-800 font-bold text-[10px]">
              ✓
            </span>
            <span>
              Manage your expenses, monitor budget vs actual variances, and plan future cash flow targets.
            </span>
          </p>
          <span className="shrink-0 font-bold uppercase tracking-wider text-[10px] text-teal-800 bg-teal-100 px-2 py-0.5 rounded">
            Live Data
          </span>
        </div>
      </div>

      <div className="mx-auto max-w-6xl px-6 pt-8 lg:px-8 space-y-8">
        {/* Success Notice after editing */}
        {editSuccessNotice && (
          <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-xs font-semibold text-emerald-800 flex items-center justify-between">
            <span>✓ Budget targets saved successfully.</span>
            <button onClick={() => setEditSuccessNotice(false)} className="text-emerald-900 font-bold">✕</button>
          </div>
        )}

        {/* ================================================================== */}
        {/* 2. CASH FLOW OVERVIEW                                              */}
        {/* ================================================================== */}
        <section aria-labelledby="cashflow-overview-title" className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 id="cashflow-overview-title" className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Cash Flow Overview ({period})
            </h2>
            <span className="text-xs font-semibold text-slate-500">
              Period: {period === "Monthly" ? "Current Month" : "Current Year"}
            </span>
          </div>

          {/* 4 Summary Cards */}
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {/* Total Income */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between text-xs font-bold text-slate-400 uppercase tracking-wider">
                <span>Total Income</span>
                <span className="rounded-md bg-emerald-50 px-2 py-0.5 text-emerald-700 text-[10px]">Inflow</span>
              </div>
              <p className="mt-3 text-2xl sm:text-3xl font-black text-slate-950">
                {formatCurrency(totalIncome)}
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Regular salary &amp; business income
              </p>
            </div>

            {/* Total Expenses */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between text-xs font-bold text-slate-400 uppercase tracking-wider">
                <span>Total Expenses</span>
                <span className="rounded-md bg-rose-50 px-2 py-0.5 text-rose-700 text-[10px]">Outflow</span>
              </div>
              <p className="mt-3 text-2xl sm:text-3xl font-black text-slate-950">
                {formatCurrency(totalExpenses)}
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Needs &amp; wants combined
              </p>
            </div>

            {/* Surplus / Deficit */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between text-xs font-bold text-slate-400 uppercase tracking-wider">
                <span>Surplus / Deficit</span>
                <span className="rounded-md bg-teal-50 px-2 py-0.5 text-teal-700 text-[10px]">Net Flow</span>
              </div>
              <p className={`mt-3 text-2xl sm:text-3xl font-black ${surplus >= 0 ? "text-teal-700" : "text-rose-700"}`}>
                {formatCurrency(surplus)}
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Net available investable buffer
              </p>
            </div>

            {/* Savings Target */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between text-xs font-bold text-slate-400 uppercase tracking-wider">
                <span>Savings Target</span>
                <span className="rounded-md bg-indigo-50 px-2 py-0.5 text-indigo-700 text-[10px]">{overview.savingsTargetPercentage}% Target</span>
              </div>
              <p className="mt-3 text-2xl sm:text-3xl font-black text-slate-950">
                {formatCurrency(savingsTarget)}
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Target monthly wealth goal allocation
              </p>
            </div>
          </div>

          {/* Visual Cash Flow Representation: Income → Expenses → Surplus/Deficit */}
          <div className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-8 shadow-sm">
            <h3 className="text-xs font-bold uppercase tracking-wider text-teal-700">
              Visual Cash Flow Pipeline
            </h3>
            <p className="mt-1 text-sm font-semibold text-slate-900">
              Income → Expenses → Investable Surplus
            </p>

            <div className="mt-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
              {/* Step 1: Income */}
              <div className="flex-1 rounded-2xl bg-emerald-50/70 border border-emerald-200 p-5">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-emerald-800">1. Total Inflow</span>
                  <span className="text-base">💰</span>
                </div>
                <p className="mt-2 text-xl font-black text-emerald-950">{formatCurrency(totalIncome)}</p>
                <p className="mt-1 text-xs text-emerald-700">Starting base</p>
              </div>

              {/* Arrow */}
              <div className="hidden md:flex items-center justify-center text-slate-400 font-bold text-xl px-2">
                →
              </div>
              <div className="flex md:hidden items-center justify-center text-slate-400 font-bold text-lg">
                ↓
              </div>

              {/* Step 2: Expenses */}
              <div className="flex-1 rounded-2xl bg-rose-50/70 border border-rose-200 p-5">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-rose-800">2. Outflow (Expenses)</span>
                  <span className="text-base">📉</span>
                </div>
                <p className="mt-2 text-xl font-black text-rose-950">- {formatCurrency(totalExpenses)}</p>
                <p className="mt-1 text-xs text-rose-700">{expensePercent}% of total income</p>
              </div>

              {/* Arrow */}
              <div className="hidden md:flex items-center justify-center text-slate-400 font-bold text-xl px-2">
                →
              </div>
              <div className="flex md:hidden items-center justify-center text-slate-400 font-bold text-lg">
                ↓
              </div>

              {/* Step 3: Surplus */}
              <div className="flex-1 rounded-2xl bg-teal-50/80 border border-teal-200 p-5">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-teal-800">3. Net Surplus</span>
                  <span className="text-base">🎯</span>
                </div>
                <p className="mt-2 text-xl font-black text-teal-950">{surplus >= 0 ? "+" : ""} {formatCurrency(surplus)}</p>
                <p className="mt-1 text-xs text-teal-700">Available to fund goals</p>
              </div>
            </div>
          </div>
        </section>

        {/* ================================================================== */}
        {/* 3. BUDGET VS ACTUAL                                                */}
        {/* ================================================================== */}
        <section aria-labelledby="budget-actual-title" className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-8 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-100 pb-5">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
                Variance Analysis
              </span>
              <h2 id="budget-actual-title" className="mt-1 text-xl font-extrabold text-slate-950 sm:text-2xl">
                Budget vs Actual
              </h2>
              <p className="mt-1 text-xs text-slate-500">
                Compare allocated budgets against actual outflows for each expense category.
              </p>
            </div>

            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => isEditingBudget ? setIsEditingBudget(false) : handleStartEditing()}
                className="inline-flex items-center rounded-xl bg-navy-900 px-4 py-2 text-xs font-bold text-white transition hover:bg-navy-800"
              >
                {isEditingBudget ? "Close Budget Editor" : "✏️ Edit Budget Limits"}
              </button>
            </div>
          </div>

          {/* Category Table */}
          <div className="mt-6 overflow-x-auto">
            <table className="w-full text-left border-collapse min-w-[620px]">
              <thead>
                <tr className="border-b border-slate-200 text-xs font-bold uppercase tracking-wider text-slate-400">
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Classification</th>
                  <th className="py-3 px-4 text-right">Budget</th>
                  <th className="py-3 px-4 text-right">Actual</th>
                  <th className="py-3 px-4 text-right">Variance</th>
                  <th className="py-3 px-4 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-sm">
                {displayItems.map((item) => {
                  const bVal = item.budgetMonthly * multiplier;
                  const aVal = item.actualMonthly * multiplier;
                  const vVal = (item.actualMonthly - item.budgetMonthly) * multiplier;

                  const itemStatus = (() => {
                    if (item.budgetMonthly === 0) return aVal === 0 ? "On Track" : "Over Budget";
                    const threshold = item.budgetMonthly * 0.05;
                    const diff = item.actualMonthly - item.budgetMonthly;
                    if (diff > threshold) return "Over Budget";
                    if (diff < -threshold) return "Under Budget";
                    return "On Track";
                  })();

                  return (
                    <tr key={item.id} className="hover:bg-slate-50/60 transition-colors">
                      {/* Category */}
                      <td className="py-4 px-4 font-bold text-slate-900">
                        <div className="flex items-center gap-2.5">
                          <span className="text-base">{item.icon}</span>
                          <span>{item.category}</span>
                        </div>
                      </td>

                      {/* Classification */}
                      <td className="py-4 px-4">
                        <span
                          className={`inline-flex items-center rounded-md px-2 py-0.5 text-xs font-bold ${
                            item.classification === "Need"
                              ? "bg-blue-50 text-blue-700"
                              : "bg-purple-50 text-purple-700"
                          }`}
                        >
                          {item.classification}
                        </span>
                      </td>

                      {/* Budget */}
                      <td className="py-4 px-4 text-right font-semibold text-slate-700">
                        {bVal > 0 ? formatCurrency(bVal) : "—"}
                      </td>

                      {/* Actual */}
                      <td className="py-4 px-4 text-right font-black text-slate-950">
                        {formatCurrency(aVal)}
                      </td>

                      {/* Variance */}
                      <td
                        className={`py-4 px-4 text-right font-bold ${
                          bVal === 0 ? "text-slate-400" : vVal > 0 ? "text-rose-600" : vVal < 0 ? "text-emerald-600" : "text-slate-500"
                        }`}
                      >
                        {bVal === 0 ? "—" : vVal > 0 ? `+${formatCurrency(vVal)}` : vVal < 0 ? formatCurrency(vVal) : "₹0"}
                      </td>

                      {/* Status */}
                      <td className="py-4 px-4 text-center">
                        <span
                          className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-bold ${
                            itemStatus === "On Track"
                              ? "bg-slate-100 text-slate-700"
                              : itemStatus === "Under Budget"
                              ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                              : "bg-rose-50 text-rose-700 border border-rose-200"
                          }`}
                        >
                          {itemStatus}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>

        {/* ================================================================== */}
        {/* 6. BUDGET EDITING UI (Inline drawer / interactive controls)        */}
        {/* ================================================================== */}
        {isEditingBudget && (
          <section className="rounded-3xl border-2 border-teal-600 bg-white p-6 lg:p-8 shadow-card">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-slate-100 pb-4">
              <div>
                <span className="rounded bg-teal-100 px-2 py-0.5 text-xs font-bold text-teal-800">
                  Set Budget Limits
                </span>
                <h3 className="mt-2 text-lg font-black text-slate-950">
                  Edit Category Budget Limits &amp; Classifications
                </h3>
                <p className="mt-0.5 text-xs text-slate-500">
                  Adjust monthly budget targets and designate whether each expense is a Need or a Want.
                </p>
              </div>

              <div className="mt-3 sm:mt-0 flex items-center gap-2">
                <button
                  type="button"
                  onClick={handleResetBudget}
                  className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs font-bold text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleSaveBudgetEdits}
                  disabled={isSaving}
                  className="rounded-xl bg-teal-700 px-4 py-2 text-xs font-bold text-white hover:bg-teal-800 disabled:opacity-50"
                >
                  {isSaving ? "Saving…" : "Save Budget Limits"}
                </button>
              </div>
            </div>

            <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {editDraftItems.map((item) => (
                <div key={item.id} className="rounded-2xl bg-slate-50 p-4 border border-slate-200">
                  <div className="flex items-center gap-2 font-bold text-sm text-slate-900">
                    <span>{item.icon}</span>
                    <span>{item.category}</span>
                  </div>

                  <div className="mt-3">
                    <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-400">
                      Monthly Budget (₹)
                    </label>
                    <input
                      type="number"
                      value={item.budgetMonthly}
                      onChange={(e) => handleEditCategoryChange(item.id, "budgetMonthly", e.target.value)}
                      className="mt-1 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm font-bold text-slate-900 outline-none focus:border-teal-600"
                    />
                  </div>

                  <div className="mt-3">
                    <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-400">
                      Classification
                    </label>
                    <div className="mt-1 flex rounded-lg bg-white border border-slate-200 p-0.5">
                      <button
                        type="button"
                        onClick={() => handleEditCategoryChange(item.id, "classification", "Need")}
                        className={`flex-1 rounded py-1 text-xs font-bold transition ${
                          item.classification === "Need"
                            ? "bg-blue-600 text-white"
                            : "text-slate-500 hover:text-slate-900"
                        }`}
                      >
                        Need
                      </button>
                      <button
                        type="button"
                        onClick={() => handleEditCategoryChange(item.id, "classification", "Want")}
                        className={`flex-1 rounded py-1 text-xs font-bold transition ${
                          item.classification === "Want"
                            ? "bg-purple-600 text-white"
                            : "text-slate-500 hover:text-slate-900"
                        }`}
                      >
                        Want
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* ================================================================== */}
        {/* 4. EXPENSE BREAKDOWN (Category Visualization + Need vs Want)       */}
        {/* ================================================================== */}
        <section aria-labelledby="expense-breakdown-title" className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          {/* Category Breakdown Visualization */}
          <div className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-8 shadow-sm">
            <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
              Proportional Allocation
            </span>
            <h3 id="expense-breakdown-title" className="mt-1 text-xl font-extrabold text-slate-950">
              Expense Category Breakdown
            </h3>
            <p className="mt-1 text-xs text-slate-500">
              Relative share of total actual monthly expenditures.
            </p>

            <div className="mt-6 space-y-4">
              {displayItems.map((item) => (
                <div key={item.id} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs font-semibold">
                    <span className="flex items-center gap-1.5 text-slate-800">
                      <span>{item.icon}</span>
                      <span>{item.category}</span>
                    </span>
                    <span className="font-bold text-slate-950">
                      {formatCurrency(item.actualMonthly * multiplier)} ({item.percentageOfBudget}%)
                    </span>
                  </div>
                  {/* Progress Bar */}
                  <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        item.classification === "Need" ? "bg-teal-600" : "bg-purple-600"
                      }`}
                      style={{ width: `${Math.min(item.percentageOfBudget * 2.2, 100)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Need vs Want Summary */}
          <div className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-8 shadow-sm flex flex-col justify-between">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
                Classification Framework
              </span>
              <h3 className="mt-1 text-xl font-extrabold text-slate-950">
                Need vs Want Summary
              </h3>
              <p className="mt-1 text-xs text-slate-500">
                Guideline rule-of-thumb: 50% Needs, 30% Wants, 20% Savings.
              </p>

              <div className="mt-6 grid grid-cols-2 gap-4">
                {/* Needs Box */}
                <div className="rounded-2xl bg-blue-50/70 border border-blue-200 p-5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold uppercase tracking-wider text-blue-900">Needs</span>
                    <span className="rounded bg-blue-200 px-1.5 py-0.5 text-[10px] font-bold text-blue-900">Essential</span>
                  </div>
                  <p className="mt-2 text-2xl font-black text-blue-950">
                    {formatCurrency(needsTotal)}
                  </p>
                  <p className="mt-1 text-xs text-blue-700">
                    Housing, utilities, groceries, basics
                  </p>
                </div>

                {/* Wants Box */}
                <div className="rounded-2xl bg-purple-50/70 border border-purple-200 p-5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold uppercase tracking-wider text-purple-900">Wants</span>
                    <span className="rounded bg-purple-200 px-1.5 py-0.5 text-[10px] font-bold text-purple-900">Discretionary</span>
                  </div>
                  <p className="mt-2 text-2xl font-black text-purple-950">
                    {formatCurrency(wantsTotal)}
                  </p>
                  <p className="mt-1 text-xs text-purple-700">
                    Dining, entertainment, lifestyle
                  </p>
                </div>
              </div>

              {/* Combined Progress Bar */}
              <div className="mt-6 space-y-2">
                <div className="flex justify-between text-xs font-bold text-slate-600">
                  <span>Needs ({needsPercent}%)</span>
                  <span>Wants ({wantsPercent}%)</span>
                </div>
                <div className="flex h-3 w-full rounded-full overflow-hidden bg-slate-100">
                  <div className="bg-blue-600" style={{ width: `${needsPercent}%` }} />
                  <div className="bg-purple-600" style={{ width: `${wantsPercent}%` }} />
                </div>
              </div>
            </div>

            <div className="mt-6 rounded-2xl bg-slate-50 p-4 border border-slate-100 text-xs text-slate-600 leading-relaxed">
              💡 <strong>Insight:</strong> {wantsTotal > 0 ? `Trimming wants by just 10% can liberate an additional ${formatCurrency(Math.round(wantsTotal * 0.1 / multiplier))} monthly directly into your critical goal corpus.` : "Add expense data to see optimization insights."}
            </div>
          </div>
        </section>

        {/* ================================================================== */}
        {/* 5. BUDGET TARGETS (Interactive UI Controls Only)                   */}
        {/* ================================================================== */}
        <section aria-labelledby="budget-targets-title" className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-8 shadow-sm">
          <div className="border-b border-slate-100 pb-5">
            <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
              Forward Planning
            </span>
            <h2 id="budget-targets-title" className="mt-1 text-xl font-extrabold text-slate-950 sm:text-2xl">
              Future Cash-Flow &amp; Budget Targets
            </h2>
            <p className="mt-1 text-xs text-slate-500">
              Set desired targets for monthly savings allocation and reserve surplus buffers.
            </p>
          </div>

          <div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-2">
            {/* Target 1: Desired Savings Target */}
            <div className="rounded-2xl bg-slate-50/80 p-6 border border-slate-200">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-bold text-slate-900">
                  Desired Savings Target
                </h3>
                <div className="inline-flex rounded-lg bg-white border border-slate-200 p-0.5 text-xs font-bold">
                  <button
                    type="button"
                    onClick={() => setTargetType("percentage")}
                    className={`px-2.5 py-1 rounded transition ${
                      targetType === "percentage" ? "bg-navy-900 text-white" : "text-slate-600"
                    }`}
                  >
                    % Percentage
                  </button>
                  <button
                    type="button"
                    onClick={() => setTargetType("amount")}
                    className={`px-2.5 py-1 rounded transition ${
                      targetType === "amount" ? "bg-navy-900 text-white" : "text-slate-600"
                    }`}
                  >
                    ₹ Amount
                  </button>
                </div>
              </div>

              <div className="mt-4">
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400">
                  {targetType === "percentage" ? "Target Savings (% of Income)" : "Target Savings Amount (₹)"}
                </label>
                <div className="mt-1.5 flex items-center gap-3">
                  <input
                    type="number"
                    value={savingsTargetInput}
                    onChange={(e) => setSavingsTargetInput(e.target.value)}
                    className="w-40 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-lg font-black text-slate-900 outline-none focus:border-teal-600"
                  />
                  <span className="text-sm font-semibold text-slate-600">
                    {targetType === "percentage" ? "% of monthly income" : "per month"}
                  </span>
                </div>
                <p className="mt-2 text-xs text-slate-500">
                  Recommended benchmark: 20% – 35% of post-tax income.
                </p>
              </div>
            </div>

            {/* Target 2: Desired Surplus Target */}
            <div className="rounded-2xl bg-slate-50/80 p-6 border border-slate-200">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-bold text-slate-900">
                  Desired Surplus Target
                </h3>
                <span className="rounded bg-teal-100 px-2 py-0.5 text-[10px] font-bold text-teal-800">
                  Reserve Goal
                </span>
              </div>

              <div className="mt-4">
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400">
                  Desired Monthly Surplus Buffer (₹)
                </label>
                <div className="mt-1.5 flex items-center gap-3">
                  <input
                    type="number"
                    value={desiredSurplusInput}
                    onChange={(e) => setDesiredSurplusInput(e.target.value)}
                    className="w-44 rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-lg font-black text-slate-950 outline-none focus:border-teal-600"
                  />
                  <span className="text-sm font-semibold text-slate-600">
                    per month
                  </span>
                </div>
                <p className="mt-2 text-xs text-slate-500">
                  Uncommitted surplus reserved for emergency buffers and lump-sum investments.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Footer Navigation Link to Strategy Builder */}
        <div className="rounded-3xl border border-slate-200 bg-white p-6 text-center shadow-xs">
          <p className="text-xs text-slate-500">
            Finished reviewing your cash flows? Proceed to design investment pathways for your goals.
          </p>
          <div className="mt-3 flex justify-center gap-4">
            <Link
              href="/investor/strategy-builder"
              className="inline-flex items-center rounded-xl bg-navy-900 px-6 py-2.5 text-xs font-bold text-white transition hover:bg-navy-800"
            >
              Open Strategy Builder →
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
