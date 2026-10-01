"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorStatus } from "../../../components/InvestorUI";
import {
  getPlanningUnitId,
  getLatestStrategyRun,
  downloadGoalStrategyReportPdf,
  downloadCompleteFinancialPlanPdf,
  downloadRetirementReportPdf,
  type StrategyRun,
} from "../../../lib/api/strategy";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";

type Goal = { id: string; name: string; type?: string | null };

export default function ReportsPage() {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [selectedGoalId, setSelectedGoalId] = useState("");
  const [selectedReport, setSelectedReport] = useState("complete-financial-plan");
  const [runs, setRuns] = useState<Record<string, StrategyRun | null>>({});
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
          type: g.goalType ?? g.goal_type ?? null,
        }));
        if (active) {
          setGoals(next);
          setSelectedGoalId(next[0]?.id ?? "");
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
    if (!selectedGoalId || runs[selectedGoalId] !== undefined) return;
    let active = true;
    (async () => {
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) return;
        const run = await getLatestStrategyRun(planningUnitId, selectedGoalId);
        if (active) setRuns((current) => ({ ...current, [selectedGoalId]: run }));
      } catch {
        if (active) setRuns((current) => ({ ...current, [selectedGoalId]: null }));
      }
    })();
    return () => { active = false; };
  }, [selectedGoalId, runs]);

  const selectedGoal = useMemo(() => goals.find((goal) => goal.id === selectedGoalId), [goals, selectedGoalId]);
  const selectedRun = selectedGoalId ? runs[selectedGoalId] : null;
  const isRetirement = /retirement|financial freedom/i.test((selectedGoal?.type || "") + " " + (selectedGoal?.name || ""));

  const options = [
    {
      id: "complete-financial-plan",
      title: "Complete Financial Plan",
      description: "Consolidated plan across all goals, funding allocation, constraints, trade-offs and action plan.",
      available: true,
      reason: "",
    },
    {
      id: "goal-strategy-report",
      title: "Individual Goal Report",
      description: "Complete strategy, calculation, feasibility and funding report for one selected goal.",
      available: Boolean(selectedRun?.strategy_run_id),
      reason: "Build a Strategy Run for this goal first.",
    },
    {
      id: "retirement-report",
      title: "Retirement Report",
      description: "Retirement-specific report for a completed retirement Strategy Run.",
      available: Boolean(isRetirement && selectedRun?.strategy_run_id),
      reason: isRetirement ? "Build a Strategy Run for the retirement goal first." : "Only available for a retirement goal.",
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
      } else {
        if (!selectedRun?.strategy_run_id) throw new Error("No completed Strategy Run is available for this goal.");
        if (selectedReport === "goal-strategy-report") {
          blob = await downloadGoalStrategyReportPdf(planningUnitId, selectedRun.strategy_run_id);
          filename = "goal-report-" + (selectedGoal?.name || selectedGoalId).replace(/[^a-z0-9]+/gi, "-").toLowerCase() + ".pdf";
        } else {
          blob = await downloadRetirementReportPdf(planningUnitId, selectedRun.strategy_run_id);
          filename = "retirement-planning-report.pdf";
        }
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
      <InvestorHeader eyebrow="Reports" title="Your Financial Reports" description="Select a report to review or download. Availability is based on your current planning data and completed Strategy Runs." />
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

        {selectedReport !== "complete-financial-plan" && (
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

        {selectedReport !== "complete-financial-plan" && !selectedRun?.strategy_run_id && (
          <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-center">
            <h3 className="font-bold">Report is not available yet</h3>
            <p className="mt-2 text-sm text-slate-500">Build the Strategy Run for the selected goal first.</p>
            {selectedGoalId && <Link href={"/investor/strategy-builder?goalId=" + encodeURIComponent(selectedGoalId)} className="mt-5 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white">Open Strategy Builder</Link>}
          </section>
        )}

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-teal-700">Selected Report</p>
              <h2 className="mt-1 text-xl font-extrabold">{options.find((option) => option.id === selectedReport)?.title}</h2>
              <p className="mt-1 text-sm text-slate-500">{selectedReport === "complete-financial-plan" ? "All goals" : selectedGoal?.name || "Select a goal"}</p>
            </div>
            <button type="button" onClick={() => void download()} disabled={working || (selectedReport !== "complete-financial-plan" && !selectedRun?.strategy_run_id)}
              className="rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-50">
              {working ? "Generating…" : "Download PDF"}
            </button>
          </div>
        </section>
      </div>
    </main>
  );
}
