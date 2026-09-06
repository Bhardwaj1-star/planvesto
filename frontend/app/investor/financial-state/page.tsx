"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { loadOnboardingData, type OnboardingData } from "../../../lib/onboarding/persistence";

function monthlyAmount(amount: string, frequency: string) {
  const value = Number(amount) || 0;
  return frequency.toLowerCase() === "annual" ? value / 12 : value;
}

function formatAmount(value: number) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(value);
}

function sumValues(values: string[]) {
  return values.reduce((total, value) => total + (Number(value) || 0), 0);
}

export default function FinancialStatePage() {
  const [data, setData] = useState<OnboardingData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    loadOnboardingData()
      .then((loaded) => {
        if (active) setData(loaded);
      })
      .catch((cause: unknown) => {
        if (active) setError(cause instanceof Error ? cause.message : "Unable to load your financial state.");
      })
      .finally(() => {
        if (active) setIsLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const monthlyIncome = data?.incomeSources.reduce((total, item) => total + monthlyAmount(item.amount, item.frequency), 0) || 0;
  const monthlyExpenses = data?.expenses.reduce((total, item) => total + monthlyAmount(item.amount, item.frequency), 0) || 0;
  const assets = data ? sumValues(data.assets.map((item) => item.currentValue)) : 0;
  const liabilities = data ? sumValues(data.liabilities.map((item) => item.outstandingAmount)) : 0;
  const commitments = data ? sumValues(data.commitments.map((item) => item.amount)) : 0;

  return (
    <div className="min-h-screen bg-[#f6f8fb] text-slate-900">
      <div className="flex min-h-screen"><main className="min-w-0 flex-1">
        <header className="border-b border-slate-200 bg-white"><div className="flex min-h-[80px] items-center justify-between gap-6 px-5 lg:px-8"><div><p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-400">Investor Dashboard</p><h1 className="mt-1 text-2xl font-extrabold tracking-tight text-slate-950 sm:text-3xl">Financial State</h1></div><div className="flex items-center gap-4"><Link href="/investor/goal-planner" className="text-sm font-bold text-teal-700 hover:text-teal-900">Goal Planner</Link><Link href="/investor" className="text-sm font-bold text-slate-600 hover:text-slate-950">Back to dashboard</Link></div></div></header>
        <div className="space-y-6 p-5 lg:p-8"><section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:p-8"><p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">Where you are today</p><h2 className="mt-2 text-2xl font-extrabold tracking-tight text-slate-950">Your current financial situation</h2><p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">Income, expenses, assets, liabilities and commitments from your financial plan.</p></section>
          {isLoading && <section className="rounded-3xl border border-slate-200 bg-white p-7 text-sm font-semibold text-slate-500 shadow-sm">Loading your financial state...</section>}
          {error && <section className="rounded-3xl border border-red-200 bg-red-50 p-7 text-sm font-semibold text-red-700" role="alert">{error}</section>}
          {!isLoading && !error && data && <>
            <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5"><StateMetric label="Monthly Income" value={monthlyIncome} /><StateMetric label="Monthly Expenses" value={monthlyExpenses} /><StateMetric label="Assets" value={assets} /><StateMetric label="Liabilities" value={liabilities} /><StateMetric label="Commitments" value={commitments} /></section>
            {!data.incomeSources.length && !data.expenses.length && !data.assets.length && !data.liabilities.length && !data.commitments.length && <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-center shadow-sm"><h2 className="text-lg font-extrabold text-slate-950">Your financial state is empty</h2><p className="mt-2 text-sm text-slate-500">Complete the onboarding sections to see your current position here.</p><Link href="/investor/onboarding/personal-information" className="mt-5 inline-flex rounded-xl bg-slate-950 px-5 py-3 text-sm font-bold text-white hover:bg-slate-800">Continue onboarding</Link></section>}
            <section className="grid gap-6 xl:grid-cols-2"><DataList title="Income" empty="No income sources added." items={data.incomeSources.map((item) => ({ label: item.incomeType, value: formatAmount(monthlyAmount(item.amount, item.frequency)) }))} /><DataList title="Expenses" empty="No expenses added." items={data.expenses.map((item) => ({ label: item.category, value: formatAmount(monthlyAmount(item.amount, item.frequency)) }))} /><DataList title="Assets" empty="No assets added." items={data.assets.map((item) => ({ label: item.description ? `${item.assetType} - ${item.description}` : item.assetType, value: formatAmount(Number(item.currentValue) || 0) }))} /><DataList title="Liabilities" empty="No liabilities added." items={data.liabilities.map((item) => ({ label: item.description ? `${item.liabilityType} - ${item.description}` : item.liabilityType, value: formatAmount(Number(item.outstandingAmount) || 0) }))} /><DataList title="Commitments" empty="No commitments added." items={data.commitments.map((item) => ({ label: item.name, value: formatAmount(Number(item.amount) || 0) }))} /></section>
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