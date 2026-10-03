"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorStatus } from "../../../components/InvestorUI";
import { getPlanningUnitId } from "../../../lib/api/client";
import { getGoals, getLatestDefinedGoal, type GoalSummary } from "../../../lib/api/goals";
import { getSelectedStrategyVersion } from "../../../lib/api/strategy";
import { getStrategyVersionById, type StrategyVersion } from "../../../lib/api/strategy-version";
import {
  completeAction,
  getActions,
  generateStrategyActions,
  type ActionPlanItem,
} from "../../../lib/api/action-plan";

type GoalExecutionState = GoalSummary & {
  strategyVersionId: string | null;
  strategyVersionNumber: number | null;
  actionCount: number;
  completedCount: number;
  pendingCount: number;
  skippedCount: number;
};

const actionStatusLabel: Record<string, string> = {
  planned: "Pending",
  confirmed: "Confirmed",
  completed: "Completed",
  cancelled: "Skipped",
};

const actionStatusClass: Record<string, string> = {
  planned: "border-amber-200 bg-amber-50 text-amber-700",
  confirmed: "border-blue-200 bg-blue-50 text-blue-700",
  completed: "border-emerald-200 bg-emerald-50 text-emerald-700",
  cancelled: "border-slate-200 bg-slate-100 text-slate-600",
};

export default function ActionPlanPage() {
  const [goals, setGoals] = useState<GoalExecutionState[]>([]);
  const [selectedGoalId, setSelectedGoalId] = useState("");
  const [strategyVersionId, setStrategyVersionId] = useState("");
  const [version, setVersion] = useState<StrategyVersion | null>(null);
  const [actions, setActions] = useState<ActionPlanItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(false);
  const [completingActionId, setCompletingActionId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const refreshGoalStates = async (planningUnitId: string) => {
    const goalSummaries = await getGoals(planningUnitId);
    const states = await Promise.all(
      goalSummaries.map(async (goal) => {
        const selectedVersion = await getSelectedStrategyVersion(planningUnitId, goal.goal_id);
        if (!selectedVersion?.strategy_version_id) {
          return {
            ...goal,
            strategyVersionId: null,
            strategyVersionNumber: null,
            actionCount: 0,
            completedCount: 0,
            pendingCount: 0,
            skippedCount: 0,
          };
        }
        const goalActions = await getActions(planningUnitId, selectedVersion.strategy_version_id);
        return {
          ...goal,
          strategyVersionId: selectedVersion.strategy_version_id,
          strategyVersionNumber: selectedVersion.version,
          actionCount: goalActions.length,
          completedCount: goalActions.filter((action) => action.status === "completed").length,
          pendingCount: goalActions.filter((action) => action.status === "planned" || action.status === "confirmed").length,
          skippedCount: goalActions.filter((action) => action.status === "cancelled").length,
        };
      }),
    );
    setGoals(states);
    return states;
  };

  const loadSelectedGoal = async (planningUnitId: string, goalId: string, selectedVersionId?: string | null) => {
    const resolvedVersionId = selectedVersionId ?? goals.find((goal) => goal.goal_id === goalId)?.strategyVersionId ?? "";
    setSelectedGoalId(goalId);
    setStrategyVersionId(resolvedVersionId);
    setVersion(null);
    setActions([]);
    setMessage(null);

    if (!resolvedVersionId) return;

    const [nextVersion, nextActions] = await Promise.all([
      getStrategyVersionById(planningUnitId, resolvedVersionId),
      getActions(planningUnitId, resolvedVersionId),
    ]);
    setVersion(nextVersion);
    setActions(nextActions);
  };

  useEffect(() => {
    let active = true;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
        const nextGoals = await refreshGoalStates(planningUnitId);
        if (!active || !nextGoals.length) return;

        const requestedGoalId = typeof window !== "undefined"
          ? new URLSearchParams(window.location.search).get("goalId")
          : null;
        const requestedGoal = nextGoals.find((goal) => goal.goal_id === requestedGoalId);
        const firstGoal = requestedGoal ?? nextGoals[0];
        await loadSelectedGoal(planningUnitId, firstGoal.goal_id, firstGoal.strategyVersionId);
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load the Action Plan.");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, []);

  const selectedGoal = useMemo(
    () => goals.find((goal) => goal.goal_id === selectedGoalId) ?? null,
    [goals, selectedGoalId],
  );

  const selectGoal = async (goal: GoalExecutionState) => {
    setError(null);
    setMessage(null);
    try {
      const planningUnitId = getPlanningUnitId();
      if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
      await loadSelectedGoal(planningUnitId, goal.goal_id, goal.strategyVersionId);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load this goal.");
    }
  };

  const generate = async () => {
    if (!strategyVersionId) return;
    setWorking(true);
    setError(null);
    setMessage(null);
    try {
      const planningUnitId = getPlanningUnitId();
      if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
      const generated = await generateStrategyActions(planningUnitId, strategyVersionId);
      const nextActions = await getActions(planningUnitId, strategyVersionId);
      setActions(nextActions);
      setMessage(
        generated.length
          ? `${generated.length} execution point${generated.length === 1 ? "" : "s"} generated from the selected Strategy Version.`
          : "No new execution points were generated. Existing execution points are already materialized for this Strategy Version.",
      );
      await refreshGoalStates(planningUnitId);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to generate execution points. The selected Strategy Version may require approval first.");
    } finally {
      setWorking(false);
    }
  };

  const markComplete = async (action: ActionPlanItem) => {
    if (!action.action_id) return;
    setCompletingActionId(action.action_id);
    setError(null);
    setMessage(null);
    try {
      const planningUnitId = getPlanningUnitId();
      if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
      const updated = await completeAction(planningUnitId, action.action_id);
      setActions((current) => current.map((item) => item.action_id === updated.action_id ? updated : item));
      await refreshGoalStates(planningUnitId);
      setMessage("Action marked as completed.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to complete this action.");
    } finally {
      setCompletingActionId(null);
    }
  };

  if (loading) {
    return (
      <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
        <div className="mx-auto max-w-6xl space-y-6">
          <div className="h-10 w-72 animate-pulse rounded-xl bg-slate-200" />
          <div className="h-32 animate-pulse rounded-3xl bg-white" />
          <div className="h-96 animate-pulse rounded-3xl bg-white" />
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
      <InvestorHeader
        eyebrow="Implement"
        title="Action Plan"
        description="Choose a goal, open its finalized Strategy Version, and execute the actions connected to that decision."
      >
        <div className="flex flex-wrap items-center gap-2">
          {strategyVersionId && (
            <Link
              href="/investor/reports"
              className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-700 shadow-sm"
            >
              View Report
            </Link>
          )}
        </div>
      </InvestorHeader>

      <div className="mx-auto max-w-6xl space-y-6 p-4 sm:p-6 lg:p-10">
        {error && <InvestorStatus tone="error">{error}</InvestorStatus>}
        {message && <InvestorStatus tone="success">{message}</InvestorStatus>}

        {goals.length === 0 ? (
          <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center shadow-sm">
            <p className="text-xs font-bold uppercase tracking-wider text-teal-700">No Goals</p>
            <h2 className="mt-2 text-2xl font-extrabold">No financial goals are available yet.</h2>
            <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-slate-500">
              Create a goal first. Once a strategy is finalized for that goal, its execution plan will appear here.
            </p>
            <Link
              href="/investor/goal-planner"
              className="mt-6 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white"
            >
              Go to Goal Planner
            </Link>
          </section>
        ) : (
          <>
            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div>
                <p className="text-xs font-bold uppercase tracking-wider text-teal-700">1 · Choose a goal</p>
                <h2 className="mt-1 text-2xl font-extrabold">Which goal are you working on?</h2>
                <p className="mt-2 text-sm leading-6 text-slate-500">
                  Every goal has its own finalized Strategy Version and execution state.
                </p>
              </div>

              <div className="mt-6 grid grid-cols-1 gap-3 md:grid-cols-2">
                {goals.map((goal) => {
                  const selected = goal.goal_id === selectedGoalId;
                  const finalized = Boolean(goal.strategyVersionId);
                  const progress = goal.actionCount ? Math.round((goal.completedCount / goal.actionCount) * 100) : 0;
                  return (
                    <button
                      key={goal.goal_id}
                      type="button"
                      onClick={() => void selectGoal(goal)}
                      className={`rounded-2xl border p-4 text-left transition ${
                        selected
                          ? "border-navy-900 bg-slate-50 shadow-sm"
                          : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50"
                      }`}
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <h3 className="font-extrabold text-slate-900">{goal.goal_name}</h3>
                          <p className="mt-1 text-xs text-slate-500">{goal.priority ?? "Medium"} priority · {goal.flexibility ?? "Flexible"}</p>
                        </div>
                        <span className={`rounded-full border px-2.5 py-1 text-[11px] font-bold ${finalized ? "border-emerald-200 bg-emerald-50 text-emerald-700" : "border-amber-200 bg-amber-50 text-amber-700"}`}>
                          {finalized ? `Version ${goal.strategyVersionNumber}` : "No finalized plan"}
                        </span>
                      </div>
                      <div className="mt-4 flex items-center justify-between text-xs">
                        <span className="text-slate-500">
                          {finalized
                            ? goal.actionCount
                              ? `${goal.completedCount}/${goal.actionCount} actions completed`
                              : "No actions generated yet"
                            : "Strategy decision still pending"}
                        </span>
                        {finalized && goal.actionCount > 0 && <strong className="text-slate-700">{progress}%</strong>}
                      </div>
                    </button>
                  );
                })}
              </div>
            </section>

            {selectedGoal && (
              <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-wider text-teal-700">2 · Goal plan</p>
                    <h2 className="mt-1 text-2xl font-extrabold">{selectedGoal.goal_name}</h2>
                    <p className="mt-2 text-sm text-slate-500">
                      {strategyVersionId
                        ? `Strategy Version ${selectedGoal.strategyVersionNumber} is the source of truth for this execution plan.`
                        : "This goal does not have a finalized Strategy Version yet."}
                    </p>
                  </div>
                  {strategyVersionId && (
                    <div className="flex flex-wrap gap-2">
                      <Link
                        href={`/investor/strategy-builder?goalId=${encodeURIComponent(selectedGoal.goal_id)}`}
                        className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-700"
                      >
                        View Strategy
                      </Link>
                      <Link
                        href="/investor/reports"
                        className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-700"
                      >
                        View Report
                      </Link>
                    </div>
                  )}
                </div>

                {!strategyVersionId ? (
                  <div className="mt-6 rounded-2xl border border-dashed border-amber-300 bg-amber-50 p-6">
                    <h3 className="font-extrabold text-amber-900">No finalized strategy for this goal</h3>
                    <p className="mt-2 text-sm leading-6 text-amber-800">
                      Finish Strategy Builder → Plan Your Implementation for this goal first. The Action Plan will become available after the Strategy Version is finalized.
                    </p>
                    <Link
                      href={`/investor/strategy-builder?goalId=${encodeURIComponent(selectedGoal.goal_id)}`}
                      className="mt-4 inline-flex rounded-xl bg-navy-900 px-4 py-2.5 text-xs font-bold text-white"
                    >
                      Build this goal's strategy
                    </Link>
                  </div>
                ) : (
                  <>
                    {version && (
                      <div className="mt-6 rounded-2xl bg-slate-50 p-5">
                        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                          <div>
                            <p className="text-xs font-bold uppercase tracking-wider text-teal-700">Finalized Strategy Version</p>
                            <h3 className="mt-1 text-lg font-extrabold text-slate-900">Version {version.version}</h3>
                            <p className="mt-1 text-xs text-slate-500">{version.strategy_id} · {version.source}</p>
                          </div>
                          <span className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-bold text-slate-700">{version.status}</span>
                        </div>
                      </div>
                    )}

                    <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
                      {[
                        ["Total", actions.length],
                        ["Completed", actions.filter((action) => action.status === "completed").length],
                        ["Pending", actions.filter((action) => action.status === "planned" || action.status === "confirmed").length],
                        ["Skipped", actions.filter((action) => action.status === "cancelled").length],
                      ].map(([label, value]) => (
                        <div key={label} className="rounded-2xl border border-slate-200 bg-white p-4">
                          <p className="text-xs font-semibold text-slate-500">{label}</p>
                          <p className="mt-1 text-2xl font-extrabold text-slate-900">{value}</p>
                        </div>
                      ))}
                    </div>

                    {actions.length === 0 ? (
                      <div className="mt-6 rounded-2xl border border-dashed border-slate-300 p-8 text-center">
                        <h3 className="text-lg font-extrabold">No execution points yet</h3>
                        <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-500">
                          The strategy is finalized, but its execution points have not been materialized yet.
                        </p>
                        <button
                          type="button"
                          onClick={() => void generate()}
                          disabled={working}
                          className="mt-5 rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white disabled:opacity-50"
                        >
                          {working ? "Generating…" : "Generate Execution Points"}
                        </button>
                      </div>
                    ) : (
                      <div className="mt-6">
                        <div className="flex items-end justify-between gap-4">
                          <div>
                            <p className="text-xs font-bold uppercase tracking-wider text-teal-700">3 · Execute</p>
                            <h3 className="mt-1 text-xl font-extrabold">What needs to be done</h3>
                            <p className="mt-1 text-sm text-slate-500">
                              Completed, pending, and skipped steps remain visible so nothing silently disappears.
                            </p>
                          </div>
                          <button
                            type="button"
                            onClick={() => void generate()}
                            disabled={working}
                            className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-700 disabled:opacity-50"
                          >
                            {working ? "Refreshing…" : "Refresh actions"}
                          </button>
                        </div>

                        <div className="mt-5 space-y-3">
                          {actions.map((action, index) => (
                            <article
                              key={action.action_id ?? `action-${index}`}
                              className={`rounded-2xl border p-5 ${
                                action.status === "completed"
                                  ? "border-emerald-200 bg-emerald-50/40"
                                  : action.status === "cancelled"
                                    ? "border-slate-200 bg-slate-50"
                                    : "border-slate-200 bg-white"
                              }`}
                            >
                              <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                                <div className="flex gap-4">
                                  <span className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-xs font-bold ${
                                    action.status === "completed" ? "bg-emerald-600 text-white" : "bg-navy-900 text-white"
                                  }`}>
                                    {action.status === "completed" ? "✓" : index + 1}
                                  </span>
                                  <div>
                                    <h4 className="font-extrabold text-slate-900">{action.title}</h4>
                                    {action.description && <p className="mt-1 text-sm leading-6 text-slate-600">{action.description}</p>}
                                    {action.deadline && (
                                      <p className="mt-3 text-xs text-slate-500">
                                        Deadline: <strong className="text-slate-700">{action.deadline}</strong>
                                      </p>
                                    )}
                                  </div>
                                </div>

                                <div className="flex shrink-0 flex-wrap items-center gap-2">
                                  <span className="rounded-full border border-slate-200 bg-white px-2.5 py-1 text-[11px] font-bold uppercase tracking-wide text-slate-600">
                                    {action.priority}
                                  </span>
                                  <span className={`rounded-full border px-2.5 py-1 text-[11px] font-bold ${actionStatusClass[action.status] ?? "border-slate-200 bg-slate-100 text-slate-600"}`}>
                                    {actionStatusLabel[action.status] ?? action.status}
                                  </span>
                                </div>
                              </div>

                              {action.status !== "completed" && action.status !== "cancelled" && action.action_id && (
                                <div className="mt-4 flex justify-end border-t border-slate-200 pt-3">
                                  <button
                                    type="button"
                                    onClick={() => void markComplete(action)}
                                    disabled={completingActionId === action.action_id}
                                    className="rounded-xl bg-emerald-600 px-4 py-2 text-xs font-bold text-white disabled:opacity-50"
                                  >
                                    {completingActionId === action.action_id ? "Saving…" : "Mark completed"}
                                  </button>
                                </div>
                              )}
                            </article>
                          ))}
                        </div>
                      </div>
                    )}
                  </>
                )}
              </section>
            )}
          </>
        )}
      </div>
    </main>
  );
}
