"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import InvestorHeader from "../../../../../components/InvestorHeader";
import { buildFinancialState } from "../../../../../lib/api/financial-state";
import { getLatestDefinedGoal } from "../../../../../lib/api/goals";
import type { DefinedGoal, FundingStrategyEvaluation } from "../../../../../lib/onboarding/goals/types";
import { getPlanningUnitId } from "../../../../../lib/planning-unit";
import { withReturnTo } from "../../../../../lib/workflow-navigation";

const money = new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
  maximumFractionDigits: 0,
});

function amount(value: number | null | undefined) {
  return value == null ? "Not available" : money.format(value);
}

function statusClass(status: string) {
  if (status === "feasible") return "border-emerald-200 bg-emerald-50 text-emerald-800";
  if (status === "constrained") return "border-amber-200 bg-amber-50 text-amber-800";
  if (status === "infeasible") return "border-rose-200 bg-rose-50 text-rose-800";
  if (status === "requires_upfront_capital") return "border-orange-200 bg-orange-50 text-orange-800";
  return "border-slate-200 bg-slate-100 text-slate-700";
}

function FundingEvaluation({ strategy, surplus }: { strategy: FundingStrategyEvaluation; surplus: number | null }) {
  const label = strategy.status.replaceAll("_", " ");
  return <article className="border-t border-slate-200 py-6 first:border-t-0">
    <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
      <div>
        <h3 className="text-lg font-extrabold text-slate-950">{strategy.strategy_name}</h3>
        <p className="mt-1 max-w-3xl text-sm leading-6 text-slate-600">{strategy.description}</p>
      </div>
      <span className={`w-fit rounded-md border px-2.5 py-1 text-xs font-bold capitalize ${statusClass(strategy.status)}`}>
        Strategy feasibility: {label}
      </span>
    </div>
    <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <Value label="Required upfront funding" value={amount(strategy.required_lumpsum)} />
      <Value label="Required monthly funding" value={amount(strategy.required_monthly_contribution)} />
      <Value label="Available monthly surplus" value={amount(surplus)} />
      <Value label="Remaining evaluated gap" value={amount(strategy.remaining_gap)} />
    </div>
    {strategy.annual_step_up != null && <p className="mt-3 text-xs font-semibold text-slate-600">Annual contribution step-up: {(strategy.annual_step_up * 100).toFixed(1)}%</p>}
    <p className="mt-3 text-sm text-slate-700">{strategy.reason}</p>
    {strategy.constraints.length > 0 && <div className="mt-3"><h4 className="text-xs font-bold uppercase text-amber-800">Constraints</h4><ul className="mt-1 list-inside list-disc text-sm text-slate-700">{strategy.constraints.map((constraint) => <li key={constraint}>{constraint}</li>)}</ul></div>}
    {strategy.trade_offs.length > 0 && <div className="mt-3"><h4 className="text-xs font-bold uppercase text-slate-500">Canonical strategy trade-offs</h4><ul className="mt-1 list-inside list-disc text-sm text-slate-600">{strategy.trade_offs.map((tradeOff) => <li key={tradeOff}>{tradeOff}</li>)}</ul></div>}
  </article>;
}

function Value({ label, value }: { label: string; value: string }) {
  return <div className="border-l-2 border-teal-700 pl-3">
    <p className="text-xs font-semibold text-slate-500">{label}</p>
    <p className="mt-1 text-sm font-extrabold text-slate-950">{value}</p>
  </div>;
}

export default function GoalFeasibilityWorkspace() {
  const { goalId } = useParams<{ goalId: string }>();
  const workspacePath = `/investor/goal-planner/${encodeURIComponent(goalId)}/feasibility`;
  const [goal, setGoal] = useState<DefinedGoal | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function refreshWorkspace() {
    setLoading(true);
    setError(null);
    try {
      const planningUnitId = await getPlanningUnitId();
      await buildFinancialState(planningUnitId, "family");
      const latest = await getLatestDefinedGoal(planningUnitId, goalId);
      setGoal(latest);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to refresh goal feasibility.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void refreshWorkspace();
  }, [goalId]);

  if (loading) return <main className="flex min-h-screen items-center justify-center bg-slate-50"><p className="text-sm font-semibold text-slate-600">Refreshing Financial State and goal feasibility...</p></main>;

  if (error || !goal) return <main className="min-h-screen bg-slate-50 px-5 py-12">
    <section className="mx-auto max-w-2xl border-l-4 border-rose-600 bg-white p-6">
      <h1 className="text-xl font-extrabold text-slate-950">Unable to load this goal analysis</h1>
      <p className="mt-2 text-sm text-slate-600">{error || "The goal could not be found."}</p>
      <div className="mt-5 flex flex-wrap gap-4 text-sm font-bold">
        <button type="button" onClick={() => void refreshWorkspace()} className="text-teal-800 underline">Retry refresh</button>
        <Link href="/investor/goal-planner" className="text-slate-700 underline">Return to Goal Planner</Link>
      </div>
    </section>
  </main>;

  const feasibility = goal.feasibility_status || "unknown";
  const missingData = goal.workflow_readiness?.blockers.flatMap((blocker) => blocker.missing_data) ?? [];
  const strategies = goal.funding_strategies ?? [];

  return <main className="min-h-screen bg-slate-50 text-slate-900">
    <InvestorHeader eyebrow="Goal Planner" title="Feasibility & Funding" />
    <div className="mx-auto max-w-5xl px-5 py-8 lg:px-8 lg:py-12">
      <Link href="/investor/goal-planner" className="text-sm font-bold text-teal-800 underline underline-offset-4">← Goal Planner</Link>

      <section className="mt-6 border-b border-slate-300 pb-7">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-slate-500">Goal summary</p>
            <h1 className="mt-1 text-3xl font-extrabold text-slate-950">{goal.goal_name}</h1>
            <p className="mt-2 text-sm text-slate-600">{goal.goal_type} · Target {new Date(goal.target_year, goal.target_month - 1).toLocaleDateString("en-IN", { month: "long", year: "numeric" })} · {goal.duration_years} years</p>
          </div>
          <span className={`w-fit rounded-md border px-3 py-1.5 text-sm font-black capitalize ${statusClass(feasibility)}`}>Goal feasibility: {feasibility}</span>
        </div>
        <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Value label="Future target" value={amount(goal.future_target)} />
          <Value label="Mapped assets" value={amount(goal.projected_mapped_asset_value)} />
          <Value label="Funding gap" value={amount(goal.funding_gap)} />
          <Value label="Required monthly contribution" value={amount(goal.required_monthly_contribution)} />
        </div>
        {goal.feasibility_reason && <p className="mt-4 max-w-3xl text-sm leading-6 text-slate-700">{goal.feasibility_reason}</p>}
      </section>

      {feasibility === "unknown" && <section className="border-b border-slate-300 py-7">
        <h2 className="text-lg font-extrabold text-slate-950">Missing information</h2>
        <p className="mt-1 text-sm text-slate-600">Complete only the prerequisites listed here. Financial State and Goal Feasibility refresh when you return.</p>
        {missingData.length > 0 ? <ul className="mt-4 space-y-3">{missingData.map((item) => <li key={`${item.label}-${item.route}`} className="text-sm">
          {item.route
            ? <Link className="font-bold text-teal-800 underline underline-offset-4" href={withReturnTo(item.route, workspacePath)}>{item.label} →</Link>
            : <span className="font-semibold text-slate-700">{item.label}</span>}
        </li>)}</ul> : <p className="mt-4 text-sm font-semibold text-slate-700">Financial State inputs are incomplete.</p>}
        {(missingData.length === 0 || missingData.some((item) => !item.route)) && <Link href={withReturnTo("/investor/financial-state", workspacePath)} className="mt-4 inline-block text-sm font-bold text-teal-800 underline underline-offset-4">Open Financial State →</Link>}
      </section>}

      <section className="border-b border-slate-300 py-7">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div><p className="text-xs font-bold uppercase tracking-wider text-teal-800">Funding analysis</p><h2 className="mt-1 text-xl font-extrabold text-slate-950">Funding Strategy Evaluation</h2></div>
          {goal.available_monthly_surplus != null && <p className="text-sm font-semibold text-slate-600">Available monthly resources: {amount(goal.available_monthly_surplus)}</p>}
        </div>
        {feasibility === "unknown" ? <p className="mt-5 text-sm text-slate-600">Funding strategies will be evaluated after the missing Financial State information is complete.</p>
          : strategies.length > 0 ? <div className="mt-3">{strategies.map((strategy) => <FundingEvaluation key={strategy.strategy_id} strategy={strategy} surplus={goal.available_monthly_surplus ?? null} />)}</div>
            : <p className="mt-5 text-sm text-slate-600">No funding strategy evaluation was returned for this goal.</p>}
      </section>

      <section className="py-7">
        <p className="text-xs font-bold uppercase tracking-wider text-slate-500">Investor decision</p>
        <h2 className="mt-1 text-lg font-extrabold text-slate-950">No funding strategy has been selected</h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">Goal Feasibility and strategy evaluations are decision inputs. Review the available alternatives before choosing how to proceed.</p>
        <Link href={`/investor/strategy-builder?goalId=${encodeURIComponent(goal.goal_id)}`} className="mt-4 inline-flex rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-bold text-white">Continue to Strategy Builder →</Link>
      </section>
    </div>
  </main>;
}