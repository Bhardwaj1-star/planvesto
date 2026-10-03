"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorStatus } from "../../../components/InvestorUI";
import {
  getPlanningUnitId,
  getSelectedStrategyVersion,
  downloadGoalStrategyReportPdfByStrategyVersion,
  downloadCompleteFinancialPlanPdf,
  downloadBasketReportPdf,
} from "../../../lib/api/strategy";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";

type Goal = { id: string; name: string };
type Basket = { id: string; name: string; goalIds: string[] };

export default function ReportsPage() {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [baskets, setBaskets] = useState<Basket[]>([]);
  const [selectedBasketId, setSelectedBasketId] = useState("");
  const [customBasketGoalIds, setCustomBasketGoalIds] = useState<string[]>([]);
  const [selectedGoalId, setSelectedGoalId] = useState("");
  const [selectedReport, setSelectedReport] = useState("complete-financial-plan");
  const [selectedVersions, setSelectedVersions] = useState<Record<string, { strategy_version_id: string; strategy_id: string; version: number } | null>>({});
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const data = await loadGoalPlannerData();
        const next = (data?.goals ?? []).map((g) => ({
          id: g.id,
          name: g.name || "Untitled Goal",
        }));
        if (active) {
          setGoals(next);
          setSelectedGoalId(next[0]?.id ?? "");
          if (next.length >= 2) {
            setCustomBasketGoalIds([next[0].id, next[1].id]);
          }
        }
        try {
          const savedBaskets = JSON.parse(window.localStorage.getItem("planvesto:planning-baskets") || "[]");
          if (Array.isArray(savedBaskets) && savedBaskets.length > 0 && active) {
            setBaskets(savedBaskets);
            setSelectedBasketId(savedBaskets[0].id);
          }
        } catch {
          // ignore local storage errors
        }
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load goals.");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!selectedGoalId || selectedVersions[selectedGoalId] !== undefined) return;
    let active = true;
    (async () => {
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) return;
        const version = await getSelectedStrategyVersion(planningUnitId, selectedGoalId);
        if (active) setSelectedVersions((current) => ({ ...current, [selectedGoalId]: version }));
      } catch {
        if (active) setSelectedVersions((current) => ({ ...current, [selectedGoalId]: null }));
      }
    })();
    return () => { active = false; };
  }, [selectedGoalId, selectedVersions]);

  const selectedGoal = useMemo(() => goals.find((goal) => goal.id === selectedGoalId), [goals, selectedGoalId]);
  const selectedVersion = selectedGoalId ? selectedVersions[selectedGoalId] : null;
  const options = [
    {
      id: "complete-financial-plan",
      title: "Complete Financial Plan",
      description: "Consolidated plan across all goals, funding allocation, constraints, trade-offs and action plan.",
      available: true,
      reason: "",
    },
    {
      id: "basket-goal-report",
      title: "Goal Basket Decision Report",
      description: "Bundled multi-goal strategy for 2–3 grouped goals with priority laddering and shared pool allocation.",
      available: goals.length >= 2,
      reason: goals.length < 2 ? "Requires at least 2 active goals to bundle a basket." : "",
    },
    {
      id: "goal-strategy-report",
      title: "Individual Goal Report",
      description: "Complete strategy, calculation, feasibility and funding report for any selected goal (Retirement, Education, Home, etc.).",
      available: Boolean(selectedVersion?.strategy_version_id),
      reason: "Finalize the implementation for this goal first.",
    },
  ];

  async function download() {
    setWorking(true);
    setError(null);
    try {
      const planningUnitId = getPlanningUnitId();
      if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");

      let blob: Blob;
      let filename: string;

      if (selectedReport === "complete-financial-plan") {
        blob = await downloadCompleteFinancialPlanPdf(planningUnitId);
        filename = "complete-financial-plan.pdf";
      } else if (selectedReport === "basket-goal-report") {
        const basket = baskets.find((b) => b.id === selectedBasketId);
        const goalIds = basket ? basket.goalIds : (customBasketGoalIds.length >= 2 ? customBasketGoalIds : goals.slice(0, 3).map((g) => g.id));
        if (goalIds.length < 2) throw new Error("Please select at least 2 goals to generate a Basket Report.");
        blob = await downloadBasketReportPdf(planningUnitId, goalIds, basket?.name || "Goal Basket Planning Report");
        filename = "goal-basket-report.pdf";
      } else {
        if (!selectedVersion?.strategy_version_id) throw new Error("No finalized Strategy Version is available for this goal.");
        blob = await downloadGoalStrategyReportPdfByStrategyVersion(planningUnitId, selectedVersion.strategy_version_id);
        filename = "goal-report-" + (selectedGoal?.name || selectedGoalId).replace(/[^a-z0-9]+/gi, "-").toLowerCase() + ".pdf";
      }

      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = filename;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to generate report.");
    } finally {
      setWorking(false);
    }
  }

  if (loading) {
    return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-5xl"><div className="h-10 w-64 animate-pulse rounded-xl bg-slate-200" /><div className="mt-6 h-64 animate-pulse rounded-3xl bg-white" /></div></main>;
  }

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
      <InvestorHeader eyebrow="Reports" title="Your Financial Reports" description="Select a report to review or download. Availability is based on your current planning data and finalized Strategy Versions." />
      <div className="mx-auto max-w-5xl space-y-6 p-4 sm:p-6 lg:p-10">
        {error && <InvestorStatus tone="error">{error}</InvestorStatus>}

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-bold">Select Report</h2>
          <p className="mt-1 text-sm text-slate-500">Only reports currently available to you can be selected.</p>
          <div className="mt-5 grid gap-3">
            {options.map((option) => {
              const active = selectedReport === option.id;
              return (
                <button key={option.id} type="button" onClick={() => option.available && setSelectedReport(option.id)} disabled={!option.available}
                  className={"w-full rounded-2xl border p-4 text-left transition " + (active ? "border-teal-500 bg-teal-50" : "border-slate-200 bg-white hover:bg-slate-50") + (!option.available ? " cursor-not-allowed opacity-55" : "")}>
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <h3 className="font-extrabold">{option.title}</h3>
                      <p className="mt-1 text-sm text-slate-500">{option.description}</p>
                      {!option.available && <p className="mt-2 text-xs font-semibold text-amber-700">{option.reason}</p>}
                    </div>
                    <span className={"mt-1 h-4 w-4 shrink-0 rounded-full border " + (active ? "border-teal-600 bg-teal-600 ring-4 ring-teal-100" : "border-slate-300")} />
                  </div>
                </button>
              );
            })}
          </div>
        </section>

        {selectedReport === "basket-goal-report" && (
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="text-base font-bold text-navy-900">Choose Goals for Basket Report</h3>
            <p className="mt-1 text-xs text-slate-500">Select 2 to 3 goals to bundle into a combined decision report.</p>
            {baskets.length > 0 && (
              <div className="mt-3">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Saved Basket</span>
                <select
                  value={selectedBasketId}
                  onChange={(e) => setSelectedBasketId(e.target.value)}
                  className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold"
                >
                  {baskets.map((b) => (
                    <option key={b.id} value={b.id}>{b.name} ({b.goalIds.length} goals)</option>
                  ))}
                </select>
              </div>
            )}
            <div className="mt-4 space-y-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Or Select Individual Goals:</span>
              <div className="grid gap-2 sm:grid-cols-2">
                {goals.map((goal) => (
                  <label key={goal.id} className="flex cursor-pointer items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 p-3 hover:bg-slate-100">
                    <input
                      type="checkbox"
                      checked={customBasketGoalIds.includes(goal.id)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setCustomBasketGoalIds((curr) => [...curr, goal.id]);
                        } else {
                          setCustomBasketGoalIds((curr) => curr.filter((id) => id !== goal.id));
                        }
                      }}
                      className="h-4 w-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500"
                    />
                    <span className="text-sm font-semibold text-slate-800">{goal.name}</span>
                  </label>
                ))}
              </div>
            </div>
          </section>
        )}

        {selectedReport !== "complete-financial-plan" && selectedReport !== "basket-goal-report" && (
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <label className="block max-w-xl">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Select Goal</span>
              <select value={selectedGoalId} onChange={(event) => setSelectedGoalId(event.target.value)}
                className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold">
                {goals.map((goal) => <option key={goal.id} value={goal.id}>{goal.name}</option>)}
              </select>
            </label>
          </section>
        )}

        {selectedReport !== "complete-financial-plan" && selectedReport !== "basket-goal-report" && !selectedVersion?.strategy_version_id && (
          <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-center">
            <h3 className="font-bold">Report is not available yet</h3>
            <p className="mt-2 text-sm text-slate-500">Finalize the implementation for the selected goal first.</p>
            {selectedGoalId && <Link href={"/investor/strategy-builder?goalId=" + encodeURIComponent(selectedGoalId)} className="mt-5 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white">Open Strategy Builder</Link>}
          </section>
        )}

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-teal-700">Selected Report</p>
              <h2 className="mt-1 text-xl font-extrabold">{options.find((option) => option.id === selectedReport)?.title}</h2>
              <p className="mt-1 text-sm text-slate-500">
                {selectedReport === "complete-financial-plan"
                  ? "All goals"
                  : selectedReport === "basket-goal-report"
                  ? "2–3 grouped goals"
                  : selectedGoal?.name || "Select a goal"}
              </p>
            </div>
            <button
              type="button"
              onClick={() => void download()}
              disabled={
                working ||
                (selectedReport !== "complete-financial-plan" &&
                  selectedReport !== "basket-goal-report" &&
                  !selectedVersion?.strategy_version_id) ||
                (selectedReport === "basket-goal-report" && customBasketGoalIds.length < 2 && !selectedBasketId)
              }
              className="rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-50">
              {working ? "Generating…" : "Download PDF"}
            </button>
          </div>
        </section>
      </div>
    </main>
  );
}
