"use client";

import { useEffect, useMemo, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import StrategyWorkflowNav from "../../../components/StrategyWorkflowNav";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorButton, InvestorStatus } from "../../../components/InvestorUI";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";
import {
  finalizeImplementation,
  getPlanningUnitId,
  getStrategyRunById,
  previewImplementation,
  downloadGoalStrategyReportPdfByStrategyVersion,
  type Scenario,
  type StrategyImplementationParamDef,
  type StrategyRun,
} from "../../../lib/api/strategy";
import { getLatestDefinedGoal } from "../../../lib/api/goals";

function displayCurrency(value: unknown): string {
  if (typeof value !== "number" || !Number.isFinite(value)) return "—";
  return `₹${Math.round(value).toLocaleString("en-IN")}`;
}

function displayPct(value: unknown): string {
  if (typeof value !== "number" || !Number.isFinite(value)) return "—";
  return `${(value * 100).toFixed(1)}%`;
}

function getProbabilityBadgeStyle(band: string | undefined, prob: number | undefined) {
  if ((prob && prob >= 0.9) || (band && band.includes("High Certainty"))) {
    return {
      bg: "bg-emerald-50",
      border: "border-emerald-200",
      text: "text-emerald-700",
      dot: "bg-emerald-500",
      label: "High Certainty (≥ 90%)",
    };
  }
  if ((prob && prob >= 0.8) || (band && band.includes("Moderate Certainty"))) {
    return {
      bg: "bg-blue-50",
      border: "border-blue-200",
      text: "text-blue-700",
      dot: "bg-blue-500",
      label: "Moderate Certainty (80–89%)",
    };
  }
  if ((prob && prob >= 0.65) || (band && band.includes("Moderate Risk"))) {
    return {
      bg: "bg-amber-50",
      border: "border-amber-200",
      text: "text-amber-700",
      dot: "bg-amber-500",
      label: "Fair / Moderate Risk (65–79%)",
    };
  }
  return {
    bg: "bg-rose-50",
    border: "border-rose-200",
    text: "text-rose-700",
    dot: "bg-rose-500",
    label: "Underfunded Risk (< 65%)",
  };
}

function StrategyScenariosContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const urlGoalId = searchParams.get("goalId");
  const urlStrategyId = searchParams.get("strategyId");
  const urlStrategyRunId = searchParams.get("strategyRunId");
  const urlScenarioId = searchParams.get("scenarioId");
  const urlArchitectureId = searchParams.get("architectureId");
  const urlGoalVersion = Number(searchParams.get("goalVersion") || "0");

  const [goals, setGoals] = useState<Array<{ id: string; name: string; targetAmount?: string }>>([]);
  const [goalId, setGoalId] = useState<string>("");
  const [definedGoal, setDefinedGoal] = useState<Record<string, unknown> | null>(null);
  const [run, setRun] = useState<StrategyRun | null>(null);
  const [strategyId, setStrategyId] = useState<string>("");

  // Parameter Adjusters
  const [scenarioName, setScenarioName] = useState<string>("");
  const [monthlyContribution, setMonthlyContribution] = useState<string>("");
  const [annualStepUpPct, setAnnualStepUpPct] = useState<string>("0");
  const [lumpsum, setLumpsum] = useState<string>("0");
  const [durationYears, setDurationYears] = useState<string>("");
  const [inflationPct, setInflationPct] = useState<string>("");
  const [strategyParams, setStrategyParams] = useState<Record<string, string>>({});

  // Active / Selected Scenario for Inspection & Decision Locking
  const [activeScenarioId, setActiveScenarioId] = useState<string | null>(null);

  // Status & Execution
  const [loading, setLoading] = useState<boolean>(true);
  const [working, setWorking] = useState<boolean>(false);
  const [locking, setLocking] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // 1. Initial Load of Goals
  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const data = await loadGoalPlannerData();
        const activeGoals = data.goals.map((g) => ({
          id: g.id,
          name: g.name,
          targetAmount: g.targetAmount,
        }));
        if (active) {
          setGoals(activeGoals);
          if (urlGoalId && activeGoals.some((g) => g.id === urlGoalId)) {
            setGoalId(urlGoalId);
          } else if (activeGoals[0]) {
            setGoalId(activeGoals[0].id);
          }
        }
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load active goals.");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, [urlGoalId]);

  // 2. Load the exact Strategy Run selected in Strategy Builder.
  // Latest-run state is never used to establish implementation context.
  useEffect(() => {
    if (!urlGoalId || !urlStrategyRunId || !urlStrategyId) {
      setRun(null);
      setDefinedGoal(null);
      setError("Implementation context is missing. Return to Strategy Builder and select a strategy.");
      return;
    }
    let active = true;
    (async () => {
      setError(null);
      setSuccess(null);
      try {
        const pu = getPlanningUnitId();
        if (!pu) throw new Error("Planning unit is not available.");
        const dg = await getLatestDefinedGoal(pu, urlGoalId);
        const selectedRun = await getStrategyRunById(pu, urlStrategyRunId);
        if (!active) return;

        if (urlGoalVersion && selectedRun.defined_goal_version !== urlGoalVersion) {
          throw new Error("The selected goal version no longer matches this Strategy Run.");
        }
        const selectedScenarioId = urlScenarioId || selectedRun.scenarios.find((item) => item.strategy_id === urlStrategyId && item.scenario_type === "baseline")?.scenario_id || "";
        if (!selectedRun.applicable_strategies.some((item) => item.strategy_id === urlStrategyId)) {
          throw new Error("The selected strategy is not available in this Strategy Run.");
        }

        setGoalId(urlGoalId);
        setDefinedGoal(dg);
        setRun(selectedRun);
        setStrategyId(urlStrategyId);
        setActiveScenarioId(selectedScenarioId);
      } catch (err) {
        if (active) {
          setRun(null);
          setError(err instanceof Error ? err.message : "Unable to load the selected implementation context.");
        }
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, [urlGoalId, urlStrategyId, urlStrategyRunId, urlScenarioId, urlGoalVersion]);

  // Strategy object
  const strategy = useMemo(
    () => run?.applicable_strategies.find((item) => item.strategy_id === strategyId) ?? null,
    [run, strategyId],
  );

  const baselineScenario = useMemo(
    () => run?.scenarios.find((s) => s.strategy_id === strategyId && s.scenario_type === "baseline") ?? run?.scenarios[0] ?? null,
    [run, strategyId],
  );

  const customScenarios = useMemo(
    () => (run?.scenarios ?? []).filter((s) => s.strategy_id === strategyId && s.is_investor_modified),
    [run, strategyId],
  );

  // Active scenario to compare with baseline (defaults to latest custom scenario, or baseline)
  const activeScenario = useMemo(() => {
    if (activeScenarioId) {
      const found = run?.scenarios.find((s) => s.scenario_id === activeScenarioId);
      if (found) return found;
    }
    if (customScenarios.length > 0) {
      return customScenarios[customScenarios.length - 1];
    }
    return baselineScenario;
  }, [activeScenarioId, customScenarios, baselineScenario, run]);

  const editableParameters = useMemo(
    () => (strategy?.implementation_parameters ?? []).filter((param) => param.editable),
    [strategy],
  );

  // Reset inputs when strategy or baseline changes
  useEffect(() => {
    if (!baselineScenario) return;
    const baseReqMonthly = Number(
      baselineScenario.metrics.required_monthly_contribution ??
      baselineScenario.funding_structure?.starting_monthly_contribution ??
      definedGoal?.required_monthly_contribution ??
      0
    );
    setMonthlyContribution(baseReqMonthly > 0 ? String(Math.round(baseReqMonthly)) : "0");

    const rawInflation = baselineScenario.assumptions?.inflation_rate ?? definedGoal?.inflation_rate;
    setInflationPct(typeof rawInflation === "number" ? String(Number((rawInflation * 100).toFixed(1))) : "6.0");

    const rawDuration = baselineScenario.metrics.duration_years ?? definedGoal?.duration_years;
    setDurationYears(rawDuration ? String(rawDuration) : "15");

    setAnnualStepUpPct(String(baselineScenario.funding_structure?.annual_step_up_pct ?? "0"));
    setLumpsum(String(baselineScenario.funding_structure?.lumpsum ?? "0"));
    setScenarioName(`Plan with ₹${Math.round(baseReqMonthly).toLocaleString("en-IN")}/mo`);

    setStrategyParams(
      Object.fromEntries(
        editableParameters.map((param) => [
          param.name,
          String(baselineScenario.funding_structure?.[param.name] ?? param.default_value ?? ""),
        ]),
      ),
    );
  }, [baselineScenario, definedGoal, editableParameters]);

  // Constraint Checks
  const availableSurplus = Number(definedGoal?.available_monthly_surplus ?? 0);
  const inputMonthly = Number(monthlyContribution) || 0;
  const isSurplusBoundaryExceeded = availableSurplus > 0 && inputMonthly > availableSurplus;
  const surplusDeficit = inputMonthly - availableSurplus;

  // Handle Recalculation
  async function handleRecalculate() {
    const pu = getPlanningUnitId();
    if (!pu || !run?.strategy_run_id || !strategyId || !selectedScenarioId) {
      return setError("The selected Strategy Run, strategy, and scenario are required.");
    }

    const assumptions: Record<string, unknown> = {};
    if (inflationPct.trim()) {
      const inf = Number(inflationPct);
      if (!Number.isFinite(inf) || inf < 0 || inf > 50) {
        return setError("Inflation assumption must be between 0% and 50%.");
      }
      assumptions.inflation_rate = inf / 100;
    }
    if (durationYears.trim()) {
      const dur = Number(durationYears);
      if (!Number.isFinite(dur) || dur < 1 || dur > 50) {
        return setError("Goal duration must be between 1 and 50 years.");
      }
      assumptions.duration_years = dur;
    }

    const fundingStructure: Record<string, unknown> = {
      starting_monthly_contribution: inputMonthly,
      annual_step_up_pct: Number(annualStepUpPct) || 0,
      lumpsum: Number(lumpsum) || 0,
    };

    for (const param of editableParameters) {
      const raw = strategyParams[param.name];
      if (param.param_type === "choice") {
        if (raw) fundingStructure[param.name] = raw;
        continue;
      }
      const val = Number(raw);
      if (!Number.isFinite(val)) return setError(`${param.label} must be a valid number.`);
      if (param.min_value != null && val < param.min_value) return setError(`${param.label} cannot be below ${param.min_value}.`);
      if (param.max_value != null && val > param.max_value) return setError(`${param.label} cannot exceed ${param.max_value}.`);
      fundingStructure[param.name] = val;
    }

    setWorking(true);
    setError(null);
    setSuccess(null);

    try {
      const updatedRun = await previewImplementation(
        pu,
        run.strategy_run_id,
        strategyId,
        selectedScenarioId,
        Object.fromEntries(
          editableParameters.map((param) => {
            const raw = strategyParams[param.name];
            return [param.name, param.param_type === "choice" ? raw : Number(raw)];
          }),
        ),
        assumptions,
        fundingStructure,
        urlArchitectureId || undefined,
      );
      setRun(updatedRun);
      const newlyAdded = updatedRun.scenarios
        .filter((s) => s.strategy_id === strategyId && s.is_investor_modified)
        .slice(-1)[0];
      if (newlyAdded) setActiveScenarioId(newlyAdded.scenario_id);
      setSuccess("What-if analysis recalculated. Nothing has been saved yet.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to calculate implementation preview.");
    } finally {
      setWorking(false);
    }
  }

  // Handle Decision Lock & Navigation to Action Plan
  async function handleLockDecision() {
    const pu = getPlanningUnitId();
    if (!pu || !run?.strategy_run_id || !strategyId || !selectedScenarioId) {
      return setError("Missing implementation context.");
    }

    const implementationParameters: Record<string, unknown> = Object.fromEntries(
      editableParameters.map((param) => {
        const raw = strategyParams[param.name];
        return [param.name, param.param_type === "choice" ? raw : Number(raw)];
      }),
    );
    const assumptions: Record<string, unknown> = {};
    if (inflationPct.trim()) assumptions.inflation_rate = Number(inflationPct) / 100;
    if (durationYears.trim()) assumptions.duration_years = Number(durationYears);

    const fundingStructure: Record<string, unknown> = {
      starting_monthly_contribution: inputMonthly,
      annual_step_up_pct: Number(annualStepUpPct) || 0,
      lumpsum: Number(lumpsum) || 0,
    };

    setLocking(true);
    setError(null);
    setSuccess(null);

    try {
      const finalizedRun = await finalizeImplementation(
        pu,
        run.strategy_run_id,
        run.defined_goal_version,
        strategyId,
        selectedScenarioId,
        implementationParameters,
        assumptions,
        fundingStructure,
        urlArchitectureId || undefined,
      );
      setRun(finalizedRun);
      const versionId = finalizedRun.selected_strategy_version_id;
      if (!versionId) throw new Error("Implementation finalized but no Strategy Version was created.");
      setSuccess("Implementation finalized. Your Strategy Version is now the source of truth.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to finalize implementation.");
      setLocking(false);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
        <div className="mx-auto max-w-6xl space-y-6">
          <div className="h-10 w-80 animate-pulse rounded-xl bg-slate-200" />
          <div className="h-64 animate-pulse rounded-3xl bg-white" />
          <div className="h-96 animate-pulse rounded-3xl bg-white" />
        </div>
      </main>
    );
  }

  const baselineMetrics = baselineScenario?.metrics ?? {};
  const activeMetrics = activeScenario?.metrics ?? baselineMetrics;
  const probStyle = getProbabilityBadgeStyle(
    activeMetrics.probability_band as string | undefined,
    activeMetrics.probability_of_success as number | undefined,
  );

  const baseTarget = Number(baselineMetrics.target_corpus ?? definedGoal?.future_target ?? 0);
  const activeTarget = Number(activeMetrics.target_corpus ?? baseTarget);
  const deltaTarget = activeTarget - baseTarget;

  const baseGap = Number(baselineMetrics.funding_gap ?? definedGoal?.funding_gap ?? 0);
  const activeGap = Number(activeMetrics.funding_gap ?? baseGap);
  const deltaGap = baseGap - activeGap; // positive means gap was reduced

  const activePros = (activeMetrics.trade_offs_pros as string[]) ?? [];
  const activeCons = (activeMetrics.trade_offs_cons as string[]) ?? [];
  const activeViolations = (activeMetrics.constraint_violations as Array<{ message: string; limit: number; current_value: number }>) ?? [];

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-20 text-slate-900">
      <InvestorHeader
        eyebrow="Step 2: Interactive Decision Workspace"
        title="Participate With Your Numbers"
        description="Interact directly with the strategy using your own financial numbers. Explore parameter changes, observe cause-and-effect trade-offs, and lock your informed decision."
      />

      <div className="mx-auto max-w-6xl space-y-6 p-4 sm:p-6 lg:p-10">
        <StrategyWorkflowNav showWorkflow={false} />

        {/* Core Product Principle Banner */}
        <div className="rounded-2xl border border-sky-200 bg-sky-50/70 p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 shadow-xs">
          <div className="flex items-center gap-3">
            <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-sky-600 text-white font-bold text-sm shadow-xs">
              ⚡
            </span>
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-sky-800">Planvesto Decision Framework</p>
              <p className="text-sm font-semibold text-sky-950 mt-0.5">
                The system calculates & explains. You participate with your numbers. You decide.
              </p>
            </div>
          </div>
          <div className="text-xs text-sky-700 bg-white/90 border border-sky-100 rounded-lg px-3 py-1.5 self-start sm:self-auto font-medium">
            Strict Boundary: Financial Constraints
          </div>
        </div>

        {error && <InvestorStatus tone="error">{error}</InvestorStatus>}
        {success && <InvestorStatus tone="success">{success}</InvestorStatus>}

        {/* Selected Goal & Strategy Context */}
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="grid gap-6 md:grid-cols-3">
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-slate-500">Goal</p>
              <p className="mt-2 text-lg font-extrabold text-slate-900">{String(definedGoal?.goal_name ?? goalId)}</p>
              <p className="mt-1 text-xs text-slate-500">Goal Version {run?.defined_goal_version ?? (urlGoalVersion || "—")}</p>
            </div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-slate-500">Selected Strategy</p>
              <p className="mt-2 text-lg font-extrabold text-slate-900">{strategy?.name ?? strategyId}</p>
              <p className="mt-1 text-xs text-slate-500">Strategy Run v{run?.run_version ?? "—"}</p>
            </div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-slate-500">Architecture</p>
              <p className="mt-2 break-all text-sm font-semibold text-slate-800">{urlArchitectureId ?? "—"}</p>
            </div>
          </div>
        </section>

        {!run ? (
          <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-12 text-center shadow-sm">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-amber-50 text-amber-600 text-2xl font-bold">
              !
            </div>
            <h2 className="mt-4 text-xl font-bold text-slate-900">Strategy Run Required</h2>
            <p className="mt-2 text-sm text-slate-500 max-w-md mx-auto">
              Before exploring numbers and trade-offs, generate initial strategies for this goal using the Strategy Builder.
            </p>
            <Link
              href={`/investor/strategy-builder?goalId=${encodeURIComponent(goalId)}`}
              className="mt-6 inline-flex items-center gap-2 rounded-xl bg-navy-900 px-6 py-3 text-sm font-bold text-white shadow-sm hover:bg-navy-800"
            >
              Open Strategy Builder →
            </Link>
          </section>
        ) : (
          <>
            {/* PILLAR 1: BASELINE REFERENCE STATS */}
            <section className="space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                  Pillar 1: Authoritative Baseline Reference ("Where Am I")
                </h3>
                <span className="text-xs font-medium text-slate-400">
                  Engine Run v{run.run_version} · Goal v{run.defined_goal_version}
                </span>
              </div>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-2xs">
                  <p className="text-xs font-medium text-slate-500">Baseline Target Corpus</p>
                  <p className="mt-1 text-xl font-black text-slate-900">{displayCurrency(baseTarget)}</p>
                  <p className="mt-1 text-xs text-slate-400">At {String(definedGoal?.inflation_rate ? Number(definedGoal.inflation_rate) * 100 : 6)}% inflation</p>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-2xs">
                  <p className="text-xs font-medium text-slate-500">Baseline Required Monthly SIP</p>
                  <p className="mt-1 text-xl font-black text-slate-900">
                    {displayCurrency(baselineMetrics.required_monthly_contribution ?? definedGoal?.required_monthly_contribution)}
                  </p>
                  <p className="mt-1 text-xs text-slate-400">To reach 100% of target</p>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-2xs">
                  <p className="text-xs font-medium text-slate-500">Investable Monthly Surplus</p>
                  <p className="mt-1 text-xl font-black text-navy-900">{displayCurrency(availableSurplus)}</p>
                  <p className="mt-1 text-xs text-slate-400">Constraint boundary limit</p>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-2xs">
                  <p className="text-xs font-medium text-slate-500">Baseline Funding Gap</p>
                  <p className="mt-1 text-xl font-black text-rose-600">{displayCurrency(baseGap)}</p>
                  <p className="mt-1 text-xs text-slate-400">
                    {baseGap === 0 ? "Fully funded" : "Unfunded gap"}
                  </p>
                </div>
              </div>
            </section>

            {/* PILLAR 2: INTERACTIVE CONTROLS & CONSTRAINT BOUNDARY */}
            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border-b border-slate-100 pb-4">
                <div>
                  <h3 className="text-lg font-bold text-slate-900">
                    Pillar 2: Participate With Your Numbers ("What If I Change?")
                  </h3>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Adjust parameters below. The system checks constraints and calculates the impact in real time.
                  </p>
                </div>
                <span className="self-start sm:self-auto rounded-full bg-slate-100 px-3 py-1 text-xs font-bold text-slate-600">
                  Interactive Controls
                </span>
              </div>

              {/* Real-time Constraint Guardrail Alert */}
              {isSurplusBoundaryExceeded ? (
                <div className="rounded-2xl border border-rose-300 bg-rose-50/80 p-4 text-rose-900 flex items-start gap-3">
                  <span className="text-lg leading-none">⚠️</span>
                  <div className="text-xs space-y-1">
                    <p className="font-bold text-rose-950">
                      Constraint Boundary Violated: Monthly SIP exceeds investable surplus
                    </p>
                    <p className="text-rose-800">
                      Your proposed monthly commitment of <strong>{displayCurrency(inputMonthly)}</strong> exceeds your
                      available investable surplus of <strong>{displayCurrency(availableSurplus)}</strong> by{" "}
                      <strong>{displayCurrency(surplusDeficit)}/month</strong>.
                    </p>
                    <p className="text-rose-700 italic">
                      Rule: To proceed with this scenario, you must either reallocate discretionary expenses, liquidate unmapped assets, or reduce your monthly commitment.
                    </p>
                  </div>
                </div>
              ) : availableSurplus > 0 ? (
                <div className="rounded-2xl border border-emerald-200 bg-emerald-50/60 p-3.5 text-xs text-emerald-900 flex items-center justify-between">
                  <span className="flex items-center gap-2">
                    <span className="text-emerald-600 font-bold">✓</span>
                    <span>
                      Feasible Cash-Flow State: Monthly commitment of <strong>{displayCurrency(inputMonthly)}</strong> is
                      well within your <strong>{displayCurrency(availableSurplus)}</strong> surplus limit.
                    </span>
                  </span>
                  <span className="font-semibold text-emerald-800">
                    Buffer: {displayCurrency(availableSurplus - inputMonthly)}/mo left
                  </span>
                </div>
              ) : null}

              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {/* 1. Monthly Contribution */}
                <div className="rounded-2xl border border-slate-200 bg-slate-50/60 p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <label className="text-xs font-bold uppercase tracking-wider text-slate-700">
                      Starting Monthly SIP
                    </label>
                    <span className="text-xs font-bold text-navy-800">{displayCurrency(inputMonthly)}</span>
                  </div>
                  <div className="relative">
                    <span className="absolute left-3.5 top-3 text-sm text-slate-400 font-semibold">₹</span>
                    <input
                      type="number"
                      value={monthlyContribution}
                      onChange={(e) => setMonthlyContribution(e.target.value)}
                      className="w-full rounded-xl border border-slate-200 bg-white pl-8 pr-4 py-2.5 text-sm font-bold text-slate-900 focus:border-navy-600 focus:outline-none"
                    />
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {availableSurplus > 0 && (
                      <button
                        type="button"
                        onClick={() => setMonthlyContribution(String(Math.round(availableSurplus)))}
                        className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-[11px] font-semibold text-slate-700 hover:bg-slate-100"
                      >
                        Max Surplus ({displayCurrency(availableSurplus)})
                      </button>
                    )}
                    <button
                      type="button"
                      onClick={() => setMonthlyContribution((prev) => String((Number(prev) || 0) + 5000))}
                      className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-[11px] font-semibold text-slate-700 hover:bg-slate-100"
                    >
                      +₹5,000
                    </button>
                    <button
                      type="button"
                      onClick={() => setMonthlyContribution((prev) => String((Number(prev) || 0) + 10000))}
                      className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-[11px] font-semibold text-slate-700 hover:bg-slate-100"
                    >
                      +₹10,000
                    </button>
                  </div>
                  <p className="text-[11px] text-slate-500">
                    Systematic monthly allocation dedicated to this specific goal.
                  </p>
                </div>

                {/* 2. Annual Step-Up % */}
                <div className="rounded-2xl border border-slate-200 bg-slate-50/60 p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <label className="text-xs font-bold uppercase tracking-wider text-slate-700">
                      Annual Step-Up Rate
                    </label>
                    <span className="text-xs font-bold text-navy-800">{annualStepUpPct}% / yr</span>
                  </div>
                  <div className="relative">
                    <input
                      type="number"
                      min={0}
                      max={30}
                      step={1}
                      value={annualStepUpPct}
                      onChange={(e) => setAnnualStepUpPct(e.target.value)}
                      className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-bold text-slate-900 focus:border-navy-600 focus:outline-none"
                    />
                    <span className="absolute right-4 top-3 text-sm text-slate-400 font-semibold">%</span>
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {["0", "5", "10", "15"].map((pct) => (
                      <button
                        key={pct}
                        type="button"
                        onClick={() => setAnnualStepUpPct(pct)}
                        className={`rounded-lg border px-2.5 py-1 text-[11px] font-semibold transition-all ${
                          annualStepUpPct === pct
                            ? "border-navy-900 bg-navy-900 text-white"
                            : "border-slate-200 bg-white text-slate-700 hover:bg-slate-100"
                        }`}
                      >
                        {pct}%
                      </button>
                    ))}
                  </div>
                  <p className="text-[11px] text-slate-500">
                    Increases SIP yearly in sync with career growth, accelerating compounding.
                  </p>
                </div>

                {/* 3. Lumpsum Influx */}
                <div className="rounded-2xl border border-slate-200 bg-slate-50/60 p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <label className="text-xs font-bold uppercase tracking-wider text-slate-700">
                      Initial Lump-Sum Influx
                    </label>
                    <span className="text-xs font-bold text-navy-800">{displayCurrency(Number(lumpsum) || 0)}</span>
                  </div>
                  <div className="relative">
                    <span className="absolute left-3.5 top-3 text-sm text-slate-400 font-semibold">₹</span>
                    <input
                      type="number"
                      value={lumpsum}
                      onChange={(e) => setLumpsum(e.target.value)}
                      className="w-full rounded-xl border border-slate-200 bg-white pl-8 pr-4 py-2.5 text-sm font-bold text-slate-900 focus:border-navy-600 focus:outline-none"
                    />
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {["0", "100000", "500000", "1000000"].map((amt) => (
                      <button
                        key={amt}
                        type="button"
                        onClick={() => setLumpsum(amt)}
                        className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-[11px] font-semibold text-slate-700 hover:bg-slate-100"
                      >
                        {amt === "0" ? "None" : `+₹${Number(amt) / 100000}L`}
                      </button>
                    ))}
                  </div>
                  <p className="text-[11px] text-slate-500">
                    One-time bonus, matured deposit, or portfolio reallocation.
                  </p>
                </div>

                {/* 4. Goal Duration / Horizon */}
                <div className="rounded-2xl border border-slate-200 bg-slate-50/60 p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <label className="text-xs font-bold uppercase tracking-wider text-slate-700">
                      Goal Horizon (Years)
                    </label>
                    <span className="text-xs font-bold text-navy-800">{durationYears} years</span>
                  </div>
                  <div className="relative">
                    <input
                      type="number"
                      min={1}
                      max={45}
                      step={0.5}
                      value={durationYears}
                      onChange={(e) => setDurationYears(e.target.value)}
                      className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-bold text-slate-900 focus:border-navy-600 focus:outline-none"
                    />
                    <span className="absolute right-4 top-3 text-xs text-slate-400 font-semibold">yrs</span>
                  </div>
                  <p className="text-[11px] text-slate-500">
                    Extending horizon lowers required monthly burden; shortening it requires higher SIP.
                  </p>
                </div>

                {/* 5. Inflation Stress Testing */}
                <div className="rounded-2xl border border-slate-200 bg-slate-50/60 p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <label className="text-xs font-bold uppercase tracking-wider text-slate-700">
                      Inflation Assumption
                    </label>
                    <span className="text-xs font-bold text-navy-800">{inflationPct}%</span>
                  </div>
                  <div className="relative">
                    <input
                      type="number"
                      min={0}
                      max={25}
                      step={0.1}
                      value={inflationPct}
                      onChange={(e) => setInflationPct(e.target.value)}
                      className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-bold text-slate-900 focus:border-navy-600 focus:outline-none"
                    />
                    <span className="absolute right-4 top-3 text-sm text-slate-400 font-semibold">%</span>
                  </div>
                  <p className="text-[11px] text-slate-500">
                    Higher inflation increases future target corpus exponentially.
                  </p>
                </div>

                {/* 6. Dynamic Strategy Parameters */}
                {editableParameters.map((param) => (
                  <div key={param.name} className="rounded-2xl border border-slate-200 bg-slate-50/60 p-4 space-y-3">
                    <div className="flex items-center justify-between">
                      <label className="text-xs font-bold uppercase tracking-wider text-slate-700">
                        {param.label}
                      </label>
                    </div>
                    {param.param_type === "choice" ? (
                      <select
                        value={strategyParams[param.name] ?? ""}
                        onChange={(e) => setStrategyParams((prev) => ({ ...prev, [param.name]: e.target.value }))}
                        className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-bold text-slate-900"
                      >
                        {(param.choices ?? []).map((ch) => (
                          <option key={ch} value={ch}>
                            {ch}
                          </option>
                        ))}
                      </select>
                    ) : (
                      <div className="relative">
                        <input
                          type="number"
                          value={strategyParams[param.name] ?? ""}
                          onChange={(e) => setStrategyParams((prev) => ({ ...prev, [param.name]: e.target.value }))}
                          className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-bold text-slate-900"
                        />
                        {param.param_type === "percentage" && (
                          <span className="absolute right-4 top-3 text-sm text-slate-400 font-semibold">%</span>
                        )}
                      </div>
                    )}
                    {param.description && <p className="text-[11px] text-slate-500">{param.description}</p>}
                  </div>
                ))}
              </div>

              {/* Scenario Label & Recalculate Trigger */}
              <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 pt-4 border-t border-slate-100">
                <div className="sm:max-w-md w-full">
                  <label className="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1">
                    Label this Scenario
                  </label>
                  <input
                    type="text"
                    value={scenarioName}
                    onChange={(e) => setScenarioName(e.target.value)}
                    placeholder="e.g. 10% Step-Up with High Surplus"
                    className="w-full rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-800"
                  />
                </div>
                <div className="sm:self-end">
                  <InvestorButton
                    className="w-full sm:w-auto px-8 py-3 text-sm font-bold shadow-md"
                    onClick={() => void handleRecalculate()}
                    disabled={working}
                  >
                    {working ? "Calculating Outcomes…" : "Recalculate & Compare Outcomes →"}
                  </InvestorButton>
                </div>
              </div>
            </section>

            {/* PILLAR 3: THE THREE ANALYTICAL ENGINES (SCENARIO + PROBABILITY + OPTIMIZATION) */}
            <section className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-bold text-slate-900">
                    Pillar 3: Analytical Engines Output
                  </h3>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Observing:{" "}
                    <strong className="text-slate-800">
                      {activeScenario?.scenario_name || "Custom Scenario"}
                    </strong>{" "}
                    vs Baseline Strategy
                  </p>
                </div>
                {activeScenario?.is_investor_modified && (
                  <span className="rounded-full bg-navy-100 px-3 py-1 text-xs font-bold text-navy-800">
                    Custom Investor Scenario
                  </span>
                )}
              </div>

              {/* 3A. Scenario Delta Comparison */}
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-2xs">
                  <div className="flex items-center justify-between text-xs text-slate-500">
                    <span>Target Corpus</span>
                    <span className="font-semibold text-slate-700">Cause & Effect</span>
                  </div>
                  <p className="mt-2 text-2xl font-black text-slate-900">{displayCurrency(activeTarget)}</p>
                  <div className="mt-2 text-xs">
                    {deltaTarget !== 0 ? (
                      <span className={deltaTarget > 0 ? "font-semibold text-rose-600" : "font-semibold text-emerald-600"}>
                        {deltaTarget > 0 ? `+${displayCurrency(deltaTarget)}` : `-${displayCurrency(Math.abs(deltaTarget))}`} vs Baseline
                      </span>
                    ) : (
                      <span className="text-slate-400">Matches baseline target</span>
                    )}
                  </div>
                </div>

                <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-2xs">
                  <div className="flex items-center justify-between text-xs text-slate-500">
                    <span>Projected Total Wealth</span>
                    <span className="font-semibold text-slate-700">Accumulation</span>
                  </div>
                  <p className="mt-2 text-2xl font-black text-slate-900">
                    {displayCurrency(activeMetrics.projected_total_resources)}
                  </p>
                  <p className="mt-2 text-xs text-slate-500">
                    Funded ratio: <strong>{displayPct(activeMetrics.funded_ratio)}</strong>
                  </p>
                </div>

                <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-2xs">
                  <div className="flex items-center justify-between text-xs text-slate-500">
                    <span>Funding Gap</span>
                    <span className="font-semibold text-slate-700">Residual</span>
                  </div>
                  <p className="mt-2 text-2xl font-black text-rose-600">{displayCurrency(activeGap)}</p>
                  <div className="mt-2 text-xs">
                    {deltaGap > 0 ? (
                      <span className="font-bold text-emerald-600">
                        ↓ Reduced gap by {displayCurrency(deltaGap)}
                      </span>
                    ) : deltaGap < 0 ? (
                      <span className="font-bold text-rose-600">
                        ↑ Gap expanded by {displayCurrency(Math.abs(deltaGap))}
                      </span>
                    ) : (
                      <span className="text-slate-400">Equal to baseline gap</span>
                    )}
                  </div>
                </div>

                {/* 3B. Probability Engine */}
                <div className={`rounded-2xl border ${probStyle.border} ${probStyle.bg} p-5 shadow-2xs`}>
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-600">Probability Engine</span>
                    <span className={`flex h-2.5 w-2.5 rounded-full ${probStyle.dot}`} />
                  </div>
                  <p className={`mt-2 text-2xl font-black ${probStyle.text}`}>
                    {typeof activeMetrics.probability_of_success === "number"
                      ? `${Math.round(activeMetrics.probability_of_success * 100)}%`
                      : "90%+"}
                  </p>
                  <p className={`mt-1 text-xs font-bold ${probStyle.text}`}>
                    {probStyle.label}
                  </p>
                  <p className="mt-1 text-[10px] text-slate-500">
                    Deterministic hurdle & funded-ratio model
                  </p>
                </div>
              </div>

              {/* 3C. Optimization & Explainability (Cause-and-Effect Trade-Off Matrix) */}
              <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
                <div>
                  <h4 className="font-bold text-slate-900">
                    Cause-and-Effect Trade-Off Matrix & Explainability
                  </h4>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Financial choices involve trade-offs. The engines explicitly surface both the gains and the sacrifices.
                  </p>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  {/* Gains (Pros) */}
                  <div className="rounded-2xl border border-emerald-100 bg-emerald-50/40 p-4 space-y-2.5">
                    <div className="flex items-center gap-2">
                      <span className="flex h-5 w-5 items-center justify-center rounded-full bg-emerald-600 text-white text-xs font-bold">
                        ✓
                      </span>
                      <h5 className="text-xs font-bold uppercase tracking-wider text-emerald-900">
                        What Improves (Gains)
                      </h5>
                    </div>
                    {activePros.length > 0 ? (
                      <ul className="space-y-1.5 text-xs text-emerald-950 font-medium">
                        {activePros.map((pro, idx) => (
                          <li key={idx} className="flex items-start gap-2">
                            <span className="text-emerald-500 mt-0.5">•</span>
                            <span>{pro}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-xs text-slate-500 italic">
                        Scenario maintains baseline funding performance without additional gains.
                      </p>
                    )}
                  </div>

                  {/* Sacrifices / Costs (Cons) */}
                  <div className="rounded-2xl border border-amber-100 bg-amber-50/40 p-4 space-y-2.5">
                    <div className="flex items-center gap-2">
                      <span className="flex h-5 w-5 items-center justify-center rounded-full bg-amber-600 text-white text-xs font-bold">
                        !
                      </span>
                      <h5 className="text-xs font-bold uppercase tracking-wider text-amber-900">
                        What Sacrifices / Risks Emerge (Costs)
                      </h5>
                    </div>
                    {activeCons.length > 0 ? (
                      <ul className="space-y-1.5 text-xs text-amber-950 font-medium">
                        {activeCons.map((con, idx) => (
                          <li key={idx} className="flex items-start gap-2">
                            <span className="text-amber-500 mt-0.5">•</span>
                            <span>{con}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-xs text-slate-500 italic">
                        No immediate cash-flow sacrifice or timeline deferral detected.
                      </p>
                    )}
                  </div>
                </div>

                {/* Constraint Violations if any */}
                {activeViolations.length > 0 && (
                  <div className="rounded-2xl border border-rose-200 bg-rose-50/80 p-4 space-y-2 text-rose-950">
                    <p className="text-xs font-bold uppercase tracking-wider text-rose-800">
                      Constraint Warning Details
                    </p>
                    {activeViolations.map((v, i) => (
                      <p key={i} className="text-xs">
                        ⚠️ {v.message}
                      </p>
                    ))}
                  </div>
                )}
              </div>
            </section>

            {/* PILLAR 4: FINAL INVESTOR DECISION & ACTION PLAN LOCK */}
            <section className="rounded-3xl border-2 border-navy-900 bg-linear-to-r from-navy-950 to-slate-900 p-6 sm:p-8 text-white shadow-xl">
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
                <div className="space-y-2 max-w-2xl">
                  <div className="inline-flex items-center gap-2 rounded-full bg-emerald-500/20 px-3 py-1 text-xs font-bold text-emerald-300 border border-emerald-500/30">
                    <span>Pillar 4</span> · <span>The Investor Decides</span>
                  </div>
                  <h3 className="text-2xl font-black tracking-tight text-white">
                    Lock This Decision & Proceed to Action Plan
                  </h3>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    By locking this decision, Planvesto commits this scenario ({activeScenario?.scenario_name}) as your
                    authoritative strategy execution baseline. Your action items, SIP schedules, asset allocations, and
                    annual step-up triggers will be generated in Report.
                  </p>
                </div>

                <div className="flex flex-col sm:flex-row lg:flex-col gap-3 shrink-0">
                  <button
                    type="button"
                    onClick={() => void handleLockDecision()}
                    disabled={locking || !activeScenario}
                    className="flex items-center justify-center gap-2 rounded-xl bg-emerald-500 px-6 py-4 text-sm font-black text-slate-950 shadow-lg hover:bg-emerald-400 active:scale-[0.99] transition-all disabled:opacity-50 cursor-pointer"
                  >
                    {locking ? "Finalizing Implementation…" : "Finalize Implementation →"}
                  </button>
                  {run.selected_strategy_version_id && (
                    <>
                      <Link
                        href={`/investor/goal-report?goalId=${encodeURIComponent(goalId)}&strategyVersionId=${encodeURIComponent(run.selected_strategy_version_id)}`}
                        className="flex items-center justify-center gap-1.5 rounded-xl border border-white/20 bg-white/10 px-5 py-3 text-xs font-semibold text-white hover:bg-white/20 transition-all text-center"
                      >
                        View Report ↗
                      </Link>
                      <button
                        type="button"
                        onClick={async () => {
                          try {
                            const blob = await downloadGoalStrategyReportPdfByStrategyVersion(getPlanningUnitId()!, run.selected_strategy_version_id!);
                            const url = URL.createObjectURL(blob);
                            const anchor = document.createElement("a");
                            anchor.href = url;
                            anchor.download = `goal-strategy-report-${run.selected_strategy_version_id}.pdf`;
                            anchor.click();
                            URL.revokeObjectURL(url);
                          } catch (err) {
                            setError(err instanceof Error ? err.message : "Unable to download the report.");
                          }
                        }}
                        className="flex items-center justify-center gap-1.5 rounded-xl border border-white/20 bg-white/10 px-5 py-3 text-xs font-semibold text-white hover:bg-white/20 transition-all text-center"
                      >
                        Download Report ↓
                      </button>
                      <Link
                        href={`/investor/action-plan?goalId=${encodeURIComponent(goalId)}&strategyVersionId=${encodeURIComponent(run.selected_strategy_version_id)}`}
                        className="flex items-center justify-center gap-1.5 rounded-xl border border-white/20 bg-white/10 px-5 py-3 text-xs font-semibold text-white hover:bg-white/20 transition-all text-center"
                      >
                        Action Plan →
                      </Link>
                    </>
                  )}
                </div>
              </div>
            </section>

            {/* PREVIOUSLY TESTED SCENARIOS SHELF */}
            {customScenarios.length > 0 && (
              <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-base font-bold text-slate-900">Your Tested Scenarios</h4>
                    <p className="text-xs text-slate-500">
                      Click any scenario below to activate, review its trade-offs, or lock it into your Action Plan.
                    </p>
                  </div>
                  <span className="text-xs font-semibold text-slate-400">
                    {customScenarios.length} {customScenarios.length === 1 ? "scenario" : "scenarios"} tested
                  </span>
                </div>

                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {customScenarios.map((scen) => {
                    const isSelected = activeScenario?.scenario_id === scen.scenario_id;
                    const m = scen.metrics;
                    return (
                      <div
                        key={scen.scenario_id}
                        onClick={() => setActiveScenarioId(scen.scenario_id)}
                        className={`cursor-pointer rounded-2xl border p-4 transition-all ${
                          isSelected
                            ? "border-navy-900 bg-navy-50/30 ring-2 ring-navy-900/10 shadow-sm"
                            : "border-slate-200 bg-slate-50/50 hover:border-slate-300 hover:bg-white"
                        }`}
                      >
                        <div className="flex items-start justify-between gap-2">
                          <h5 className="font-bold text-sm text-slate-900 line-clamp-1">
                            {scen.scenario_name}
                          </h5>
                          {isSelected && (
                            <span className="rounded-full bg-navy-900 px-2 py-0.5 text-[10px] font-bold text-white shrink-0">
                              Active
                            </span>
                          )}
                        </div>
                        <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
                          <div>
                            <span className="text-slate-400 block text-[10px]">Monthly SIP</span>
                            <span className="font-bold text-slate-800">
                              {displayCurrency(scen.funding_structure?.starting_monthly_contribution ?? m.effective_monthly_contribution)}
                            </span>
                          </div>
                          <div>
                            <span className="text-slate-400 block text-[10px]">Step-Up</span>
                            <span className="font-bold text-slate-800">
                              {String(scen.funding_structure?.annual_step_up_pct ?? "0")}%
                            </span>
                          </div>
                          <div>
                            <span className="text-slate-400 block text-[10px]">Funding Gap</span>
                            <span className="font-bold text-rose-600">
                              {displayCurrency(m.funding_gap)}
                            </span>
                          </div>
                          <div>
                            <span className="text-slate-400 block text-[10px]">Probability</span>
                            <span className="font-bold text-emerald-700">
                              {typeof m.probability_of_success === "number"
                                ? `${Math.round(m.probability_of_success * 100)}%`
                                : "High"}
                            </span>
                          </div>
                        </div>
                        <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px]">
                          <span className="text-slate-500 font-medium">Click to inspect</span>
                          <span className="text-navy-900 font-bold">Select →</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </section>
            )}
          </>
        )}
      </div>
    </main>
  );
}

export default function StrategyScenariosPage() {
  return (
    <Suspense
      fallback={
        <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
          <div className="mx-auto max-w-6xl space-y-6">
            <div className="h-10 w-80 animate-pulse rounded-xl bg-slate-200" />
            <div className="h-96 animate-pulse rounded-3xl bg-white" />
          </div>
        </main>
      }
    >
      <StrategyScenariosContent />
    </Suspense>
  );
}
