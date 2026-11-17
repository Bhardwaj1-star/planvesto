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
import { apiRequest } from "../../../../../lib/api/client";

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
  const [revisedCost, setRevisedCost] = useState("");
  const [revisedTargetDate, setRevisedTargetDate] = useState("");
  const [case2APreview, setCase2APreview] = useState<DefinedGoal | null>(null);
  const [case2ALoading, setCase2ALoading] = useState(false);
  const [scenarioError, setScenarioError] = useState<string | null>(null);

  async function refreshWorkspace() {
    setLoading(true);
    setError(null);
    try {
      const planningUnitId = await getPlanningUnitId();
      await buildFinancialState(planningUnitId, "family");
      const latest = await getLatestDefinedGoal(planningUnitId, goalId);
      setGoal(latest);
      setRevisedCost(String(latest.today_cost ?? ""));
      setRevisedTargetDate(`${latest.target_year}-${String(latest.target_month).padStart(2, "0")}`);
      setCase2APreview(null);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to refresh goal feasibility.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void refreshWorkspace();
  }, [goalId]);
  async function evaluateCase2A(costInput = revisedCost, dateInput = revisedTargetDate) {
    if (!goal) return;
    const [year, month] = dateInput.split("-").map(Number);
    if (!Number.isFinite(Number(costInput)) || Number(costInput) <= 0 || !year || !month) {
      setScenarioError("Enter a valid revised goal amount and target month.");
      return;
    }
    setCase2ALoading(true);
    setScenarioError(null);
    setCase2APreview(null);
    try {
      const preview = await apiRequest<DefinedGoal>("/api/goals/calculate", {
        method: "POST",
        body: JSON.stringify({
          planning_unit_id: goal.planning_unit_id,
          goal_id: goal.goal_id,
          goal_name: goal.goal_name,
          goal_type: goal.goal_type,
          today_cost: Number(costInput),
          target_month: month,
          target_year: year,
          inflation_rate_pct: goal.inflation_rate,
          expected_return_pct: goal.funding_return_assumption ?? 10,
          priority: goal.priority,
          flexibility: goal.flexibility,
          status: goal.status,
          asset_mappings: (goal.mapped_assets ?? []).map((mapping) => ({
            asset_id: mapping.asset_id,
            asset_name: mapping.asset_name ?? "Asset",
            current_value: Number(mapping.allocated_amount ?? 0),
            allocation_type: mapping.allocation_type,
            allocation_value: Number(mapping.allocation_value ?? mapping.allocated_percentage ?? 100),
            allocation_percentage: Number(mapping.allocated_percentage ?? 100),
            expected_annual_return_pct: Number(mapping.expected_return ?? 10),
            return_frequency: mapping.return_frequency ?? "annual",
          })),
          dynamic_details: (goal.version_metadata?.dynamic_details as Record<string, unknown>) ?? {},
        }),
      });
      setCase2APreview(preview);
    } catch (cause) {
      setScenarioError(cause instanceof Error ? cause.message : "Unable to evaluate the revised goal scenario.");
    } finally {
      setCase2ALoading(false);
    }
  }


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
          <div><p className="text-xs font-bold uppercase tracking-wider text-teal-800">Funding analysis</p><h2 className="mt-1 text-xl font-extrabold text-slate-950">Fund Feasibility — Funding Methods</h2></div>
          {goal.available_monthly_surplus != null && <p className="text-sm font-semibold text-slate-600">Available monthly resources: {amount(goal.available_monthly_surplus)}</p>}
        </div>
        {feasibility === "unknown" ? <p className="mt-5 text-sm text-slate-600">Funding strategies will be evaluated after the missing Financial State information is complete.</p>
          : strategies.length > 0 ? <div className="mt-3">{strategies.map((strategy) => <FundingEvaluation key={strategy.strategy_id} strategy={strategy} surplus={goal.available_monthly_surplus ?? null} />)}</div>
            : <p className="mt-5 text-sm text-slate-600">No funding strategy evaluation was returned for this goal.</p>}
      </section>


      {feasibility !== "unknown" && <section className="border-b border-slate-300 py-7">
        <p className="text-xs font-bold uppercase tracking-wider text-teal-800">Chapter 10 · Fund Feasibility</p>
        <h2 className="mt-1 text-xl font-extrabold text-slate-950">
          {goal.fund_feasibility_case === "case_1_affordable" ? "Case 1 — SIP affordability test passed" : "Case 2 — Funding capacity shortfall"}
        </h2>
        <p className="mt-2 text-sm leading-6 text-slate-600">
          Existing goal SIP is deducted from the required SIP before comparing the additional contribution with Available Monthly Surplus. This is an affordability test, not confirmation that the goal has already been funded.
        </p>
        {goal.fund_feasibility_case === "case_2_capacity_shortfall" && <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-4">
          <h3 className="font-extrabold text-amber-950">Case 2A — Change Goal Amount or Extend Timeline</h3>
          <p className="mt-1 text-sm text-amber-900">Change the target amount and/or target month to preview the revised Future Goal Target, Funding Gap and Required SIP. Nothing is saved until the investor chooses to update the goal.</p>
          <div className="mt-3 grid gap-4 md:grid-cols-2">
            <div className="rounded-lg border border-amber-200 bg-white p-3">
              <h4 className="font-bold text-slate-900">Option A — Reduce Goal Amount</h4>
              <p className="mt-1 text-xs text-slate-600">Keep the current target date; change only today's goal cost.</p>
              <label className="mt-3 block text-xs font-bold text-slate-700">Revised goal amount (today's cost)
                <input type="number" min="1" step="1" value={revisedCost} onChange={(event) => setRevisedCost(event.target.value)} className="mt-1 w-full rounded-lg border border-amber-300 px-3 py-2 text-sm" />
              </label>
              <button type="button" disabled={case2ALoading} onClick={() => void evaluateCase2A(revisedCost, `${goal.target_year}-${String(goal.target_month).padStart(2, "0")}`)} className="mt-3 rounded-lg bg-amber-900 px-3 py-2 text-xs font-bold text-white disabled:opacity-50">Recalculate reduced target</button>
            </div>
            <div className="rounded-lg border border-amber-200 bg-white p-3">
              <h4 className="font-bold text-slate-900">Option B — Extend Timeline</h4>
              <p className="mt-1 text-xs text-slate-600">Keep today's goal cost unchanged; change only the target date.</p>
              <label className="mt-3 block text-xs font-bold text-slate-700">Revised target month
                <input type="month" value={revisedTargetDate} onChange={(event) => setRevisedTargetDate(event.target.value)} className="mt-1 w-full rounded-lg border border-amber-300 px-3 py-2 text-sm" />
              </label>
              <button type="button" disabled={case2ALoading} onClick={() => void evaluateCase2A(String(goal.today_cost), revisedTargetDate)} className="mt-3 rounded-lg bg-amber-900 px-3 py-2 text-xs font-bold text-white disabled:opacity-50">Recalculate extended timeline</button>
            </div>
          </div>
          {scenarioError && <p role="alert" className="mt-2 text-sm font-semibold text-rose-700">{scenarioError}</p>}
          {case2APreview && <div className="mt-4 rounded-lg border border-amber-200 bg-white p-3">
            <p className="text-xs font-black uppercase tracking-wider text-slate-500">Unsaved scenario result · {case2APreview.feasibility_status ?? "unknown"}</p>
            <div className="mt-2 grid gap-2 sm:grid-cols-3">
              <Value label="Revised future target" value={amount(case2APreview.future_target)} />
              <Value label="Revised funding gap" value={amount(case2APreview.funding_gap)} />
              <Value label="Additional required SIP" value={amount(case2APreview.additional_required_monthly_sip ?? case2APreview.required_monthly_contribution)} />
            </div>
            <p className="mt-2 text-sm text-slate-700">{case2APreview.feasibility_reason ?? case2APreview.explanation}</p>
          </div>}
        </div>}
        {goal.fund_feasibility_case === "case_2_capacity_shortfall" && <div className="mt-4 rounded-xl border border-slate-200 bg-white p-4">
          <h3 className="font-extrabold text-slate-950">Case 2B — Keep Goal Amount and Target Date Fixed</h3>
          <div className="mt-2 grid gap-3 sm:grid-cols-2">
            <Value label="Surplus gap" value={amount(goal.surplus_gap)} />
            <Value label="Required surplus increase" value={goal.available_monthly_surplus != null && goal.available_monthly_surplus <= 0 ? "Amount required; percentage not applicable" : goal.required_surplus_increase_pct == null ? "Not available" : `${goal.required_surplus_increase_pct.toFixed(1)}%`} />
          </div>
          <ul className="mt-3 list-inside list-disc space-y-1 text-sm text-slate-700">
            <li>Review reliable income increases and expense reductions through Budgeting / Cash Flow; changes require investor approval.</li>
            <li>Step-Up SIP is shown only when an investor-approved dated contribution schedule is supplied; no assumed step-up rate is used.</li>
            <li>Lump Sum / Lump Sum + SIP remain unassessed until an eligible, liquid, suitable, uncommitted funding amount and approved dated method are available.</li>
            <li>Review debt / EMI restructuring only where a verified reduction in monthly EMI is available, including fees and total borrowing cost.</li>
          </ul>
          <p className="mt-3 text-xs font-semibold text-slate-500">No borrowing, asset sale, withdrawal, redirection of another goal's investments or plan change is performed by this assessment.</p>
        </div>}
      </section>}
      <section className="py-7">
        <p className="text-xs font-bold uppercase tracking-wider text-slate-500">Investor decision</p>
        <h2 className="mt-1 text-lg font-extrabold text-slate-950">No funding strategy has been selected</h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">Goal Feasibility and strategy evaluations are decision inputs. Review the available alternatives before choosing how to proceed.</p>
        <Link href={`/investor/strategy-builder?goalId=${encodeURIComponent(goal.goal_id)}`} className="mt-4 inline-flex rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-bold text-white">Continue to Strategy Builder →</Link>
      </section>
    </div>
  </main>;
}