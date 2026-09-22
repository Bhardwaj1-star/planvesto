"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import StrategyWorkflowNav from "../../../components/StrategyWorkflowNav";
import { InvestorButton, InvestorPageHeader, InvestorStatus } from "../../../components/InvestorUI";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";
import { addCustomScenario, getLatestStrategyRun, getPlanningUnitId, type Scenario, type StrategyImplementationParamDef, type StrategyRun } from "../../../lib/api/strategy";

function displayMetric(value: unknown, currency = false) {
  if (typeof value !== "number" || !Number.isFinite(value)) return "—";
  return currency ? `₹${Math.round(value).toLocaleString("en-IN")}` : String(value);
}

export default function StrategyScenariosPage() {
  const [goals, setGoals] = useState<Array<{ id: string; name: string }>>([]);
  const [goalId, setGoalId] = useState("");
  const [run, setRun] = useState<StrategyRun | null>(null);
  const [strategyId, setStrategyId] = useState("");
  const [name, setName] = useState("");
  const [inflationPct, setInflationPct] = useState("");
  const [funding, setFunding] = useState<Record<string, string>>({});
  const [working, setWorking] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const data = await loadGoalPlannerData();
        const activeGoals = data.goals.map((goal) => ({ id: goal.id, name: goal.name }));
        if (active) {
          setGoals(activeGoals);
          if (activeGoals[0]) setGoalId(activeGoals[0].id);
        }
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load active goals.");
      } finally {
        if (active) setLoading(false);
      }
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
        if (active) {
          setRun(latest);
          setStrategyId(latest.selected_strategy_id ?? latest.recommendation.recommended_strategy_id ?? latest.applicable_strategies[0]?.strategy_id ?? "");
        }
      } catch (err) {
        if (active) { setRun(null); setError(err instanceof Error ? err.message : "No Strategy Run is available for this goal."); }
      }
    })();
    return () => { active = false; };
  }, [goalId]);

  const strategy = useMemo(
    () => run?.applicable_strategies.find((item) => item.strategy_id === strategyId) ?? null,
    [run, strategyId],
  );
  const editableParameters = useMemo(
    () => (strategy?.implementation_parameters ?? []).filter((param) => param.editable),
    [strategy],
  );

  useEffect(() => {
    if (!run || !strategy) return;
    const baseline = run.scenarios.find((scenario) => scenario.strategy_id === strategy.strategy_id && scenario.scenario_type === "baseline");
    const rawInflation = baseline?.assumptions?.inflation_rate;
    setInflationPct(typeof rawInflation === "number" ? String(Number((rawInflation * 100).toFixed(2))) : "");
    setFunding(Object.fromEntries(editableParameters.map((param) => [
      param.name,
      String(baseline?.funding_structure?.[param.name] ?? param.default_value ?? ""),
    ])));
  }, [run, strategy, editableParameters]);

  function renderParameter(param: StrategyImplementationParamDef) {
    const value = funding[param.name] ?? "";
    const common = "mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm";
    if (param.param_type === "choice") {
      return <select value={value} onChange={(e) => setFunding((prev) => ({ ...prev, [param.name]: e.target.value }))} className={common}>
        {(param.choices ?? []).map((choice) => <option key={choice} value={choice}>{choice}</option>)}
      </select>;
    }
    return <div className="relative">
      <input
        type="number"
        value={value}
        min={param.min_value ?? undefined}
        max={param.max_value ?? undefined}
        step={param.param_type === "integer" ? 1 : "any"}
        onChange={(e) => setFunding((prev) => ({ ...prev, [param.name]: e.target.value }))}
        className={common}
      />
      {param.param_type === "percentage" && <span className="pointer-events-none absolute right-4 top-5 text-sm text-slate-400">%</span>}
    </div>;
  }

  async function submit() {
    const pu = getPlanningUnitId();
    if (!pu || !run?.strategy_run_id || !strategyId) return setError("A Strategy Run and applicable strategy are required.");
    if (!name.trim()) return setError("Scenario name is required.");

    const assumptions: Record<string, unknown> = {};
    if (inflationPct.trim()) {
      const inflation = Number(inflationPct);
      if (!Number.isFinite(inflation) || inflation < 0 || inflation > 100) return setError("Inflation assumption must be between 0% and 100%.");
      assumptions.inflation_rate = inflation / 100;
    }

    const fundingStructure: Record<string, unknown> = {};
    for (const param of editableParameters) {
      const raw = funding[param.name];
      if (param.param_type === "choice") {
        if (raw) fundingStructure[param.name] = raw;
        continue;
      }
      const value = Number(raw);
      if (!Number.isFinite(value)) return setError(`${param.label} must be a valid number.`);
      if (param.min_value != null && value < param.min_value) return setError(`${param.label} cannot be below ${param.min_value}.`);
      if (param.max_value != null && value > param.max_value) return setError(`${param.label} cannot exceed ${param.max_value}.`);
      fundingStructure[param.name] = value;
    }

    setWorking(true); setError(null); setSuccess(null);
    try {
      const next = await addCustomScenario(pu, run.strategy_run_id, strategyId, name.trim(), assumptions, fundingStructure);
      setRun(next);
      setName("");
      setSuccess("Custom scenario added. Funding impact and strategy rankings were recalculated.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to add custom scenario.");
    } finally {
      setWorking(false);
    }
  }

  if (loading) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-5xl"><div className="h-10 w-72 animate-pulse rounded-xl bg-slate-200" /><div className="mt-6 h-96 animate-pulse rounded-3xl bg-white" /></div></main>;

  const customScenarios = run?.scenarios.filter((scenario) => scenario.is_investor_modified) ?? [];

  return <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900"><div className="mx-auto max-w-5xl space-y-6 p-4 sm:p-6 lg:p-10">
    <StrategyWorkflowNav />
    <InvestorPageHeader eyebrow="Scenario planning" title="Custom Scenarios" description="Test changes to the assumptions and implementation choices that the selected strategy actually supports." />
    {error && <InvestorStatus tone="error">{error}</InvestorStatus>}
    {success && <InvestorStatus tone="success">{success}</InvestorStatus>}

    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <label className="block"><span className="text-sm font-bold">Active goal</span>
        <select value={goalId} onChange={(e) => setGoalId(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm">
          <option value="">Select goal</option>
          {goals.map((goal) => <option key={goal.id} value={goal.id}>{goal.name}</option>)}
        </select>
      </label>
      {!goals.length && <p className="mt-3 text-sm text-slate-500">No active goals are available. Cancelled goals remain in Goal History but are excluded from planning.</p>}
      {run && <div className="mt-4 flex flex-wrap gap-3 text-xs text-slate-500"><span className="rounded-full bg-slate-100 px-3 py-1">Run v{run.run_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Goal v{run.defined_goal_version}</span></div>}
    </section>

    {run ? <section className="space-y-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div>
        <label className="block"><span className="text-sm font-bold">Strategy</span>
          <select value={strategyId} onChange={(e) => setStrategyId(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm">
            {run.applicable_strategies.map((item) => <option key={item.strategy_id} value={item.strategy_id}>{item.name}</option>)}
          </select>
        </label>
        {strategy?.description && <p className="mt-2 text-sm text-slate-500">{strategy.description}</p>}
      </div>

      <label className="block"><span className="text-sm font-bold">Scenario name</span><input value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Higher growth allocation" className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm" /></label>

      <div className="rounded-2xl bg-slate-50 p-5">
        <h2 className="font-bold">What are you changing?</h2>
        <p className="mt-1 text-sm text-slate-500">Change only the inputs you want to test. Planvesto will keep the engine payload and calculations behind the interface.</p>
        <div className="mt-5 grid gap-5 md:grid-cols-2">
          <label className="block">
            <span className="text-sm font-semibold">Inflation assumption</span>
            <div className="relative"><input type="number" min={0} max={100} step="0.1" value={inflationPct} onChange={(e) => setInflationPct(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm" /><span className="pointer-events-none absolute right-4 top-5 text-sm text-slate-400">%</span></div>
            <span className="mt-1 block text-xs text-slate-500">Changes the future cost of this goal.</span>
          </label>
          {editableParameters.map((param) => <label key={param.name} className="block">
            <span className="text-sm font-semibold">{param.label}</span>
            {renderParameter(param)}
            {param.description && <span className="mt-1 block text-xs text-slate-500">{param.description}</span>}
          </label>)}
        </div>
        {!editableParameters.length && <p className="mt-4 text-sm text-slate-500">This strategy has no editable implementation parameters. You can still stress-test its inflation assumption.</p>}
      </div>

      <InvestorButton className="w-full" onClick={() => void submit()} disabled={working}>{working ? "Recalculating…" : "Create & Recalculate Scenario"}</InvestorButton>
    </section> : goalId ? <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center"><h2 className="text-xl font-bold">No Strategy Run</h2><p className="mt-2 text-sm text-slate-500">Build a Strategy Run before creating a custom scenario.</p><Link href={`/investor/strategy-builder?goalId=${encodeURIComponent(goalId)}`} className="mt-6 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white">Open Strategy Builder</Link></section> : null}

    {customScenarios.length > 0 && <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-lg font-bold">Your custom scenarios</h2>
      <p className="mt-1 text-sm text-slate-500">See what changed and the recalculated funding impact.</p>
      <div className="mt-4 space-y-4">{customScenarios.map((scenario: Scenario) => <article key={scenario.scenario_id} className="rounded-2xl border border-slate-100 bg-slate-50 p-5">
        <div className="flex flex-wrap items-start justify-between gap-3"><div><h3 className="font-bold">{scenario.scenario_name}</h3><p className="mt-1 text-xs text-slate-500">{run?.applicable_strategies.find((item) => item.strategy_id === scenario.strategy_id)?.name ?? "Strategy scenario"}</p></div><span className="rounded-full bg-white px-3 py-1 text-xs font-semibold text-slate-600">Custom</span></div>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <div className="rounded-xl bg-white p-3"><p className="text-xs text-slate-500">Target corpus</p><p className="mt-1 font-bold">{displayMetric(scenario.metrics.target_corpus, true)}</p></div>
          <div className="rounded-xl bg-white p-3"><p className="text-xs text-slate-500">Funding gap</p><p className="mt-1 font-bold">{displayMetric(scenario.metrics.funding_gap, true)}</p></div>
          <div className="rounded-xl bg-white p-3"><p className="text-xs text-slate-500">Required monthly contribution</p><p className="mt-1 font-bold">{displayMetric(scenario.metrics.required_monthly_contribution, true)}</p></div>
        </div>
        <p className="mt-4 text-sm text-slate-600"><span className="font-semibold text-slate-800">Trade-off: </span>{scenario.trade_off_notes || "Recalculated using your scenario choices."}</p>
      </article>)}</div>
    </section>}
  </div></main>;
}
