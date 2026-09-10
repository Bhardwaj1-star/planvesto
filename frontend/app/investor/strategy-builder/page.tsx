"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";
import {
  buildStrategy,
  getLatestStrategyRun,
  getStrategyRunHistory,
  getPlanningUnitId,
  selectStrategy,
  updateStrategyPriorities,
  type InvestorPriorities,
  type StrategyRun,
} from "../../../lib/api/strategy";

const DEFAULT_PRIORITIES: InvestorPriorities = { safety: 0.25, liquidity: 0.25, growth: 0.25, flexibility: 0.25 };

function percent(value: number) { return `${Math.round(value * 100)}%`; }
function displayMetric(value: unknown) {
  if (value === null || value === undefined || value === "") return "—";
  if (typeof value === "number") return new Intl.NumberFormat("en-IN", { maximumFractionDigits: 2 }).format(value);
  return String(value);
}

export default function InvestorStrategyBuilderPage() {
  const [goals, setGoals] = useState<Array<{ id: string; name: string }>>([]);
  const [selectedGoalId, setSelectedGoalId] = useState("");
  const [run, setRun] = useState<StrategyRun | null>(null);
  const [history, setHistory] = useState<StrategyRun[]>([]);
  const [priorities, setPriorities] = useState(DEFAULT_PRIORITIES);
  const [selectedStrategyId, setSelectedStrategyId] = useState("");
  const [selectedScenarioId, setSelectedScenarioId] = useState("");
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
        if (nextGoals[0]) setSelectedGoalId(nextGoals[0].id);
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load goals.");
      } finally { if (active) setLoading(false); }
    })();
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!selectedGoalId) { setRun(null); setHistory([]); return; }
    let active = true;
    (async () => {
      setWorking(true); setError(null); setRun(null);
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
        try {
          const latest = await getLatestStrategyRun(planningUnitId, selectedGoalId);
          if (!active) return;
          setRun(latest);
          setPriorities(latest.investor_priorities);
          setSelectedStrategyId(latest.selected_strategy_id ?? latest.recommendation.recommended_strategy_id ?? "");
          setSelectedScenarioId(latest.selected_scenario_id ?? latest.recommendation.recommended_scenario_id ?? "");
          setParameters(latest.selected_implementation_parameters ?? {});
          setHistory(await getStrategyRunHistory(planningUnitId, selectedGoalId));
        } catch {
          if (active) { setRun(null); setHistory([]); setPriorities(DEFAULT_PRIORITIES); setSelectedStrategyId(""); setSelectedScenarioId(""); setParameters({}); }
        }
      } catch (err) { if (active) setError(err instanceof Error ? err.message : "Unable to load Strategy Builder."); }
      finally { if (active) setWorking(false); }
    })();
    return () => { active = false; };
  }, [selectedGoalId]);

  const selectedStrategy = useMemo(() => run?.applicable_strategies.find((s) => s.strategy_id === selectedStrategyId) ?? null, [run, selectedStrategyId]);
  const scenarios = useMemo(() => run?.scenarios.filter((s) => s.strategy_id === selectedStrategyId) ?? [], [run, selectedStrategyId]);
  const selectedScenario = scenarios.find((s) => s.scenario_id === selectedScenarioId) ?? null;

  const execute = async (operation: () => Promise<StrategyRun>) => {
    setWorking(true); setError(null);
    try {
      const next = await operation();
      setRun(next);
      setPriorities(next.investor_priorities);
      setSelectedStrategyId(next.selected_strategy_id ?? next.recommendation.recommended_strategy_id ?? "");
      setSelectedScenarioId(next.selected_scenario_id ?? next.recommendation.recommended_scenario_id ?? "");
      setParameters(next.selected_implementation_parameters ?? {});
      const planningUnitId = getPlanningUnitId();
      if (planningUnitId && selectedGoalId) setHistory(await getStrategyRunHistory(planningUnitId, selectedGoalId));
    } catch (err) { setError(err instanceof Error ? err.message : "Strategy operation failed."); }
    finally { setWorking(false); }
  };

  const handleBuild = () => {
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId || !selectedGoalId) return;
    void execute(() => buildStrategy(planningUnitId, selectedGoalId, priorities));
  };

  const handlePriorities = () => {
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId || !run?.strategy_run_id) return;
    void execute(() => updateStrategyPriorities(planningUnitId, run.strategy_run_id!, priorities));
  };

  const handleSelect = () => {
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId || !run?.strategy_run_id || !selectedStrategyId || !selectedScenarioId) return;
    void execute(() => selectStrategy(planningUnitId, run.strategy_run_id!, selectedStrategyId, selectedScenarioId, parameters));
  };

  if (loading) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-6xl space-y-6"><div className="h-9 w-64 animate-pulse rounded-xl bg-slate-200" /><div className="h-24 animate-pulse rounded-3xl bg-white" /><div className="h-96 animate-pulse rounded-3xl bg-white" /></div></main>;

  if (!goals.length) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-2xl rounded-3xl border border-slate-200 bg-white p-10 text-center shadow-sm"><h1 className="text-2xl font-extrabold">No goals available</h1><p className="mt-2 text-sm text-slate-500">Strategy Builder needs a defined goal before a Strategy Run can be created.</p><Link href="/investor/goal-planner" className="mt-6 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white">Open Goal Planner</Link></div></main>;

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
      <div className="mx-auto max-w-6xl space-y-6 p-6 lg:p-10">
        <header>
          <p className="text-sm font-semibold uppercase tracking-[0.16em] text-teal-700">Planning</p>
          <h1 className="mt-1 text-3xl font-extrabold tracking-tight">Strategy Builder</h1>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">Build and compare strategy pathways for a defined goal. Strategy calculations, rankings and recommendations are generated by the backend.</p>
        </header>

        {error && <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">{error}</div>}

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <label className="block flex-1"><span className="text-sm font-bold text-slate-700">Goal</span><select value={selectedGoalId} onChange={(e) => setSelectedGoalId(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-teal-600"><option value="">Select goal</option>{goals.map((g) => <option key={g.id} value={g.id}>{g.name}</option>)}</select></label>
            <button onClick={handleBuild} disabled={working || !selectedGoalId} className="rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-50">{working ? "Working…" : run ? "Rebuild Strategy Run" : "Build Strategy"}</button>
          </div>
          {run && <div className="mt-4 flex flex-wrap gap-3 text-xs text-slate-500"><span className="rounded-full bg-slate-100 px-3 py-1">Run v{run.run_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Goal version {run.defined_goal_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Status: {run.status}</span></div>}
        </section>

        {!run ? (
          <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center"><h2 className="text-xl font-bold">No Strategy Run yet</h2><p className="mt-2 text-sm text-slate-500">Set the investor priorities below, then build the Strategy Run.</p></section>
        ) : (
          <>
            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between gap-4"><div><h2 className="text-lg font-bold">Investor priorities</h2><p className="mt-1 text-sm text-slate-500">These weights tell the engine what matters most to the investor.</p></div><button onClick={handlePriorities} disabled={working} className="rounded-xl border border-slate-200 px-4 py-2 text-sm font-bold text-slate-700 disabled:opacity-50">Recalculate</button></div>
              <div className="mt-6 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
                {(Object.keys(priorities) as Array<keyof InvestorPriorities>).map((key) => <label key={key} className="rounded-2xl bg-slate-50 p-4"><div className="flex justify-between text-sm font-bold capitalize"><span>{key}</span><span>{percent(priorities[key])}</span></div><input type="range" min="0" max="100" value={Math.round(priorities[key] * 100)} onChange={(e) => setPriorities((p) => ({ ...p, [key]: Number(e.target.value) / 100 }))} className="mt-4 w-full" /><p className="mt-2 text-xs text-slate-500">Weights are normalized by the backend.</p></label>)}
              </div>
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div><h2 className="text-lg font-bold">Recommendation</h2><p className="mt-1 text-sm text-slate-500">Backend recommendation for the current Strategy Run.</p></div>
              <div className="mt-5 rounded-2xl border border-teal-200 bg-teal-50 p-5"><p className="text-xs font-bold uppercase tracking-wide text-teal-700">Recommended</p><h3 className="mt-1 text-xl font-extrabold">{run.recommendation.recommended_strategy_id}</h3><p className="mt-1 text-sm text-slate-600">Scenario: {run.recommendation.recommended_scenario_id}</p>{run.recommendation.short_reasons.length > 0 && <ul className="mt-4 space-y-2 text-sm text-slate-700">{run.recommendation.short_reasons.map((reason, i) => <li key={i}>• {reason}</li>)}</ul>} {run.recommendation.complete_reasoning && <details className="mt-4"><summary className="cursor-pointer text-sm font-bold text-teal-800">View complete reasoning</summary><p className="mt-3 text-sm leading-6 text-slate-600">{run.recommendation.complete_reasoning}</p></details>}</div>
            </section>

            <section>
              <div className="mb-4"><h2 className="text-lg font-bold">Strategy alternatives</h2><p className="mt-1 text-sm text-slate-500">All applicable strategies returned by the engine. No fixed number is assumed.</p></div>
              <div className="grid gap-5 lg:grid-cols-2">
                {run.rankings.map((ranking) => { const strategy = run.applicable_strategies.find((s) => s.strategy_id === ranking.strategy_id); const isSelected = selectedStrategyId === ranking.strategy_id && selectedScenarioId === ranking.scenario_id; return <article key={`${ranking.strategy_id}-${ranking.scenario_id}`} className={`rounded-3xl border bg-white p-6 shadow-sm ${isSelected ? "border-teal-500 ring-2 ring-teal-100" : "border-slate-200"}`}><div className="flex items-start justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-wide text-slate-400">Rank #{ranking.rank}</p><h3 className="mt-1 text-xl font-extrabold">{ranking.strategy_name}</h3><p className="mt-1 text-sm text-slate-500">{ranking.scenario_name}</p></div>{ranking.is_recommended && <span className="rounded-full bg-teal-50 px-3 py-1 text-xs font-bold text-teal-700">Recommended</span>}</div><p className="mt-4 text-sm leading-6 text-slate-600">{strategy?.description ?? "Strategy definition supplied by the engine."}</p><div className="mt-5 grid grid-cols-2 gap-3">{Object.entries(ranking.dimension_scores).map(([k,v]) => <div key={k} className="rounded-xl bg-slate-50 p-3"><p className="text-xs capitalize text-slate-400">{k}</p><p className="mt-1 font-bold">{displayMetric(v)}</p></div>)}<div className="rounded-xl bg-slate-50 p-3"><p className="text-xs text-slate-400">Composite</p><p className="mt-1 font-bold">{displayMetric(ranking.composite_score)}</p></div></div><button onClick={() => { setSelectedStrategyId(ranking.strategy_id); setSelectedScenarioId(ranking.scenario_id); const s = run.applicable_strategies.find((x) => x.strategy_id === ranking.strategy_id); const defaults = Object.fromEntries((s?.implementation_parameters ?? []).map((p) => [p.name, p.default_value])); setParameters(defaults); }} className="mt-5 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm font-bold hover:bg-slate-50">{isSelected ? "Selected" : "Select this pathway"}</button></article>; })}
              </div>
            </section>

            {selectedStrategy && <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Implementation parameters</h2><p className="mt-1 text-sm text-slate-500">Only parameters defined as editable by the backend are presented for investor input.</p><div className="mt-5 grid gap-4 md:grid-cols-2">{selectedStrategy.implementation_parameters.filter((p) => p.editable).map((p) => <label key={p.name} className="rounded-2xl bg-slate-50 p-4"><span className="text-sm font-bold text-slate-800">{p.label}</span><p className="mt-1 text-xs text-slate-500">{p.description}</p>{p.param_type === "choice" ? <select value={String(parameters[p.name] ?? p.default_value)} onChange={(e) => setParameters((x) => ({ ...x, [p.name]: e.target.value }))} className="mt-3 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm">{(p.choices ?? []).map((choice) => <option key={choice}>{choice}</option>)}</select> : <input type={p.param_type === "integer" ? "number" : "number"} step={p.param_type === "integer" ? 1 : "any"} min={p.min_value ?? undefined} max={p.max_value ?? undefined} value={String(parameters[p.name] ?? p.default_value)} onChange={(e) => setParameters((x) => ({ ...x, [p.name]: p.param_type === "integer" || p.param_type === "currency" || p.param_type === "percentage" ? Number(e.target.value) : e.target.value }))} className="mt-3 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm" />}</label>)}</div>{selectedScenario && <div className="mt-5 rounded-2xl border border-slate-100 p-4"><p className="text-sm font-bold">Scenario: {selectedScenario.scenario_name}</p><p className="mt-1 text-sm text-slate-500">{selectedScenario.trade_off_notes || "No additional trade-off notes supplied."}</p></div>}<button onClick={handleSelect} disabled={working || !selectedScenarioId} className="mt-6 rounded-xl bg-navy-900 px-6 py-3 text-sm font-bold text-white disabled:opacity-50">{working ? "Saving…" : run.selected_strategy_version_id ? "Selection saved" : "Confirm selection"}</button>{run.selected_strategy_version_id && <p className="mt-3 text-sm text-teal-700">Strategy Version created: {run.selected_strategy_version_id} (v{run.selected_strategy_version ?? "—"}).</p>}</section>}

            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><div className="flex items-center justify-between"><div><h2 className="text-lg font-bold">Strategy Run history</h2><p className="mt-1 text-sm text-slate-500">Immutable run versions returned by the backend.</p></div><span className="text-xs font-semibold text-slate-400">{history.length} runs</span></div>{history.length > 0 && <div className="mt-5 space-y-2">{history.map((item) => <div key={item.strategy_run_id ?? `${item.created_at}-${item.run_version}`} className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-slate-100 p-4"><div><span className="font-bold">Run v{item.run_version}</span><span className="ml-3 text-sm text-slate-500">Goal v{item.defined_goal_version}</span></div><span className="text-xs text-slate-400">{item.created_at ? new Date(item.created_at).toLocaleString("en-IN") : "—"}</span></div>)}</div>}</section>
          </>
        )}
      </div>
    </main>
  );
}
