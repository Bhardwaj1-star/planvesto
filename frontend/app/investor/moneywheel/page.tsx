"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
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
  attention: "Needs attention",
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

const categories = [
  {
    key: "cash-flow",
    name: "Cash Flow",
    question: "Is your current income creating room for the future?",
    ratios: ["savings_ratio", "expense_ratio"],
    ratioNames: ["Savings Rate", "Essential Expense Ratio"],
  },
  {
    key: "liquidity",
    name: "Liquidity & Resilience",
    question: "Can your finances absorb a disruption without breaking?",
    ratios: ["emergency_fund_coverage", "current_liquidity_ratio"],
    ratioNames: ["Liquidity Coverage", "Current Liquidity Ratio"],
  },
  {
    key: "debt",
    name: "Debt & Solvency",
    question: "How much of your financial capacity is already committed?",
    ratios: ["debt_to_income_ratio", "leverage_ratio"],
    ratioNames: ["Debt Service Ratio", "Leverage Ratio"],
  },
  {
    key: "wealth",
    name: "Wealth",
    question: "How strong is your actual financial ownership?",
    ratios: ["solvency_ratio"],
    ratioNames: ["Net Worth / Solvency"],
  },
  {
    key: "investment",
    name: "Investment Structure",
    question: "Is your capital being deployed in a sustainable structure?",
    ratios: ["financial_asset_ratio", "liquid_asset_to_total_asset"],
    ratioNames: ["Investment Rate / Financial Asset Ratio", "Liquid Asset Share"],
  },
  {
    key: "goals",
    name: "Goal Readiness",
    question: "Is your current financial trajectory aligned with what you want to achieve?",
    ratios: ["goal_funding_ratio", "future_funding_ratio"],
    ratioNames: ["Goal Funding Ratio", "Future Funding Ratio"],
  },
  {
    key: "protection",
    name: "Financial Protection",
    question: "Would your financial plan remain resilient after a major financial shock?",
    ratios: ["insurance_gap_ratio"],
    ratioNames: ["Insurance Gap Ratio"],
  },
] as const;

function formatValue(ratio: MoneywheelRatio) {
  if (!ratio.available || ratio.value === null) return "Not available";
  const value = new Intl.NumberFormat("en-IN", { maximumFractionDigits: 2 }).format(ratio.value);
  return `${value}${ratio.unit ? ` ${ratio.unit}` : ""}`;
}

function getRatio(result: MoneywheelResult, key: string) {
  return result.ratios.find((ratio) => ratio.key === key);
}

function CategoryCard({
  category,
  result,
}: {
  category: (typeof categories)[number];
  result: MoneywheelResult;
}) {
  const ratios = category.ratios.map((key) => getRatio(result, key)).filter(Boolean) as MoneywheelRatio[];
  const available = ratios.filter((ratio) => ratio.available);

  return (
    <article className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="text-lg font-bold text-slate-900">{category.name}</h3>
          <p className="mt-2 text-sm leading-6 text-slate-500">{category.question}</p>
        </div>
        <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-500">
          {available.length}/{category.ratios.length} signals
        </span>
      </div>

      <div className="mt-5 space-y-3">
        {category.ratios.map((key, index) => {
          const ratio = getRatio(result, key);
          const fallbackName = category.ratioNames[index];
          if (!ratio) {
            return (
              <div key={key} className="rounded-2xl border border-dashed border-slate-200 bg-slate-50 p-4">
                <p className="text-sm font-semibold text-slate-700">{fallbackName}</p>
                <p className="mt-1 text-xs text-slate-400">Awaiting backend calculation</p>
              </div>
            );
          }

          return (
            <div key={ratio.key} className="rounded-2xl border border-slate-100 bg-slate-50/70 p-4">
              <div className="flex items-center justify-between gap-3">
                <p className="text-sm font-semibold text-slate-700">{ratio.name}</p>
                <span className={`rounded-full border px-2.5 py-1 text-[11px] font-bold ${statusClass[ratio.status]}`}>
                  {statusLabel[ratio.status]}
                </span>
              </div>
              <div className="mt-2 flex items-end justify-between gap-4">
                <p className="text-xl font-extrabold tracking-tight text-slate-900">{formatValue(ratio)}</p>
                <p className="max-w-[58%] text-right text-xs leading-5 text-slate-500">{ratio.explanation}</p>
              </div>
            </div>
          );
        })}
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

  const availableRatioCount = useMemo(
    () => result?.ratios.filter((ratio) => ratio.available).length ?? 0,
    [result],
  );

  if (loading) {
    return (
      <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
        <div className="mx-auto max-w-6xl space-y-6">
          <div className="h-10 w-56 animate-pulse rounded-xl bg-slate-200" />
          <div className="h-80 animate-pulse rounded-3xl bg-white" />
          <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
            <div className="h-56 animate-pulse rounded-3xl bg-white" />
            <div className="h-56 animate-pulse rounded-3xl bg-white" />
            <div className="h-56 animate-pulse rounded-3xl bg-white" />
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
      <div className="mx-auto max-w-6xl space-y-8">
        <header className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.16em] text-teal-700">Financial Health</p>
            <h1 className="mt-1 text-3xl font-extrabold tracking-tight text-slate-900">Moneywheel</h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
              Numbers and ratios are signals. Moneywheel brings those signals together to show what your financial position is saying.
            </p>
          </div>
          <button
            onClick={() => void recalculate()}
            disabled={calculating}
            className="rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white transition hover:bg-navy-800 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {calculating ? "Calculating…" : "Refresh assessment"}
          </button>
        </header>

        {error && <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">{error}</div>}

        {!result ? (
          <section className="rounded-3xl border border-slate-200 bg-white p-10 text-center shadow-sm">
            <h2 className="text-xl font-bold text-slate-900">Your financial signals are not available yet</h2>
            <p className="mt-2 text-sm text-slate-500">Moneywheel will use the latest Financial State calculated by Planvesto&apos;s backend.</p>
            <button onClick={() => void recalculate()} disabled={calculating} className="mt-6 rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white disabled:opacity-60">
              Refresh assessment
            </button>
          </section>
        ) : (
          <>
            <section className="rounded-3xl border border-slate-200 bg-white p-7 shadow-sm">
              <div className="grid items-center gap-8 lg:grid-cols-[280px_1fr]">
                <div className="mx-auto flex h-64 w-64 items-center justify-center rounded-full p-4" style={{ background: "conic-gradient(from -90deg, #0f766e 0deg 51.43deg, #0f172a 51.43deg 102.86deg, #334155 102.86deg 154.29deg, #64748b 154.29deg 205.72deg, #0d9488 205.72deg 257.15deg, #475569 257.15deg 308.58deg, #94a3b8 308.58deg 360deg)" }}>
                  <div className="flex h-44 w-44 flex-col items-center justify-center rounded-full bg-white text-center shadow-inner">
                    <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-400">Moneywheel</p>
                    <p className="mt-2 text-2xl font-extrabold text-slate-900">Financial</p>
                    <p className="text-2xl font-extrabold text-slate-900">Condition</p>
                  </div>
                </div>

                <div>
                  <p className="text-sm font-semibold text-slate-500">What your numbers are saying</p>
                  <h2 className="mt-1 text-2xl font-extrabold tracking-tight text-slate-900">Your financial position has seven dimensions</h2>
                  <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
                    Each spoke is interpreted from underlying financial ratios. The ratios themselves are calculated by the backend; this screen is only their presentation and interpretation layer.
                  </p>
                  <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
                    {categories.map((category, index) => (
                      <div key={category.key} className="flex items-center gap-3 rounded-2xl border border-slate-100 bg-slate-50 p-3">
                        <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-white text-xs font-bold text-slate-600 shadow-sm">{index + 1}</span>
                        <span className="text-sm font-semibold text-slate-700">{category.name}</span>
                      </div>
                    ))}
                  </div>
                  <p className="mt-5 text-xs text-slate-400">{availableRatioCount} backend signals currently available.</p>
                </div>
              </div>
            </section>

            <section>
              <div className="mb-5">
                <h2 className="text-xl font-extrabold tracking-tight text-slate-900">What the ratios are telling you</h2>
                <p className="mt-1 text-sm text-slate-500">The numbers are evidence. The financial meaning comes from understanding the signal behind them.</p>
              </div>
              <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
                {categories.map((category) => (
                  <CategoryCard key={category.key} category={category} result={result} />
                ))}
              </div>
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Assessment history</h2>
                <p className="mt-1 text-sm text-slate-500">Previous Moneywheel assessments calculated by the backend.</p>
              </div>
              {history.length === 0 ? (
                <p className="mt-6 rounded-2xl bg-slate-50 p-5 text-sm text-slate-500">No previous assessments are available.</p>
              ) : (
                <div className="mt-5 space-y-3">
                  {history.map((item) => (
                    <div key={item.calculated_at} className="flex flex-col justify-between gap-2 rounded-2xl border border-slate-100 p-4 sm:flex-row sm:items-center">
                      <div>
                        <p className="text-sm font-semibold text-slate-800">{new Date(item.calculated_at).toLocaleString("en-IN")}</p>
                        <p className="text-xs text-slate-400">{item.rule_set_version}</p>
                      </div>
                      <p className="text-sm text-slate-500">{item.ratios.filter((ratio) => ratio.available).length} signals available</p>
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
