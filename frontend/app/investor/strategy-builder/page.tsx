"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import StrategyWorkflowNav from "../../../components/StrategyWorkflowNav";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorButton, InvestorStatus } from "../../../components/InvestorUI";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";
import { apiRequest } from "../../../lib/api/client";
import { buildStrategy, getStrategyRunHistory, getPlanningUnitId, selectStrategy, type StrategyRun } from "../../../lib/api/strategy";
import { getLatestDefinedGoal } from "../../../lib/api/goals";
import type { DefinedGoal } from "../../../lib/onboarding/goals/types";

type PlanningBasket = { id: string; name: string; goalIds: string[] };
const BASKET_STORAGE_KEY = "planvesto:planning-baskets";

function displayMetric(value: unknown) {
  if (value === null || value === undefined || value === "") return "—";
  if (typeof value === "number") return new Intl.NumberFormat("en-IN", { maximumFractionDigits: 2 }).format(value);
  return String(value);
}
function formatINR(value: number | null | undefined) {
  if (value === null || value === undefined || !Number.isFinite(value)) return "—";
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(value);
}
function resolveArchitectureId(run: StrategyRun | null, strategyId: string) {
  if (!run) return "";
  return run.architectures.find((architecture) => architecture.primary_strategy_id === strategyId)?.architecture_id
    ?? run.recommendation.architecture?.architecture_id
    ?? "";
}

export default function InvestorStrategyBuilderPage() {
  const [goals, setGoals] = useState<Array<{ id: string; name: string }>>([]);
  const [baskets, setBaskets] = useState<PlanningBasket[]>([]);
  const [selectedGoalId, setSelectedGoalId] = useState("");
  const [selectedBasketId, setSelectedBasketId] = useState("");
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
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(false);

  const selectedTargetKey = selectedBasketId ? `basket:${selectedBasketId}` : selectedGoalId;
  const selectedBasket = baskets.find((basket) => basket.id === selectedBasketId) ?? null;

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const data = await loadGoalPlannerData();
        if (!active) return;
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
        const canonicalGoals = await Promise.all(
          (data?.goals ?? []).map(async (goal) => {
            try {
              const defined = await getLatestDefinedGoal(planningUnitId, goal.id);
              return { id: defined.goal_id, name: defined.goal_name || defined.goal_type || "Untitled Goal" };
            } catch {
              return null;
            }
          }),
        );
        const nextGoals = canonicalGoals.filter((goal): goal is { id: string; name: string } => Boolean(goal));
        setGoals(nextGoals);
        try {
          const saved = JSON.parse(window.localStorage.getItem(BASKET_STORAGE_KEY) || "[]");
          setBaskets(Array.isArray(saved) ? saved : []);
        } catch {
          setBaskets([]);
        }
        const requested = new URLSearchParams(window.location.search).get("goalId");
        setSelectedBasketId("");
        setSelectedGoalId(nextGoals.find((g) => g.id === requested)?.id ?? nextGoals[0]?.id ?? "");
      } catch (err) { if (active) setError(err instanceof Error ? err.message : "Unable to load goals."); }
      finally { if (active) setLoading(false); }
    })();
    return () => { active = false; };
  }, []);

  const handleTargetChange = (value: string) => {
    setError(null);
    setSuccessMessage(null);
    if (value.startsWith("basket:")) {
      setSelectedBasketId(value.slice("basket:".length));
      setSelectedGoalId("");
      return;
    }
    setSelectedBasketId("");
    setSelectedGoalId(value);
  };

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
        // Strategy Builder always evaluates the current goal directly.
        // Latest-run state is historical data only and never drives the decision flow.
        const currentRun = await buildStrategy(planningUnitId, selectedGoalId);
        if (!active) return;
        setGoalPreview(preview);
        setRun(currentRun);
        const restoredStrategyId = currentRun.selected_strategy_id ?? "";
        setSelectedStrategyId(restoredStrategyId);
        setSelectedScenarioId(currentRun.selected_scenario_id ?? "");
        setSelectedArchitectureId(resolveArchitectureId(currentRun, restoredStrategyId));
        setParameters(currentRun.selected_implementation_parameters ?? {});
        setHistory(await getStrategyRunHistory(planningUnitId, selectedGoalId));
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
    // The Builder always presents two strategy alternatives when two are available.
    return [...run.rankings]
      .sort((a, b) => a.rank - b.rank)
      .filter((ranking, index, items) => items.findIndex((item) => item.strategy_id === ranking.strategy_id) === index)
      .slice(0, 2);
  }, [run]);

  const execute = async (operation: () => Promise<StrategyRun>, successMessage?: string) => {
    setWorking(true); setError(null); setSuccessMessage(null);
    try {
      const next = await operation();
      setRun(next);
      const nextStrategyId = next.selected_strategy_id ?? next.recommendation.recommended_strategy_id ?? "";
      setSelectedStrategyId(nextStrategyId);
      setSelectedScenarioId(next.selected_scenario_id ?? next.recommendation.recommended_scenario_id ?? "");
      setSelectedArchitectureId(resolveArchitectureId(next, nextStrategyId));
      setParameters(next.selected_implementation_parameters ?? {});
      const planningUnitId = getPlanningUnitId();
      if (planningUnitId && selectedGoalId) setHistory(await getStrategyRunHistory(planningUnitId, selectedGoalId));
      if (successMessage) setSuccessMessage(successMessage);
    } catch (err) { setError(err instanceof Error ? err.message : "Strategy operation failed."); }
    finally { setWorking(false); }
  };

  const handleBuild = () => { const planningUnitId = getPlanningUnitId(); if (planningUnitId && selectedGoalId) void execute(() => buildStrategy(planningUnitId, selectedGoalId)); };
  const handleSelect = () => {
    setError(null);
    setSuccessMessage(null);

    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId) {
      setError("Planning unit is missing. Please refresh the page and try again.");
      return;
    }
    if (!run?.strategy_run_id) {
      setError("Strategy run is missing. Rebuild the Strategy Run before saving the selection.");
      return;
    }
    if (!selectedStrategyId) {
      setError("No strategy is selected. Select an architecture before saving.");
      return;
    }
    if (!selectedScenarioId) {
      setError("No scenario is selected. Select an architecture before saving.");
      return;
    }

    const architecture = run.architectures.find((item) => item.architecture_id === selectedArchitectureId && item.primary_strategy_id === selectedStrategyId)
      ?? run.architectures.find((item) => item.primary_strategy_id === selectedStrategyId);
    if (!architecture) {
      setError("A matching strategy architecture is unavailable. Please select the architecture again.");
      return;
    }

    void execute(
      () => selectStrategy(planningUnitId, run.strategy_run_id!, selectedStrategyId, selectedScenarioId, parameters, architecture.architecture_id),
      "Selection saved successfully.",
    );
  };

  if (loading) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-6xl space-y-6"><div className="h-9 w-64 animate-pulse rounded-xl bg-slate-200"/><div className="h-96 animate-pulse rounded-3xl bg-white"/></div></main>;
  if (!goals.length) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-2xl rounded-3xl border border-slate-200 bg-white p-10 text-center"><h1 className="text-2xl font-extrabold">No goals available</h1><Link href="/investor/goal-planner" className="mt-6 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white">Open Goal Planner</Link></div></main>;

  return <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
    <InvestorHeader eyebrow="Decide" title="Strategy Builder" description="Build a coherent strategy architecture for a defined goal. The decision engine determines applicability, feasibility, trade-offs and recommendation.">
      <button
        type="button"
        onClick={() => setShowHistory((value) => !value)}
        aria-expanded={showHistory}
        className="inline-flex min-h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-bold text-slate-700 shadow-sm transition hover:bg-slate-50"
      >
        <span>History</span>
        <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs">{history.length}</span>
        <span aria-hidden="true">{showHistory ? "↑" : "↓"}</span>
      </button>
    </InvestorHeader>
    {showHistory && (
      <section className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-6xl px-4 py-4 sm:px-6 lg:px-10">
          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h2 className="text-sm font-extrabold text-slate-900">Strategy Run History</h2>
                <p className="mt-1 text-xs text-slate-500">Immutable strategy run versions for the selected goal.</p>
              </div>
              <span className="text-xs font-semibold text-slate-400">{history.length} runs</span>
            </div>
            {history.length > 0 ? (
              <div className="mt-3 grid gap-2 sm:grid-cols-3">
                {history.map((item) => (
                  <div key={item.strategy_run_id ?? `${item.created_at}-${item.run_version}`} className="rounded-xl border border-slate-200 bg-white px-4 py-3">
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-sm font-bold text-slate-800">Run v{item.run_version}</span>
                      <span className="text-[11px] font-semibold text-slate-400">Goal v{item.defined_goal_version}</span>
                    </div>
                    <p className="mt-1 text-[11px] text-slate-400">{item.created_at ? new Date(item.created_at).toLocaleString("en-IN") : "—"}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="mt-3 text-xs text-slate-500">No strategy runs yet for this goal.</p>
            )}
          </div>
        </div>
      </section>
    )}
    <div className="mx-auto max-w-6xl space-y-6 p-4 sm:p-6 lg:p-10">
      <StrategyWorkflowNav/>
      {error && <InvestorStatus tone="error">{error}</InvestorStatus>}
      {successMessage && <InvestorStatus tone="success">{successMessage}</InvestorStatus>}
      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <label className="block flex-1">
            <span className="text-sm font-bold text-slate-700">Goal / Planning Basket</span>
            <select value={selectedTargetKey} onChange={(e)=>handleTargetChange(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm">
              <option value="">Select goal or planning basket</option>
              <optgroup label="Goals">
                {goals.map((g)=><option key={g.id} value={g.id}>{g.name}</option>)}
              </optgroup>
              {baskets.length > 0 && <optgroup label="Planning Baskets">
                {baskets.map((basket)=><option key={basket.id} value={`basket:${basket.id}`}>🧺 {basket.name} · {basket.goalIds.length} goals</option>)}
              </optgroup>}
            </select>
          </label>
          <InvestorButton onClick={handleBuild} disabled={working||!selectedGoalId}>{working?"Working…":run?"Rebuild Strategy Run":"Build Strategy"}</InvestorButton>
        </div>
        {selectedBasket && <div className="mt-4 rounded-2xl border border-teal-200 bg-teal-50/60 p-4"><div className="flex items-center gap-2"><span className="text-lg">🧺</span><div><p className="text-sm font-extrabold text-teal-900">{selectedBasket.name}</p><p className="text-xs text-teal-700">{selectedBasket.goalIds.length} goals in this planning basket</p></div></div><p className="mt-3 text-xs leading-5 text-teal-800">This basket is selected as a planning target. Basket-level strategy execution will use the basket’s goals together; the current Strategy Run endpoint remains goal-based.</p><div className="mt-2 flex flex-wrap gap-1.5">{selectedBasket.goalIds.map((id)=>{const goal=goals.find((g)=>g.id===id); return goal ? <span key={id} className="rounded-full bg-white/80 px-2.5 py-1 text-[11px] font-semibold text-teal-800">{goal.name}</span> : null;})}</div></div>}
        {run && <div className="mt-4 flex flex-wrap gap-3 text-xs text-slate-500"><span className="rounded-full bg-slate-100 px-3 py-1">Run v{run.run_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Goal v{run.defined_goal_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Status: {run.status}</span><Link href={`/investor/goal-report?goalId=${encodeURIComponent(selectedGoalId)}`} className="rounded-full border border-teal-200 bg-teal-50/50 px-3 py-1 font-semibold text-teal-700 hover:bg-teal-50">View Goal Report</Link><Link href="/investor/strategy-scenarios" className="rounded-full border border-slate-200 px-3 py-1 font-semibold">Custom Scenarios</Link><Link href="/investor/strategy-history" className="rounded-full border border-slate-200 px-3 py-1 font-semibold">Strategy History</Link></div>}
      </section>

      {goalPreview && <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Goal Calculation &amp; Preview</h2><div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">{[["Today’s Cost",formatINR(goalPreview.today_cost)],["Inflation",`${(goalPreview.inflation_rate*100).toFixed(1)}%`],["Required Corpus",formatINR(goalPreview.future_target)],["Funding Gap",formatINR(goalPreview.funding_gap)]].map(([label,value])=><div key={label} className="rounded-2xl bg-slate-50 p-4"><p className="text-xs font-bold uppercase tracking-wide text-slate-400">{label}</p><p className="mt-1 text-lg font-extrabold">{value}</p></div>)}</div><div className="mt-4 flex flex-wrap gap-3 text-sm text-slate-600"><span>Target: <strong>{String(goalPreview.target_month).padStart(2,"0")}/{goalPreview.target_year}</strong></span><span>Mapped Assets: <strong>{formatINR(goalPreview.projected_mapped_asset_value)}</strong></span><span>Monthly Contribution: <strong>{formatINR(goalPreview.required_monthly_contribution)}</strong></span><span>Status: <strong>{goalPreview.funding_status}</strong></span></div></section>}

      {!run ? <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center"><h2 className="text-xl font-bold">{selectedBasket ? "Basket selected" : "No Strategy Run yet"}</h2><p className="mt-2 text-sm text-slate-500">{selectedBasket ? "Select an individual goal to build its Strategy Run. Basket-level execution will be connected to the multi-goal strategy flow." : "Build the Strategy Run after reviewing the goal calculation."}</p></section> : <>
        <section><div className="mb-4"><h2 className="text-lg font-bold">Strategy Architectures</h2><p className="mt-1 text-sm text-slate-500">Applicable architectures evaluated for this goal.</p></div><div className="grid gap-5 lg:grid-cols-2">{displayedRankings.map((ranking)=><article key={`${ranking.strategy_id}-${ranking.scenario_id}`} className={`rounded-3xl border bg-white p-6 shadow-sm ${selectedStrategyId===ranking.strategy_id&&selectedScenarioId===ranking.scenario_id?"border-teal-500 ring-2 ring-teal-100":"border-slate-200"}`}><div className="flex items-start justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-wide text-slate-400">{ranking.is_recommended?"Recommended Architecture":"Alternative Architecture"}</p><h3 className="mt-1 text-xl font-extrabold">{ranking.strategy_name}</h3><p className="mt-1 text-sm text-slate-500">{ranking.scenario_name}</p></div>{ranking.is_recommended&&<span className="rounded-full bg-teal-50 px-3 py-1 text-xs font-bold text-teal-700">Recommended</span>}</div><p className="mt-4 text-sm leading-6 text-slate-600">{run.applicable_strategies.find(s=>s.strategy_id===ranking.strategy_id)?.description}</p><div className="mt-4 space-y-2 text-xs text-slate-600">{run.architectures.find(a=>a.primary_strategy_id===ranking.strategy_id)?.rationale?.length? <div><b>Goal fit:</b> {run.architectures.find(a=>a.primary_strategy_id===ranking.strategy_id)?.rationale.join("; ")}</div>:null}<div><b>Feasibility:</b> {run.architectures.find(a=>a.primary_strategy_id===ranking.strategy_id)?.feasibility_status}</div>{run.applicable_strategies.find(s=>s.strategy_id===ranking.strategy_id)?.trade_offs?.length?<div><b>Trade-offs:</b> {run.applicable_strategies.find(s=>s.strategy_id===ranking.strategy_id)?.trade_offs.join("; ")}</div>:null}</div><button onClick={()=>{setSelectedStrategyId(ranking.strategy_id);setSelectedScenarioId(ranking.scenario_id);const architecture=run.architectures.find(a=>a.primary_strategy_id===ranking.strategy_id);setSelectedArchitectureId(architecture?.architecture_id??"");const s=run.applicable_strategies.find(x=>x.strategy_id===ranking.strategy_id);setParameters(Object.fromEntries((s?.implementation_parameters??[]).map(p=>[p.name,p.default_value])));}} className="mt-5 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm font-bold hover:bg-slate-50">{selectedStrategyId===ranking.strategy_id&&selectedScenarioId===ranking.scenario_id?"Selected":"Select this architecture"}</button></article>)}</div></section>

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Recommendation</h2><p className="mt-3 text-sm leading-6 text-slate-600">{run.recommendation.complete_reasoning}</p><ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-slate-600">{run.recommendation.short_reasons.map((reason,i)=><li key={i}>{reason}</li>)}</ul><p className="mt-4 text-xs font-bold uppercase tracking-wide text-slate-400">Feasibility: {run.recommendation.feasibility_status}</p></section>

        {selectedStrategy&&<section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Implementation Parameters</h2><div className="mt-5 grid gap-4 md:grid-cols-2">{selectedStrategy.implementation_parameters.filter(p=>p.editable).map(p=><label key={p.name} className="rounded-2xl bg-slate-50 p-4"><span className="text-sm font-bold">{p.label}</span><p className="mt-1 text-xs text-slate-500">{p.description}</p>{p.param_type==="choice"?<select value={String(parameters[p.name]??p.default_value)} onChange={e=>setParameters(x=>({...x,[p.name]:e.target.value}))} className="mt-3 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm">{(p.choices??[]).map(choice=><option key={choice}>{choice}</option>)}</select>:<input type="number" step={p.param_type==="integer"?1:"any"} min={p.min_value??undefined} max={p.max_value??undefined} value={String(parameters[p.name]??p.default_value)} onChange={e=>setParameters(x=>({...x,[p.name]:Number(e.target.value)}))} className="mt-3 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"/>}</label>)}</div>{selectedScenario&&<div className="mt-5 rounded-2xl border border-slate-100 p-4"><p className="text-sm font-bold">Scenario: {selectedScenario.scenario_name}</p><p className="mt-1 text-sm text-slate-500">{selectedScenario.trade_off_notes||"No additional trade-off notes supplied."}</p></div>}<InvestorButton className="mt-6" onClick={handleSelect} disabled={working||!selectedScenarioId}>{working?"Saving…":run.selected_strategy_version_id?"Save selection":"Confirm selection"}</InvestorButton></section>}

      </>}
    </div>
  </main>;
}