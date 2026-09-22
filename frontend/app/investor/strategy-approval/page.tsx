"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import StrategyWorkflowNav from "../../../components/StrategyWorkflowNav";
import { InvestorButton, InvestorPageHeader, InvestorStatus } from "../../../components/InvestorUI";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";
import { getLatestStrategyRun, getPlanningUnitId, type StrategyRun } from "../../../lib/api/strategy";
import { approveStrategy, type SuitabilityStatus } from "../../../lib/api/strategy-approval";

const STATUSES: SuitabilityStatus[] = ["Suitable", "Needs Attention", "Unsuitable"];
type GoalOption = { id: string; name: string };

export default function StrategyApprovalPage() {
  const [goals, setGoals] = useState<GoalOption[]>([]);
  const [goalId, setGoalId] = useState("");
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
  const [approvedVersionId, setApprovedVersionId] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const data = await loadGoalPlannerData();
        const nextGoals = (data?.goals ?? []).map((goal) => ({ id: goal.id, name: goal.name || "Untitled Goal" }));
        if (active) { setGoals(nextGoals); if (nextGoals[0]) setGoalId(nextGoals[0].id); }
      } catch (err) { if (active) setError(err instanceof Error ? err.message : "Unable to load goals."); }
      finally { if (active) setLoading(false); }
    })();
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!goalId) { setRun(null); return; }
    let active = true;
    (async () => {
      setError(null); setSuccess(null); setRun(null);
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
        const latest = await getLatestStrategyRun(planningUnitId, goalId);
        if (active) setRun(latest);
      } catch (err) { if (active) setError(err instanceof Error ? err.message : "Unable to load the latest Strategy Run."); }
    })();
    return () => { active = false; };
  }, [goalId]);

  const selectedStrategy = useMemo(() => run?.selected_strategy_id ? run.applicable_strategies.find((s) => s.strategy_id === run.selected_strategy_id) ?? null : null, [run]);
  const requiresAcknowledgement = status !== "Suitable";

  const handleApprove = async () => {
    if (!run?.strategy_run_id || !run.selected_strategy_version_id || run.selected_strategy_version == null) { setError("A selected Strategy Version is required before approval."); return; }
    if (requiresAcknowledgement && !acknowledgement.trim()) { setError(`${status} requires acknowledgement text.`); return; }
    setWorking(true); setError(null); setSuccess(null);
    try {
      const planningUnitId = getPlanningUnitId();
      if (!planningUnitId) throw new Error("Planning unit is not available.");
      const result = await approveStrategy({
        planning_unit_id: planningUnitId,
        strategy_run_id: run.strategy_run_id,
        suitability: { status },
        acknowledgement_text: requiresAcknowledgement ? acknowledgement.trim() : null,
        make_primary: makePrimary,
        primary_transition_decision: makePrimary ? primaryDecision : null,
        pending_action_disposition: makePrimary ? pendingDisposition : null,
      });
      setApprovedVersionId(result.strategy_version_id);
      setSuccess(`Strategy Version ${result.strategy_version} approved${result.is_primary ? " and made Primary" : ""}.`);
    } catch (err) { setError(err instanceof Error ? err.message : "Approval failed."); }
    finally { setWorking(false); }
  };

  if (loading) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-4xl"><div className="h-10 w-72 animate-pulse rounded-xl bg-slate-200" /><div className="mt-6 h-96 animate-pulse rounded-3xl bg-white" /></div></main>;

  return <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900"><div className="mx-auto max-w-4xl space-y-6 p-4 sm:p-6 lg:p-10">
    <StrategyWorkflowNav />
    <InvestorPageHeader eyebrow="Final decision" title="Strategy Approval" description="Review the selected Strategy Version, record suitability, and approve the immutable strategy snapshot." />
    {error && <InvestorStatus tone="error">{error}</InvestorStatus>}
    {success && <InvestorStatus tone="success">{success}{approvedVersionId && <Link href={`/investor/action-plan?strategyVersionId=${encodeURIComponent(approvedVersionId)}`} className="ml-3 font-bold underline">Continue to Action Plan →</Link>}</InvestorStatus>}
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><label className="block"><span className="text-sm font-bold text-slate-700">Goal</span><select value={goalId} onChange={(e) => setGoalId(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm"><option value="">Select goal</option>{goals.map((goal) => <option key={goal.id} value={goal.id}>{goal.name}</option>)}</select></label></section>
    {!run?.selected_strategy_id || !run.selected_strategy_version_id ? <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center"><h2 className="text-xl font-bold">No Strategy Version selected</h2><p className="mt-2 text-sm text-slate-500">Approval is available only after Strategy Builder creates a selected Strategy Version.</p><Link href="/investor/strategy-builder" className="mt-6 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white">Return to Strategy Builder</Link></section> : <>
      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><p className="text-xs font-bold uppercase tracking-wide text-slate-400">Selected Strategy</p><h2 className="mt-2 text-2xl font-extrabold">{selectedStrategy?.name ?? run.selected_strategy_id}</h2><p className="mt-1 text-sm text-slate-500">Scenario: {run.selected_scenario_id ?? "—"}</p><div className="mt-5 flex flex-wrap gap-3 text-xs text-slate-600"><span className="rounded-full bg-slate-100 px-3 py-1">Strategy Version {run.selected_strategy_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Goal Version {run.defined_goal_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Run v{run.run_version}</span></div></section>
      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Suitability</h2><p className="mt-1 text-sm text-slate-500">Record the suitability assessment. The backend owns approval validation.</p><div className="mt-5 grid gap-3 sm:grid-cols-3">{STATUSES.map((option) => <button key={option} type="button" onClick={() => setStatus(option)} className={`rounded-2xl border p-4 text-left ${status === option ? "border-teal-500 bg-teal-50 ring-2 ring-teal-100" : "border-slate-200 hover:bg-slate-50"}`}><p className="font-bold">{option}</p><p className="mt-1 text-xs text-slate-500">{option === "Suitable" ? "No acknowledgement required." : "Explicit acknowledgement required."}</p></button>)}</div>{requiresAcknowledgement && <label className="mt-5 block"><span className="text-sm font-bold">Acknowledgement</span><textarea value={acknowledgement} onChange={(e) => setAcknowledgement(e.target.value)} rows={4} placeholder={`Explain why you acknowledge the ${status} assessment.`} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-teal-600" /></label>}</section>
      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Primary Strategy</h2><label className="mt-4 flex items-start gap-3"><input type="checkbox" checked={makePrimary} onChange={(e) => setMakePrimary(e.target.checked)} className="mt-1 h-4 w-4" /><span><span className="text-sm font-bold">Make this the Primary Strategy</span><span className="mt-1 block text-xs text-slate-500">The backend applies the Primary Strategy lifecycle rules.</span></span></label>{makePrimary && <div className="mt-5 grid gap-4 md:grid-cols-2"><label className="block"><span className="text-sm font-bold">Primary transition</span><select value={primaryDecision} onChange={(e) => setPrimaryDecision(e.target.value as typeof primaryDecision)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm"><option value="archive_previous">Archive previous</option><option value="keep_previous_approved">Keep previous approved</option></select></label><label className="block"><span className="text-sm font-bold">Pending implementation actions</span><select value={pendingDisposition} onChange={(e) => setPendingDisposition(e.target.value as typeof pendingDisposition)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm"><option value="retain_for_reassessment">Retain for reassessment</option><option value="cancel">Cancel</option></select></label></div>}</section>
      <InvestorButton className="w-full" onClick={handleApprove} disabled={working || Boolean(approvedVersionId)}>{working ? "Approving…" : approvedVersionId ? "Strategy Version Approved" : "Approve Strategy Version"}</InvestorButton>
    </>}
  </div></main>;
}
