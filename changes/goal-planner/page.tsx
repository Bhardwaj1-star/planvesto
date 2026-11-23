"use client";

/**
 * PROPOSED CHANGE — Goal Planner / Case 2A
 *
 * This file is intentionally kept under /changes and is not wired into the
 * production Next.js route. It does not modify the existing Goal Planner.
 *
 * Case 1's verified Available Monthly Surplus is treated as a fixed ceiling.
 * Case 2A searches for:
 *   A. The highest affordable today's goal cost at the existing target date.
 *   B. The earliest affordable target month at the existing today's goal cost.
 *
 * Every candidate is evaluated by the existing canonical /api/goals/calculate
 * endpoint. Only a preview is produced; saving still requires investor approval.
 */

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { buildFinancialState } from "../../frontend/lib/api/financial-state";
import { getLatestDefinedGoal } from "../../frontend/lib/api/goals";
import type { DefinedGoal } from "../../frontend/lib/onboarding/goals/types";
import { getPlanningUnitId } from "../../frontend/lib/planning-unit";
import { apiRequest } from "../../frontend/lib/api/client";

type Scenario = {
  kind: "amount" | "timeline";
  result: DefinedGoal;
  label: string;
};

const money = new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
  maximumFractionDigits: 0,
});

const amount = (value: number | null | undefined) =>
  value == null ? "Not available" : money.format(value);

function monthIndex(year: number, month: number) {
  return year * 12 + month - 1;
}

function monthParts(index: number) {
  return { year: Math.floor(index / 12), month: (index % 12) + 1 };
}

function isAffordable(candidate: DefinedGoal, fixedSurplus: number) {
  const required = Number(candidate.required_monthly_contribution ?? 0);
  const alreadyAllocated = Number(candidate.existing_goal_sip_monthly ?? 0);
  const additional = Math.max(
    0,
    Number(candidate.additional_required_monthly_sip ?? required - alreadyAllocated),
  );
  return Number.isFinite(additional) && additional <= fixedSurplus;
}

async function calculateCandidate(
  goal: DefinedGoal,
  todayCost: number,
  targetYear: number,
  targetMonth: number,
) {
  return apiRequest<DefinedGoal>("/api/goals/calculate", {
    method: "POST",
    body: JSON.stringify({
      planning_unit_id: goal.planning_unit_id,
      goal_id: goal.goal_id,
      goal_name: goal.goal_name,
      goal_type: goal.goal_type,
      today_cost: todayCost,
      target_month: targetMonth,
      target_year: targetYear,
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
        allocation_value: Number(
          mapping.allocation_value ?? mapping.allocated_percentage ?? 100,
        ),
        allocation_percentage: Number(mapping.allocated_percentage ?? 100),
        expected_annual_return_pct: Number(mapping.expected_return ?? 10),
        return_frequency: mapping.return_frequency ?? "annual",
      })),
      dynamic_details:
        (goal.version_metadata?.dynamic_details as Record<string, unknown>) ?? {},
    }),
  });
}

export default function ProposedGoalFeasibilityPage() {
  const { goalId } = useParams<{ goalId: string }>();
  const [goal, setGoal] = useState<DefinedGoal | null>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<"amount" | "timeline" | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [scenario, setScenario] = useState<Scenario | null>(null);

  useEffect(() => {
    let active = true;
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const planningUnitId = await getPlanningUnitId();
        await buildFinancialState(planningUnitId, "family");
        const latest = await getLatestDefinedGoal(planningUnitId, goalId);
        if (active) setGoal(latest);
      } catch (cause) {
        if (active) {
          setError(
            cause instanceof Error
              ? cause.message
              : "Unable to load Goal Feasibility.",
          );
        }
      } finally {
        if (active) setLoading(false);
      }
    }
    void load();
    return () => {
      active = false;
    };
  }, [goalId]);

  async function findAffordableAmount() {
    if (!goal || goal.available_monthly_surplus == null) return;
    setBusy("amount");
    setError(null);
    setScenario(null);
    try {
      const ceiling = Number(goal.available_monthly_surplus);
      let low = 1;
      let high = Math.floor(Number(goal.today_cost));
      let best: DefinedGoal | null = null;

      // Monotonic search: lower today's cost cannot increase the SIP requirement.
      for (let step = 0; step < 24 && low <= high; step += 1) {
        const mid = Math.floor((low + high) / 2);
        const candidate = await calculateCandidate(
          goal,
          mid,
          Number(goal.target_year),
          Number(goal.target_month),
        );
        if (isAffordable(candidate, ceiling)) {
          best = candidate;
          low = mid + 1;
        } else {
          high = mid - 1;
        }
      }

      if (!best) {
        throw new Error(
          "No affordable goal amount was found in the valid search range. Review the funding assumptions and eligible assets.",
        );
      }
      setScenario({
        kind: "amount",
        result: best,
        label: "Highest affordable goal amount (today's cost)",
      });
    } catch (cause) {
      setError(
        cause instanceof Error ? cause.message : "Amount scenario failed.",
      );
    } finally {
      setBusy(null);
    }
  }

  async function findEarliestAffordableMonth() {
    if (!goal || goal.available_monthly_surplus == null) return;
    setBusy("timeline");
    setError(null);
    setScenario(null);
    try {
      const ceiling = Number(goal.available_monthly_surplus);
      const currentIndex = monthIndex(
        Number(goal.target_year),
        Number(goal.target_month),
      );
      let low = currentIndex + 1;
      let high = currentIndex + 50 * 12;
      const highDate = monthParts(high);

      // First verify that a solution exists within the 50-year search horizon.
      const farCandidate = await calculateCandidate(
        goal,
        Number(goal.today_cost),
        highDate.year,
        highDate.month,
      );
      if (!isAffordable(farCandidate, ceiling)) {
        throw new Error(
          "The current surplus does not support this goal within the 50-year search horizon. Review the goal assumptions or funding capacity.",
        );
      }

      let best = farCandidate;
      // Find the earliest month that satisfies the same fixed surplus ceiling.
      for (let step = 0; step < 24 && low <= high; step += 1) {
        const mid = Math.floor((low + high) / 2);
        const date = monthParts(mid);
        const candidate = await calculateCandidate(
          goal,
          Number(goal.today_cost),
          date.year,
          date.month,
        );
        if (isAffordable(candidate, ceiling)) {
          best = candidate;
          high = mid - 1;
        } else {
          low = mid + 1;
        }
      }

      setScenario({
        kind: "timeline",
        result: best,
        label: "Earliest affordable target month",
      });
    } catch (cause) {
      setError(
        cause instanceof Error ? cause.message : "Timeline scenario failed.",
      );
    } finally {
      setBusy(null);
    }
  }

  if (loading) {
    return <main className="min-h-screen bg-slate-50 p-8">Loading Goal Feasibility…</main>;
  }

  if (error && !goal) {
    return <main className="min-h-screen bg-slate-50 p-8 text-rose-700">{error}</main>;
  }

  if (!goal) {
    return <main className="min-h-screen bg-slate-50 p-8">Goal not found.</main>;
  }

  const surplus = goal.available_monthly_surplus;
  const hasSurplus = surplus != null && Number.isFinite(Number(surplus));

  return (
    <main className="min-h-screen bg-slate-50 px-5 py-10 text-slate-900">
      <div className="mx-auto max-w-5xl space-y-6">
        <header>
          <p className="text-xs font-bold uppercase tracking-wider text-teal-800">
            Proposed change · Goal Planner
          </p>
          <h1 className="mt-1 text-3xl font-extrabold">Goal Feasibility</h1>
          <p className="mt-2 text-sm text-slate-600">
            Case 1's verified monthly surplus is the fixed affordability limit
            for both Case 2A options.
          </p>
        </header>

        <section className="grid gap-4 rounded-xl border border-teal-200 bg-white p-5 sm:grid-cols-3">
          <div>
            <p className="text-xs font-semibold text-slate-500">Goal</p>
            <p className="mt-1 font-bold">{goal.goal_name}</p>
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500">
              Case 1 · Verified Available Monthly Surplus
            </p>
            <p className="mt-1 text-xl font-extrabold text-teal-800">
              {amount(surplus)}
            </p>
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500">
              Current required additional SIP
            </p>
            <p className="mt-1 text-xl font-extrabold">
              {amount(goal.additional_required_monthly_sip)}
            </p>
          </div>
        </section>

        {!hasSurplus && (
          <p className="rounded-lg border border-amber-300 bg-amber-50 p-4 text-sm text-amber-900">
            Verified Available Monthly Surplus is unavailable. Complete Financial
            State before evaluating Case 2A.
          </p>
        )}

        <section className="rounded-xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-xs font-black uppercase tracking-wider text-amber-800">
            Case 2A
          </p>
          <h2 className="mt-1 text-xl font-extrabold">
            Adjust goal amount or timeline
          </h2>
          <p className="mt-2 text-sm text-amber-950">
            The surplus above is held fixed. Each option changes only one goal
            variable and searches for a result whose additional required SIP does
            not exceed that surplus.
          </p>

          <div className="mt-5 grid gap-4 md:grid-cols-2">
            <article className="rounded-lg border border-amber-200 bg-white p-4">
              <h3 className="font-bold">Option A · Reduce goal amount</h3>
              <p className="mt-1 text-sm text-slate-600">
                Keep the existing target month unchanged. Find the highest
                affordable today's goal cost.
              </p>
              <button
                type="button"
                disabled={!hasSurplus || busy !== null}
                onClick={() => void findAffordableAmount()}
                className="mt-4 rounded-lg bg-amber-900 px-4 py-2.5 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-50"
              >
                {busy === "amount" ? "Calculating…" : "Find affordable goal amount"}
              </button>
            </article>

            <article className="rounded-lg border border-amber-200 bg-white p-4">
              <h3 className="font-bold">Option B · Extend goal timeline</h3>
              <p className="mt-1 text-sm text-slate-600">
                Keep today's goal amount unchanged. Find the earliest affordable
                target month (search horizon: 50 years).
              </p>
              <button
                type="button"
                disabled={!hasSurplus || busy !== null}
                onClick={() => void findEarliestAffordableMonth()}
                className="mt-4 rounded-lg bg-amber-900 px-4 py-2.5 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-50"
              >
                {busy === "timeline" ? "Calculating…" : "Find affordable target month"}
              </button>
            </article>
          </div>
        </section>

        {error && (
          <p role="alert" className="rounded-lg border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800">
            {error}
          </p>
        )}

        {scenario && (
          <section className="space-y-4 rounded-xl border border-teal-200 bg-white p-5">
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-teal-800">
                Proposed scenario · Not saved
              </p>
              <h2 className="mt-1 text-xl font-extrabold">{scenario.label}</h2>
            </div>
            <div className="grid gap-4 sm:grid-cols-3">
              <div>
                <p className="text-xs text-slate-500">Revised today's goal cost</p>
                <p className="mt-1 font-extrabold">{amount(scenario.result.today_cost)}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500">Revised future target</p>
                <p className="mt-1 font-extrabold">{amount(scenario.result.future_target)}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500">Required additional SIP</p>
                <p className="mt-1 font-extrabold">
                  {amount(scenario.result.additional_required_monthly_sip)}
                </p>
              </div>
              <div>
                <p className="text-xs text-slate-500">Fixed Case 1 surplus</p>
                <p className="mt-1 font-extrabold">{amount(surplus)}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500">Revised target month</p>
                <p className="mt-1 font-extrabold">
                  {new Date(
                    Number(scenario.result.target_year),
                    Number(scenario.result.target_month) - 1,
                    1,
                  ).toLocaleDateString("en-IN", { month: "long", year: "numeric" })}
                </p>
              </div>
              <div>
                <p className="text-xs text-slate-500">Funding gap</p>
                <p className="mt-1 font-extrabold">{amount(scenario.result.funding_gap)}</p>
              </div>
            </div>
            <p className="text-sm text-slate-700">
              {scenario.result.feasibility_reason || scenario.result.explanation}
            </p>
            <p className="border-t border-slate-200 pt-3 text-xs font-semibold text-slate-500">
              This is a calculation preview only. The saved goal remains unchanged;
              investor approval is required before any adoption.
            </p>
          </section>
        )}
      </div>
    </main>
  );
}
