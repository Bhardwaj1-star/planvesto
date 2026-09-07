"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { supabase } from "../../../lib/supabase";

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
};

function formatAmount(value: number) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(value);
}

export default function FinancialStatePage() {
  const [data, setData] = useState<FinancialStateResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function fetchFinancialState() {
      try {
        const { data: sessionData, error: sessionError } = await supabase.auth.getSession();
        if (sessionError) throw sessionError;
        const session = sessionData?.session;
        if (!session) {
          throw new Error("Please log in to view your financial state.");
        }

        const user = session.user;
        let planningUnitId = typeof window !== "undefined" ? window.localStorage.getItem("planvesto-planning-unit-id") : null;

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
            setData(null);
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
          setError(cause instanceof Error ? cause.message : "Unable to load your financial state.");
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

  const monthlyIncome = data?.income_monthly?.value ?? 0;
  const monthlyExpenses = data?.expenses_monthly?.value ?? 0;
  const assets = data?.total_assets?.value ?? 0;
  const liabilities = data?.total_liabilities?.value ?? 0;
  const commitments = data?.commitments_monthly?.available && data.commitments_monthly.value !== null
    ? data.commitments_monthly.value
    : (data?.commitment_breakdown?.reduce((total, item) => total + (Number(item.amount) || 0), 0) ?? 0);

  const hasNoData = !data || (
    !data.income_breakdown.length &&
    !data.expense_breakdown.length &&
    !data.asset_breakdown.length &&
    !data.liability_breakdown.length &&
    !data.commitment_breakdown.length
  );

  return (
    <div className="min-h-screen bg-[#f6f8fb] text-slate-900">
      <div className="flex min-h-screen"><main className="min-w-0 flex-1">
        <header className="border-b border-slate-200 bg-white"><div className="flex min-h-[80px] items-center justify-between gap-6 px-5 lg:px-8"><div><p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-400">Investor Dashboard</p><h1 className="mt-1 text-2xl font-extrabold tracking-tight text-slate-950 sm:text-3xl">Financial State</h1></div><div className="flex items-center gap-4"><Link href="/investor/goal-planner" className="text-sm font-bold text-teal-700 hover:text-teal-900">Goal Planner</Link><Link href="/investor" className="text-sm font-bold text-slate-600 hover:text-slate-950">Back to dashboard</Link></div></div></header>
        <div className="space-y-6 p-5 lg:p-8"><section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:p-8"><p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">Where you are today</p><h2 className="mt-2 text-2xl font-extrabold tracking-tight text-slate-950">Your current financial situation</h2><p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">Income, expenses, assets, liabilities and commitments from your financial plan.</p></section>
          {isLoading && <section className="rounded-3xl border border-slate-200 bg-white p-7 text-sm font-semibold text-slate-500 shadow-sm">Loading your financial state...</section>}
          {error && <section className="rounded-3xl border border-red-200 bg-red-50 p-7 text-sm font-semibold text-red-700" role="alert">{error}</section>}
          {!isLoading && !error && data && <>
            <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5"><StateMetric label="Monthly Income" value={monthlyIncome} /><StateMetric label="Monthly Expenses" value={monthlyExpenses} /><StateMetric label="Assets" value={assets} /><StateMetric label="Liabilities" value={liabilities} /><StateMetric label="Commitments" value={commitments} /></section>
            {hasNoData && <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-center shadow-sm"><h2 className="text-lg font-extrabold text-slate-950">Your financial state is empty</h2><p className="mt-2 text-sm text-slate-500">Complete the onboarding sections to see your current position here.</p><Link href="/investor/onboarding/personal-information" className="mt-5 inline-flex rounded-xl bg-slate-950 px-5 py-3 text-sm font-bold text-white hover:bg-slate-800">Continue onboarding</Link></section>}
            <section className="grid gap-6 xl:grid-cols-2">
              <DataList title="Income" empty="No income sources added." items={data.income_breakdown.map((item) => ({ label: item.type, value: formatAmount(item.monthly) }))} />
              <DataList title="Expenses" empty="No expenses added." items={data.expense_breakdown.map((item) => ({ label: item.type, value: formatAmount(item.monthly) }))} />
              <DataList title="Assets" empty="No assets added." items={data.asset_breakdown.map((item) => ({ label: item.name, value: formatAmount(item.current_value) }))} />
              <DataList title="Liabilities" empty="No liabilities added." items={data.liability_breakdown.map((item) => ({ label: item.name, value: formatAmount(item.outstanding_amount) }))} />
              <DataList title="Commitments" empty="No commitments added." items={data.commitment_breakdown.map((item) => ({ label: item.name, value: formatAmount(Number(item.amount) || 0) }))} />
            </section>
          </>}
        </div>
      </main></div>
    </div>
  );
}

function StateMetric({ label, value }: { label: string; value: number }) {
  return <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><p className="text-xs font-bold uppercase tracking-wide text-slate-400">{label}</p><p className="mt-3 text-2xl font-extrabold tracking-tight text-slate-950">{formatAmount(value)}</p><p className="mt-2 text-xs text-slate-500">Current recorded value</p></div>;
}

function DataList({ title, empty, items }: { title: string; empty: string; items: Array<{ label: string; value: string }> }) {
  return <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm lg:p-7"><h2 className="text-lg font-extrabold text-slate-950">{title}</h2>{items.length ? <div className="mt-5 divide-y divide-slate-100">{items.map((item, index) => <div key={`${item.label}-${index}`} className="flex items-center justify-between gap-4 py-3 first:pt-0 last:pb-0"><p className="text-sm font-semibold text-slate-700">{item.label || "Unnamed"}</p><p className="text-sm font-extrabold text-slate-950">{item.value}</p></div>)}</div> : <p className="mt-4 text-sm text-slate-500">{empty}</p>}</section>;
}