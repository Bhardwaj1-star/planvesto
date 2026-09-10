"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getGoals, type GoalSummary } from "../../../lib/api/goals";
import { addCustomScenario, getLatestStrategyRun, getPlanningUnitId, type StrategyRun } from "../../../lib/api/strategy";

export default function StrategyScenariosPage() {
  const [goals, setGoals] = useState<GoalSummary[]>([]);
  const [goalId, setGoalId] = useState("");
  const [run, setRun] = useState<StrategyRun | null>(null);
  const [strategyId, setStrategyId] = useState("");
  const [name, setName] = useState("");
  const [assumptions, setAssumptions] = useState("{}\n");
  const [funding, setFunding] = useState("{}\n");
  const [working, setWorking] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const pu = getPlanningUnitId();
        if (!pu) throw new Error("Planning unit is not available. Please complete onboarding first.");
        const data = await getGoals(pu);
        if (active) { setGoals(data); if (data[0]) setGoalId(data[0].goal_id); }
      } catch (err) { if (active) setError(err instanceof Error ? err.message : "Unable to load goals."); }
      finally { if (active) setLoading(false); }
    })();
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!goalId) { setRun(null); return; }
    let active = true;
    (async () => {
      setError(null); setSuccess(null);
      try {
        const pu = getPlanningUnitId();
        if (!pu) throw new Error("Planning unit is not available.");
        const latest = await getLatestStrategyRun(pu, goalId);
        if (active) { setRun(latest); setStrategyId(latest.selected_strategy_id ?? latest.recommendation.recommended_strategy_id ?? latest.applicable_strategies[0]?.strategy_id ?? ""); }
      } catch (err) { if (active) setError(err instanceof Error ? err.message : "No Strategy Run is available for this goal."); }
    })();
    return () => { active = false; };
  }, [goalId]);

  async function submit() {
    const pu = getPlanningUnitId();
    if (!pu || !run?.strategy_run_id || !strategyId) return setError("A Strategy Run and applicable strategy are required.");
    if (!name.trim()) return setError("Scenario name is required.");
    let parsedAssumptions: Record<string, unknown>;
    let parsedFunding: Record<string, unknown>;
    try { parsedAssumptions = JSON.parse(assumptions); parsedFunding = JSON.parse(funding); } catch { setError("Assumptions and funding structure must be valid JSON objects."); return; }
    if (!parsedAssumptions || Array.isArray(parsedAssumptions) || typeof parsedAssumptions !== "object" || !parsedFunding || Array.isArray(parsedFunding) || typeof parsedFunding !== "object") { setError("Assumptions and funding structure must be JSON objects."); return; }
    setWorking(true); setError(null); setSuccess(null);
    try {
      const next = await addCustomScenario(pu, run.strategy_run_id, strategyId, name.trim(), parsedAssumptions, parsedFunding);
      setRun(next);
      setName("");
      setSuccess("Custom scenario added. The backend recalculated the Strategy Run and rankings.");
    } catch (err) { setError(err instanceof Error ? err.message : "Unable to add custom scenario."); }
    finally { setWorking(false); }
  }

  if (loading) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-5xl"><div className="h-10 w-72 animate-pulse rounded-xl bg-slate-200" /><div className="mt-6 h-96 animate-pulse rounded-3xl bg-white" /></div></main>;

  return <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900"><div className="mx-auto max-w-5xl space-y-6 p-6 lg:p-10">
    <header><Link href="/investor/strategy-builder" className="text-sm font-semibold text-teal-700">← Strategy Builder</Link><p className="mt-6 text-sm font-semibold uppercase tracking-[0.16em] text-teal-700">Scenario planning</p><h1 className="mt-1 text-3xl font-extrabold tracking-tight">Custom Scenarios</h1><p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">Create investor-modified assumptions or funding structures. The backend recalculates the run and preserves the new run version.</p></header>
    {error && <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">{error}</div>}
    {success && <div className="rounded-2xl border border-emerald-200 bg-emerald-50 px-5 py-4 text-sm text-emerald-700">{success}</div>}
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><label className="block"><span className="text-sm font-bold">Goal</span><select value={goalId} onChange={(e) => setGoalId(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm"><option value="">Select goal</option>{goals.map((g) => <option key={g.goal_id} value={g.goal_id}>{g.goal_name}</option>)}</select></label>{run && <div className="mt-4 flex flex-wrap gap-3 text-xs text-slate-500"><span className="rounded-full bg-slate-100 px-3 py-1">Run v{run.run_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Goal v{run.defined_goal_version}</span></div>}</section>
    {run ? <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm space-y-5"><label className="block"><span className="text-sm font-bold">Strategy</span><select value={strategyId} onChange={(e) => setStrategyId(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm">{run.applicable_strategies.map((s) => <option key={s.strategy_id} value={s.strategy_id}>{s.name}</option>)}</select></label><label className="block"><span className="text-sm font-bold">Scenario name</span><input value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Higher monthly contribution" className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm" /></label><div className="grid gap-5 md:grid-cols-2"><label className="block"><span className="text-sm font-bold">Assumptions (JSON)</span><textarea value={assumptions} onChange={(e) => setAssumptions(e.target.value)} rows={9} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 font-mono text-xs" /></label><label className="block"><span className="text-sm font-bold">Funding structure (JSON)</span><textarea value={funding} onChange={(e) => setFunding(e.target.value)} rows={9} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 font-mono text-xs" /></label></div><button onClick={() => void submit()} disabled={working} className="w-full rounded-2xl bg-navy-900 px-5 py-4 text-sm font-extrabold text-white disabled:opacity-50">{working ? "Recalculating…" : "Add Custom Scenario"}</button></section> : <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center"><h2 className="text-xl font-bold">No Strategy Run</h2><p className="mt-2 text-sm text-slate-500">Build a Strategy Run before creating a custom scenario.</p><Link href="/investor/strategy-builder" className="mt-6 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white">Open Strategy Builder</Link></section>}
    {run?.scenarios.filter((s) => s.is_investor_modified).length ? <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Investor-modified scenarios</h2><div className="mt-4 space-y-3">{run.scenarios.filter((s) => s.is_investor_modified).map((s) => <article key={s.scenario_id} className="rounded-2xl bg-slate-50 p-4"><div className="flex items-center justify-between gap-4"><h3 className="font-bold">{s.scenario_name}</h3><span className="text-xs text-slate-500">{s.scenario_id}</span></div><p className="mt-2 text-sm text-slate-600">{s.trade_off_notes || "Backend-defined scenario trade-offs."}</p></article>)}</div></section> : null}
  </div></main>;
}
