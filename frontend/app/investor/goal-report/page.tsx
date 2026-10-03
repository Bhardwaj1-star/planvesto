"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorStatus } from "../../../components/InvestorUI";
import { getPlanningUnitId, getGoalStrategyReportByStrategyVersion, downloadGoalStrategyReportPdfByStrategyVersion, type GoalStrategyReport } from "../../../lib/api/strategy";

export default function GoalReportPage() {
  const [strategyVersionId, setStrategyVersionId] = useState("");
  const [report, setReport] = useState<GoalStrategyReport | null>(null);
  const [working, setWorking] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const requested = typeof window !== "undefined" ? new URLSearchParams(window.location.search).get("strategyVersionId") : null;
    setStrategyVersionId(requested ?? "");
  }, []);

  useEffect(() => {
    if (!strategyVersionId) {
      setReport(null);
      setError("A selected Strategy Version is required to open the goal report. Return to Participate With Numbers and lock a decision first.");
      setLoading(false);
      return;
    }
    let active = true;
    (async () => {
      setWorking(true); setLoading(true); setError(null);
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
        const next = await getGoalStrategyReportByStrategyVersion(planningUnitId, strategyVersionId);
        if (active) setReport(next);
      } catch (err) {
        if (active) { setReport(null); setError(err instanceof Error ? err.message : "Unable to load goal report."); }
      } finally {
        if (active) { setWorking(false); setLoading(false); }
      }
    })();
    return () => { active = false; };
  }, [strategyVersionId]);

  const download = async () => {
    if (!strategyVersionId) return;
    setWorking(true); setError(null);
    try {
      const planningUnitId = getPlanningUnitId();
      if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
      const blob = await downloadGoalStrategyReportPdfByStrategyVersion(planningUnitId, strategyVersionId);
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `goal-strategy-report-${strategyVersionId}.pdf`;
      document.body.appendChild(anchor); anchor.click(); anchor.remove(); URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to download PDF.");
    } finally { setWorking(false); }
  };


  if (loading) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-6xl space-y-6"><div className="h-10 w-64 animate-pulse rounded-xl bg-slate-200" /><div className="h-96 animate-pulse rounded-3xl bg-white" /></div></main>;

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
      <InvestorHeader
        eyebrow="Planvesto Report"
        title={report?.goal_name ?? report?.goal?.name ?? "Goal Report"}
        description={report ? `${report.goal_type ?? report.goal?.type ?? "Financial"} goal report generated from the selected Strategy Version and Financial State.` : "Detailed goal report"}
      >
        <div className="flex flex-wrap items-center gap-2">
          {report && (
            <Link
              href={`/investor/strategy-builder?goalId=${encodeURIComponent(report.goal?.id ?? report.goal_id ?? "")}`}
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

        {error && <InvestorStatus tone="error">{error}</InvestorStatus>}

        {!report && !error && !working && (
          <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
            <h2 className="text-xl font-bold">No Report Available</h2>
            <p className="mt-2 text-sm text-slate-500">Lock a Strategy Version in Participate With Numbers to generate its detailed goal report.</p>
          </section>
        )}

        {report && (
          <>
            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wide text-teal-700">Strategy Result</p>
                  <h2 className="mt-2 text-2xl font-extrabold">{report.strategy.name ?? report.strategy.selected_strategy_name ?? "Strategy not selected"}</h2>
                  <p className="mt-1 text-sm text-slate-500">{report.strategy.objective ?? report.strategy.rationale ?? "Goal-specific strategy recommendation"}</p>
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

            {report.goal_details && typeof report.goal_details === 'object' && Object.keys(report.goal_details).length > 0 && (
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

            {/* 3-Bucket Product Architecture */}
            {report.product_architecture && report.product_architecture.length > 0 && (
              <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-bold text-navy-900">3-Bucket Product Architecture</h2>
                <p className="mt-1 text-xs text-slate-500">Asset allocation partitioned across time horizon and volatility tolerances.</p>
                <div className="mt-5 grid gap-4 md:grid-cols-3">
                  {report.product_architecture.map((bucket, idx) => (
                    <div key={idx} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold uppercase tracking-wider text-teal-700">{bucket.role || "Bucket"}</span>
                        <span className="rounded-full bg-teal-100 px-2 py-0.5 text-xs font-extrabold text-teal-800">
                          {bucket.allocation_pct ?? bucket.allocation ?? "—"}{bucket.allocation_pct != null ? "%" : ""}
                        </span>
                      </div>
                      <h3 className="mt-2 font-bold text-slate-900">{bucket.bucket_name ?? bucket.bucket ?? "Product Bucket"}</h3>
                      {bucket.horizon_years != null && (
                        <p className="mt-1 text-xs text-slate-500">Horizon: {bucket.horizon_years} years</p>
                      )}
                      <div className="mt-3 flex flex-wrap gap-1">
                        {(Array.isArray(bucket.instruments)
                          ? bucket.instruments
                          : typeof bucket.instruments === "string"
                            ? bucket.instruments.split(",").map((inst) => inst.trim()).filter(Boolean)
                            : Object.values(bucket.instruments).map(String)
                        ).map((inst, i) => (
                          <span key={i} className="rounded-md bg-white px-2 py-1 text-[11px] font-semibold text-slate-700 border border-slate-200">
                            {inst}
                          </span>
                        ))}
                      </div>
                      <p className="mt-3 text-xs leading-relaxed text-slate-600">{bucket.rationale ?? bucket.strategic_rule ?? "—"}</p>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* Multi-Year Cash Flow Trajectory */}
            {report.cash_flow_trajectory && report.cash_flow_trajectory.length > 0 && (
              <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-bold text-navy-900">Multi-Year Cash Flow Trajectory</h2>
                <p className="mt-1 text-xs text-slate-500">Year-by-year projected wealth trajectory with annual contributions and compounding.</p>
                <div className="mt-4 overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead>
                      <tr className="border-b bg-slate-50 text-xs font-bold uppercase tracking-wider text-slate-500">
                        <th className="px-4 py-3">Year</th>
                        <th className="px-4 py-3">Opening Balance</th>
                        <th className="px-4 py-3">Annual Contribution</th>
                        <th className="px-4 py-3">Projected Growth</th>
                        <th className="px-4 py-3">Closing Balance</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {report.cash_flow_trajectory.map((row, idx) => (
                        <tr key={idx} className="hover:bg-slate-50/50">
                          <td className="px-4 py-3 font-semibold text-slate-900">{row.year || `Yr ${row.year_index}`}</td>
                          <td className="px-4 py-3 text-slate-600">₹{Math.round(row.opening_balance).toLocaleString("en-IN")}</td>
                          <td className="px-4 py-3 text-teal-700 font-semibold">₹{Math.round(row.annual_contribution).toLocaleString("en-IN")}</td>
                          <td className="px-4 py-3 text-slate-600">₹{Math.round(row.growth).toLocaleString("en-IN")}</td>
                          <td className="px-4 py-3 font-bold text-slate-900">₹{Math.round(row.closing_balance).toLocaleString("en-IN")}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
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

            {/* Action Plan Timeline */}
            {report.action_plan_timeline && report.action_plan_timeline.length > 0 && (
              <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-bold text-navy-900">Implementation Roadmap &amp; Milestones</h2>
                <div className="mt-4 space-y-3">
                  {report.action_plan_timeline.map((item, idx) => (
                    <div key={idx} className="flex flex-col gap-2 rounded-2xl border border-slate-100 bg-slate-50 p-4 md:flex-row md:items-center md:justify-between">
                      <div>
                        <span className="rounded-md bg-teal-100 px-2 py-0.5 text-xs font-bold text-teal-800">{item.timeline}</span>
                        <h4 className="mt-1 font-bold text-slate-900">{item.action}</h4>
                        <p className="text-xs text-slate-500">Milestone: {item.milestone}</p>
                      </div>
                      <span className="shrink-0 text-xs font-semibold text-slate-400">Owner: {item.owner}</span>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* Contingency & Stress Matrix */}
            {report.contingency_matrix && report.contingency_matrix.length > 0 && (
              <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-bold text-navy-900">Contingency &amp; Stress Defense Matrix</h2>
                <div className="mt-4 grid gap-4 md:grid-cols-2">
                  {report.contingency_matrix.map((c, idx) => (
                    <div key={idx} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                      <h4 className="font-bold text-slate-900">{c.risk_event}</h4>
                      <p className="mt-2 text-xs text-slate-600"><b className="text-teal-700">Immediate Action:</b> {c.immediate_action}</p>
                      <p className="mt-1 text-xs text-slate-600"><b className="text-navy-900">Planning Change:</b> {c.planning_change}</p>
                      <p className="mt-1 text-xs text-red-600"><b className="text-red-700">What NOT to do:</b> {c.what_not_to_do}</p>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {report.recommendation && (
              <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-bold">Recommendation</h2>
                <p className="mt-3 text-sm leading-6 text-slate-600">{String(report.recommendation.complete_reasoning ?? report.strategy.rationale ?? "")}</p>
              </section>
            )}
          </>
        )}
      </div>
    </main>
  );
}
