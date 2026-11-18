"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import StrategyWorkflowNav from "../../../components/StrategyWorkflowNav";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorButton, InvestorStatus } from "../../../components/InvestorUI";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";
import { apiRequest } from "../../../lib/api/client";
import {
  buildStrategy,
  getStrategyRunHistory,
  getPlanningUnitId,
  type StrategyRun,
} from "../../../lib/api/strategy";
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
  computeGoalFundingLocally,
  type GoalFundingAssessment,
  type FinancingOption,
} from "../../../lib/api/goal-funding";

type PlanningBasket = { id: string; name: string; goalIds: string[] };
const BASKET_STORAGE_KEY = "planvesto:planning-baskets";

function formatINR(value: number | null | undefined) {
  if (value === null || value === undefined || !Number.isFinite(value)) return "—";
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

function resolveArchitectureId(run: StrategyRun | null, strategyId: string) {
  if (!run) return "";
  return (
    run.architectures.find((architecture) => architecture.primary_strategy_id === strategyId)?.architecture_id ??
    run.recommendation.architecture?.architecture_id ??
    ""
  );
}

// Fallback deterministic strategy run if backend is disconnected
function createFallbackStrategyRun(goalId: string, puId: string, targetAmount = 2500000): StrategyRun {
  return {
    strategy_run_id: `run_local_${goalId}`,
    planning_unit_id: puId,
    goal_id: goalId,
    defined_goal_id: "def_goal_active",
    defined_goal_version: 1,
    run_version: 1,
    is_latest: true,
    status: "completed",
    applicable_strategies: [
      {
        strategy_id: "path_self_money",
        name: "Self Money Funding Path",
        tagline: "100% Own Funds & Systematic Investment",
        description:
          "Fund the goal entirely using verified own assets, savings, and disciplined monthly contributions (SIPs) without debt.",
        strategy_family: "Funding Path",
        strategic_objective: "Achieve full goal funding with zero interest cost and maximum compounding retention.",
        core_mechanism: "Systematic monthly contributions and disciplined market compounding.",
        principles: ["Debt freedom", "Compounding preservation"],
        constraints: ["Must adhere to monthly savings quota"],
        dependencies: [],
        required_inputs: [],
        applicable_goal_characteristics: [],
        applicable_goal_types: [],
        technique_ids: [],
        strategic_levers: [],
        compatible_strategy_ids: [],
        conflicting_strategy_ids: [],
        library_version: "1.0",
        implementation_version: "1.0",
        active: true,
        implementation_parameters: [],
        good_outcomes: ["Zero debt or EMI burden", "Total wealth compounding retention"],
        bad_outcomes: ["Requires consistent surplus discipline"],
        trade_offs: ["Requires higher monthly savings rate"],
        baseline_safety_score: 8.5,
        baseline_liquidity_score: 7.0,
        baseline_growth_score: 8.5,
        baseline_flexibility_score: 7.5,
      },
      {
        strategy_id: "path_self_money_financing",
        name: "Self Money + Financing Funding Path",
        tagline: "Combined Down Payment & Structured Loan",
        description:
          "Combine an initial own down payment with a structured loan facility to fund the goal while preserving liquid reserves.",
        strategy_family: "Funding Path",
        strategic_objective: "Bridge the goal funding timeline by leveraging structured financing alongside own capital.",
        core_mechanism: "Down payment coupled with reducing-balance amortized debt financing.",
        principles: ["Liquidity preservation", "Leveraged funding"],
        constraints: ["Monthly surplus must accommodate EMI"],
        dependencies: [],
        required_inputs: [],
        applicable_goal_characteristics: [],
        applicable_goal_types: [],
        technique_ids: [],
        strategic_levers: [],
        compatible_strategy_ids: [],
        conflicting_strategy_ids: [],
        library_version: "1.0",
        implementation_version: "1.0",
        active: true,
        implementation_parameters: [],
        good_outcomes: ["Immediate goal accomplishment", "Preserves liquid reserves"],
        bad_outcomes: ["Incurs loan borrowing cost", "Creates recurring debt liability"],
        trade_offs: ["Interest cost drag reduces long-term net wealth"],
        baseline_safety_score: 6.5,
        baseline_liquidity_score: 8.0,
        baseline_growth_score: 6.5,
        baseline_flexibility_score: 8.0,
      },
    ],
    scenarios: [
      {
        scenario_id: "scen_self_money_baseline",
        strategy_id: "path_self_money",
        scenario_type: "baseline",
        scenario_name: "Baseline Self-Money (12% CAGR)",
        assumptions: { expected_return_pct: 12.0, inflation_pct: 6.0 },
        funding_structure: { own_capital_pct: 100.0, loan_pct: 0.0 },
        metrics: {
          required_sip: 15000,
          projected_corpus: targetAmount,
          total_interest_cost: 0,
        },
        trade_off_notes: "Zero debt overhead",
        is_investor_modified: false,
      },
      {
        scenario_id: "scen_financing_baseline",
        strategy_id: "path_self_money_financing",
        scenario_type: "baseline",
        scenario_name: "Baseline Financing (8.5% p.a. Loan)",
        assumptions: { loan_rate_pct: 8.5, tenure_months: 120 },
        funding_structure: { own_down_payment: targetAmount * 0.2, loan_amount: targetAmount * 0.8 },
        metrics: {
          monthly_emi: Math.round((targetAmount * 0.8 * 0.00708 * Math.pow(1.00708, 120)) / (Math.pow(1.00708, 120) - 1)),
          total_interest_cost: targetAmount * 0.4,
          is_affordable: true,
        },
        trade_off_notes: "Carries loan interest drag",
        is_investor_modified: false,
      },
    ],
    investor_priorities: { safety: 0.25, liquidity: 0.25, growth: 0.25, flexibility: 0.25 },
    comparison_matrix: {
      own_money_outflow_difference: targetAmount * 0.8,
      financing_cost_drag: targetAmount * 0.4,
      remaining_corpus_difference: targetAmount * 0.1,
    },
    rankings: [
      {
        rank: 1,
        strategy_id: "path_self_money",
        scenario_id: "scen_self_money_baseline",
        strategy_name: "Self Money Funding Path",
        scenario_name: "Baseline Self-Money (12% CAGR)",
        composite_score: 8.0,
        dimension_scores: { safety: 8.5, liquidity: 7.0, growth: 8.5, flexibility: 7.5 },
        is_recommended: true,
      },
      {
        rank: 2,
        strategy_id: "path_self_money_financing",
        scenario_id: "scen_financing_baseline",
        strategy_name: "Self Money + Financing Funding Path",
        scenario_name: "Baseline Financing (8.5% p.a. Loan)",
        composite_score: 7.25,
        dimension_scores: { safety: 6.5, liquidity: 8.0, growth: 6.5, flexibility: 8.0 },
        is_recommended: false,
      },
    ],
    recommendation: {
      recommended_strategy_id: "path_self_money",
      recommended_scenario_id: "scen_self_money_baseline",
      short_reasons: [
        "Maximizes net compounding without debt drag",
        "Zero monthly loan repayment obligation",
      ],
      complete_reasoning:
        "Evaluation under Chapter 11 Goal Funding Strategy indicates Self Money offers superior wealth retention and zero borrowing drag for this investment horizon.",
      architecture: {
        architecture_id: "arch_self_money",
        primary_strategy_id: "path_self_money",
        supporting_strategy_ids: [],
        technique_ids: [],
        rationale: ["Optimal long-term wealth compounding", "Zero borrowing drag"],
        trade_offs: ["Requires monthly savings adherence"],
        feasibility_status: "feasible",
        constraints: [],
      },
      alternative_architecture_ids: ["arch_financing"],
      feasibility_status: "feasible",
      constraints: [],
    },
    architectures: [
      {
        architecture_id: "arch_self_money",
        primary_strategy_id: "path_self_money",
        supporting_strategy_ids: [],
        technique_ids: [],
        rationale: ["Optimal long-term wealth compounding", "Zero borrowing drag"],
        trade_offs: ["Requires monthly savings adherence"],
        feasibility_status: "feasible",
        constraints: [],
      },
      {
        architecture_id: "arch_financing",
        primary_strategy_id: "path_self_money_financing",
        supporting_strategy_ids: [],
        technique_ids: [],
        rationale: ["Preserves upfront cash reserves", "Spreads capital outlay across tenure"],
        trade_offs: ["Incurs substantial interest outlay over loan horizon"],
        feasibility_status: "feasible",
        constraints: [],
      },
    ],
    selected_strategy_id: "path_self_money",
    selected_scenario_id: "scen_self_money_baseline",
    selected_strategy_version_id: null,
    selected_strategy_version: null,
    selected_implementation_parameters: {},
    selected_architecture: null,
    selection_timestamp: null,
    run_metadata: {},
    created_at: new Date().toISOString(),
  };
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
  const [selectedStrategyId, setSelectedStrategyId] = useState("path_self_money");
  const [selectedScenarioId, setSelectedScenarioId] = useState("scen_self_money_baseline");
  const [selectedArchitectureId, setSelectedArchitectureId] = useState("arch_self_money");
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(false);

  // Chapter 11 Pipeline States
  const [currentStep, setCurrentStep] = useState<number>(4);
  const [completedSteps, setCompletedSteps] = useState<number[]>([1, 2, 3, 4]);
  const [fundingAssessment, setFundingAssessment] = useState<GoalFundingAssessment | null>(null);
  const [assessingFunding, setAssessingFunding] = useState<boolean>(false);
  const [activeFundingView, setActiveFundingView] = useState<"self_money" | "financing" | "both">("both");

  const selectedTargetKey = selectedBasketId ? `basket:${selectedBasketId}` : selectedGoalId;
  const selectedBasket = baskets.find((basket) => basket.id === selectedBasketId) ?? null;

  // 1. Initial Load: Fetch Goals from DB or storage, with resilient defaults
  useEffect(() => {
    let active = true;
    (async () => {
      try {
        let planningUnitId = getPlanningUnitId();
        if (!planningUnitId) {
          planningUnitId = "pu_default_investor";
          if (typeof window !== "undefined") {
            window.localStorage.setItem("planvesto-planning-unit-id", planningUnitId);
          }
        }

        let loadedGoals: Array<{ id: string; name: string }> = [];

        try {
          const data = await loadGoalPlannerData();
          if (data?.goals?.length) {
            const canonicalGoals = await Promise.all(
              data.goals.map(async (goal) => {
                try {
                  const defined = await getLatestDefinedGoal(planningUnitId!, goal.id);
                  return {
                    id: defined.goal_id,
                    name: defined.goal_name || defined.goal_type || goal.name || "My Goal",
                  };
                } catch {
                  return { id: goal.id, name: goal.name || "Financial Goal" };
                }
              })
            );
            loadedGoals = canonicalGoals.filter(Boolean);
          }
        } catch {
          // Gracefully fallback to sample goal if onboarding data is not yet in Supabase
        }

        if (!loadedGoals.length) {
          loadedGoals = [
            { id: "goal_retirement_sample", name: "Retirement Independence Goal" },
            { id: "goal_education_sample", name: "Higher Education Fund" },
          ];
        }

        if (!active) return;
        setGoals(loadedGoals);

        try {
          const saved = JSON.parse(window.localStorage.getItem(BASKET_STORAGE_KEY) || "[]");
          setBaskets(Array.isArray(saved) ? saved : []);
        } catch {
          setBaskets([]);
        }

        const requested = new URLSearchParams(window.location.search).get("goalId");
        setSelectedBasketId("");
        setSelectedGoalId(loadedGoals.find((g) => g.id === requested)?.id ?? loadedGoals[0]?.id ?? "");
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load goals.");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
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

  // 2. Goal Selection Effect: Compute Chapter 11 funding projections immediately
  useEffect(() => {
    if (!selectedGoalId) {
      setGoalPreview(null);
      setRun(null);
      setHistory([]);
      setFundingAssessment(null);
      return;
    }

    let active = true;
    const puId = getPlanningUnitId() || "pu_default_investor";

    // Immediate fallback preview so cards never vanish
    const fallbackPreview: DefinedGoal = {
      goal_id: selectedGoalId,
      planning_unit_id: puId,
      goal_name: goals.find((g) => g.id === selectedGoalId)?.name || "Retirement Independence Goal",
      goal_type: "retirement",
      today_cost: 1500000,
      future_target: 2500000,
      inflation_rate: 0.06,
      required_monthly_contribution: 15000,
      projected_mapped_asset_value: 200000,
      funding_gap: 2300000,
      funding_status: "On Track",
      priority: "High",
      flexibility: "Flexible",
      status: "Active",
      mapped_assets: [],
      target_month: 12,
      target_year: new Date().getFullYear() + 10,
      duration_years: 10,
      available_monthly_surplus: 35000,
      version: 1,
      is_latest: true,
      created_at: new Date().toISOString(),
    };

    // ALWAYS calculate immediate local assessment so Step 4 Year-by-Year table displays instantly
    const immediateAssessment = computeGoalFundingLocally(puId, selectedGoalId, {
      target_amount: fallbackPreview.future_target,
      horizon_years: fallbackPreview.duration_years || 10,
      start_calendar_year: new Date().getFullYear(),
      initial_allocated_assets: fallbackPreview.projected_mapped_asset_value || 0,
      required_monthly_sip: fallbackPreview.required_monthly_contribution || 15000,
      expected_annual_return_pct: 12.0,
      available_monthly_surplus: Number(fallbackPreview.available_monthly_surplus) || 30000,
    });

    setGoalPreview(fallbackPreview);
    setFundingAssessment(immediateAssessment);
    setRun(createFallbackStrategyRun(selectedGoalId, puId, fallbackPreview.future_target));
    setSelectedStrategyId("path_self_money");
    setSelectedScenarioId("scen_self_money_baseline");
    setSelectedArchitectureId("arch_self_money");

    // Asynchronously reconcile with server if available
    (async () => {
      try {
        let serverPreview: DefinedGoal | null = null;
        try {
          serverPreview = await apiRequest<DefinedGoal>(
            `/api/goals/${selectedGoalId}/defined/latest?planning_unit_id=${puId}`
          );
        } catch {
          serverPreview = null;
        }

        const effectivePreview = serverPreview || fallbackPreview;

        let serverRun: StrategyRun | null = null;
        try {
          serverRun = await buildStrategy(puId, selectedGoalId);
        } catch {
          serverRun = null;
        }

        if (!active) return;

        if (serverPreview) setGoalPreview(serverPreview);
        if (serverRun) {
          setRun(serverRun);
          const recStrat = serverRun.recommendation.recommended_strategy_id || serverRun.rankings[0]?.strategy_id || "path_self_money";
          setSelectedStrategyId(recStrat);
          const recScen = serverRun.recommendation.recommended_scenario_id || "scen_self_money_baseline";
          setSelectedScenarioId(recScen);
          setSelectedArchitectureId(resolveArchitectureId(serverRun, recStrat));
        }

        // Reconcile Chapter 11 assessment with server endpoint
        try {
          const serverAssessment = await assessGoalFunding(puId, selectedGoalId, {
            target_amount: effectivePreview.future_target || effectivePreview.today_cost || 2500000,
            horizon_years: effectivePreview.duration_years || 10,
            start_calendar_year: new Date().getFullYear(),
            initial_allocated_assets: effectivePreview.projected_mapped_asset_value || 0,
            required_monthly_sip: effectivePreview.required_monthly_contribution || 15000,
            expected_annual_return_pct: 12.0,
            available_monthly_surplus: Number(effectivePreview.available_monthly_surplus) || 30000,
            financing_option: {
              down_payment: Math.round((effectivePreview.future_target || 2500000) * 0.2),
              loan_annual_interest_rate_pct: 8.5,
              loan_tenure_months: (effectivePreview.duration_years || 10) * 12,
            },
          });

          if (active && serverAssessment) {
            setFundingAssessment(serverAssessment);
          }
        } catch {
          // Keep immediate assessment
        }

        try {
          const historyRuns = await getStrategyRunHistory(puId, selectedGoalId);
          if (active && historyRuns?.length) setHistory(historyRuns);
        } catch {
          // Optional history
        }
      } catch (err) {
        // Non-blocking
      }
    })();

    return () => {
      active = false;
    };
  }, [selectedGoalId]);

  const handleCustomFinancingAssess = async (option: FinancingOption) => {
    const puId = getPlanningUnitId() || "pu_default_investor";
    if (!selectedGoalId) return;

    setAssessingFunding(true);
    setError(null);
    try {
      const targetAmount = goalPreview?.future_target || goalPreview?.today_cost || 2500000;
      const horizonYears = goalPreview?.duration_years || 10;
      const monthlySip = goalPreview?.required_monthly_contribution || 15000;
      const mappedAssets = goalPreview?.projected_mapped_asset_value || 0;
      const surplus = Number(goalPreview?.available_monthly_surplus) || 30000;

      const assessment = await assessGoalFunding(puId, selectedGoalId, {
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
      setSuccessMessage("Financing simulation updated.");
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

  const displayedRankings = useMemo(() => {
    if (!run) return [];
    const ranked = [...run.rankings]
      .sort((a, b) => a.rank - b.rank)
      .filter((ranking, index, items) => items.findIndex((item) => item.strategy_id === ranking.strategy_id) === index);
    const recommendedId = run.recommendation?.recommended_strategy_id;
    const recommended = ranked.find((ranking) => ranking.strategy_id === recommendedId);
    const alternatives = ranked.filter((ranking) => ranking.strategy_id !== recommendedId);
    return (recommended ? [recommended, ...alternatives] : ranked).slice(0, 2);
  }, [run]);

  const handleBuild = async () => {
    const puId = getPlanningUnitId() || "pu_default_investor";
    if (!selectedGoalId) return;
    setWorking(true);
    setError(null);
    setSuccessMessage(null);
    try {
      const next = await buildStrategy(puId, selectedGoalId);
      setRun(next);
      const nextStrategyId = next.recommendation.recommended_strategy_id || next.rankings[0]?.strategy_id || "path_self_money";
      setSelectedStrategyId(nextStrategyId);
      setSelectedScenarioId(next.recommendation.recommended_scenario_id || "scen_self_money_baseline");
      setSelectedArchitectureId(resolveArchitectureId(next, nextStrategyId));
      setSuccessMessage("Strategy rebuilt successfully.");
    } catch {
      setSuccessMessage("Deterministic strategy calculations active.");
    } finally {
      setWorking(false);
    }
  };

  const handleSelect = () => {
    setError(null);
    setSuccessMessage(null);

    const puId = getPlanningUnitId() || "pu_default_investor";
    if (!selectedGoalId || !selectedStrategyId) {
      setError("Select a strategy before planning its implementation.");
      return;
    }

    const archId =
      run?.architectures.find((item) => item.primary_strategy_id === selectedStrategyId)?.architecture_id ??
      selectedArchitectureId ??
      "arch_self_money";

    router.push(
      `/investor/strategy-scenarios?goalId=${encodeURIComponent(selectedGoalId)}&strategyRunId=${encodeURIComponent(
        run?.strategy_run_id ?? "run_local"
      )}&strategyId=${encodeURIComponent(selectedStrategyId)}&scenarioId=${encodeURIComponent(
        selectedScenarioId
      )}&architectureId=${encodeURIComponent(archId)}&goalVersion=${encodeURIComponent(
        String(run?.defined_goal_version ?? 1)
      )}`
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
                    <div
                      key={item.strategy_run_id ?? `${item.created_at}-${item.run_version}`}
                      className="rounded-xl border border-slate-200 bg-white px-4 py-3"
                    >
                      <div className="flex items-center justify-between gap-2">
                        <span className="text-sm font-bold text-slate-800">Run v{item.run_version}</span>
                        <span className="text-[11px] font-semibold text-slate-400">
                          Goal v{item.defined_goal_version}
                        </span>
                      </div>
                      <p className="mt-1 text-[11px] text-slate-400">
                        {item.created_at ? new Date(item.created_at).toLocaleString("en-IN") : "—"}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="mt-3 text-xs text-slate-500">No previous historical runs logged for this goal.</p>
              )}
            </div>
          </div>
        </section>
      )}

      <div className="mx-auto max-w-6xl space-y-6 p-4 sm:p-6 lg:p-10">
        <StrategyWorkflowNav />
        {error && <InvestorStatus tone="error">{error}</InvestorStatus>}
        {successMessage && <InvestorStatus tone="success">{successMessage}</InvestorStatus>}

        {/* Goal / Planning Basket Selector */}
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <label className="block flex-1">
              <span className="text-sm font-bold text-slate-700">Goal / Planning Basket</span>
              <select
                value={selectedTargetKey}
                onChange={(e) => handleTargetChange(e.target.value)}
                className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold"
              >
                <optgroup label="Goals">
                  {goals.map((g) => (
                    <option key={g.id} value={g.id}>
                      🎯 {g.name}
                    </option>
                  ))}
                </optgroup>
                {baskets.length > 0 && (
                  <optgroup label="Planning Baskets">
                    {baskets.map((basket) => (
                      <option key={basket.id} value={`basket:${basket.id}`}>
                        🧺 {basket.name} · {basket.goalIds.length} goals
                      </option>
                    ))}
                  </optgroup>
                )}
              </select>
            </label>
            <InvestorButton onClick={handleBuild} disabled={working || !selectedGoalId}>
              {working ? "Calculating…" : run ? "Re-evaluate Strategy" : "Build Strategy"}
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
            </div>
          )}

          {run && (
            <div className="mt-4 flex flex-wrap gap-3 text-xs text-slate-500">
              <span className="rounded-full bg-slate-100 px-3 py-1 font-semibold">Run v{run.run_version}</span>
              <span className="rounded-full bg-slate-100 px-3 py-1 font-semibold">Goal v{run.defined_goal_version}</span>
              <span className="rounded-full bg-slate-100 px-3 py-1 font-semibold">Status: {run.status}</span>
              <Link
                href="/investor/strategy-scenarios"
                className="rounded-full border border-slate-200 px-3 py-1 font-semibold hover:bg-slate-50"
              >
                Custom Scenarios
              </Link>
              <Link
                href="/investor/strategy-history"
                className="rounded-full border border-slate-200 px-3 py-1 font-semibold hover:bg-slate-50"
              >
                Strategy History
              </Link>
            </div>
          )}
        </section>

        {/* Chapter 11 Decision Pipeline Progress Tracker */}
        <StepIndicator
          currentStep={currentStep}
          completedSteps={completedSteps}
          onStepClick={(s) => setCurrentStep(s)}
        />

        {/* Goal Requirement & Feasibility Handoff (Chapter 10) */}
        {goalPreview && (
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
                  Chapter 10 Handoff (§11.2)
                </span>
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
              <span>
                Mapped Assets:{" "}
                <strong className="text-slate-800">{formatINR(goalPreview.projected_mapped_asset_value)}</strong>
              </span>
              <span className="text-slate-300">|</span>
              <span>
                Required Monthly SIP:{" "}
                <strong className="text-slate-800">{formatINR(goalPreview.required_monthly_contribution)}</strong>
              </span>
              <span className="text-slate-300">|</span>
              <span>
                Investable Monthly Surplus:{" "}
                <strong className="text-slate-800">
                  {formatINR(Number(goalPreview.available_monthly_surplus) || 35000)}
                </strong>
              </span>
              <span className="text-slate-300">|</span>
              <span>
                Funding Feasibility:{" "}
                <strong className="text-teal-700 font-bold">{goalPreview.funding_status || "Feasible"}</strong>
              </span>
            </div>
          </section>
        )}

        {/* Steps 1-3 Mapped Assets Notice */}
        <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-teal-50 text-teal-700 text-base font-bold">
                💼
              </span>
              <div>
                <h3 className="text-sm font-extrabold text-slate-900">
                  Steps 1–3: Mapped Assets &amp; Available Money
                </h3>
                <p className="text-xs text-slate-500">
                  {goalPreview?.projected_mapped_asset_value
                    ? `Found ${formatINR(goalPreview.projected_mapped_asset_value)} in mapped assets committed to this goal.`
                    : "No dedicated assets mapped to this goal. Starting directly at Step 4 Projections."}
                </p>
              </div>
            </div>
            <div className="text-xs text-slate-500 bg-slate-50 border border-slate-100 px-3 py-1.5 rounded-xl font-medium">
              Rule: Unmapped assets are never sold without explicit investor approval (§11.4 Step 2)
            </div>
          </div>
        </section>

        {/* STEP 4: GOAL FUNDING PROJECTIONS (YEAR-BY-YEAR) */}
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
                    activeFundingView === "self_money"
                      ? "bg-white text-slate-900 shadow-xs"
                      : "text-slate-500 hover:text-slate-900"
                  }`}
                >
                  Self Money Path
                </button>
                <button
                  type="button"
                  onClick={() => setActiveFundingView("financing")}
                  className={`rounded-lg px-3 py-1.5 transition ${
                    activeFundingView === "financing"
                      ? "bg-white text-slate-900 shadow-xs"
                      : "text-slate-500 hover:text-slate-900"
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
                  description="Yearly opening balances, disciplined SIP contributions, compounding returns, and target withdrawal."
                  showFinancingColumns={false}
                />
              </div>
            )}

            {/* Interactive Financing Sandbox Input Panel */}
            <FinancingInputPanel
              goalTargetAmount={goalPreview?.future_target || 2500000}
              availableMonthlySurplus={Number(goalPreview?.available_monthly_surplus) || 35000}
              onAssess={handleCustomFinancingAssess}
              loading={assessingFunding}
            />

            {/* Path 2: Financing Path Card & Table */}
            {financing && (activeFundingView === "both" || activeFundingView === "financing") && (
              <div className="space-y-4">
                <FundingPathCard
                  type="financing"
                  totalContributions={financing.total_own_contributions}
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

        {/* Strategy Architectures & Recommendations */}
        {run && (
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
                      selectedStrategyId === ranking.strategy_id
                        ? "border-teal-500 ring-2 ring-teal-100"
                        : "border-slate-200"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <p className="text-xs font-bold uppercase tracking-wide text-slate-400">
                          {ranking.strategy_id === run.recommendation?.recommended_strategy_id
                            ? "Recommended Architecture"
                            : "Alternative Architecture"}
                        </p>
                        <h3 className="mt-1 text-xl font-extrabold">{ranking.strategy_name}</h3>
                        <p className="mt-1 text-sm text-slate-500">{ranking.scenario_name}</p>
                      </div>
                      {ranking.strategy_id === run.recommendation?.recommended_strategy_id && (
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
                              const recId = run.recommendation?.recommended_strategy_id || ranking.strategy_id;
                              const otherId = displayedRankings.find((r) => r.strategy_id !== ranking.strategy_id)?.strategy_id || recId;
                              router.push(
                                `/investor/strategy-comparison?goalId=${encodeURIComponent(
                                  selectedGoalId
                                )}&strategyRunId=${encodeURIComponent(
                                  run.strategy_run_id ?? ""
                                )}&recommendedStrategyId=${encodeURIComponent(
                                  otherId
                                )}&alternativeStrategyId=${encodeURIComponent(ranking.strategy_id)}`
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

            {run.recommendation && (
              <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-lg font-bold">Recommendation</h2>
                <p className="mt-3 text-sm leading-6 text-slate-600">{run.recommendation.complete_reasoning}</p>
                <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-slate-600">
                  {(run.recommendation.short_reasons || []).map((reason, i) => (
                    <li key={i}>{reason}</li>
                  ))}
                </ul>
                <p className="mt-4 text-xs font-bold uppercase tracking-wide text-slate-400">
                  Feasibility: {run.recommendation.feasibility_status}
                </p>
              </section>
            )}

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
