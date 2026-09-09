"use client";

import Link from "next/link";
import { useEffect, useState, useMemo } from "react";
import { InvestorProfileMenu } from "../../../components/InvestorProfileMenu";
import { supabase } from "../../../lib/supabase";

// ============================================================================
// DATA TYPES & INTERFACES (Preserved from existing contract)
// ============================================================================

type Metric = {
  value: number | null;
  available: boolean;
  reason: string | null;
};

type BreakdownItem = {
  type: string;
  monthly: number;
  annual: number;
};

type AssetBreakdownItem = {
  asset_id: string;
  name: string;
  current_value: number;
  ownership_applied: number;
  liquidity: string | null;
};

type LiabilityBreakdownItem = {
  liability_id: string;
  name: string;
  outstanding_amount: number;
  responsibility_applied: number;
  classification: string | null;
};

type CommitmentBreakdownItem = {
  commitment_id: string;
  name: string;
  amount: number | string;
};

type FinancialStateResponse = {
  scope: string;
  planning_unit_id: string;
  investor_id: string | null;
  income_monthly: Metric;
  income_annual: Metric;
  income_breakdown: BreakdownItem[];
  expenses_monthly: Metric;
  expenses_annual: Metric;
  expense_breakdown: BreakdownItem[];
  commitments_monthly: Metric;
  commitments_annual: Metric;
  commitment_breakdown: CommitmentBreakdownItem[];
  investable_surplus_monthly: Metric;
  investable_surplus_annual: Metric;
  cash_flow_ratio: Metric;
  savings_investment_rate: Metric;
  total_assets: Metric;
  asset_breakdown: AssetBreakdownItem[];
  total_liabilities: Metric;
  liability_breakdown: LiabilityBreakdownItem[];
  emi_burden_monthly: Metric;
  net_worth: Metric;
  safety_reserve_months: Metric;
  safety_reserve_required_amount: Metric;
  isPlaceholderPreview?: boolean;
};

function formatAmount(value: number) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

// ============================================================================
// STATIC UI PREVIEW PLACEHOLDER (Used only when backend is offline/unauthenticated)
// ============================================================================

const FALLBACK_FINANCIAL_STATE: FinancialStateResponse = {
  scope: "family",
  planning_unit_id: "preview-unit",
  investor_id: "preview-investor",
  isPlaceholderPreview: true,
  income_monthly: { value: 210000, available: true, reason: null },
  income_annual: { value: 2520000, available: true, reason: null },
  income_breakdown: [
    { type: "Primary Salary", monthly: 175000, annual: 2100000 },
    { type: "Consulting / Professional Fees", monthly: 35000, annual: 420000 },
  ],
  expenses_monthly: { value: 128000, available: true, reason: null },
  expenses_annual: { value: 1536000, available: true, reason: null },
  expense_breakdown: [
    { type: "Housing & Rent", monthly: 45000, annual: 540000 },
    { type: "Groceries & Household", monthly: 24000, annual: 288000 },
    { type: "Transport & Fuel", monthly: 12000, annual: 144000 },
    { type: "Utilities & Bills", monthly: 7000, annual: 84000 },
    { type: "Healthcare", monthly: 6000, annual: 72000 },
    { type: "Lifestyle & Discretionary", monthly: 34000, annual: 408000 },
  ],
  commitments_monthly: { value: 15000, available: true, reason: null },
  commitments_annual: { value: 180000, available: true, reason: null },
  commitment_breakdown: [
    { commitment_id: "c-1", name: "Family Support Contribution", amount: 10000 },
    { commitment_id: "c-2", name: "Annual Insurance Premium Reserve", amount: 5000 },
  ],
  investable_surplus_monthly: { value: 67000, available: true, reason: null },
  investable_surplus_annual: { value: 804000, available: true, reason: null },
  cash_flow_ratio: { value: 0.32, available: true, reason: null },
  savings_investment_rate: { value: 0.32, available: true, reason: null },
  total_assets: { value: 5850000, available: true, reason: null },
  asset_breakdown: [
    { asset_id: "a-1", name: "Equity Mutual Funds", current_value: 2200000, ownership_applied: 2200000, liquidity: "High" },
    { asset_id: "a-2", name: "EPF / Employee Provident Fund", current_value: 1650000, ownership_applied: 1650000, liquidity: "Low" },
    { asset_id: "a-3", name: "Fixed Deposits", current_value: 800000, ownership_applied: 800000, liquidity: "Moderate" },
    { asset_id: "a-4", name: "Bank Savings Account", current_value: 400000, ownership_applied: 400000, liquidity: "High" },
    { asset_id: "a-5", name: "Digital & Physical Gold", current_value: 800000, ownership_applied: 800000, liquidity: "Moderate" },
  ],
  total_liabilities: { value: 1850000, available: true, reason: null },
  liability_breakdown: [
    { liability_id: "l-1", name: "Home Loan Outstanding", outstanding_amount: 1500000, responsibility_applied: 1500000, classification: "Secured" },
    { liability_id: "l-2", name: "Vehicle Loan Outstanding", outstanding_amount: 350000, responsibility_applied: 350000, classification: "Secured" },
  ],
  emi_burden_monthly: { value: 28000, available: true, reason: null },
  net_worth: { value: 4000000, available: true, reason: null },
  safety_reserve_months: { value: 3.8, available: true, reason: null },
  safety_reserve_required_amount: { value: 768000, available: true, reason: null },
};

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export default function FinancialStatePage() {
  const [data, setData] = useState<FinancialStateResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Period Selector: Monthly vs Annual
  const [period, setPeriod] = useState<"Monthly" | "Annual">("Monthly");

  // UI state switcher (allows previewing Empty, Loading, Error, Populated)
  const [uiState, setUiState] = useState<"normal" | "empty" | "loading" | "error">("normal");

  useEffect(() => {
    let active = true;

    async function fetchFinancialState() {
      try {
        const { data: sessionData, error: sessionError } = await supabase.auth.getSession();
        if (sessionError) throw sessionError;
        const session = sessionData?.session;

        if (!session) {
          // If unauthenticated, fallback to preview data for UI presentation
          if (active) {
            setData(FALLBACK_FINANCIAL_STATE);
            setIsLoading(false);
          }
          return;
        }

        const user = session.user;
        let planningUnitId =
          typeof window !== "undefined" ? window.localStorage.getItem("planvesto-planning-unit-id") : null;

        if (!planningUnitId) {
          const { data: puData, error: puError } = await supabase
            .from("planning_units")
            .select("planning_unit_id")
            .eq("user_id", user.id)
            .order("created_at", { ascending: false })
            .limit(1)
            .maybeSingle();

          if (puError) throw puError;
          if (puData?.planning_unit_id) {
            const resolvedId = String(puData.planning_unit_id);
            planningUnitId = resolvedId;
            if (typeof window !== "undefined") {
              window.localStorage.setItem("planvesto-planning-unit-id", resolvedId);
            }
          }
        }

        if (!planningUnitId) {
          if (active) {
            setData(FALLBACK_FINANCIAL_STATE);
            setIsLoading(false);
          }
          return;
        }

        const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";
        const response = await fetch(`${backendUrl}/api/financial-state/build`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${session.access_token}`,
          },
          body: JSON.stringify({
            planning_unit_id: planningUnitId,
            scope: "family",
          }),
        });

        const responseBody = await response.json();
        if (!response.ok) {
          throw new Error(responseBody.detail || "Unable to load your financial state.");
        }

        if (active) {
          setData(responseBody);
        }
      } catch (cause: unknown) {
        if (active) {
          // If backend API is not running locally, use isolated fallback preview data so UI is verifiable
          setData(FALLBACK_FINANCIAL_STATE);
        }
      } finally {
        if (active) {
          setIsLoading(false);
        }
      }
    }

    fetchFinancialState();

    return () => {
      active = false;
    };
  }, []);

  // Selected period multiplier for display
  const isAnnual = period === "Annual";

  // Data values depending on period
  const totalIncome = isAnnual
    ? (data?.income_annual?.value ?? (data?.income_monthly?.value ? data.income_monthly.value * 12 : 0))
    : (data?.income_monthly?.value ?? 0);

  const totalExpenses = isAnnual
    ? (data?.expenses_annual?.value ?? (data?.expenses_monthly?.value ? data.expenses_monthly.value * 12 : 0))
    : (data?.expenses_monthly?.value ?? 0);

  const surplus = isAnnual
    ? (data?.investable_surplus_annual?.value ?? totalIncome - totalExpenses)
    : (data?.investable_surplus_monthly?.value ?? totalIncome - totalExpenses);

  const totalAssets = data?.total_assets?.value ?? 0;
  const totalLiabilities = data?.total_liabilities?.value ?? 0;
  const netWorth = data?.net_worth?.value ?? totalAssets - totalLiabilities;

  const commitments = isAnnual
    ? (data?.commitments_annual?.value ?? (data?.commitments_monthly?.value ? data.commitments_monthly.value * 12 : 0))
    : (data?.commitments_monthly?.value ?? 0);

  const hasNoData =
    !data ||
    (!data.income_breakdown.length &&
      !data.expense_breakdown.length &&
      !data.asset_breakdown.length &&
      !data.liability_breakdown.length &&
      !data.commitment_breakdown.length);

  // Category grouping for assets (Presentation only)
  const groupedAssets = useMemo(() => {
    if (!data?.asset_breakdown) return [];
    return data.asset_breakdown;
  }, [data?.asset_breakdown]);

  // Category grouping for liabilities (Presentation only)
  const groupedLiabilities = useMemo(() => {
    if (!data?.liability_breakdown) return [];
    return data.liability_breakdown;
  }, [data?.liability_breakdown]);

  // ==========================================================================
  // RENDER: LOADING STATE
  // ==========================================================================
  if (isLoading || uiState === "loading") {
    return (
      <main className="min-w-0 flex-1 p-5 lg:p-8" aria-busy="true">
        <div className="mx-auto max-w-6xl space-y-6">
          <div className="flex justify-end gap-2 pb-2">
            <span className="text-xs font-semibold text-slate-400 self-center">UI State Preview:</span>
            <button
              onClick={() => setUiState("normal")}
              className="rounded-lg bg-white px-3 py-1 text-xs font-bold text-slate-700 border border-slate-200"
            >
              Normal
            </button>
            <button
              onClick={() => setUiState("empty")}
              className="rounded-lg bg-white px-3 py-1 text-xs font-bold text-slate-700 border border-slate-200"
            >
              Empty
            </button>
          </div>
          <div className="h-8 w-64 animate-pulse rounded-lg bg-slate-200" />
          <div className="h-28 w-full animate-pulse rounded-3xl bg-white shadow-sm" />
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <div className="h-28 animate-pulse rounded-2xl bg-white shadow-sm" />
            <div className="h-28 animate-pulse rounded-2xl bg-white shadow-sm" />
            <div className="h-28 animate-pulse rounded-2xl bg-white shadow-sm" />
            <div className="h-28 animate-pulse rounded-2xl bg-white shadow-sm" />
          </div>
          <div className="h-64 animate-pulse rounded-3xl bg-white shadow-sm" />
        </div>
      </main>
    );
  }

  // ==========================================================================
  // RENDER: ERROR STATE
  // ==========================================================================
  if (uiState === "error" || (error && !data)) {
    return (
      <main className="min-w-0 flex-1 p-5 lg:p-8">
        <div className="mx-auto max-w-2xl rounded-3xl border border-red-200 bg-white p-8 text-center shadow-sm">
          <div className="flex justify-end gap-2 pb-4">
            <button
              onClick={() => setUiState("normal")}
              className="rounded-lg bg-navy-900 px-3 py-1 text-xs font-bold text-white"
            >
              Back to Normal
            </button>
          </div>
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-red-50 text-red-600">
            <svg className="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h2 className="mt-4 text-xl font-bold text-slate-900">Unable to Load Financial State</h2>
          <p className="mt-2 text-sm text-slate-600">
            {error || "We encountered an issue fetching your recorded balances. Please retry."}
          </p>
          <button
            onClick={() => {
              setError(null);
              setUiState("normal");
            }}
            className="mt-6 inline-flex items-center rounded-xl bg-navy-900 px-6 py-2.5 text-sm font-semibold text-white transition hover:bg-navy-800"
          >
            Retry Loading
          </button>
        </div>
      </main>
    );
  }

  // ==========================================================================
  // RENDER: EMPTY STATE
  // ==========================================================================
  if (uiState === "empty" || hasNoData) {
    return (
      <main className="min-w-0 flex-1 p-5 lg:p-8">
        <header className="border-b border-slate-200 bg-white -mx-5 -mt-5 mb-8 lg:-mx-8 lg:-mt-8">
          <div className="flex min-h-[80px] items-center justify-between gap-6 px-5 lg:px-8">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-400">
                Current Financial Snapshot
              </p>
              <h1 className="mt-1 text-2xl font-extrabold tracking-tight text-slate-950 sm:text-3xl">
                Financial State
              </h1>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => setUiState("normal")}
                className="rounded-xl border border-slate-200 bg-white px-3 py-1.5 text-xs font-bold text-slate-700 hover:bg-slate-50"
              >
                Show Populated Demo
              </button>
              <InvestorProfileMenu />
            </div>
          </div>
        </header>

        <div className="mx-auto max-w-2xl rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center shadow-sm">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-teal-50 text-teal-700">
            <svg className="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h2 className="mt-4 text-2xl font-black text-slate-950">Your Financial State is Empty</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-500 max-w-md mx-auto">
            Complete the onboarding steps to record your income, expenses, assets, and liabilities. Your current financial situation will be summarized here.
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <Link
              href="/investor/onboarding/income"
              className="inline-flex rounded-xl bg-slate-950 px-5 py-3 text-sm font-bold text-white transition hover:bg-slate-800"
            >
              Start Recording Finances →
            </Link>
          </div>
        </div>
      </main>
    );
  }

  // ==========================================================================
  // RENDER: POPULATED FINANCIAL STATE
  // ==========================================================================
  return (
    <main className="min-w-0 flex-1 pb-20">
      {/* 1. PAGE HEADER */}
      <header className="border-b border-slate-200 bg-white sticky top-0 z-10">
        <div className="flex min-h-[80px] items-center justify-between gap-6 px-5 lg:px-8">
          <div>
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center rounded-md bg-teal-50 px-2 py-0.5 text-xs font-semibold text-teal-700 ring-1 ring-inset ring-teal-600/20">
                Current Position
              </span>
              <p className="text-xs font-bold uppercase tracking-[0.14em] text-slate-400">
                Investor Dashboard
              </p>
            </div>
            <h1 className="mt-1 text-2xl font-extrabold tracking-tight text-slate-950 sm:text-3xl">
              Financial State
            </h1>
          </div>

          <div className="flex items-center gap-3">
            {/* Period Selector: Monthly vs Annual */}
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

            {/* Quick Navigation Links */}
            <div className="hidden lg:flex items-center gap-3 border-l border-slate-200 pl-3">
              <Link
                href="/investor/budgeting"
                className="text-xs font-bold text-slate-600 hover:text-navy-900 transition"
              >
                Budgeting
              </Link>
              <Link
                href="/investor/goal-planner"
                className="text-xs font-bold text-teal-700 hover:text-teal-900 transition"
              >
                Goal Planner
              </Link>
              <Link
                href="/investor/strategy-builder"
                className="text-xs font-bold text-slate-600 hover:text-navy-900 transition"
              >
                Strategy Builder
              </Link>
            </div>

            {/* Demo State Switcher */}
            <select
              aria-label="UI Preview State Switcher"
              value={uiState}
              onChange={(e) => setUiState(e.target.value as typeof uiState)}
              className="rounded-lg border border-slate-200 bg-white px-2 py-1.5 text-xs font-semibold text-slate-600 outline-none hover:bg-slate-50"
            >
              <option value="normal">UI: Populated</option>
              <option value="empty">UI: Empty</option>
              <option value="loading">UI: Loading</option>
              <option value="error">UI: Error</option>
            </select>

            <InvestorProfileMenu />
          </div>
        </div>
      </header>

      {/* Preview Tag Banner if using placeholder */}
      {data?.isPlaceholderPreview && (
        <div className="border-b border-teal-200 bg-teal-50/60 px-5 py-2 text-xs text-teal-900 lg:px-8">
          <div className="mx-auto flex max-w-6xl items-center justify-between gap-4">
            <p className="flex items-center gap-2">
              <span className="flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-teal-200 text-teal-800 font-bold text-[10px]">
                ✓
              </span>
              <span>
                <strong>Current Position Snapshot:</strong> Where you stand financially today across income, expenses, assets, liabilities, and commitments.
              </span>
            </p>
            <span className="shrink-0 font-bold uppercase tracking-wider text-[10px] text-teal-800 bg-teal-100 px-2 py-0.5 rounded">
              Preview / Placeholder Data
            </span>
          </div>
        </div>
      )}

      <div className="space-y-8 p-5 lg:p-8 max-w-6xl mx-auto">
        {/* Purpose Card */}
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:p-8">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">
                Where you are today
              </p>
              <h2 className="mt-1 text-2xl font-extrabold tracking-tight text-slate-950">
                Your Current Financial Situation
              </h2>
              <p className="mt-1 max-w-2xl text-sm leading-6 text-slate-500">
                A factual snapshot of your income, expenses, investable surplus, assets, liabilities, and commitments.
              </p>
            </div>

            <div className="flex items-center gap-2">
              <Link
                href="/investor/onboarding/income"
                className="inline-flex rounded-xl border border-slate-200 bg-white px-3.5 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 transition"
              >
                ✏️ Edit Entries
              </Link>
            </div>
          </div>
        </section>

        {/* ================================================================== */}
        {/* 2. TOP SNAPSHOT: Total Income, Expenses, Surplus, Net Worth        */}
        {/* ================================================================== */}
        <section aria-labelledby="top-snapshot-title" className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 id="top-snapshot-title" className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Key Metrics ({period})
            </h3>
            <span className="text-xs font-semibold text-slate-500">
              Showing: {period === "Monthly" ? "Monthly figures" : "Annualized figures"}
            </span>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {/* Total Income */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wide text-slate-400">
                <span>Total Income</span>
                <span className="rounded-md bg-emerald-50 px-2 py-0.5 text-emerald-700 text-[10px]">Inflow</span>
              </div>
              <p className="mt-3 text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-950">
                {formatAmount(totalIncome)}
              </p>
              <p className="mt-2 text-xs text-slate-500">
                {period} total recorded inflow
              </p>
            </div>

            {/* Total Expenses */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wide text-slate-400">
                <span>Total Expenses</span>
                <span className="rounded-md bg-rose-50 px-2 py-0.5 text-rose-700 text-[10px]">Outflow</span>
              </div>
              <p className="mt-3 text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-950">
                {formatAmount(totalExpenses)}
              </p>
              <p className="mt-2 text-xs text-slate-500">
                {period} recurring living expenses
              </p>
            </div>

            {/* Surplus / Deficit */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wide text-slate-400">
                <span>Surplus / Deficit</span>
                <span className="rounded-md bg-teal-50 px-2 py-0.5 text-teal-700 text-[10px]">Net Cash Flow</span>
              </div>
              <p className="mt-3 text-2xl sm:text-3xl font-extrabold tracking-tight text-teal-700">
                {formatAmount(surplus)}
              </p>
              <p className="mt-2 text-xs text-slate-500">
                Uncommitted {period.toLowerCase()} buffer
              </p>
            </div>

            {/* Net Worth */}
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wide text-slate-400">
                <span>Net Worth</span>
                <span className="rounded-md bg-navy-50 px-2 py-0.5 text-navy-900 text-[10px]">Assets - Debt</span>
              </div>
              <p className="mt-3 text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-950">
                {formatAmount(netWorth)}
              </p>
              <p className="mt-2 text-xs text-slate-500">
                Total accumulated equity position
              </p>
            </div>
          </div>
        </section>

        {/* ================================================================== */}
        {/* 3. CASH FLOW SECTION (Visual Pipeline: Income → Expenses → Surplus) */}
        {/* ================================================================== */}
        <section aria-labelledby="cash-flow-title" className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-8 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-slate-100 pb-4">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
                Cash Flow Dynamics
              </span>
              <h3 id="cash-flow-title" className="mt-1 text-xl font-extrabold text-slate-950">
                Cash Flow Movement ({period})
              </h3>
              <p className="mt-0.5 text-xs text-slate-500">
                Visualizing how your inflows translate through expenses into net investable surplus.
              </p>
            </div>

            <Link
              href="/investor/budgeting"
              className="mt-2 sm:mt-0 inline-flex items-center text-xs font-bold text-teal-700 hover:text-teal-900"
            >
              Open Detailed Budgeting →
            </Link>
          </div>

          <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-3">
            {/* Step 1: Inflow */}
            <div className="rounded-2xl bg-emerald-50/70 border border-emerald-200 p-5 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-emerald-800">1. Total Income</span>
                  <span className="text-base">💰</span>
                </div>
                <p className="mt-2 text-2xl font-black text-emerald-950">{formatAmount(totalIncome)}</p>
              </div>
              <p className="mt-3 text-xs text-emerald-700">Starting inflow pool</p>
            </div>

            {/* Step 2: Outflow */}
            <div className="rounded-2xl bg-rose-50/70 border border-rose-200 p-5 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-rose-800">2. Total Expenses</span>
                  <span className="text-base">📉</span>
                </div>
                <p className="mt-2 text-2xl font-black text-rose-950">- {formatAmount(totalExpenses)}</p>
              </div>
              <p className="mt-3 text-xs text-rose-700">
                {totalIncome > 0 ? `${Math.round((totalExpenses / totalIncome) * 100)}% of income consumed` : "Recorded expenses"}
              </p>
            </div>

            {/* Step 3: Surplus */}
            <div className="rounded-2xl bg-teal-50/80 border border-teal-200 p-5 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-teal-800">3. Net Surplus</span>
                  <span className="text-base">🎯</span>
                </div>
                <p className="mt-2 text-2xl font-black text-teal-950">+ {formatAmount(surplus)}</p>
              </div>
              <p className="mt-3 text-xs text-teal-700">
                {totalIncome > 0 ? `${Math.round((surplus / totalIncome) * 100)}% available to fund goals` : "Investable buffer"}
              </p>
            </div>
          </div>
        </section>

        {/* ================================================================== */}
        {/* 4. NET WORTH SECTION (Assets vs Liabilities Comparison)            */}
        {/* ================================================================== */}
        <section aria-labelledby="net-worth-title" className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-8 shadow-sm">
          <div className="border-b border-slate-100 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
              Balance Sheet Overview
            </span>
            <h3 id="net-worth-title" className="mt-1 text-xl font-extrabold text-slate-950">
              Net Worth Position: Assets vs Liabilities
            </h3>
            <p className="mt-0.5 text-xs text-slate-500">
              Total Assets minus Total Liabilities yields your cumulative Net Worth.
            </p>
          </div>

          <div className="mt-6 grid grid-cols-1 gap-5 md:grid-cols-3">
            {/* Total Assets Card */}
            <div className="rounded-2xl bg-slate-50 p-5 border border-slate-200">
              <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Total Assets</p>
              <p className="mt-2 text-2xl font-black text-slate-950">{formatAmount(totalAssets)}</p>
              <p className="mt-1 text-xs text-slate-500">{data?.asset_breakdown?.length ?? 0} asset items recorded</p>
            </div>

            {/* Total Liabilities Card */}
            <div className="rounded-2xl bg-slate-50 p-5 border border-slate-200">
              <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Total Liabilities</p>
              <p className="mt-2 text-2xl font-black text-slate-950">{formatAmount(totalLiabilities)}</p>
              <p className="mt-1 text-xs text-slate-500">{data?.liability_breakdown?.length ?? 0} liabilities recorded</p>
            </div>

            {/* Net Worth Equity Card */}
            <div className="rounded-2xl bg-teal-50/70 p-5 border border-teal-200">
              <p className="text-xs font-bold uppercase tracking-wider text-teal-800">Net Worth</p>
              <p className="mt-2 text-2xl font-black text-teal-950">{formatAmount(netWorth)}</p>
              <p className="mt-1 text-xs text-teal-700">Total net financial capital</p>
            </div>
          </div>

          {/* Visual Bar Comparison: Assets vs Liabilities */}
          <div className="mt-6 space-y-2">
            <div className="flex justify-between text-xs font-bold text-slate-600">
              <span>Assets ({formatAmount(totalAssets)})</span>
              <span>Debt ({formatAmount(totalLiabilities)})</span>
            </div>
            <div className="flex h-3.5 w-full rounded-full overflow-hidden bg-slate-100">
              <div
                className="bg-teal-600"
                style={{
                  width: `${
                    totalAssets + totalLiabilities > 0
                      ? Math.round((totalAssets / (totalAssets + totalLiabilities)) * 100)
                      : 100
                  }%`,
                }}
              />
              <div
                className="bg-rose-500"
                style={{
                  width: `${
                    totalAssets + totalLiabilities > 0
                      ? Math.round((totalLiabilities / (totalAssets + totalLiabilities)) * 100)
                      : 0
                  }%`,
                }}
              />
            </div>
          </div>
        </section>

        {/* ================================================================== */}
        {/* 5. ASSETS & 6. LIABILITIES DETAIL LISTS                            */}
        {/* ================================================================== */}
        <div className="grid gap-6 xl:grid-cols-2">
          {/* ASSETS SECTION */}
          <section className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-7 shadow-sm flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <div>
                  <h3 className="text-lg font-extrabold text-slate-950">Assets Breakdown</h3>
                  <p className="text-xs text-slate-500 mt-0.5">Total: {formatAmount(totalAssets)}</p>
                </div>
                <Link
                  href="/investor/onboarding/assets"
                  className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-bold text-slate-700 hover:bg-slate-50"
                >
                  Edit Assets
                </Link>
              </div>

              {groupedAssets.length > 0 ? (
                <div className="mt-4 divide-y divide-slate-100">
                  {groupedAssets.map((asset) => (
                    <div key={asset.asset_id} className="flex items-center justify-between py-3">
                      <div>
                        <p className="text-sm font-semibold text-slate-800">{asset.name || "Asset"}</p>
                        {asset.liquidity && (
                          <span className="text-[10px] font-bold text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
                            {asset.liquidity} Liquidity
                          </span>
                        )}
                      </div>
                      <p className="text-sm font-black text-slate-950">{formatAmount(asset.current_value)}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="mt-4 text-sm text-slate-500 italic">No assets recorded yet.</p>
              )}
            </div>
          </section>

          {/* LIABILITIES SECTION */}
          <section className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-7 shadow-sm flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <div>
                  <h3 className="text-lg font-extrabold text-slate-950">Liabilities Breakdown</h3>
                  <p className="text-xs text-slate-500 mt-0.5">Total: {formatAmount(totalLiabilities)}</p>
                </div>
                <Link
                  href="/investor/onboarding/liabilities"
                  className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-bold text-slate-700 hover:bg-slate-50"
                >
                  Edit Liabilities
                </Link>
              </div>

              {groupedLiabilities.length > 0 ? (
                <div className="mt-4 divide-y divide-slate-100">
                  {groupedLiabilities.map((liability) => (
                    <div key={liability.liability_id} className="flex items-center justify-between py-3">
                      <div>
                        <p className="text-sm font-semibold text-slate-800">{liability.name || "Liability"}</p>
                        {liability.classification && (
                          <span className="text-[10px] font-bold text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
                            {liability.classification}
                          </span>
                        )}
                      </div>
                      <p className="text-sm font-black text-rose-700">{formatAmount(liability.outstanding_amount)}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="mt-4 text-sm text-slate-500 italic">No liabilities recorded yet.</p>
              )}
            </div>
          </section>
        </div>

        {/* ================================================================== */}
        {/* 7. COMMITMENTS SECTION                                             */}
        {/* ================================================================== */}
        <section aria-labelledby="commitments-title" className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-8 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-slate-100 pb-4">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
                  Obligations
                </span>
                <span className="rounded bg-slate-100 px-2 py-0.5 text-[10px] font-bold text-slate-600">
                  {data?.commitment_breakdown?.length ?? 0} Recorded
                </span>
              </div>
              <h3 id="commitments-title" className="mt-1 text-xl font-extrabold text-slate-950">
                Financial Commitments ({period})
              </h3>
              <p className="mt-0.5 text-xs text-slate-500">
                Existing family, dependent, or recurring contractual support obligations.
              </p>
            </div>

            <div className="flex items-center gap-3 mt-3 sm:mt-0">
              <span className="text-sm font-black text-slate-950">
                Total: {formatAmount(commitments)}
              </span>
              <Link
                href="/investor/onboarding/commitments"
                className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-bold text-slate-700 hover:bg-slate-50"
              >
                Edit Commitments
              </Link>
            </div>
          </div>

          <div className="mt-6">
            {data?.commitment_breakdown && data.commitment_breakdown.length > 0 ? (
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {data.commitment_breakdown.map((item) => (
                  <div key={item.commitment_id} className="rounded-2xl bg-slate-50 p-4 border border-slate-200">
                    <p className="text-xs font-bold text-slate-800">{item.name || "Commitment"}</p>
                    <p className="mt-2 text-lg font-black text-slate-950">
                      {formatAmount(Number(item.amount) * (isAnnual ? 12 : 1) || 0)}
                    </p>
                    <p className="mt-0.5 text-[11px] text-slate-400">Recurring obligation ({period.toLowerCase()})</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-slate-500 italic">No recurring financial commitments recorded.</p>
            )}
          </div>
        </section>

        {/* ================================================================== */}
        {/* 8. SUMMARY: Consolidated Financial Position Snapshot               */}
        {/* ================================================================== */}
        <section aria-labelledby="summary-title" className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-8 shadow-sm">
          <div className="border-b border-slate-100 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
              Consolidated Record
            </span>
            <h3 id="summary-title" className="mt-1 text-xl font-extrabold text-slate-950">
              Financial Position Summary ({period})
            </h3>
            <p className="mt-0.5 text-xs text-slate-500">
              Consolidated snapshot table of all core financial metrics.
            </p>
          </div>

          <div className="mt-6 overflow-x-auto">
            <table className="w-full text-left border-collapse min-w-[500px]">
              <thead>
                <tr className="border-b border-slate-200 text-xs font-bold uppercase tracking-wider text-slate-400">
                  <th className="py-3 px-4">Metric</th>
                  <th className="py-3 px-4">Period / Scope</th>
                  <th className="py-3 px-4 text-right">Recorded Value</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-sm">
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-900">Total Income</td>
                  <td className="py-3 px-4 text-slate-500 text-xs">{period} Inflow</td>
                  <td className="py-3 px-4 text-right font-black text-emerald-700">{formatAmount(totalIncome)}</td>
                  <td className="py-3 px-4 text-right">
                    <Link href="/investor/onboarding/income" className="text-xs font-bold text-teal-700 hover:underline">
                      Edit
                    </Link>
                  </td>
                </tr>
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-900">Total Expenses</td>
                  <td className="py-3 px-4 text-slate-500 text-xs">{period} Living Costs</td>
                  <td className="py-3 px-4 text-right font-black text-rose-700">{formatAmount(totalExpenses)}</td>
                  <td className="py-3 px-4 text-right">
                    <Link href="/investor/onboarding/expenses" className="text-xs font-bold text-teal-700 hover:underline">
                      Edit
                    </Link>
                  </td>
                </tr>
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-900">Surplus / Deficit</td>
                  <td className="py-3 px-4 text-slate-500 text-xs">{period} Investable Balance</td>
                  <td className="py-3 px-4 text-right font-black text-teal-700">{formatAmount(surplus)}</td>
                  <td className="py-3 px-4 text-right">
                    <Link href="/investor/budgeting" className="text-xs font-bold text-teal-700 hover:underline">
                      Budget
                    </Link>
                  </td>
                </tr>
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-900">Total Assets</td>
                  <td className="py-3 px-4 text-slate-500 text-xs">Accumulated Wealth Base</td>
                  <td className="py-3 px-4 text-right font-black text-slate-950">{formatAmount(totalAssets)}</td>
                  <td className="py-3 px-4 text-right">
                    <Link href="/investor/onboarding/assets" className="text-xs font-bold text-teal-700 hover:underline">
                      Edit
                    </Link>
                  </td>
                </tr>
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-900">Total Liabilities</td>
                  <td className="py-3 px-4 text-slate-500 text-xs">Outstanding Debt</td>
                  <td className="py-3 px-4 text-right font-black text-slate-950">{formatAmount(totalLiabilities)}</td>
                  <td className="py-3 px-4 text-right">
                    <Link href="/investor/onboarding/liabilities" className="text-xs font-bold text-teal-700 hover:underline">
                      Edit
                    </Link>
                  </td>
                </tr>
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-900">Net Worth</td>
                  <td className="py-3 px-4 text-slate-500 text-xs">Assets minus Debt</td>
                  <td className="py-3 px-4 text-right font-black text-teal-800">{formatAmount(netWorth)}</td>
                  <td className="py-3 px-4 text-right">
                    <span className="text-xs text-slate-400 font-semibold">—</span>
                  </td>
                </tr>
                <tr>
                  <td className="py-3 px-4 font-bold text-slate-900">Commitments</td>
                  <td className="py-3 px-4 text-slate-500 text-xs">{period} Recurring Obligations</td>
                  <td className="py-3 px-4 text-right font-black text-slate-950">{formatAmount(commitments)}</td>
                  <td className="py-3 px-4 text-right">
                    <Link href="/investor/onboarding/commitments" className="text-xs font-bold text-teal-700 hover:underline">
                      Edit
                    </Link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* 9. INTERACTION: Related Planning Destinations */}
        <section className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-8 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
                Planning Workflow
              </span>
              <h3 className="mt-1 text-lg font-extrabold text-slate-950">
                Next Steps from your Financial State
              </h3>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <Link
              href="/investor/budgeting"
              className="rounded-2xl border border-slate-200 p-5 hover:border-teal-400 hover:shadow-sm transition group bg-slate-50/60"
            >
              <p className="text-xs font-bold uppercase tracking-wider text-teal-700">Manage Cash Flows</p>
              <h4 className="mt-2 text-base font-extrabold text-slate-950 group-hover:text-teal-900">
                Budgeting →
              </h4>
              <p className="mt-1 text-xs text-slate-500">
                Set category limits and track budget vs actual variances.
              </p>
            </Link>

            <Link
              href="/investor/goal-planner"
              className="rounded-2xl border border-slate-200 p-5 hover:border-teal-400 hover:shadow-sm transition group bg-slate-50/60"
            >
              <p className="text-xs font-bold uppercase tracking-wider text-teal-700">Map Future Milestones</p>
              <h4 className="mt-2 text-base font-extrabold text-slate-950 group-hover:text-teal-900">
                Goal Planner →
              </h4>
              <p className="mt-1 text-xs text-slate-500">
                Allocate recorded assets and target amounts to your goals.
              </p>
            </Link>

            <Link
              href="/investor/strategy-builder"
              className="rounded-2xl border border-slate-200 p-5 hover:border-teal-400 hover:shadow-sm transition group bg-slate-50/60"
            >
              <p className="text-xs font-bold uppercase tracking-wider text-teal-700">Bridge Funding Gaps</p>
              <h4 className="mt-2 text-base font-extrabold text-slate-950 group-hover:text-teal-900">
                Strategy Builder →
              </h4>
              <p className="mt-1 text-xs text-slate-500">
                Evaluate calibrated pathways across Safety, Liquidity & Return.
              </p>
            </Link>
          </div>
        </section>
      </div>
    </main>
  );
}