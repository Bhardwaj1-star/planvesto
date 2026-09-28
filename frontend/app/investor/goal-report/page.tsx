"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import StrategyWorkflowNav from "../../../components/StrategyWorkflowNav";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorStatus } from "../../../components/InvestorUI";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";
import { getPlanningUnitId, getLatestStrategyRun, getGoalStrategyReport, downloadGoalStrategyReportPdf, type GoalStrategyReport } from "../../../lib/api/strategy";

export default function GoalReportPage() {
  const [report, setReport] = useState<GoalStrategyReport | null>(null);
  const [working, setWorking] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
        const data = await loadGoalPlannerData();
        const goals = data?.goals ?? [];
        const requested = typeof window !== "undefined" ? new URLSearchParams(window.location.search).get("goalId") : null;
        const candidates = requested ? goals.filter((item) => item.id === requested) : goals;
        if (!candidates.length) throw new Error("No goal is available for reporting.");

        let selectedRun: Awaited<ReturnType<typeof getLatestStrategyRun>> | null = null;
        for (const goal of candidates) {
          try {
            const candidate = await getLatestStrategyRun(planningUnitId, goal.id);
            if (candidate.strategy_run_id && (!selectedRun || String(candidate.created_at ?? "") > String(selectedRun.created_at ?? ""))) selectedRun = candidate;
          } catch {
            // Skip goals that do not yet have a Strategy Run.
          }
        }
        if (!selectedRun?.strategy_run_id) throw new Error("No completed Strategy Run is available for the selected goal.");
        const next = await getGoalStrategyReport(planningUnitId, selectedRun.strategy_run_id);
        if (active) setReport(next);
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load goal report.");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, []);

  const download = async () => {
    if (!report) return;
    setWorking(true); setError(null);
    try {
      const planningUnitId = getPlanningUnitId();
      if (!planningUnitId) throw new Error("Planning unit is not available.");
      const blob = await downloadGoalStrategyReportPdf(planningUnitId, report.strategy_run_id);
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `goal-strategy-report-${report.strategy_run_id}.pdf`;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to download PDF.");
    } finally {
      setWorking(false);
    }
  };

  if (loading) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-6xl space-y-6"><div className="h-10 w-64 animate-pulse rounded-xl bg-slate-200" /><div className="h-96 animate-pulse rounded-3xl bg-white" /></div></main>;

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
      <InvestorHeader
        eyebrow="Planvesto Report"
        title={report?.goal_name ?? "Goal Report"}
        description="A goal-specific report generated from the completed Strategy Run and current Financial State."
      >
        {report && (
          <button
            onClick={() => void download()}
            disabled={working}
            className="rounded-xl bg-navy-900 px-4 py-2.5 text-xs font-bold text-white transition hover:bg-navy-800 disabled:opacity-50"
          >
            {working ? "Preparing PDF…" : "Download PDF"}
          </button>
        )}
      </InvestorHeader>
      <div className="mx-auto max-w-6xl space-y-6 p-6 lg:p-10">
        <StrategyWorkflowNav />
        {error && <InvestorStatus tone="error">{error}</InvestorStatus>}
    {report && <>
      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"><div><p className="text-xs font-bold uppercase tracking-wide text-teal-700">Strategy Result</p><h2 className="mt-2 text-2xl font-extrabold">{report.strategy.name ?? "Strategy not selected"}</h2><p className="mt-1 text-sm text-slate-500">{report.strategy.objective ?? "Goal-specific strategy recommendation"}</p></div><button onClick={() => void download()} disabled={working} className="rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white disabled:opacity-50">{working ? "Preparing PDF…" : "Download PDF"}</button></div></section>
      <section className="grid gap-5 lg:grid-cols-2"><div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Goal Calculation</h2><div className="mt-4 grid gap-3 sm:grid-cols-2">{Object.entries(report.goal_calculation).map(([key, value]) => <div key={key} className="rounded-2xl bg-slate-50 p-4"><p className="text-xs font-bold uppercase tracking-wide text-slate-400">{key.replaceAll("_", " ")}</p><p className="mt-1 font-extrabold">{value == null ? "—" : String(value)}</p></div>)}</div></div><div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Financial State</h2><div className="mt-4 grid gap-3 sm:grid-cols-2">{Object.entries(report.financial_state).map(([key, value]) => <div key={key} className="rounded-2xl bg-slate-50 p-4"><p className="text-xs font-bold uppercase tracking-wide text-slate-400">{key.replaceAll("_", " ")}</p><p className="mt-1 font-extrabold">{value == null ? "Not available" : String(value)}</p></div>)}</div></div></section>
      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Recommendation</h2><p className="mt-3 text-sm leading-6 text-slate-600">{String(report.recommendation.complete_reasoning ?? "")}</p></section>
    </>}
      </div>
    </main>
  );
}
