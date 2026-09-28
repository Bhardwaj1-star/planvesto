"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import StrategyWorkflowNav from "../../../components/StrategyWorkflowNav";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorButton, InvestorStatus } from "../../../components/InvestorUI";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";
import { apiRequest } from "../../../lib/api/client";
import {
  buildStrategy,
  getLatestStrategyRun,
  getStrategyRunHistory,
  getPlanningUnitId,
  selectStrategy,
  type StrategyRun,
} from "../../../lib/api/strategy";
import type { DefinedGoal } from "../../../lib/onboarding/goals/types";

function formatStatus(value: unknown) {
  if (typeof value !== "string" || !value) return "—";
  return value.replaceAll("_", " ");
}
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
        const requestedGoalId = typeof window !== "undefined" ? new URLSearchParams(window.location.search).get("goalId") : null;
        const handoffGoal = requestedGoalId ? nextGoals.find((goal) => goal.id === requestedGoalId) : null;
        setSelectedGoalId(handoffGoal?.id ?? "");
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load goals.");
      } finally { if (active) setLoading(false); }
    })();
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!selectedGoalId) { setGoalPreview(null); setRun(null); setHistory([]); return; }
    let active = true;
    (async () => {
      setWorking(true); setError(null); setRun(null); setGoalPreview(null);
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");

        let preview: DefinedGoal | null = null;
        try {
          preview = await apiRequest<DefinedGoal>(`/api/goals/${selectedGoalId}/defined/latest?planning_unit_id=${planningUnitId}`);
          if (active) setGoalPreview(preview);
        } catch { if (active) setGoalPreview(null); }

        let latest: StrategyRun | null = null;
        try {
          latest = await getLatestStrategyRun(planningUnitId, selectedGoalId);
        } catch {
          latest = null;
        }

        const runIsStale = Boolean(preview && latest && latest.defined_goal_version !== preview.version);
        if (preview && (!latest || runIsStale)) {
          latest = await buildStrategy(planningUnitId, selectedGoalId);
        }

        if (!active) return;
        if (!latest) {
          setRun(null); setHistory([]);
          setSelectedStrategyId(""); setSelectedScenarioId(""); setSelectedArchitectureId(""); setParameters({});
          return;
        }

        setRun(latest);
        setSelectedStrategyId(latest.selected_strategy_id ?? latest.recommendation.recommended_strategy_id ?? "");
        setSelectedScenarioId(latest.selected_scenario_id ?? latest.recommendation.recommended_scenario_id ?? "");
        setSelectedArchitectureId(latest.selected_architecture?.architecture_id ?? latest.recommendation.architecture?.architecture_id ?? "");
        setParameters(latest.selected_implementation_parameters ?? {});
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
    const recommendedStrategyId = run.recommendation.architecture?.primary_strategy_id ?? run.recommendation.recommended_strategy_id;
    const recommended = run.rankings.find((ranking) => ranking.is_recommended || ranking.strategy_id === recommendedStrategyId);
    const normal = run.rankings.find((ranking) => ranking.strategy_id !== recommended?.strategy_id);
    return [recommended, normal].filter((ranking): ranking is typeof run.rankings[number] => Boolean(ranking));
  }, [run]);

  const isRetirementGoal = useMemo(() => {
    const rawGoalType = goalPreview?.goal_type || goals.find((g) => g.id === selectedGoalId)?.name || "";
    const lower = rawGoalType.toLowerCase();
    return lower.includes("retirement") || lower.includes("financial freedom");
  }, [goalPreview, goals, selectedGoalId]);

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

  const handleBuild = () => {
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId || !selectedGoalId) return;
    void execute(() => buildStrategy(planningUnitId, selectedGoalId));
  };
  const handleSelect = () => {
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId || !run?.strategy_run_id || !selectedStrategyId || !selectedScenarioId) return;
    void execute(() => selectStrategy(planningUnitId, run.strategy_run_id!, selectedStrategyId, selectedScenarioId, parameters, selectedArchitectureId || undefined));
  };

  if (loading) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-6xl space-y-6"><div className="h-9 w-64 animate-pulse rounded-xl bg-slate-200" /><div className="h-24 animate-pulse rounded-3xl bg-white" /><div className="h-96 animate-pulse rounded-3xl bg-white" /></div></main>;
  if (!goals.length) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-2xl rounded-3xl border border-slate-200 bg-white p-10 text-center shadow-sm"><h1 className="text-2xl font-extrabold">No goals available</h1><p className="mt-2 text-sm text-slate-500">Strategy Builder needs a defined goal before a Strategy Run can be created.</p><Link href="/investor/goal-planner" className="mt-6 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white">Open Goal Planner</Link></div></main>;

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
      <InvestorHeader
        eyebrow="Decide"
        title="Strategy Builder"
        description="Build a coherent strategy architecture for a defined goal. The backend determines applicability, composition, feasibility, trade-offs and recommendation."
      />
      <div className="mx-auto max-w-6xl space-y-6 p-4 sm:p-6 lg:p-10">
        <StrategyWorkflowNav />
        {error && <InvestorStatus tone="error">{error}</InvestorStatus>}

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <label className="block flex-1"><span className="text-sm font-bold text-slate-700">Goal</span><select value={selectedGoalId} onChange={(e) => setSelectedGoalId(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-teal-600"><option value="">Select goal</option>{goals.map((g) => <option key={g.id} value={g.id}>{g.name}</option>)}</select>{selectedGoalId && <span className="mt-2 block text-xs font-semibold text-teal-700">Planning strategy for: {goals.find((g) => g.id === selectedGoalId)?.name ?? "Selected goal"}</span>}</label>
            <InvestorButton onClick={handleBuild} disabled={working || !selectedGoalId}>{working ? "Working…" : run ? "Rebuild Strategy Run" : "Build Strategy"}</InvestorButton>
          </div>
          {run && (
            <div className="mt-4 flex flex-wrap items-center gap-3 text-xs text-slate-500">
              <span className="rounded-full bg-slate-100 px-3 py-1">Run v{run.run_version}</span>
              <span className="rounded-full bg-slate-100 px-3 py-1">Goal version {run.defined_goal_version}</span>
              <span className="rounded-full bg-slate-100 px-3 py-1">Status: {run.status}</span>
              <span className="rounded-full bg-slate-100 px-3 py-1">Approval: {formatStatus(run.approval_status)}</span>
              {isRetirementGoal && (
                <Link
                  href={`/investor/retirement-report?run_id=${encodeURIComponent(run.strategy_run_id ?? "")}&planning_unit_id=${encodeURIComponent(run.planning_unit_id ?? "")}`}
                  className="rounded-full bg-navy-900 px-3 py-1 font-bold text-white hover:opacity-90"
                >
                  View Retirement Report
                </Link>
              )}
              <Link href="/investor/strategy-scenarios" className="rounded-full border border-slate-200 bg-white px-3 py-1 font-semibold text-slate-600 hover:bg-slate-50">Custom Scenarios</Link>
              <Link href="/investor/strategy-history" className="rounded-full border border-slate-200 bg-white px-3 py-1 font-semibold text-slate-600 hover:bg-slate-50">Strategy History</Link>
            </div>
          )}
        </section>

        {goalPreview && <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><div><h2 className="text-lg font-bold">Goal Calculation &amp; Preview</h2><p className="mt-1 text-sm text-slate-500">This is the Goal Planner calculation that the Strategy Run is based on.</p></div><div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4"><div className="rounded-2xl bg-slate-50 p-4"><p className="text-xs font-bold uppercase tracking-wide text-slate-400">Today&apos;s Cost</p><p className="mt-1 text-lg font-extrabold">{formatINR(goalPreview.today_cost)}</p></div><div className="rounded-2xl bg-slate-50 p-4"><p className="text-xs font-bold uppercase tracking-wide text-slate-400">Inflation</p><p className="mt-1 text-lg font-extrabold">{(goalPreview.inflation_rate * 100).toFixed(1)}%</p></div><div className="rounded-2xl bg-slate-50 p-4"><p className="text-xs font-bold uppercase tracking-wide text-slate-400">Required Corpus</p><p className="mt-1 text-lg font-extrabold">{formatINR(goalPreview.future_target)}</p></div><div className="rounded-2xl bg-slate-50 p-4"><p className="text-xs font-bold uppercase tracking-wide text-slate-400">Funding Gap</p><p className="mt-1 text-lg font-extrabold">{formatINR(goalPreview.funding_gap)}</p></div></div><div className="mt-4 flex flex-wrap gap-3 text-sm text-slate-600"><span>Target: <strong>{String(goalPreview.target_month).padStart(2, "0")}/{goalPreview.target_year}</strong></span><span>•</span><span>Mapped Assets: <strong>{formatINR(goalPreview.projected_mapped_asset_value)}</strong></span><span>•</span><span>Monthly Contribution: <strong>{formatINR(goalPreview.required_monthly_contribution)}</strong></span><span>•</span><span>Status: <strong>{goalPreview.funding_status}</strong></span></div></section>}

        {!run ? <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center"><h2 className="text-xl font-bold">No Strategy Run yet</h2><p className="mt-2 text-sm text-slate-500">Review the Goal Calculation &amp; Preview above, then build the Strategy Run.</p></section> : <>
          <section>
            <div className="mb-4"><h2 className="text-lg font-bold">Strategy Architectures</h2><p className="mt-1 text-sm text-slate-500">Applicable strategy architectures evaluated for this goal by the decision engine.</p></div>
            <div className="grid gap-5 lg:grid-cols-2">
              {displayedRankings.map((ranking) => {
                const strategy = run.applicable_strategies.find((s) => s.strategy_id === ranking.strategy_id);
                const isSelected = selectedStrategyId === ranking.strategy_id && selectedScenarioId === ranking.scenario_id;
                const arch = run.architectures?.find((a) => a.primary_strategy_id === ranking.strategy_id);
                return (
                  <article key={`${ranking.strategy_id}-${ranking.scenario_id}`} className={`rounded-3xl border bg-white p-6 shadow-sm ${isSelected ? "border-teal-500 ring-2 ring-teal-100" : "border-slate-200"}`}>
                    <div className="flex items-start justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-wide text-slate-400">{ranking.is_recommended ? "Recommended Architecture" : "Alternative Architecture"}</p><h3 className="mt-1 text-xl font-extrabold">{ranking.strategy_name}</h3><p className="mt-1 text-sm font-medium text-slate-500">{ranking.scenario_name}</p></div>{ranking.is_recommended && <span className="rounded-full bg-teal-50 px-3 py-1 text-xs font-bold text-teal-700">Recommended</span>}</div>
                    <p className="mt-4 text-sm leading-6 text-slate-600">{strategy?.description ?? "Strategy architecture evaluated by the engine."}</p>
                    <div className="mt-4 space-y-2 border-t border-slate-100 pt-4 text-xs text-slate-600">
                      {strategy?.strategic_objective && <div><span className="font-bold text-slate-700">Purpose: </span><span>{strategy.strategic_objective}</span></div>}
                      {arch?.rationale && arch.rationale.length > 0 && <div><span className="font-bold text-slate-700">Why applicable / Goal fit: </span><span>{arch.rationale.join("; ")}</span></div>}
                      {arch && <div><span className="font-bold text-slate-700">Feasibility: </span><span className={`inline-block rounded-full px-2 py-0.5 text-[10px] font-bold uppercase ${arch.feasibility_status === "feasible" ? "bg-emerald-50 text-emerald-700" : arch.feasibility_status === "conditional" ? "bg-amber-50 text-amber-700" : "bg-red-50 text-red-700"}`}>{arch.feasibility_status}</span></div>}
                      {arch?.constraints && arch.constraints.length > 0 && <div><span className="font-bold text-slate-700">Constraints: </span><span>{arch.constraints.join("; ")}</span></div>}
                      {strategy?.trade_offs && strategy.trade_offs.length > 0 && <div><span className="font-bold text-slate-700">Trade-offs: </span><span>{strategy.trade_offs.join("; ")}</span></div>}
                      {(() => { const baselineScenario = run.scenarios.find((s) => s.strategy_id === ranking.strategy_id && s.scenario_type === "baseline"); if (!baselineScenario) return null; const assumptionEntries = Object.entries(baselineScenario.assumptions); return assumptionEntries.length > 0 ? <div><span className="font-bold text-slate-700">Assumptions: </span><span>{assumptionEntries.map(([k, v]) => `${k.replaceAll("_", " ")}: ${displayMetric(v)}`).join("; ")}</span></div> : null; })()}
                      {strategy?.technique_ids && strategy.technique_ids.length > 0 && <div><span className="font-bold text-slate-700">Techniques / implementation direction: </span><span className="capitalize">{strategy.technique_ids.join(", ").replaceAll("-", " ")}</span></div>}
                      {(() => { const scenariosForStrategy = run.scenarios.filter((s) => s.strategy_id === ranking.strategy_id); if (scenariosForStrategy.length <= 1) return null; return <div><span className="font-bold text-slate-700">Scenarios: </span><span>{scenariosForStrategy.map((s) => s.scenario_name).join("; ")}</span></div>; })()}
                    </div>
                    <button onClick={() => { setSelectedStrategyId(ranking.strategy_id); setSelectedScenarioId(ranking.scenario_id); const s = run.applicable_strategies.find((x) => x.strategy_id === ranking.strategy_id); const defaults = Object.fromEntries((s?.implementation_parameters ?? []).map((p) => [p.name, p.default_value])); setParameters(defaults); }} className="mt-5 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm font-bold hover:bg-slate-50">{isSelected ? "Selected" : "Select this architecture"}</button>
                  </article>
                );
              })}
            </div>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Recommendation</h2><div className="mt-4 space-y-3 text-sm text-slate-600">
            {(() => { const recStrategy = run.applicable_strategies.find((s) => s.strategy_id === run.recommendation.recommended_strategy_id); return <div className="rounded-2xl border border-teal-100 bg-teal-50/50 p-4"><p className="text-xs font-bold uppercase tracking-wide text-teal-700">Recommended Architecture</p><p className="mt-1 text-base font-extrabold text-slate-900">{recStrategy?.name ?? run.recommendation.recommended_strategy_id}</p></div>; })()}
            {run.recommendation.short_reasons.length > 0 && <div><p className="text-xs font-bold uppercase tracking-wide text-slate-400">Reasoning</p><ul className="mt-1 list-disc space-y-0.5 pl-5 text-sm text-slate-600">{run.recommendation.short_reasons.map((reason, i) => <li key={i}>{reason}</li>)}</ul></div>}
            {run.recommendation.complete_reasoning && <p className="text-sm leading-6 text-slate-600">{run.recommendation.complete_reasoning}</p>}
            {run.recommendation.constraints.length > 0 && <div><p className="text-xs font-bold uppercase tracking-wide text-slate-400">Constraints</p><p className="mt-1 text-sm text-slate-600">{run.recommendation.constraints.join("; ")}</p></div>}
            {run.recommendation.feasibility_status && <div><span className="text-xs font-bold uppercase tracking-wide text-slate-400">Feasibility: </span><span className={`inline-block rounded-full px-2 py-0.5 text-[10px] font-bold uppercase ${run.recommendation.feasibility_status === "feasible" ? "bg-emerald-50 text-emerald-700" : run.recommendation.feasibility_status === "conditional" ? "bg-amber-50 text-amber-700" : "bg-red-50 text-red-700"}`}>{run.recommendation.feasibility_status}</span></div>}
            {run.recommendation.alternative_architecture_ids.length > 0 && <div><p className="text-xs font-bold uppercase tracking-wide text-slate-400">Alternatives</p><div className="mt-1 flex flex-wrap gap-2">{run.recommendation.alternative_architecture_ids.map((altId) => { const altArch = run.architectures.find((a) => a.architecture_id === altId); const altStrategy = altArch ? run.applicable_strategies.find((s) => s.strategy_id === altArch.primary_strategy_id) : null; return <span key={altId} className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">{altStrategy?.name ?? altId}</span>; })}</div></div>}
          </div></section>

          {selectedStrategy && <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Implementation parameters</h2><p className="mt-1 text-sm text-slate-500">Only editable parameters defined by the backend are presented for investor input.</p><div className="mt-5 grid gap-4 md:grid-cols-2">{selectedStrategy.implementation_parameters.filter((p) => p.editable).map((p) => <label key={p.name} className="rounded-2xl bg-slate-50 p-4"><span className="text-sm font-bold text-slate-800">{p.label}</span><p className="mt-1 text-xs text-slate-500">{p.description}</p>{p.param_type === "choice" ? <select value={String(parameters[p.name] ?? p.default_value)} onChange={(e) => setParameters((x) => ({ ...x, [p.name]: e.target.value }))} className="mt-3 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm">{(p.choices ?? []).map((choice) => <option key={choice}>{choice}</option>)}</select> : <input type="number" step={p.param_type === "integer" ? 1 : "any"} min={p.min_value ?? undefined} max={p.max_value ?? undefined} value={String(parameters[p.name] ?? p.default_value)} onChange={(e) => setParameters((x) => ({ ...x, [p.name]: Number(e.target.value) }))} className="mt-3 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm" />}</label>)}</div>{selectedScenario && <div className="mt-5 rounded-2xl border border-slate-100 p-4"><p className="text-sm font-bold">Scenario: {selectedScenario.scenario_name}</p><p className="mt-1 text-sm text-slate-500">{selectedScenario.trade_off_notes || "No additional trade-off notes supplied."}</p></div>}<InvestorButton className="mt-6" onClick={handleSelect} disabled={working || !selectedScenarioId}>{working ? "Saving…" : run.selected_strategy_version_id ? "Save selection again" : "Confirm selection"}</InvestorButton>
            {run.selected_strategy_version_id && <div className="mt-6 rounded-2xl border border-teal-200 bg-teal-50/70 p-5"><div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"><div><span className="inline-block rounded-full bg-teal-600 px-2.5 py-0.5 text-[11px] font-extrabold uppercase tracking-wider text-white">Selected &amp; Stored</span><h3 className="mt-2 text-lg font-extrabold text-navy-900">Strategy Architecture: {selectedStrategy?.name ?? run.selected_strategy_id}</h3><p className="mt-0.5 text-xs text-slate-600">Strategy Version {run.selected_strategy_version_id} (v{run.selected_strategy_version ?? "1"}) persisted. {isRetirementGoal ? "You can now view your comprehensive retirement report or proceed through approval." : "You can now proceed through strategy approval and implementation action planning."}</p></div><div className="flex flex-wrap items-center gap-2">{isRetirementGoal && <Link href={`/investor/retirement-report?run_id=${encodeURIComponent(run.strategy_run_id ?? "")}&planning_unit_id=${encodeURIComponent(run.planning_unit_id ?? "")}`} className="inline-flex items-center justify-center rounded-xl bg-navy-900 px-5 py-2.5 text-sm font-bold text-white shadow-sm transition hover:bg-navy-800">View Retirement Report →</Link>}<Link href="/investor/strategy-approval" className={`inline-flex items-center justify-center rounded-xl px-5 py-2.5 text-sm font-bold transition ${isRetirementGoal ? "border border-slate-300 bg-white text-slate-700 hover:bg-slate-50" : "bg-navy-900 text-white shadow-sm hover:bg-navy-800"}`}>{isRetirementGoal ? "Proceed to Approval" : "Proceed to Approval →"}</Link><Link href="/investor/action-plan" className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm font-bold text-slate-700 hover:bg-slate-50">Action Plan</Link></div></div></div>}
          </section>}

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><div className="flex items-center justify-between"><div><h2 className="text-lg font-bold">Strategy Run history</h2><p className="mt-1 text-sm text-slate-500">Immutable run versions returned by the backend.</p></div><span className="text-xs font-semibold text-slate-400">{history.length} runs</span></div>{history.length > 0 && <div className="mt-5 space-y-2">{history.map((item) => <div key={item.strategy_run_id ?? `${item.created_at}-${item.run_version}`} className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-slate-100 p-4"><div><span className="font-bold">Run v{item.run_version}</span><span className="ml-3 text-sm text-slate-500">Goal v{item.defined_goal_version}</span><span className="ml-3 text-xs text-slate-400">{formatStatus(item.approval_status)}</span></div><span className="text-xs text-slate-400">{item.created_at ? new Date(item.created_at).toLocaleString("en-IN") : "—"}</span></div>)}</div>}</section>
        </>}
      </div>
    </main>
  );
}
