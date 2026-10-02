import React from "react";
import Link from "next/link";
import { formatINR } from "../../lib/onboarding/goals/goals";
import { withReturnTo } from "../../lib/workflow-navigation";
import type { DefinedGoal } from "../../lib/onboarding/goals/types";

type GoalFeasibilityProps = {
  goal: Pick<
    DefinedGoal,
    | "feasibility_status"
    | "feasibility_reason"
    | "available_monthly_surplus"
    | "required_monthly_contribution"
    | "workflow_readiness"
  >;
};

export default function GoalFeasibility({ goal }: GoalFeasibilityProps) {
  const status = goal.feasibility_status || "unknown";
  const config = status === "feasible"
    ? { label: "Feasible", cls: "border-teal-200 bg-teal-50 text-teal-800" }
    : status === "constrained"
      ? { label: "Constrained", cls: "border-amber-200 bg-amber-50 text-amber-800" }
      : status === "infeasible"
        ? { label: "Infeasible", cls: "border-rose-200 bg-rose-50 text-rose-800" }
        : { label: "Unknown", cls: "border-slate-200 bg-slate-50 text-slate-700" };
  const nextAction = goal.workflow_readiness?.next_action
    ?? goal.workflow_readiness?.blockers.find((blocker) => blocker.next_action)?.next_action;
  const returnTo = goal.workflow_readiness?.return_to;
  const missingData = goal.workflow_readiness?.blockers.flatMap((blocker) => blocker.missing_data) ?? [];
  const financialStateReturn = withReturnTo("/investor/financial-state", returnTo);

  return <div className={`mt-4 rounded-xl border p-3 ${config.cls}`}>
    <div className="flex flex-wrap items-center justify-between gap-2">
      <span className="text-xs font-black uppercase tracking-wider">Goal Feasibility</span>
      <span className="rounded-md border border-current/20 px-2 py-0.5 text-xs font-black uppercase">{config.label}</span>
    </div>
    {goal.feasibility_reason && <p className="mt-1.5 text-xs font-semibold">{goal.feasibility_reason}</p>}
    {goal.available_monthly_surplus != null && goal.required_monthly_contribution != null && (
      <p className="mt-1.5 text-[11px] font-medium opacity-80">
        Current surplus {formatINR(goal.available_monthly_surplus)} / month · Required {formatINR(goal.required_monthly_contribution)} / month
      </p>
    )}
    {missingData.length > 0 && (
      <div className="mt-2 text-xs">
        <p className="font-bold">Missing data</p>
        <ul className="mt-1 list-inside list-disc space-y-1">
          {missingData.map((item) => (
            <li key={item.label}>
              {item.route
                ? <Link href={withReturnTo(item.route, financialStateReturn)} className="font-semibold underline underline-offset-2">{item.label}</Link>
                : item.label}
            </li>
          ))}
        </ul>
      </div>
    )}
    {nextAction && (
      <Link href={withReturnTo(nextAction.route, returnTo)} className="mt-2 inline-flex items-center gap-1 text-xs font-bold underline underline-offset-2">
        {nextAction.label} <span aria-hidden="true">→</span>
      </Link>
    )}
  </div>;
}