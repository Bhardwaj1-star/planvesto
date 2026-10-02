"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import StrategyWorkflowNav from "../../../components/StrategyWorkflowNav";
import InvestorHeader from "../../../components/InvestorHeader";
import {
  getPlanningUnitId,
  getCompleteFinancialPlan,
  buildCompleteFinancialPlan,
  downloadCompleteFinancialPlanPdf,
  type ConsolidatedFinancialPlan,
  type ConsolidatedActionItem,
} from "../../../lib/api/strategy";

function formatINR(value: number | null | undefined) {
  if (value === null || value === undefined || !Number.isFinite(value)) return "—";
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(value);
}

function statusBadge(status: string) {
  switch (status.toLowerCase()) {
    case "completed":
    case "pass":
      return "bg-emerald-50 text-emerald-700 border-emerald-200";
    case "conditional":
    case "in_progress":
      return "bg-amber-50 text-amber-700 border-amber-200";
    case "fail":
    case "critical":
      return "bg-red-50 text-red-700 border-red-200";
    default:
      return "bg-slate-100 text-slate-700 border-slate-200";
  }
}

export default function ActionPlanPage() {
  const [plan, setPlan] = useState<ConsolidatedFinancialPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [completedActionIds, setCompletedActionIds] = useState<Set<string>>(new Set());

  const loadPlan = async () => {
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
    try {
      const data = await getCompleteFinancialPlan(planningUnitId);
      setPlan(data);
    } catch {
      // If plan not built yet, build it
      const built = await buildCompleteFinancialPlan(planningUnitId);
      setPlan(built);
    }
  };

  useEffect(() => {
    let active = true;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        await loadPlan();
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load financial plan.");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, []);

  const handleRebuild = async () => {
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId) return;
    setWorking(true);
    setError(null);
    try {
      const next = await buildCompleteFinancialPlan(planningUnitId);
      setPlan(next);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to rebuild financial plan.");
    } finally {
      setWorking(false);
    }
  };

  const handleDownloadPdf = async () => {
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId) return;
    setDownloading(true);
    setError(null);
    try {
      const blob = await downloadCompleteFinancialPlanPdf(planningUnitId);
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `complete-financial-plan-${planningUnitId}.pdf`;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to download PDF.");
    } finally {
      setDownloading(false);
    }
  };

  const toggleAction = (id: string) => {
    setCompletedActionIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  if (loading) {
    return (
      <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
        <div className="mx-auto max-w-6xl space-y-6">
          <div className="h-10 w-72 animate-pulse rounded-xl bg-slate-200" />
          <div className="h-96 animate-pulse rounded-3xl bg-white" />
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
      <InvestorHeader
        eyebrow="Implement &amp; Review"
        title="Report &amp; Action Plan"
        description="Comprehensive consolidated financial plan uniting all financial goals, emergency reserve rules, waterfall resource allocation, and prioritized action steps."
      >
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => void handleRebuild()}
            disabled={working}
            className="rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-xs font-bold text-slate-700 shadow-sm transition hover:bg-slate-50 disabled:opacity-50"
          >
            {working ? "Rebuilding…" : "Rebuild Plan"}
          </button>
          <button
            onClick={() => void handleDownloadPdf()}
            disabled={downloading}
            className="rounded-xl bg-navy-900 px-4 py-2.5 text-xs font-bold text-white shadow-sm transition hover:bg-navy-800 disabled:opacity-50"
          >
            {downloading ? "Generating PDF…" : "Download Financial Plan (PDF)"}
          </button>
        </div>
      </InvestorHeader>

      <div className="mx-auto max-w-6xl space-y-6 p-4 sm:p-6 lg:p-10">
        <StrategyWorkflowNav />

        {error && (
          <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">
            {error}
          </div>
        )}

        {plan && (
          <>
            {/* Deficit / Infeasible Warning */}
            {plan.consolidated_funding && (plan.consolidated_funding.monthly_gap ?? 0) > 0 && (
              <div className="rounded-2xl border border-rose-300 bg-rose-50/90 p-5 shadow-sm">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">⚠️</span>
                  <div>
                    <h3 className="text-base font-extrabold text-rose-900">Resource Shortfall / Constrained Allocation</h3>
                    <p className="mt-1 text-xs leading-5 text-rose-700">
                      Total required monthly contributions ({formatINR(plan.consolidated_funding.required_monthly_contribution)}) exceed your available surplus ({formatINR(plan.consolidated_funding.available_monthly_surplus)}) by <b>{formatINR(plan.consolidated_funding.monthly_gap)}/month</b>.
                      The backend allocation engine prioritized foundational goals and partially funded lower-priority goals.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Incomplete Financial Context Warning */}
            {(!plan.resource_allocation.total_monthly_surplus || plan.resource_allocation.total_monthly_surplus <= 0) && (
              <div className="rounded-2xl border border-amber-300 bg-amber-50 p-5 shadow-sm">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">ℹ️</span>
                  <div className="flex-1">
                    <h3 className="text-base font-extrabold text-amber-900">Incomplete Financial State (Surplus is Zero or Unset)</h3>
                    <p className="mt-1 text-xs text-amber-700">
                      Monthly investable surplus has not been computed or is ₹0. Goals cannot receive monthly allocations until cash flows are recorded.
                    </p>
                    <Link href="/investor/financial-state" className="mt-3 inline-block rounded-xl bg-amber-800 px-4 py-2 text-xs font-bold text-white hover:bg-amber-900">
                      Update Financial State →
                    </Link>
                  </div>
                </div>
              </div>
            )}

            {/* Plan Executive Summary */}
            <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Total Goals Planned</p>
                <p className="mt-2 text-2xl font-extrabold text-navy-900">{plan.summary.total_goals_count}</p>
                <p className="mt-1 text-xs text-slate-500">
                  {plan.summary.fully_funded_goals_count} fully funded · {plan.summary.partially_funded_goals_count} partial
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Monthly Surplus</p>
                <p className="mt-2 text-2xl font-extrabold text-teal-700">
                  {formatINR(plan.resource_allocation.total_monthly_surplus)}
                </p>
                <p className="mt-1 text-xs text-slate-500">
                  Allocated: {formatINR(plan.resource_allocation.total_allocated_monthly)}
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Monthly Commitment</p>
                <p className="mt-2 text-2xl font-extrabold text-navy-900">
                  {formatINR(plan.summary.total_monthly_commitment)}
                </p>
                <p className="mt-1 text-xs text-slate-500">Across foundation &amp; goal SIPs</p>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Unallocated Surplus</p>
                <p className="mt-2 text-2xl font-extrabold text-slate-700">
                  {formatINR(plan.resource_allocation.unallocated_surplus)}
                </p>
                <p className="mt-1 text-xs text-slate-500">Available liquidity buffer</p>
              </div>
            </section>

            {/* Financial Ratio Constraints & Guardrails */}
            {plan.ratio_constraints && plan.ratio_constraints.length > 0 && (
              <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <h2 className="text-lg font-bold text-navy-900">Financial Ratio Guardrails &amp; Constraints</h2>
                    <p className="mt-0.5 text-xs text-slate-500">
                      Evaluated against approved Moneywheel &amp; Financial State rules to protect your financial foundation.
                    </p>
                  </div>
                </div>

                <div className="mt-5 grid gap-4 md:grid-cols-2">
                  {plan.ratio_constraints.map((c) => (
                    <div key={c.rule_id} className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                      <div className="flex items-center justify-between">
                        <h3 className="font-bold text-slate-900">{c.rule_name}</h3>
                        <span className={`rounded-full border px-2.5 py-0.5 text-xs font-bold uppercase ${statusBadge(c.status)}`}>
                          {c.status}
                        </span>
                      </div>
                      <p className="mt-2 text-xs leading-5 text-slate-600">{c.reason}</p>
                      {c.corrective_action && (
                        <p className="mt-2 text-xs font-semibold text-teal-800">
                          Recommended Action: {c.corrective_action}
                        </p>
                      )}
                      <div className="mt-3 flex flex-wrap gap-4 text-xs text-slate-500">
                        <span>Current: <b>{c.current_ratio != null ? c.current_ratio.toFixed(1) : "—"}</b></span>
                        <span>Target: <b>{c.target_threshold}</b></span>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* Goal-Wise Allocation & Detailed Reports */}
            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h2 className="text-lg font-bold text-navy-900">Goal Allocations &amp; Reports</h2>
                  <p className="mt-0.5 text-xs text-slate-500">
                    Waterfall surplus distribution based on investor priority and foundational constraints.
                  </p>
                </div>
              </div>

              <div className="mt-5 space-y-4">
                {plan.resource_allocation.goal_allocations.map((alloc) => {
                  const goalPlan = plan.goal_plans.find((gp) => gp.goal_id === alloc.goal_id);
                  const isRetirement = alloc.goal_name.toLowerCase().includes("retire");
                  return (
                    <article
                      key={alloc.goal_id}
                      className="flex flex-col gap-4 rounded-2xl border border-slate-100 bg-slate-50 p-5 md:flex-row md:items-center md:justify-between"
                    >
                      <div className="min-w-0 flex-1">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-bold text-slate-700 border border-slate-200">
                            Client Priority: <b className="capitalize text-navy-900">{alloc.client_priority || "high"}</b>
                          </span>
                          <span className={`rounded-full px-2.5 py-0.5 text-xs font-bold border ${alloc.override_applied ? "bg-amber-100 text-amber-900 border-amber-300" : "bg-teal-50 text-teal-800 border-teal-200"}`}>
                            Resolved Priority: <b className="capitalize">{alloc.resolved_priority || alloc.client_priority || "high"}</b>
                          </span>
                          <span className="rounded-full bg-white px-2.5 py-0.5 text-xs font-semibold text-slate-600 border border-slate-200">
                            {alloc.funding_percentage.toFixed(0)}% Funded
                          </span>
                          {alloc.override_applied && (
                            <span className="rounded-full bg-amber-600 px-2.5 py-0.5 text-xs font-bold text-white">
                              Rule Adjustment Applied
                            </span>
                          )}
                        </div>

                        <h3 className="mt-2 text-lg font-extrabold text-navy-900">{alloc.goal_name}</h3>
                        {goalPlan && (
                          <p className="mt-0.5 text-xs text-slate-500">
                            Strategy: <b className="text-slate-700">{goalPlan.strategy_name}</b> · Target:{" "}
                            {formatINR(goalPlan.target_amount)}
                          </p>
                        )}
                        {alloc.override_reason && (
                          <div className="mt-2 rounded-xl bg-amber-50/90 border border-amber-200 p-3 text-xs text-amber-900 leading-relaxed">
                            <span className="font-bold">System Rule Explanation: </span>
                            <span>{alloc.override_reason}</span>
                          </div>
                        )}

                        <div className="mt-3 flex flex-wrap gap-4 text-xs text-slate-600">
                          <span>Allocated SIP: <b className="text-teal-700">{formatINR(alloc.allocated_amount)}/mo</b></span>
                          <span>Requested: {formatINR(alloc.requested_amount)}/mo</span>
                          {alloc.shortfall > 0 && (
                            <span className="text-red-600">Shortfall: {formatINR(alloc.shortfall)}/mo</span>
                          )}
                        </div>
                      </div>

                      <div className="flex shrink-0 flex-wrap items-center gap-2">
                        <Link
                          href={`/investor/goal-report?goalId=${encodeURIComponent(alloc.goal_id)}`}
                          className="rounded-xl border border-slate-200 bg-white px-3.5 py-2 text-xs font-bold text-slate-700 shadow-sm transition hover:bg-slate-50"
                        >
                          Goal Decision Report →
                        </Link>
                      </div>
                    </article>
                  );
                })}
              </div>
            </section>

            {/* Consolidated Action Plan */}
            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h2 className="text-lg font-bold text-navy-900">Action Plan &amp; Implementation Steps</h2>
                  <p className="mt-0.5 text-xs text-slate-500">
                    Concrete execution steps required to implement your unified financial strategy.
                  </p>
                </div>
                <span className="text-xs font-bold text-slate-400">
                  {plan.action_plan.actions.length} Total Actions
                </span>
              </div>

              <div className="mt-5 space-y-3">
                {plan.action_plan.actions.map((action: ConsolidatedActionItem) => {
                  const isDone = completedActionIds.has(action.action_id);
                  return (
                    <article
                      key={action.action_id}
                      className={`flex flex-col gap-4 rounded-2xl border p-4 transition md:flex-row md:items-center md:justify-between ${
                        isDone ? "border-emerald-200 bg-emerald-50/40 opacity-75" : "border-slate-100 bg-slate-50"
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <input
                          type="checkbox"
                          checked={isDone}
                          onChange={() => toggleAction(action.action_id)}
                          className="mt-1 h-4 w-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500"
                          aria-label={`Mark ${action.title} as completed`}
                        />
                        <div>
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="rounded-full bg-white px-2.5 py-0.5 text-xs font-bold uppercase tracking-wider text-slate-500 border border-slate-200">
                              {action.category}
                            </span>
                            <span
                              className={`rounded-full px-2 py-0.5 text-[10px] font-bold uppercase ${
                                action.priority === "high"
                                  ? "bg-red-100 text-red-700"
                                  : action.priority === "medium"
                                  ? "bg-amber-100 text-amber-700"
                                  : "bg-slate-100 text-slate-600"
                              }`}
                            >
                              {action.priority} priority
                            </span>
                          </div>
                          <h4 className={`mt-1 font-bold ${isDone ? "line-through text-slate-500" : "text-slate-900"}`}>
                            {action.title}
                          </h4>
                          <p className="mt-0.5 text-xs text-slate-600">{action.description}</p>
                          <div className="mt-2 flex flex-wrap gap-4 text-xs text-slate-500">
                            {action.monthly_commitment > 0 && (
                              <span>Monthly: <b className="text-teal-700">{formatINR(action.monthly_commitment)}</b></span>
                            )}
                            {action.lump_sum_commitment > 0 && (
                              <span>Lump sum: <b className="text-teal-700">{formatINR(action.lump_sum_commitment)}</b></span>
                            )}
                            {action.deadline && <span>Target by: <b>{action.deadline}</b></span>}
                          </div>
                        </div>
                      </div>

                      <button
                        onClick={() => toggleAction(action.action_id)}
                        className={`rounded-xl px-3.5 py-1.5 text-xs font-bold transition shrink-0 ${
                          isDone
                            ? "bg-emerald-100 text-emerald-800 hover:bg-emerald-200"
                            : "border border-slate-200 bg-white text-slate-700 hover:bg-slate-100"
                        }`}
                      >
                        {isDone ? "Completed ✓" : "Mark Done"}
                      </button>
                    </article>
                  );
                })}
              </div>
            </section>
          </>
        )}
      </div>
    </main>
  );
}
