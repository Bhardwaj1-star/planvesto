"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import StrategyWorkflowNav from "../../../components/StrategyWorkflowNav";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorButton, InvestorStatus } from "../../../components/InvestorUI";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";
import { apiRequest } from "../../../lib/api/client";
import { buildStrategy, getLatestStrategyRun, getStrategyRunHistory, getPlanningUnitId, selectStrategy, type StrategyRun } from "../../../lib/api/strategy";
import type { DefinedGoal } from "../../../lib/onboarding/goals/types";

function displayMetric(value: unknown) {
  if (value === null || value === undefined || value === "") return "—";
  if (typeof value === "number") return new Intl.NumberFormat("en-IN", { maximumFractionDigits: 2 }).format(value);
  return String(value);
}
function formatINR(value: number | null | undefined) {
  if (value === null || value === undefined || !Number.isFinite(value)) return "—";
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(value);
}

export default function InvestorStrategyBuilderPage() {
  const [goals, setGoals] = useState<Array<{ id: string; name: string }>>([]);
  const [selectedGoalId, setSelectedGoalId] = useState("");
  const [goalPreview, setGoalPreview] = useState<DefinedGoal | null>(null);
  const [run, setRun] = useState<StrategyRun | null>(null);
  const [history, setHistory] = useState<StrategyRun[]>([]);
  const [selectedStrategyId, setSelectedStrategyId] = useState("");
  const [selectedScenarioId, setSelectedScenarioId] = useState("");
  const [selectedArchitectureId, setSelectedArchitectureId] = useState("");
  const [parameters, setParameters] = useState<Record<string, unknown>>({});
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const data = await loadGoalPlannerData();
        if (!active) return;
        const nextGoals = (data?.goals ?? []).map((goal) => ({ id: goal.id, name: goal.name || "Untitled Goal" }));
        setGoals(nextGoals);
        const requested = new URLSearchParams(window.location.search).get("goalId");
        setSelectedGoalId(nextGoals.find((g) => g.id === requested)?.id ?? nextGoals[0]?.id ?? "");
      } catch (err) { if (active) setError(err instanceof Error ? err.message : "Unable to load goals."); }
      finally { if (active) setLoading(false); }
    })();
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!selectedGoalId) { setGoalPreview(null); setRun(null); setHistory([]); return; }
    let active = true;
    (async () => {
      setWorking(true); setError(null);
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
        let preview: DefinedGoal | null = null;
        try { preview = await apiRequest<DefinedGoal>(`/api/goals/${selectedGoalId}/defined/latest?planning_unit_id=${planningUnitId}`); } catch { preview = null; }
        let latest: StrategyRun | null = null;
        try { latest = await getLatestStrategyRun(planningUnitId, selectedGoalId); } catch { latest = null; }
        if (preview && (!latest || latest.defined_goal_version !== preview.version)) latest = await buildStrategy(planningUnitId, selectedGoalId);
        if (!active) return;
        setGoalPreview(preview);
        setRun(latest);
        setSelectedStrategyId(latest?.selected_strategy_id ?? latest?.recommendation.recommended_strategy_id ?? "");
        setSelectedScenarioId(latest?.selected_scenario_id ?? latest?.recommendation.recommended_scenario_id ?? "");
        setSelectedArchitectureId(latest?.selected_architecture?.architecture_id ?? latest?.recommendation.architecture?.architecture_id ?? "");
        setParameters(latest?.selected_implementation_parameters ?? {});
        setHistory(latest ? await getStrategyRunHistory(planningUnitId, selectedGoalId) : []);
      } catch (err) { if (active) setError(err instanceof Error ? err.message : "Unable to load Strategy Builder."); }
      finally { if (active) setWorking(false); }
    })();
    return () => { active = false; };
  }, [selectedGoalId]);

  const selectedStrategy = useMemo(() => run?.applicable_strategies.find((s) => s.strategy_id === selectedStrategyId) ?? null, [run, selectedStrategyId]);
  const scenarios = useMemo(() => run?.scenarios.filter((s) => s.strategy_id === selectedStrategyId) ?? [], [run, selectedStrategyId]);
  const selectedScenario = scenarios.find((s) => s.scenario_id === selectedScenarioId) ?? null;
  const displayedRankings = useMemo(() => {
    if (!run) return [];
    const recommendedId = run.recommendation.architecture?.primary_strategy_id ?? run.recommendation.recommended_strategy_id;
    const recommended = run.rankings.find((r) => r.is_recommended || r.strategy_id === recommendedId);
    const alternative = run.rankings.find((r) => r.strategy_id !== recommended?.strategy_id);
    return [recommended, alternative].filter(Boolean) as typeof run.rankings;
  }, [run]);

  const execute = async (operation: () => Promise<StrategyRun>) => {
    setWorking(true); setError(null);
    try {
      const next = await operation();
      setRun(next);
      setSelectedStrategyId(next.selected_strategy_id ?? next.recommendation.recommended_strategy_id ?? "");
      setSelectedScenarioId(next.selected_scenario_id ?? next.recommendation.recommended_scenario_id ?? "");
      setSelectedArchitectureId(next.selected_architecture?.architecture_id ?? next.recommendation.architecture?.architecture_id ?? "");
      setParameters(next.selected_implementation_parameters ?? {});
      const planningUnitId = getPlanningUnitId();
      if (planningUnitId && selectedGoalId) setHistory(await getStrategyRunHistory(planningUnitId, selectedGoalId));
    } catch (err) { setError(err instanceof Error ? err.message : "Strategy operation failed."); }
    finally { setWorking(false); }
  };

  const handleBuild = () => { const planningUnitId = getPlanningUnitId(); if (planningUnitId && selectedGoalId) void execute(() => buildStrategy(planningUnitId, selectedGoalId)); };
  const handleSelect = () => { const planningUnitId = getPlanningUnitId(); if (planningUnitId && run?.strategy_run_id && selectedStrategyId && selectedScenarioId) void execute(() => selectStrategy(planningUnitId, run.strategy_run_id!, selectedStrategyId, selectedScenarioId, parameters, selectedArchitectureId || undefined)); };

  if (loading) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-6xl space-y-6"><div className="h-9 w-64 animate-pulse rounded-xl bg-slate-200"/><div className="h-96 animate-pulse rounded-3xl bg-white"/></div></main>;
  if (!goals.length) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-2xl rounded-3xl border border-slate-200 bg-white p-10 text-center"><h1 className="text-2xl font-extrabold">No goals available</h1><Link href="/investor/goal-planner" className="mt-6 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white">Open Goal Planner</Link></div></main>;

  return <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
    <InvestorHeader eyebrow="Decide" title="Strategy Builder" description="Build a coherent strategy architecture for a defined goal. The decision engine determines applicability, feasibility, trade-offs and recommendation."/>
    <div className="mx-auto max-w-6xl space-y-6 p-4 sm:p-6 lg:p-10">
      <StrategyWorkflowNav/>
      {error && <InvestorStatus tone="error">{error}</InvestorStatus>}
      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between"><label className="block flex-1"><span className="text-sm font-bold text-slate-700">Goal</span><select value={selectedGoalId} onChange={(e)=>setSelectedGoalId(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm"><option value="">Select goal</option>{goals.map((g)=><option key={g.id} value={g.id}>{g.name}</option>)}</select></label><InvestorButton onClick={handleBuild} disabled={working||!selectedGoalId}>{working?"Working…":run?"Rebuild Strategy Run":"Build Strategy"}</InvestorButton></div>
        {run && <div className="mt-4 flex flex-wrap gap-3 text-xs text-slate-500"><span className="rounded-full bg-slate-100 px-3 py-1">Run v{run.run_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Goal v{run.defined_goal_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Status: {run.status}</span><Link href="/investor/strategy-scenarios" className="rounded-full border border-slate-200 px-3 py-1 font-semibold">Custom Scenarios</Link><Link href="/investor/strategy-history" className="rounded-full border border-slate-200 px-3 py-1 font-semibold">Strategy History</Link></div>}
      </section>

      {goalPreview && <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Goal Calculation &amp; Preview</h2><div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">{[["Today’s Cost",formatINR(goalPreview.today_cost)],["Inflation",`${(goalPreview.inflation_rate*100).toFixed(1)}%`],["Required Corpus",formatINR(goalPreview.future_target)],["Funding Gap",formatINR(goalPreview.funding_gap)]].map(([label,value])=><div key={label} className="rounded-2xl bg-slate-50 p-4"><p className="text-xs font-bold uppercase tracking-wide text-slate-400">{label}</p><p className="mt-1 text-lg font-extrabold">{value}</p></div>)}</div><div className="mt-4 flex flex-wrap gap-3 text-sm text-slate-600"><span>Target: <strong>{String(goalPreview.target_month).padStart(2,"0")}/{goalPreview.target_year}</strong></span><span>Mapped Assets: <strong>{formatINR(goalPreview.projected_mapped_asset_value)}</strong></span><span>Monthly Contribution: <strong>{formatINR(goalPreview.required_monthly_contribution)}</strong></span><span>Status: <strong>{goalPreview.funding_status}</strong></span></div></section>}

      {!run ? <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center"><h2 className="text-xl font-bold">No Strategy Run yet</h2><p className="mt-2 text-sm text-slate-500">Build the Strategy Run after reviewing the goal calculation.</p></section> : <>
        <section><div className="mb-4"><h2 className="text-lg font-bold">Strategy Architectures</h2><p className="mt-1 text-sm text-slate-500">Applicable architectures evaluated for this goal.</p></div><div className="grid gap-5 lg:grid-cols-2">{displayedRankings.map((ranking)=><article key={`${ranking.strategy_id}-${ranking.scenario_id}`} className={`rounded-3xl border bg-white p-6 shadow-sm ${selectedStrategyId===ranking.strategy_id&&selectedScenarioId===ranking.scenario_id?"border-teal-500 ring-2 ring-teal-100":"border-slate-200"}`}><div className="flex items-start justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-wide text-slate-400">{ranking.is_recommended?"Recommended Architecture":"Alternative Architecture"}</p><h3 className="mt-1 text-xl font-extrabold">{ranking.strategy_name}</h3><p className="mt-1 text-sm text-slate-500">{ranking.scenario_name}</p></div>{ranking.is_recommended&&<span className="rounded-full bg-teal-50 px-3 py-1 text-xs font-bold text-teal-700">Recommended</span>}</div><p className="mt-4 text-sm leading-6 text-slate-600">{run.applicable_strategies.find(s=>s.strategy_id===ranking.strategy_id)?.description}</p><div className="mt-4 space-y-2 text-xs text-slate-600">{run.architectures.find(a=>a.primary_strategy_id===ranking.strategy_id)?.rationale?.length? <div><b>Goal fit:</b> {run.architectures.find(a=>a.primary_strategy_id===ranking.strategy_id)?.rationale.join("; ")}</div>:null}<div><b>Feasibility:</b> {run.architectures.find(a=>a.primary_strategy_id===ranking.strategy_id)?.feasibility_status}</div>{run.applicable_strategies.find(s=>s.strategy_id===ranking.strategy_id)?.trade_offs?.length?<div><b>Trade-offs:</b> {run.applicable_strategies.find(s=>s.strategy_id===ranking.strategy_id)?.trade_offs.join("; ")}</div>:null}</div><button onClick={()=>{setSelectedStrategyId(ranking.strategy_id);setSelectedScenarioId(ranking.scenario_id);const s=run.applicable_strategies.find(x=>x.strategy_id===ranking.strategy_id);setParameters(Object.fromEntries((s?.implementation_parameters??[]).map(p=>[p.name,p.default_value])));}} className="mt-5 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm font-bold hover:bg-slate-50">{selectedStrategyId===ranking.strategy_id&&selectedScenarioId===ranking.scenario_id?"Selected":"Select this architecture"}</button></article>)}</div></section>

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Recommendation</h2><p className="mt-3 text-sm leading-6 text-slate-600">{run.recommendation.complete_reasoning}</p><ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-slate-600">{run.recommendation.short_reasons.map((reason,i)=><li key={i}>{reason}</li>)}</ul><p className="mt-4 text-xs font-bold uppercase tracking-wide text-slate-400">Feasibility: {run.recommendation.feasibility_status}</p></section>

        {selectedStrategy&&<section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Implementation Parameters</h2><div className="mt-5 grid gap-4 md:grid-cols-2">{selectedStrategy.implementation_parameters.filter(p=>p.editable).map(p=><label key={p.name} className="rounded-2xl bg-slate-50 p-4"><span className="text-sm font-bold">{p.label}</span><p className="mt-1 text-xs text-slate-500">{p.description}</p>{p.param_type==="choice"?<select value={String(parameters[p.name]??p.default_value)} onChange={e=>setParameters(x=>({...x,[p.name]:e.target.value}))} className="mt-3 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm">{(p.choices??[]).map(choice=><option key={choice}>{choice}</option>)}</select>:<input type="number" step={p.param_type==="integer"?1:"any"} min={p.min_value??undefined} max={p.max_value??undefined} value={String(parameters[p.name]??p.default_value)} onChange={e=>setParameters(x=>({...x,[p.name]:Number(e.target.value)}))} className="mt-3 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"/>}</label>)}</div>{selectedScenario&&<div className="mt-5 rounded-2xl border border-slate-100 p-4"><p className="text-sm font-bold">Scenario: {selectedScenario.scenario_name}</p><p className="mt-1 text-sm text-slate-500">{selectedScenario.trade_off_notes||"No additional trade-off notes supplied."}</p></div>}<InvestorButton className="mt-6" onClick={handleSelect} disabled={working||!selectedScenarioId}>{working?"Saving…":run.selected_strategy_version_id?"Save selection":"Confirm selection"}</InvestorButton></section>}

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><div className="flex items-center justify-between"><div><h2 className="text-lg font-bold">Strategy Run History</h2><p className="mt-1 text-sm text-slate-500">Immutable strategy run versions.</p></div><span className="text-xs text-slate-400">{history.length} runs</span></div>{history.length>0&&<div className="mt-5 space-y-2">{history.map(item=><div key={item.strategy_run_id??`${item.created_at}-${item.run_version}`} className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-slate-100 p-4"><span className="font-bold">Run v{item.run_version}</span><span className="text-xs text-slate-400">Goal v{item.defined_goal_version} · {item.created_at?new Date(item.created_at).toLocaleString("en-IN"):"—"}</span></div>)}</div>}</section>
      </>}
    </div>
  </main>;
}
