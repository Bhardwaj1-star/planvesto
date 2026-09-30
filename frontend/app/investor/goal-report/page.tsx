"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import StrategyWorkflowNav from "../../../components/StrategyWorkflowNav";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorStatus } from "../../../components/InvestorUI";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";
import { getPlanningUnitId, getLatestStrategyRun, getGoalStrategyReport, downloadGoalStrategyReportPdf, type GoalStrategyReport } from "../../../lib/api/strategy";

export default function GoalReportPage() {
  const [goals, setGoals] = useState<Array<{ id: string; name: string }>>([]);
  const [selectedGoalId, setSelectedGoalId] = useState("");
  const [report, setReport] = useState<GoalStrategyReport | null>(null);
  const [working, setWorking] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const data = await loadGoalPlannerData();
        const activeGoals = (data?.goals ?? []).map((g) => ({ id: g.id, name: g.name || "Untitled Goal" }));
        if (!active) return;
        setGoals(activeGoals);
        const requested = typeof window !== "undefined" ? new URLSearchParams(window.location.search).get("goalId") : null;
        const initialGoalId = activeGoals.find((g) => g.id === requested)?.id ?? activeGoals[0]?.id ?? "";
        setSelectedGoalId(initialGoalId);
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load goals.");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!selectedGoalId) {
      setReport(null);
      return;
    }
    let active = true;
    (async () => {
      setWorking(true);
      setError(null);
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");

        const selectedRun = await getLatestStrategyRun(planningUnitId, selectedGoalId);
        if (!selectedRun?.strategy_run_id) throw new Error("No completed Strategy Run is available for the selected goal. Please build a strategy first.");

        const next = await getGoalStrategyReport(planningUnitId, selectedRun.strategy_run_id);
        if (active) setReport(next);
      } catch (err) {
        if (active) {
          setReport(null);
          setError(err instanceof Error ? err.message : "Unable to load goal report.");
        }
      } finally {
        if (active) setWorking(false);
      }
    })();
    return () => { active = false; };
  }, [selectedGoalId]);

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
        description={report ? `${report.goal_type ?? "Financial"} goal report generated from the selected Strategy Run and Financial State.` : "Goal report"}
      >
        <div className="flex flex-wrap items-center gap-2">
          {selectedGoalId && (
            <Link
              href={`/investor/strategy-builder?goalId=${encodeURIComponent(selectedGoalId)}`}
              className="rounded-xl border border-slate-200 bg-white px-3.5 py-2 text-xs font-bold text-slate-700 shadow-sm transition hover:bg-slate-50"
            >
              Strategy Builder
            </Link>
          )}
          {report && (
            <button
              onClick={() => void download()}
              disabled={working}
              className="rounded-xl bg-navy-900 px-4 py-2.5 text-xs font-bold text-white transition hover:bg-navy-800 disabled:opacity-50"
            >
              {working ? "Preparing PDF…" : "Download PDF"}
            </button>
          )}
        </div>
      </InvestorHeader>
      <div className="mx-auto max-w-6xl space-y-6 p-6 lg:p-10">
        <StrategyWorkflowNav />

        {goals.length > 0 && (
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <label className="block max-w-sm">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Select Goal</span>
              <select
                value={selectedGoalId}
                onChange={(e) => setSelectedGoalId(e.target.value)}
                className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold"
              >
                {goals.map((g) => (
                  <option key={g.id} value={g.id}>
                    {g.name}
                  </option>
                ))}
              </select>
            </label>
          </section>
        )}

        {error && <InvestorStatus tone="error">{error}</InvestorStatus>}

        {!report && !error && !working && (
          <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
            <h2 className="text-xl font-bold">No Report Available</h2>
            <p className="mt-2 text-sm text-slate-500">Build a strategy run for this goal to generate a goal report.</p>
            {selectedGoalId && (
              <Link
                href={`/investor/strategy-builder?goalId=${encodeURIComponent(selectedGoalId)}`}
                className="mt-6 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white"
              >
                Open Strategy Builder
              </Link>
            )}
          </section>
        )}

        {report && (
          <>
            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wide text-teal-700">Strategy Result</p>
                  <h2 className="mt-2 text-2xl font-extrabold">{report.strategy.name ?? "Strategy not selected"}</h2>
                  <p className="mt-1 text-sm text-slate-500">{report.strategy.objective ?? "Goal-specific strategy recommendation"}</p>
                </div>
                <button
                  onClick={() => void download()}
                  disabled={working}
                  className="rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white disabled:opacity-50"
                >
                  {working ? "Preparing PDF…" : "Download PDF"}
                </button>
              </div>
            </section>

            {Object.keys(report.goal_details).length > 0 && (
              <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-bold">Goal Details</h2>
                <div className="mt-4 grid gap-3 sm:grid-cols-2">
                  {Object.entries(report.goal_details).map(([key, value]) => (
                    <div key={key} className="rounded-2xl bg-slate-50 p-4">
                      <p className="text-xs font-bold uppercase tracking-wide text-slate-400">{key.replaceAll("_", " ")}</p>
                      <p className="mt-1 font-extrabold">{value == null ? "—" : String(value)}</p>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {report.mapped_assets && report.mapped_assets.length > 0 && (
              <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-bold">Mapped Assets</h2>
                <div className="mt-4 overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead>
                      <tr className="border-b bg-slate-50 text-xs font-bold uppercase tracking-wider text-slate-500">
                        <th className="px-4 py-3">Asset</th>
                        <th className="px-4 py-3">Allocated Amount</th>
                        <th className="px-4 py-3">Allocation %</th>
                        <th className="px-4 py-3">Expected Return</th>
                        <th className="px-4 py-3">Projected Value</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {report.mapped_assets.map((asset, idx) => (
                        <tr key={idx} className="hover:bg-slate-50/50">
                          <td className="px-4 py-3 font-semibold text-slate-900">{asset.asset_name || "—"}</td>
                          <td className="px-4 py-3 text-slate-600">
                            {asset.allocation != null ? `₹${Math.round(asset.allocation).toLocaleString("en-IN")}` : "—"}
                          </td>
                          <td className="px-4 py-3 text-slate-600">
                            {asset.allocation_percentage != null ? `${(asset.allocation_percentage * 100).toFixed(1)}%` : "—"}
                          </td>
                          <td className="px-4 py-3 text-slate-600">
                            {asset.expected_return != null ? `${(asset.expected_return * 100).toFixed(1)}%` : "—"}
                          </td>
                          <td className="px-4 py-3 font-bold text-slate-900">
                            {asset.projected_value != null ? `₹${Math.round(asset.projected_value).toLocaleString("en-IN")}` : "—"}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </section>
            )}

            <section className="grid gap-5 lg:grid-cols-2">
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-bold">Goal Calculation</h2>
                <div className="mt-4 grid gap-3 sm:grid-cols-2">
                  {Object.entries(report.goal_calculation).map(([key, value]) => (
                    <div key={key} className="rounded-2xl bg-slate-50 p-4">
                      <p className="text-xs font-bold uppercase tracking-wide text-slate-400">{key.replaceAll("_", " ")}</p>
                      <p className="mt-1 font-extrabold">{value == null ? "—" : String(value)}</p>
                    </div>
                  ))}
                </div>
              </div>
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-bold">Financial State</h2>
                <div className="mt-4 grid gap-3 sm:grid-cols-2">
                  {Object.entries(report.financial_state).map(([key, value]) => (
                    <div key={key} className="rounded-2xl bg-slate-50 p-4">
                      <p className="text-xs font-bold uppercase tracking-wide text-slate-400">{key.replaceAll("_", " ")}</p>
                      <p className="mt-1 font-extrabold">{value == null ? "Not available" : String(value)}</p>
                    </div>
                  ))}
                </div>
              </div>
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="text-lg font-bold">Recommendation</h2>
              <p className="mt-3 text-sm leading-6 text-slate-600">{String(report.recommendation.complete_reasoning ?? "")}</p>
            </section>
          </>
        )}
      </div>
    </main>
  );
}
