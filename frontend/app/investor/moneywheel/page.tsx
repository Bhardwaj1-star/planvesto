"use client";

import { useCallback, useEffect, useState } from "react";
import { getPlanningUnitId, getLatestFinancialState } from "../../../lib/api/financial-state";
import {
  calculateMoneywheel,
  getLatestMoneywheel,
  getMoneywheelHistory,
  type MoneywheelResult,
  type MoneywheelRatio,
  type MoneywheelStatus,
} from "../../../lib/api/moneywheel";

const statusLabel: Record<MoneywheelStatus, string> = {
  excellent: "Excellent",
  healthy: "Healthy",
  attention: "Attention",
  critical: "Critical",
  unavailable: "Unavailable",
};

const statusClass: Record<MoneywheelStatus, string> = {
  excellent: "bg-emerald-50 text-emerald-700 border-emerald-200",
  healthy: "bg-teal-50 text-teal-700 border-teal-200",
  attention: "bg-amber-50 text-amber-700 border-amber-200",
  critical: "bg-red-50 text-red-700 border-red-200",
  unavailable: "bg-slate-50 text-slate-500 border-slate-200",
};

function formatValue(ratio: MoneywheelRatio) {
  if (!ratio.available || ratio.value === null) return "—";
  const value = new Intl.NumberFormat("en-IN", { maximumFractionDigits: 2 }).format(ratio.value);
  return `${value}${ratio.unit ? ` ${ratio.unit}` : ""}`;
}

function RatioCard({ ratio }: { ratio: MoneywheelRatio }) {
  return (
    <article className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-slate-500">{ratio.name}</p>
          <p className="mt-3 text-3xl font-extrabold tracking-tight text-slate-900">{formatValue(ratio)}</p>
        </div>
        <span className={`rounded-full border px-2.5 py-1 text-xs font-bold ${statusClass[ratio.status]}`}>
          {statusLabel[ratio.status]}
        </span>
      </div>
      <div className="mt-5 border-t border-slate-100 pt-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Formula</p>
        <p className="mt-1 text-sm text-slate-600">{ratio.formula || "Not provided"}</p>
        <p className="mt-3 text-sm leading-6 text-slate-500">{ratio.explanation}</p>
      </div>
    </article>
  );
}

export default function MoneywheelPage() {
  const [result, setResult] = useState<MoneywheelResult | null>(null);
  const [history, setHistory] = useState<MoneywheelResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [calculating, setCalculating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const planningUnitId = getPlanningUnitId();
      if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
      const [latest, past] = await Promise.all([
        getLatestMoneywheel(planningUnitId),
        getMoneywheelHistory(planningUnitId),
      ]);
      setResult(latest);
      setHistory(past ?? []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load Moneywheel.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void load(); }, [load]);

  const recalculate = async () => {
    setCalculating(true);
    setError(null);
    try {
      const planningUnitId = getPlanningUnitId();
      if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
      const financialState = await getLatestFinancialState(planningUnitId);
      const next = await calculateMoneywheel(
        planningUnitId,
        financialState as unknown as Record<string, unknown>,
      );
      setResult(next);
      setHistory(await getMoneywheelHistory(planningUnitId));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to calculate Moneywheel.");
    } finally {
      setCalculating(false);
    }
  };

  if (loading) {
    return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-6xl space-y-6"><div className="h-10 w-56 animate-pulse rounded-xl bg-slate-200" /><div className="h-28 animate-pulse rounded-3xl bg-white" /><div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3"><div className="h-56 animate-pulse rounded-3xl bg-white" /><div className="h-56 animate-pulse rounded-3xl bg-white" /><div className="h-56 animate-pulse rounded-3xl bg-white" /></div></div></main>;
  }

  const ratios = result?.ratios ?? [];

  return (
    <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
      <div className="mx-auto max-w-6xl space-y-8">
        <header className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.16em] text-teal-700">Financial Health</p>
            <h1 className="mt-1 text-3xl font-extrabold tracking-tight text-slate-900">Moneywheel</h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">Nine financial ratios showing the current structure of your financial position. The calculations and status rules come from Planvesto&apos;s backend.</p>
          </div>
          <button onClick={() => void recalculate()} disabled={calculating} className="rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white transition hover:bg-navy-800 disabled:cursor-not-allowed disabled:opacity-60">
            {calculating ? "Calculating…" : "Recalculate"}
          </button>
        </header>

        {error && <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">{error}</div>}

        {!result ? (
          <section className="rounded-3xl border border-slate-200 bg-white p-10 text-center shadow-sm">
            <h2 className="text-xl font-bold text-slate-900">Moneywheel has not been calculated yet</h2>
            <p className="mt-2 text-sm text-slate-500">Calculate it from your latest Financial State to populate the nine ratios.</p>
            <button onClick={() => void recalculate()} disabled={calculating} className="mt-6 rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white disabled:opacity-60">Calculate Moneywheel</button>
          </section>
        ) : (
          <>
            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
                <div>
                  <p className="text-sm font-semibold text-slate-500">Current assessment</p>
                  <p className="mt-1 text-sm text-slate-600">Calculated {new Date(result.calculated_at).toLocaleString("en-IN")}</p>
                </div>
                <div className="text-sm text-slate-500">Rule set: <span className="font-semibold text-slate-700">{result.rule_set_version}</span></div>
              </div>
            </section>

            <section className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
              {ratios.map((ratio) => <RatioCard key={ratio.key} ratio={ratio} />)}
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between gap-4">
                <div><h2 className="text-lg font-bold text-slate-900">History</h2><p className="mt-1 text-sm text-slate-500">Previous Moneywheel calculations.</p></div>
              </div>
              {history.length === 0 ? (
                <p className="mt-6 rounded-2xl bg-slate-50 p-5 text-sm text-slate-500">No previous calculations are available.</p>
              ) : (
                <div className="mt-5 space-y-3">
                  {history.map((item) => (
                    <div key={item.calculated_at} className="flex flex-col justify-between gap-2 rounded-2xl border border-slate-100 p-4 sm:flex-row sm:items-center">
                      <div><p className="text-sm font-semibold text-slate-800">{new Date(item.calculated_at).toLocaleString("en-IN")}</p><p className="text-xs text-slate-400">{item.rule_set_version}</p></div>
                      <p className="text-sm text-slate-500">{item.ratios.filter((ratio) => ratio.available).length}/9 ratios available</p>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </>
        )}
      </div>
    </main>
  );
}
