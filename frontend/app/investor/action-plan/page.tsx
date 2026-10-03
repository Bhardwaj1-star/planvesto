"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorStatus } from "../../../components/InvestorUI";
import { getPlanningUnitId } from "../../../lib/api/client";
import { getStrategyVersionById, type StrategyVersion } from "../../../lib/api/strategy-version";
import { getActions, generateStrategyActions, type ActionPlanItem } from "../../../lib/api/action-plan";

export default function ActionPlanPage() {
  const [strategyVersionId, setStrategyVersionId] = useState("");
  const [version, setVersion] = useState<StrategyVersion | null>(null);
  const [actions, setActions] = useState<ActionPlanItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    const requested = typeof window !== "undefined"
      ? new URLSearchParams(window.location.search).get("strategyVersionId")
      : null;
    setStrategyVersionId(requested ?? "");
  }, []);

  const load = async (versionId: string) => {
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
    const [nextVersion, nextActions] = await Promise.all([
      getStrategyVersionById(planningUnitId, versionId),
      getActions(planningUnitId, versionId),
    ]);
    setVersion(nextVersion);
    setActions(nextActions);
  };

  useEffect(() => {
    if (!strategyVersionId) {
      setLoading(false);
      setError("A selected Strategy Version is required to open the Action Plan. Lock a decision in Participate With Numbers first.");
      return;
    }
    let active = true;
    (async () => {
      setLoading(true);
      setError(null);
      setMessage(null);
      try {
        await load(strategyVersionId);
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load the Action Plan.");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, [strategyVersionId]);

  const generate = async () => {
    if (!strategyVersionId) return;
    setWorking(true);
    setError(null);
    setMessage(null);
    try {
      const planningUnitId = getPlanningUnitId();
      if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
      const generated = await generateStrategyActions(planningUnitId, strategyVersionId);
      setActions(generated);
      setMessage(
        generated.length
          ? `${generated.length} execution point${generated.length === 1 ? "" : "s"} generated from the selected Strategy Version.`
          : "No new execution points were generated. Existing execution points are already materialized for this Strategy Version.",
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to generate execution points. The selected Strategy Version may require approval first.");
    } finally {
      setWorking(false);
    }
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
        eyebrow="Implement"
        title="Action Plan"
        description="Execution points derived from the selected Strategy Version. This is the implementation layer, not the detailed goal report."
      >
        <div className="flex flex-wrap items-center gap-2">
          <Link
            href="/investor/reports"
            className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-700 shadow-sm"
          >
            View Report
          </Link>
          <button
            type="button"
            onClick={() => void generate()}
            disabled={working || !strategyVersionId}
            className="rounded-xl bg-navy-900 px-4 py-2.5 text-xs font-bold text-white shadow-sm disabled:opacity-50"
          >
            {working ? "Generating…" : "Generate Execution Points"}
          </button>
        </div>
      </InvestorHeader>

      <div className="mx-auto max-w-6xl space-y-6 p-4 sm:p-6 lg:p-10">

        {error && <InvestorStatus tone="error">{error}</InvestorStatus>}
        {message && <InvestorStatus tone="success">{message}</InvestorStatus>}

        {version && (
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-wider text-teal-700">Single Source of Truth</p>
                <h2 className="mt-1 text-xl font-extrabold text-slate-900">
                  Strategy Version {version.version}
                </h2>
                <p className="mt-1 text-sm text-slate-500">
                  {version.strategy_id} · {version.source} · Version ID: {version.strategy_version_id}
                </p>
              </div>
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold text-slate-700">
                {version.status}
              </span>
            </div>
          </section>
        )}

        {!strategyVersionId && (
          <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
            <h2 className="text-xl font-bold">No Strategy Version selected</h2>
            <p className="mt-2 text-sm text-slate-500">Return to Participate With Numbers and lock a strategy decision.</p>
          </section>
        )}

        {strategyVersionId && !error && actions.length === 0 && (
          <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
            <h2 className="text-xl font-bold">No Execution Points Yet</h2>
            <p className="mx-auto mt-2 max-w-2xl text-sm leading-6 text-slate-500">
              The Action Plan is generated from this exact Strategy Version. If generation is blocked, the Strategy Version must pass the existing approval gate before implementation actions can be materialized.
            </p>
            <button
              type="button"
              onClick={() => void generate()}
              disabled={working}
              className="mt-6 rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white disabled:opacity-50"
            >
              {working ? "Generating…" : "Generate Execution Points"}
            </button>
          </section>
        )}

        {actions.length > 0 && (
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-end justify-between gap-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-wider text-teal-700">Execution Layer</p>
                <h2 className="mt-1 text-2xl font-extrabold">What needs to be executed</h2>
                <p className="mt-1 text-sm text-slate-500">
                  These are implementation points, not another financial report.
                </p>
              </div>
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold text-slate-700">
                {actions.length} points
              </span>
            </div>

            <div className="mt-6 space-y-3">
              {actions.map((action, index) => (
                <article key={action.action_id ?? `action-${index}`} className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                    <div className="flex gap-4">
                      <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-navy-900 text-xs font-bold text-white">
                        {index + 1}
                      </span>
                      <div>
                        <h3 className="font-extrabold text-slate-900">{action.title}</h3>
                        {action.description && <p className="mt-1 text-sm leading-6 text-slate-600">{action.description}</p>}
                      </div>
                    </div>
                    <div className="flex shrink-0 items-center gap-2">
                      <span className="rounded-full border border-slate-200 bg-white px-2.5 py-1 text-[11px] font-bold uppercase tracking-wide text-slate-600">
                        {action.priority}
                      </span>
                      <span className="rounded-full border border-slate-200 bg-white px-2.5 py-1 text-[11px] font-bold text-slate-600">
                        {action.status}
                      </span>
                    </div>
                  </div>
                  {(action.deadline || action.planned_impact) && (
                    <div className="mt-4 flex flex-wrap gap-3 border-t border-slate-200 pt-3 text-xs text-slate-500">
                      {action.deadline && <span>Deadline: <strong className="text-slate-700">{action.deadline}</strong></span>}
                      <span>Strategy Version: <strong className="text-slate-700">{action.strategy_version_id}</strong></span>
                    </div>
                  )}
                </article>
              ))}
            </div>
          </section>
        )}
      </div>
    </main>
  );
}
