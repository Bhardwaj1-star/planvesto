"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { getLatestStrategyRun, getPlanningUnitId, type StrategyRun } from "../../../lib/api/strategy";
import { approveStrategy, type SuitabilityStatus } from "../../../lib/api/strategy-approval";

const STATUSES: SuitabilityStatus[] = ["Suitable", "Needs Attention", "Unsuitable"];

export default function StrategyApprovalPage() {
  const [run, setRun] = useState<StrategyRun | null>(null);
  const [status, setStatus] = useState<SuitabilityStatus>("Suitable");
  const [acknowledgement, setAcknowledgement] = useState("");
  const [makePrimary, setMakePrimary] = useState(true);
  const [primaryDecision, setPrimaryDecision] = useState<"archive_previous" | "keep_previous_approved">("archive_previous");
  const [pendingDisposition, setPendingDisposition] = useState<"retain_for_reassessment" | "cancel">("retain_for_reassessment");
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
        const savedGoalId = typeof window !== "undefined" ? window.localStorage.getItem("planvesto-strategy-approval-goal-id") : null;
        if (!savedGoalId) throw new Error("No Strategy Builder selection is ready for approval. Select and save a Strategy Version first.");
        const latest = await getLatestStrategyRun(planningUnitId, savedGoalId);
        if (active) setRun(latest);
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load selected strategy.");
      } finally { if (active) setLoading(false); }
    })();
    return () => { active = false; };
  }, []);

  const selectedStrategy = useMemo(() => {
    if (!run?.selected_strategy_id) return null;
    return run.applicable_strategies.find((strategy) => strategy.strategy_id === run.selected_strategy_id) ?? null;
  }, [run]);

  const requiresAcknowledgement = status !== "Suitable";
  const replacingExistingPrimary = makePrimary && false;

  const handleApprove = async () => {
    if (!run?.strategy_run_id || !run.selected_strategy_id || !run.selected_strategy_version_id || run.selected_strategy_version == null) {
      setError("A selected Strategy Version is required before approval.");
      return;
    }
    if (requiresAcknowledgement && !acknowledgement.trim()) {
      setError(`${status} requires acknowledgement text.`);
      return;
    }

    setWorking(true); setError(null); setSuccess(null);
    try {
      const planningUnitId = getPlanningUnitId();
      if (!planningUnitId) throw new Error("Planning unit is not available.");
      const result = await approveStrategy({
        planning_unit_id: planningUnitId,
        strategy_run_id: run.strategy_run_id,
        suitability: {
          status,
          diagnostics: [],
          rule_set_version: "framework-1.0",
          evaluated_at: new Date().toISOString(),
        },
        acknowledgement_text: requiresAcknowledgement ? acknowledgement.trim() : null,
        make_primary: makePrimary,
        primary_transition_decision: makePrimary ? primaryDecision : null,
        pending_action_disposition: makePrimary ? pendingDisposition : null,
      });
      setSuccess(`Strategy Version ${result.strategy_version} approved${result.is_primary ? " and made Primary" : ""}.`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Approval failed.");
    } finally { setWorking(false); }
  };

  if (loading) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-4xl"><div className="h-10 w-72 animate-pulse rounded-xl bg-slate-200" /><div className="mt-6 h-96 animate-pulse rounded-3xl bg-white" /></div></main>;

  if (!run?.selected_strategy_id || !run.selected_strategy_version_id) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-2xl rounded-3xl border border-slate-200 bg-white p-10 text-center shadow-sm"><h1 className="text-2xl font-extrabold">No Strategy Version selected</h1><p className="mt-2 text-sm text-slate-500">Approval is available only after Strategy Builder creates a selected Strategy Version.</p><Link href="/investor/strategy-builder" className="mt-6 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white">Return to Strategy Builder</Link></div></main>;

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
      <div className="mx-auto max-w-4xl space-y-6 p-6 lg:p-10">
        <header>
          <Link href="/investor/strategy-builder" className="text-sm font-semibold text-teal-700">← Strategy Builder</Link>
          <p className="mt-6 text-sm font-semibold uppercase tracking-[0.16em] text-teal-700">Final decision</p>
          <h1 className="mt-1 text-3xl font-extrabold tracking-tight">Strategy Approval</h1>
          <p className="mt-2 text-sm leading-6 text-slate-500">Review the selected Strategy Version, record suitability, and approve the immutable strategy snapshot.</p>
        </header>

        {error && <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">{error}</div>}
        {success && <div className="rounded-2xl border border-emerald-200 bg-emerald-50 px-5 py-4 text-sm text-emerald-700">{success}</div>}

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Selected Strategy</p>
          <h2 className="mt-2 text-2xl font-extrabold">{selectedStrategy?.name ?? run.selected_strategy_id}</h2>
          <p className="mt-1 text-sm text-slate-500">Scenario: {run.selected_scenario_id ?? "—"}</p>
          <div className="mt-5 flex flex-wrap gap-3 text-xs text-slate-600"><span className="rounded-full bg-slate-100 px-3 py-1">Strategy Version {run.selected_strategy_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Goal Version {run.defined_goal_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Run v{run.run_version}</span></div>
        </section>

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-bold">Suitability</h2>
          <p className="mt-1 text-sm text-slate-500">Record the suitability assessment for this selected Strategy Version. The backend owns approval validation.</p>
          <div className="mt-5 grid gap-3 sm:grid-cols-3">
            {STATUSES.map((option) => <button key={option} type="button" onClick={() => setStatus(option)} className={`rounded-2xl border p-4 text-left transition ${status === option ? "border-teal-500 bg-teal-50 ring-2 ring-teal-100" : "border-slate-200 hover:bg-slate-50"}`}><p className="font-bold">{option}</p><p className="mt-1 text-xs text-slate-500">{option === "Suitable" ? "No acknowledgement required." : "Explicit acknowledgement required."}</p></button>)}
          </div>
          {requiresAcknowledgement && <label className="mt-5 block"><span className="text-sm font-bold">Acknowledgement</span><textarea value={acknowledgement} onChange={(e) => setAcknowledgement(e.target.value)} rows={4} placeholder={`Explain why you acknowledge the ${status} assessment.`} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-teal-600" /></label>}
        </section>

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-bold">Primary Strategy</h2>
          <label className="mt-4 flex items-start gap-3"><input type="checkbox" checked={makePrimary} onChange={(e) => setMakePrimary(e.target.checked)} className="mt-1 h-4 w-4" /><span><span className="text-sm font-bold">Make this the Primary Strategy</span><span className="mt-1 block text-xs text-slate-500">If enabled, the backend will apply the Primary Strategy lifecycle rules.</span></span></label>
          {makePrimary && <div className="mt-5 grid gap-4 md:grid-cols-2"><label className="block"><span className="text-sm font-bold">Existing Primary transition</span><select value={primaryDecision} onChange={(e) => setPrimaryDecision(e.target.value as typeof primaryDecision)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm"><option value="archive_previous">Archive previous</option><option value="keep_previous_approved">Keep previous approved</option></select><p className="mt-1 text-xs text-slate-500">Used by the backend when replacing an existing Primary Strategy.</p></label><label className="block"><span className="text-sm font-bold">Pending implementation actions</span><select value={pendingDisposition} onChange={(e) => setPendingDisposition(e.target.value as typeof pendingDisposition)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm"><option value="retain_for_reassessment">Retain for reassessment</option><option value="cancel">Cancel</option></select><p className="mt-1 text-xs text-slate-500">Used when the backend detects replacement of an existing Primary Strategy.</p></label></div>}
        </section>

        <button onClick={handleApprove} disabled={working} className="w-full rounded-2xl bg-navy-900 px-5 py-4 text-sm font-extrabold text-white disabled:cursor-not-allowed disabled:opacity-50">{working ? "Approving…" : "Approve Strategy Version"}</button>
        {replacingExistingPrimary && <p className="text-xs text-slate-500">Primary transition decisions are validated by the backend.</p>}
      </div>
    </main>
  );
}
