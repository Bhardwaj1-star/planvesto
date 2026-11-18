"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import StrategyWorkflowNav from "../../../components/StrategyWorkflowNav";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorButton, InvestorStatus } from "../../../components/InvestorUI";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";
import { apiRequest } from "../../../lib/api/client";
import { buildStrategy, getStrategyRunHistory, getPlanningUnitId, type StrategyRun } from "../../../lib/api/strategy";
import { getLatestDefinedGoal } from "../../../lib/api/goals";
import type { DefinedGoal } from "../../../lib/onboarding/goals/types";

// Chapter 11 Strategy Builder Components
import {
  StepIndicator,
  YearlyProjectionTable,
  FundingPathCard,
  FundingPathComparison,
  FinancingInputPanel,
} from "../../../components/strategy";
import {
  assessGoalFunding,
  type GoalFundingAssessment,
  type FinancingOption,
} from "../../../lib/api/goal-funding";

type PlanningBasket = { id: string; name: string; goalIds: string[] };
const BASKET_STORAGE_KEY = "planvesto:planning-baskets";

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
  const router = useRouter();
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
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(false);

  // Chapter 11 Pipeline States
  const [currentStep, setCurrentStep] = useState<number>(4);
  const [completedSteps, setCompletedSteps] = useState<number[]>([1, 2, 3]);
  const [fundingAssessment, setFundingAssessment] = useState<GoalFundingAssessment | null>(null);
  const [assessingFunding, setAssessingFunding] = useState<boolean>(false);
  const [activeFundingView, setActiveFundingView] = useState<"self_money" | "financing" | "both">("both");

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
    if (!selectedGoalId) {
      setGoalPreview(null);
      setRun(null);
      setHistory([]);
      setFundingAssessment(null);
      return;
    }

    let active = true;
    (async () => {
      setWorking(true);
      setError(null);
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");

        let preview: DefinedGoal | null = null;
        try {
          preview = await apiRequest<DefinedGoal>(`/api/goals/${selectedGoalId}/defined/latest?planning_unit_id=${planningUnitId}`);
        } catch {
          preview = null;
        }

        const currentRun = await buildStrategy(planningUnitId, selectedGoalId);
        if (!active) return;

        setGoalPreview(preview);
        setRun(currentRun);

        const recommendedStrategyId = currentRun.recommendation.recommended_strategy_id || currentRun.rankings[0]?.strategy_id || "";
        setSelectedStrategyId(recommendedStrategyId);
        const recommendedScenarioId = currentRun.recommendation.recommended_scenario_id || currentRun.rankings.find((item) => item.strategy_id === recommendedStrategyId)?.scenario_id || "";
        setSelectedScenarioId(recommendedScenarioId);
        setSelectedArchitectureId(resolveArchitectureId(currentRun, recommendedStrategyId));

        const historyRuns = await getStrategyRunHistory(planningUnitId, selectedGoalId);
        if (active) setHistory(historyRuns);

        // Compute Chapter 11 Goal Funding Assessment (Step 4 Projections & Comparison)
        const targetAmount = preview?.future_target || preview?.today_cost || 2500000;
        const horizonYears = preview?.duration_years || 10;
        const monthlySip = preview?.required_monthly_contribution || 15000;
        const mappedAssets = preview?.projected_mapped_asset_value || 0;
        const surplus = Number(preview?.available_monthly_surplus) || 30000;

        try {
          const defaultFinancing: FinancingOption = {
            down_payment: Math.round(targetAmount * 0.2),
            loan_annual_interest_rate_pct: 8.5,
            loan_tenure_months: horizonYears * 12,
          };

          const assessment = await assessGoalFunding(planningUnitId, selectedGoalId, {
            target_amount: targetAmount,
            horizon_years: horizonYears,
            start_calendar_year: new Date().getFullYear(),
            initial_allocated_assets: mappedAssets,
            required_monthly_sip: monthlySip,
            expected_annual_return_pct: 12.0,
            available_monthly_surplus: surplus,
            financing_option: defaultFinancing,
          });

          if (active) {
            setFundingAssessment(assessment);
            setCompletedSteps([1, 2, 3, 4, 7]);
            setCurrentStep(4);
          }
        } catch {
          // Fallback gracefully if assess endpoint times out
        }
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load Strategy Builder.");
      } finally {
        if (active) setWorking(false);
      }
    })();

    return () => { active = false; };
  }, [selectedGoalId]);

  const handleCustomFinancingAssess = async (option: FinancingOption) => {
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId || !selectedGoalId) return;

    setAssessingFunding(true);
    setError(null);
    try {
      const targetAmount = goalPreview?.future_target || goalPreview?.today_cost || 2500000;
      const horizonYears = goalPreview?.duration_years || 10;
      const monthlySip = goalPreview?.required_monthly_contribution || 15000;
      const mappedAssets = goalPreview?.projected_mapped_asset_value || 0;
      const surplus = Number(goalPreview?.available_monthly_surplus) || 30000;

      const assessment = await assessGoalFunding(planningUnitId, selectedGoalId, {
        target_amount: targetAmount,
        horizon_years: horizonYears,
        start_calendar_year: new Date().getFullYear(),
        initial_allocated_assets: mappedAssets,
        required_monthly_sip: monthlySip,
        expected_annual_return_pct: 12.0,
        available_monthly_surplus: surplus,
        financing_option: option,
      });

      setFundingAssessment(assessment);
      setSuccessMessage("Financing parameters recalculated successfully.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to assess financing scenario.");
    } finally {
      setAssessingFunding(false);
    }
  };

  const selectedStrategy = useMemo(
    () => run?.applicable_strategies.find((s) => s.strategy_id === selectedStrategyId) ?? null,
    [run, selectedStrategyId]
  );
  const scenarios = useMemo(
    () => run?.scenarios.filter((s) => s.strategy_id === selectedStrategyId) ?? [],
    [run, selectedStrategyId]
  );
  const selectedScenario = scenarios.find((s) => s.scenario_id === selectedScenarioId) ?? null;

  const displayedRankings = useMemo(() => {
    if (!run) return [];
    const ranked = [...run.rankings]
      .sort((a, b) => a.rank - b.rank)
      .filter((ranking, index, items) => items.findIndex((item) => item.strategy_id === ranking.strategy_id) === index);
    const recommendedId = run.recommendation.recommended_strategy_id;
    const recommended = ranked.find((ranking) => ranking.strategy_id === recommendedId);
    const alternatives = ranked.filter((ranking) => ranking.strategy_id !== recommendedId);
    return (recommended ? [recommended, ...alternatives] : ranked).slice(0, 2);
  }, [run]);

  const execute = async (operation: () => Promise<StrategyRun>, successMsg?: string) => {
    setWorking(true);
    setError(null);
    setSuccessMessage(null);
    try {
      const next = await operation();
      setRun(next);
      const nextStrategyId = next.recommendation.recommended_strategy_id || next.rankings[0]?.strategy_id || "";
      setSelectedStrategyId(nextStrategyId);
      setSelectedScenarioId(next.recommendation.recommended_scenario_id || next.rankings.find((item) => item.strategy_id === nextStrategyId)?.scenario_id || "");
      setSelectedArchitectureId(resolveArchitectureId(next, nextStrategyId));
      const planningUnitId = getPlanningUnitId();
      if (planningUnitId && selectedGoalId) setHistory(await getStrategyRunHistory(planningUnitId, selectedGoalId));
      if (successMsg) setSuccessMessage(successMsg);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Strategy operation failed.");
    } finally {
      setWorking(false);
    }
  };

  const handleBuild = () => {
    const planningUnitId = getPlanningUnitId();
    if (planningUnitId && selectedGoalId) void execute(() => buildStrategy(planningUnitId, selectedGoalId));
  };

  const handleSelect = () => {
    setError(null);
    setSuccessMessage(null);

    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId) {
      setError("Planning unit is missing. Please refresh the page and try again.");
      return;
    }
    if (!run?.strategy_run_id || !selectedGoalId || !selectedStrategyId) {
      setError("Select a strategy before planning its implementation.");
      return;
    }

    const architecture = run.architectures.find(
      (item) => item.primary_strategy_id === selectedStrategyId,
    );
    const scenario = run.scenarios.find(
      (item) => item.strategy_id === selectedStrategyId && item.scenario_id === selectedScenarioId,
    );
    if (!architecture || !scenario) {
      setError("The selected strategy architecture is incomplete. Please select it again.");
      return;
    }

    router.push(
      `/investor/strategy-scenarios?goalId=${encodeURIComponent(selectedGoalId)}&strategyRunId=${encodeURIComponent(run.strategy_run_id)}&strategyId=${encodeURIComponent(selectedStrategyId)}&scenarioId=${encodeURIComponent(selectedScenarioId)}&architectureId=${encodeURIComponent(architecture.architecture_id)}&goalVersion=${encodeURIComponent(String(run.defined_goal_version))}`,
    );
  };

  if (loading) {
    return (
      <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
        <div className="mx-auto max-w-6xl space-y-6">
          <div className="h-9 w-64 animate-pulse rounded-xl bg-slate-200" />
          <div className="h-96 animate-pulse rounded-3xl bg-white" />
        </div>
      </main>
    );
  }

  if (!goals.length) {
    return (
      <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
        <div className="mx-auto max-w-2xl rounded-3xl border border-slate-200 bg-white p-10 text-center">
          <h1 className="text-2xl font-extrabold text-slate-900">No goals available</h1>
          <p className="mt-2 text-sm text-slate-500">Define a goal first to build its funding strategy.</p>
          <Link href="/investor/goal-planner" className="mt-6 inline-flex rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white">
            Open Goal Planner
          </Link>
        </div>
      </main>
    );
  }

  const selfMoney = fundingAssessment?.self_money_path;
  const financing = fundingAssessment?.financing_path;
  const comparison = fundingAssessment?.comparison_matrix;

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
      <InvestorHeader
        eyebrow="Decide"
        title="Strategy Builder"
        description="Chapter 11 Goal Funding Strategy plans how and when a specific goal will be funded across Self Money and Financing paths."
      >
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
        <StrategyWorkflowNav />
        {error && <InvestorStatus tone="error">{error}</InvestorStatus>}
        {successMessage && <InvestorStatus tone="success">{successMessage}</InvestorStatus>}

        {/* Goal Selector */}
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <label className="block flex-1">
              <span className="text-sm font-bold text-slate-700">Goal / Planning Basket</span>
              <select value={selectedTargetKey} onChange={(e) => handleTargetChange(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm">
                <option value="">Select goal or planning basket</option>
                <optgroup label="Goals">
                  {goals.map((g) => <option key={g.id} value={g.id}>{g.name}</option>)}
                </optgroup>
                {baskets.length > 0 && (
                  <optgroup label="Planning Baskets">
                    {baskets.map((basket) => <option key={basket.id} value={`basket:${basket.id}`}>🧺 {basket.name} · {basket.goalIds.length} goals</option>)}
                  </optgroup>
                )}
              </select>
            </label>
            <InvestorButton onClick={handleBuild} disabled={working || !selectedGoalId}>
              {working ? "Working…" : run ? "Rebuild Strategy Run" : "Build Strategy"}
            </InvestorButton>
          </div>

          {selectedBasket && (
            <div className="mt-4 rounded-2xl border border-teal-200 bg-teal-50/60 p-4">
              <div className="flex items-center gap-2">
                <span className="text-lg">🧺</span>
                <div>
                  <p className="text-sm font-extrabold text-teal-900">{selectedBasket.name}</p>
                  <p className="text-xs text-teal-700">{selectedBasket.goalIds.length} goals in this planning basket</p>
                </div>
              </div>
              <p className="mt-3 text-xs leading-5 text-teal-800">
                This basket is selected as a planning target. Multi-goal strategy will execute jointly.
              </p>
            </div>
          )}

          {run && (
            <div className="mt-4 flex flex-wrap gap-3 text-xs text-slate-500">
              <span className="rounded-full bg-slate-100 px-3 py-1 font-semibold">Run v{run.run_version}</span>
              <span className="rounded-full bg-slate-100 px-3 py-1 font-semibold">Goal v{run.defined_goal_version}</span>
              <span className="rounded-full bg-slate-100 px-3 py-1 font-semibold">Status: {run.status}</span>
              {run.selected_strategy_version_id && (
                <Link href="/investor/reports" className="rounded-full border border-teal-200 bg-teal-50/50 px-3 py-1 font-semibold text-teal-700 hover:bg-teal-50">
                  View Reports
                </Link>
              )}
              <Link href="/investor/strategy-scenarios" className="rounded-full border border-slate-200 px-3 py-1 font-semibold hover:bg-slate-50">
                Custom Scenarios
              </Link>
              <Link href="/investor/strategy-history" className="rounded-full border border-slate-200 px-3 py-1 font-semibold hover:bg-slate-50">
                Strategy History
              </Link>
            </div>
          )}
        </section>

        {/* Chapter 11 Pipeline Progress Tracker */}
        <StepIndicator
          currentStep={currentStep}
          completedSteps={completedSteps}
          onStepClick={(s) => setCurrentStep(s)}
        />

        {/* Goal Calculation & Feasibility Handoff (Chapter 10 -> Chapter 11) */}
        {goalPreview && (
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-teal-700">Chapter 10 Handoff (§11.2)</span>
                <h2 className="text-lg font-bold text-slate-900">Goal Requirement &amp; Feasibility Data</h2>
              </div>
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
                Target: {String(goalPreview.target_month).padStart(2, "0")}/{goalPreview.target_year} ({goalPreview.duration_years || 10} yrs)
              </span>
            </div>

            <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {[
                ["Today’s Cost", formatINR(goalPreview.today_cost)],
                ["Inflation Rate", `${((goalPreview.inflation_rate || 0.06) * 100).toFixed(1)}%`],
                ["Target Corpus (§10.2)", formatINR(goalPreview.future_target)],
                ["Funding Gap", formatINR(goalPreview.funding_gap)],
              ].map(([label, value]) => (
                <div key={label} className="rounded-2xl bg-slate-50 p-4">
                  <p className="text-xs font-bold uppercase tracking-wide text-slate-400">{label}</p>
                  <p className="mt-1 text-lg font-extrabold text-slate-900">{value}</p>
                </div>
              ))}
            </div>

            <div className="mt-4 flex flex-wrap gap-4 text-xs text-slate-600 bg-slate-50/70 p-3.5 rounded-2xl border border-slate-100">
              <span>Mapped Assets: <strong className="text-slate-800">{formatINR(goalPreview.projected_mapped_asset_value)}</strong></span>
              <span className="text-slate-300">|</span>
              <span>Required Monthly SIP: <strong className="text-slate-800">{formatINR(goalPreview.required_monthly_contribution)}</strong></span>
              <span className="text-slate-300">|</span>
              <span>Investable Monthly Surplus: <strong className="text-slate-800">{formatINR(Number(goalPreview.available_monthly_surplus) || 30000)}</strong></span>
              <span className="text-slate-300">|</span>
              <span>Funding Feasibility: <strong className="text-teal-700 font-bold">{goalPreview.funding_status || "Evaluated"}</strong></span>
            </div>
          </section>
        )}

        {/* Steps 1-3 Mapped Assets Disposition Notice */}
        {goalPreview && (
          <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-teal-50 text-teal-700 text-base font-bold">
                  💼
                </span>
                <div>
                  <h3 className="text-sm font-extrabold text-slate-900">
                    Steps 1–3: Mapped Assets &amp; Self-Money Requirement
                  </h3>
                  <p className="text-xs text-slate-500">
                    {goalPreview.projected_mapped_asset_value > 0
                      ? `Found ${formatINR(goalPreview.projected_mapped_asset_value)} in mapped assets committed to this goal.`
                      : "No dedicated assets mapped to this goal. Commencing directly at Step 4 Projection."}
                  </p>
                </div>
              </div>
              <div className="text-xs text-slate-500 bg-slate-50 border border-slate-100 px-3 py-1.5 rounded-xl font-medium">
                Rule: No automatic liquidation without explicit confirmation (§11.4 Step 2)
              </div>
            </div>
          </section>
        )}

        {/* FUNDING PATH ASSESSMENT (STEP 4: PROJECTIONS & COMPARISON) */}
        {selfMoney && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-3">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
                  Step 4 — Goal Funding Projection (Year-by-Year)
                </span>
                <h2 className="text-xl font-extrabold text-slate-900">
                  Funding Trajectory &amp; Financing Simulation
                </h2>
              </div>

              {/* View Switcher Pills */}
              <div className="flex items-center gap-1 rounded-xl bg-slate-100 p-1 text-xs font-bold">
                <button
                  type="button"
                  onClick={() => setActiveFundingView("both")}
                  className={`rounded-lg px-3 py-1.5 transition ${
                    activeFundingView === "both" ? "bg-white text-slate-900 shadow-xs" : "text-slate-500 hover:text-slate-900"
                  }`}
                >
                  All Views
                </button>
                <button
                  type="button"
                  onClick={() => setActiveFundingView("self_money")}
                  className={`rounded-lg px-3 py-1.5 transition ${
                    activeFundingView === "self_money" ? "bg-white text-slate-900 shadow-xs" : "text-slate-500 hover:text-slate-900"
                  }`}
                >
                  Self Money Path
                </button>
                <button
                  type="button"
                  onClick={() => setActiveFundingView("financing")}
                  className={`rounded-lg px-3 py-1.5 transition ${
                    activeFundingView === "financing" ? "bg-white text-slate-900 shadow-xs" : "text-slate-500 hover:text-slate-900"
                  }`}
                >
                  Financing Path
                </button>
              </div>
            </div>

            {/* Path 1: Self Money Card */}
            {(activeFundingView === "both" || activeFundingView === "self_money") && (
              <div className="space-y-4">
                <FundingPathCard
                  type="self_money"
                  totalContributions={selfMoney.total_own_contributions}
                  projectedCorpus={selfMoney.projected_corpus_at_goal}
                  goalAmountFunded={selfMoney.goal_amount_funded}
                  remainingCorpus={selfMoney.remaining_corpus}
                  isFullyFunded={selfMoney.is_fully_funded}
                  explanation={selfMoney.explanation}
                  selected={selectedStrategyId === "path_self_money"}
                  onSelect={() => setSelectedStrategyId("path_self_money")}
                />

                {/* Step 4 Year-by-Year Table (Self Money) */}
                <YearlyProjectionTable
                  projections={selfMoney.yearly_projections}
                  title="Self Money: Year-by-Year Funding Trajectory (§11.4 Step 4)"
                  description="Yearly opening balances, discipline SIP contributions, compounding returns, and target payout."
                  showFinancingColumns={false}
                />
              </div>
            )}

            {/* Financing Sandbox Input Panel */}
            <FinancingInputPanel
              goalTargetAmount={goalPreview?.future_target || goalPreview?.today_cost || 2500000}
              availableMonthlySurplus={Number(goalPreview?.available_monthly_surplus) || 30000}
              onAssess={handleCustomFinancingAssess}
              loading={assessingFunding}
            />

            {/* Path 2: Financing Path Card & Table */}
            {financing && (activeFundingView === "both" || activeFundingView === "financing") && (
              <div className="space-y-4">
                <FundingPathCard
                  type="financing"
                  totalContributions={financing.down_payment + financing.total_repayment}
                  projectedCorpus={financing.projected_corpus_at_goal}
                  goalAmountFunded={financing.goal_amount_funded}
                  remainingCorpus={financing.remaining_corpus}
                  isFullyFunded={financing.is_fully_funded}
                  explanation={financing.explanation}
                  financingDetails={{
                    downPayment: financing.down_payment,
                    financingAmount: financing.financing_amount,
                    monthlyEmi: financing.monthly_emi,
                    totalInterestCost: financing.total_interest_cost,
                    totalRepayment: financing.total_repayment,
                    emiAffordable: financing.emi_affordable,
                    loanTenureMonths: financing.loan_tenure_months,
                    interestRatePct: financing.loan_interest_rate_pct,
                  }}
                  selected={selectedStrategyId === "path_self_money_financing"}
                  onSelect={() => setSelectedStrategyId("path_self_money_financing")}
                />

                <YearlyProjectionTable
                  projections={financing.yearly_projections}
                  title="Self Money + Financing: Year-by-Year Debt & Payout Trajectory (§11.6)"
                  description="Yearly loan disbursements, monthly EMI obligations, and post-goal repayment cash flows."
                  showFinancingColumns={true}
                />
              </div>
            )}

            {/* Step 7 & §11.7 Comparison Matrix */}
            {comparison && financing && (
              <FundingPathComparison
                selfMoneyPath={selfMoney}
                financingPath={financing}
                comparisonMatrix={comparison}
                selectedPath={selectedStrategyId === "path_self_money_financing" ? "financing" : "self_money"}
                onSelectPath={(path) => {
                  setSelectedStrategyId(path === "self_money" ? "path_self_money" : "path_self_money_financing");
                }}
              />
            )}
          </div>
        )}

        {/* Existing Strategy Architectures & Recommendations */}
        {!run ? (
          <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
            <h2 className="text-xl font-bold">{selectedBasket ? "Basket selected" : "No Strategy Run yet"}</h2>
            <p className="mt-2 text-sm text-slate-500">
              {selectedBasket
                ? "Select an individual goal to build its Strategy Run."
                : "Build the Strategy Run after reviewing the goal calculation."}
            </p>
          </section>
        ) : (
          <>
            <section className="space-y-4">
              <div>
                <h2 className="text-lg font-bold">Strategy Architectures</h2>
                <p className="text-sm text-slate-500">Applicable architectures evaluated for this goal.</p>
              </div>
              <div className="grid gap-5 lg:grid-cols-2">
                {displayedRankings.map((ranking) => (
                  <article
                    key={`${ranking.strategy_id}-${ranking.scenario_id}`}
                    className={`rounded-3xl border bg-white p-6 shadow-sm transition-all ${
                      selectedStrategyId === ranking.strategy_id && selectedScenarioId === ranking.scenario_id
                        ? "border-teal-500 ring-2 ring-teal-100"
                        : "border-slate-200"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <p className="text-xs font-bold uppercase tracking-wide text-slate-400">
                          {ranking.strategy_id === run.recommendation.recommended_strategy_id
                            ? "Recommended Architecture"
                            : "Alternative Architecture"}
                        </p>
                        <h3 className="mt-1 text-xl font-extrabold">{ranking.strategy_name}</h3>
                        <p className="mt-1 text-sm text-slate-500">{ranking.scenario_name}</p>
                      </div>
                      {ranking.strategy_id === run.recommendation.recommended_strategy_id && (
                        <span className="rounded-full bg-teal-50 px-3 py-1 text-xs font-bold text-teal-700">
                          Recommended
                        </span>
                      )}
                    </div>

                    <p className="mt-4 text-sm leading-6 text-slate-600">
                      {run.applicable_strategies.find((s) => s.strategy_id === ranking.strategy_id)?.description}
                    </p>

                    <div className="mt-4 space-y-2 text-xs text-slate-600">
                      {run.architectures.find((a) => a.primary_strategy_id === ranking.strategy_id)?.rationale?.length ? (
                        <div>
                          <b>Goal fit:</b>{" "}
                          {run.architectures.find((a) => a.primary_strategy_id === ranking.strategy_id)?.rationale.join("; ")}
                        </div>
                      ) : null}
                      <div>
                        <b>Feasibility:</b>{" "}
                        {run.architectures.find((a) => a.primary_strategy_id === ranking.strategy_id)?.feasibility_status}
                      </div>
                      {run.applicable_strategies.find((s) => s.strategy_id === ranking.strategy_id)?.trade_offs?.length ? (
                        <div>
                          <b>Trade-offs:</b>{" "}
                          {run.applicable_strategies.find((s) => s.strategy_id === ranking.strategy_id)?.trade_offs.join("; ")}
                        </div>
                      ) : null}
                    </div>

                    <div className="mt-5 flex gap-2">
                      {selectedStrategyId === ranking.strategy_id ? (
                        <button
                          type="button"
                          className="flex-1 rounded-xl bg-teal-600 px-4 py-3 text-sm font-bold text-white shadow-sm"
                        >
                          Selected
                        </button>
                      ) : (
                        <>
                          <button
                            type="button"
                            onClick={() => {
                              setSelectedStrategyId(ranking.strategy_id);
                              setSelectedScenarioId(ranking.scenario_id);
                              const architecture = run.architectures.find((a) => a.primary_strategy_id === ranking.strategy_id);
                              setSelectedArchitectureId(architecture?.architecture_id ?? "");
                            }}
                            className="flex-1 rounded-xl border border-teal-600 bg-white px-4 py-3 text-sm font-bold text-teal-700 hover:bg-teal-50"
                          >
                            Select Strategy
                          </button>
                          <button
                            type="button"
                            onClick={() => {
                              const recId = run.recommendation.recommended_strategy_id;
                              const otherId = displayedRankings.find((r) => r.strategy_id !== ranking.strategy_id)?.strategy_id || recId;
                              router.push(
                                `/investor/strategy-comparison?goalId=${encodeURIComponent(selectedGoalId)}&strategyRunId=${encodeURIComponent(run.strategy_run_id ?? "")}&recommendedStrategyId=${encodeURIComponent(otherId)}&alternativeStrategyId=${encodeURIComponent(ranking.strategy_id)}`,
                              );
                            }}
                            className="rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-bold text-slate-700 hover:bg-slate-50"
                          >
                            Compare
                          </button>
                        </>
                      )}
                    </div>
                  </article>
                ))}
              </div>
            </section>

            <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="text-lg font-bold">Recommendation</h2>
              <p className="mt-3 text-sm leading-6 text-slate-600">{run.recommendation.complete_reasoning}</p>
              <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-slate-600">
                {run.recommendation.short_reasons.map((reason, i) => (
                  <li key={i}>{reason}</li>
                ))}
              </ul>
              <p className="mt-4 text-xs font-bold uppercase tracking-wide text-slate-400">
                Feasibility: {run.recommendation.feasibility_status}
              </p>
            </section>

            {selectedStrategy && (
              <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <h2 className="text-lg font-bold">Selected Strategy: {selectedStrategy.name}</h2>
                    <p className="mt-1 text-sm text-slate-500">
                      Strategy selection is complete. Implementation parameters and what-if analysis happen next.
                    </p>
                  </div>
                  <InvestorButton onClick={handleSelect} disabled={working}>
                    Plan Your Implementation →
                  </InvestorButton>
                </div>
              </section>
            )}
          </>
        )}
      </div>
    </main>
  );
}
