"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { InvestorProfileMenu } from "../../../components/InvestorProfileMenu";
import {
  FinancialState,
  getFinancialStateHistory,
  getLatestFinancialState,
  getPlanningUnitId,
  Metric,
} from "../../../lib/api/financial-state";

type Period = "Monthly" | "Annual";
type Detail = "assets" | "liabilities" | "liquidity" | "history" | null;

const money = new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
  maximumFractionDigits: 0,
});

function amount(metric: Metric, period: Period = "Monthly") {
  if (!metric?.available || metric.value === null) return "Unavailable";
  return money.format(metric.value);
}

function numberValue(metric: Metric) {
  if (!metric?.available || metric.value === null) return "Unavailable";
  return metric.value.toLocaleString("en-IN", { maximumFractionDigits: 2 });
}

function MetricCard({ label, metric, period }: { label: string; metric?: Metric; period?: Period }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-xs font-bold uppercase tracking-wide text-slate-400">{label}</p>
      <p className="mt-3 text-2xl font-extrabold tracking-tight text-slate-950">
        {amount(metric as Metric, period)}
      </p>
      {!metric?.available && metric?.reason && (
        <p className="mt-2 text-xs leading-5 text-slate-500">{metric.reason}</p>
      )}
    </div>
  );
}

function SnapshotRow({ snapshot, onSelect }: { snapshot: FinancialState; onSelect: () => void }) {
  return (
    <button
      type="button"
      onClick={onSelect}
      className="flex w-full items-center justify-between gap-4 rounded-xl border border-slate-200 bg-white p-4 text-left transition hover:border-teal-300 hover:bg-slate-50"
    >
      <div>
        <p className="text-sm font-bold text-slate-900">
          {snapshot.created_at ? new Date(snapshot.created_at).toLocaleString("en-IN") : "Snapshot"}
        </p>
        <p className="mt-1 text-xs text-slate-500">
          {snapshot.scope === "individual" ? "Individual" : "Family"} financial snapshot
        </p>
      </div>
      <span className="text-xs font-bold text-teal-700">View →</span>
    </button>
  );
}

export default function FinancialStatePage() {
  const [data, setData] = useState<FinancialState | null>(null);
  const [history, setHistory] = useState<FinancialState[]>([]);
  const [period, setPeriod] = useState<Period>("Monthly");
  const [detail, setDetail] = useState<Detail>(null);
  const [loading, setLoading] = useState(true);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [historyError, setHistoryError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const planningUnitId = getPlanningUnitId();
      if (!planningUnitId) {
        setData(null);
        setLoading(false);
        return;
      }
      const latest = await getLatestFinancialState(planningUnitId);
      setData(latest);
    } catch (cause) {
      setData(null);
      setError(cause instanceof Error ? cause.message : "Unable to load Financial State.");
    } finally {
      setLoading(false);
    }
  }

  async function loadHistory() {
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId) return;
    setHistoryLoading(true);
    setHistoryError(null);
    try {
      setHistory(await getFinancialStateHistory(planningUnitId));
    } catch (cause) {
      setHistoryError(cause instanceof Error ? cause.message : "Unable to load Financial State history.");
    } finally {
      setHistoryLoading(false);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  useEffect(() => {
    if (detail === "history") void loadHistory();
  }, [detail]);

  const isAnnual = period === "Annual";
  const income = isAnnual ? data?.income_annual : data?.income_monthly;
  const expenses = isAnnual ? data?.expenses_annual : data?.expenses_monthly;
  const surplus = isAnnual ? data?.investable_surplus_annual : data?.investable_surplus_monthly;

  const hasBreakdown = useMemo(
    () => Boolean(data && (data.income_breakdown?.length || data.expense_breakdown?.length || data.asset_breakdown?.length || data.liability_breakdown?.length)),
    [data],
  );

  if (loading) {
    return (
      <main className="min-w-0 flex-1 p-5 lg:p-8" aria-busy="true">
        <div className="mx-auto max-w-6xl space-y-6">
          <div className="h-8 w-72 animate-pulse rounded-lg bg-slate-200" />
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {[1, 2, 3, 4].map((item) => <div key={item} className="h-32 animate-pulse rounded-2xl bg-white shadow-sm" />)}
          </div>
          <div className="h-56 animate-pulse rounded-3xl bg-white shadow-sm" />
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-w-0 flex-1 p-5 lg:p-8">
        <div className="mx-auto max-w-2xl rounded-3xl border border-slate-200 bg-white p-10 text-center shadow-sm">
          <h1 className="text-2xl font-extrabold text-slate-950">Unable to load Financial State</h1>
          <p className="mx-auto mt-3 max-w-lg text-sm leading-6 text-slate-500">{error}</p>
          <div className="mt-6 flex justify-center gap-3">
            <button type="button" onClick={() => void load()} className="rounded-xl bg-slate-950 px-5 py-2.5 text-sm font-bold text-white">Retry</button>
            <Link href="/investor/onboarding" className="rounded-xl border border-slate-200 px-5 py-2.5 text-sm font-bold text-slate-700">Review information</Link>
          </div>
        </div>
      </main>
    );
  }

  if (!data) {
    return (
      <main className="min-w-0 flex-1 p-5 lg:p-8">
        <div className="mx-auto max-w-2xl rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center shadow-sm">
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">Financial State</p>
          <h1 className="mt-2 text-2xl font-extrabold text-slate-950">Your Financial State is not available yet</h1>
          <p className="mx-auto mt-3 max-w-lg text-sm leading-6 text-slate-500">Complete your financial information first. Planvesto will calculate and persist the Financial State through the backend.</p>
          <Link href="/investor/onboarding" className="mt-6 inline-flex rounded-xl bg-slate-950 px-5 py-3 text-sm font-bold text-white">Continue onboarding →</Link>
        </div>
      </main>
    );
  }

  return (
    <main className="min-w-0 flex-1 pb-20">
      <header className="border-b border-slate-200 bg-white">
        <div className="flex min-h-[80px] items-center justify-between gap-4 px-5 lg:px-8">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-700">Current Financial State</p>
            <h1 className="mt-1 text-2xl font-extrabold tracking-tight text-slate-950 sm:text-3xl">Financial State</h1>
            <p className="mt-1 text-xs text-slate-500">{data.scope === "individual" ? "Individual" : "Family"} · backend snapshot</p>
          </div>
          <div className="flex items-center gap-3">
            <div className="inline-flex rounded-xl border border-slate-200 bg-slate-100 p-1">
              {(["Monthly", "Annual"] as Period[]).map((item) => (
                <button key={item} type="button" onClick={() => setPeriod(item)} className={`rounded-lg px-3.5 py-1.5 text-xs font-bold ${period === item ? "bg-white text-slate-950 shadow-sm" : "text-slate-500"}`}>{item}</button>
              ))}
            </div>
            <InvestorProfileMenu />
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-6xl space-y-8 p-5 lg:p-8">
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:p-8">
          <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">Where you stand today</p>
              <h2 className="mt-1 text-2xl font-extrabold text-slate-950">Current Financial Position</h2>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">A backend-calculated snapshot of your current financial position. Calculated values are not edited on this screen.</p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Link href="/investor/onboarding/income" className="rounded-xl border border-slate-200 px-3.5 py-2 text-xs font-bold text-slate-700">Update Income</Link>
              <Link href="/investor/onboarding/expenses" className="rounded-xl border border-slate-200 px-3.5 py-2 text-xs font-bold text-slate-700">Update Expenses</Link>
              <Link href="/investor/onboarding/assets" className="rounded-xl border border-slate-200 px-3.5 py-2 text-xs font-bold text-slate-700">Update Assets</Link>
              <Link href="/investor/onboarding/liabilities" className="rounded-xl border border-slate-200 px-3.5 py-2 text-xs font-bold text-slate-700">Update Liabilities</Link>
            </div>
          </div>
        </section>

        <section>
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Key Metrics · {period}</h3>
            <button type="button" onClick={() => { setDetail("history"); }} className="text-xs font-bold text-teal-700">View history →</button>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <MetricCard label="Income" metric={income!} period={period} />
            <MetricCard label="Expenses" metric={expenses!} period={period} />
            <MetricCard label="Investable Surplus" metric={surplus!} period={period} />
            <MetricCard label="Net Worth" metric={data.net_worth} />
          </div>
        </section>

        <section className="grid gap-4 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Cash Flow Ratio</p>
            <p className="mt-3 text-2xl font-extrabold text-slate-950">{numberValue(data.cash_flow_ratio)}</p>
            {!data.cash_flow_ratio?.available && data.cash_flow_ratio?.reason && <p className="mt-2 text-xs text-slate-500">{data.cash_flow_ratio.reason}</p>}
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Savings / Investment Rate</p>
            <p className="mt-3 text-2xl font-extrabold text-slate-950">{numberValue(data.savings_investment_rate)}</p>
            {!data.savings_investment_rate?.available && data.savings_investment_rate?.reason && <p className="mt-2 text-xs text-slate-500">{data.savings_investment_rate.reason}</p>}
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Safety Reserve</p>
            <p className="mt-3 text-2xl font-extrabold text-slate-950">{numberValue(data.safety_reserve_months)} months</p>
            <p className="mt-2 text-xs text-slate-500">Required amount: {amount(data.safety_reserve_required_amount)}</p>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-2">
          <button type="button" onClick={() => setDetail("assets")} className="rounded-3xl border border-slate-200 bg-white p-6 text-left shadow-sm transition hover:border-teal-300">
            <div className="flex items-center justify-between"><h3 className="text-lg font-extrabold text-slate-950">Assets</h3><span className="text-xs font-bold text-teal-700">View details →</span></div>
            <p className="mt-2 text-2xl font-extrabold text-slate-950">{amount(data.total_assets)}</p>
            <p className="mt-2 text-sm text-slate-500">{(data.asset_breakdown ?? []).length} recorded asset entries</p>
          </button>
          <button type="button" onClick={() => setDetail("liabilities")} className="rounded-3xl border border-slate-200 bg-white p-6 text-left shadow-sm transition hover:border-teal-300">
            <div className="flex items-center justify-between"><h3 className="text-lg font-extrabold text-slate-950">Liabilities</h3><span className="text-xs font-bold text-teal-700">View details →</span></div>
            <p className="mt-2 text-2xl font-extrabold text-slate-950">{amount(data.total_liabilities)}</p>
            <p className="mt-2 text-sm text-slate-500">EMI burden: {amount(data.emi_burden_monthly)}</p>
          </button>
        </section>

        {hasBreakdown && (
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:p-8">
            <div className="flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">Cash flow</p><h3 className="mt-1 text-xl font-extrabold text-slate-950">Income & Expenses</h3></div><Link href="/investor/onboarding/income" className="text-xs font-bold text-teal-700">Update inputs →</Link></div>
            <div className="mt-6 grid gap-6 lg:grid-cols-2">
              <div><h4 className="text-sm font-bold text-slate-800">Income breakdown</h4><div className="mt-3 space-y-2">{(data.income_breakdown ?? []).map((item) => <div key={item.type} className="flex justify-between border-b border-slate-100 py-2 text-sm"><span className="text-slate-600">{item.type}</span><span className="font-semibold text-slate-900">{money.format(isAnnual ? item.annual : item.monthly)}</span></div>)}</div></div>
              <div><h4 className="text-sm font-bold text-slate-800">Expense breakdown</h4><div className="mt-3 space-y-2">{(data.expense_breakdown ?? []).map((item) => <div key={item.type} className="flex justify-between border-b border-slate-100 py-2 text-sm"><span className="text-slate-600">{item.type}</span><span className="font-semibold text-slate-900">{money.format(isAnnual ? item.annual : item.monthly)}</span></div>)}</div></div>
            </div>
          </section>
        )}
      </div>

      {detail && (
        <div className="fixed inset-0 z-50 bg-slate-950/30 p-4 sm:p-8" role="dialog" aria-modal="true">
          <div className="mx-auto flex h-full max-w-3xl flex-col overflow-hidden rounded-3xl bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-200 p-5 sm:p-6"><div><p className="text-xs font-bold uppercase tracking-wider text-teal-700">Financial State</p><h2 className="mt-1 text-xl font-extrabold text-slate-950">{detail === "history" ? "Snapshot History" : detail === "assets" ? "Asset Details" : "Liability Details"}</h2></div><button type="button" onClick={() => setDetail(null)} className="rounded-xl border border-slate-200 px-3 py-2 text-xs font-bold text-slate-700">Close</button></div>
            <div className="flex-1 overflow-y-auto p-5 sm:p-6">
              {detail === "assets" && <div className="space-y-3">{(data.asset_breakdown ?? []).map((item) => <div key={item.asset_id} className="rounded-2xl border border-slate-200 p-4"><div className="flex justify-between gap-4"><div><p className="font-bold text-slate-900">{item.name}</p><p className="mt-1 text-xs text-slate-500">Liquidity: {item.liquidity ?? "Unavailable"}</p></div><p className="font-extrabold text-slate-950">{money.format(item.ownership_applied)}</p></div></div>)}</div>}
              {detail === "liabilities" && <div className="space-y-3">{(data.liability_breakdown ?? []).map((item) => <div key={item.liability_id} className="rounded-2xl border border-slate-200 p-4"><div className="flex justify-between gap-4"><div><p className="font-bold text-slate-900">{item.name}</p><p className="mt-1 text-xs text-slate-500">Classification: {item.classification ?? "Unavailable"}</p></div><p className="font-extrabold text-slate-950">{money.format(item.responsibility_applied)}</p></div></div>)}</div>}
              {detail === "history" && <div className="space-y-3">{historyLoading && <p className="text-sm text-slate-500">Loading snapshots…</p>}{historyError && <div className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-600">{historyError}</div>}{!historyLoading && !historyError && history.length === 0 && <p className="text-sm text-slate-500">No previous snapshots are available.</p>}{history.map((snapshot) => <SnapshotRow key={snapshot.snapshot_id ?? `${snapshot.created_at}-${snapshot.planning_unit_id}`} snapshot={snapshot} onSelect={() => undefined} />)}</div>}
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
