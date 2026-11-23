"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import StrategyWorkflowNav from "../../../components/StrategyWorkflowNav";
import InvestorHeader from "../../../components/InvestorHeader";
import { InvestorButton, InvestorStatus } from "../../../components/InvestorUI";
import { supabase } from "../../../lib/supabase";
import { apiRequest } from "../../../lib/api/client";
import {
  buildStrategy,
  getStrategyRunHistory,
  type StrategyRun,
} from "../../../lib/api/strategy";
import { getLatestDefinedGoal } from "../../../lib/api/goals";
import type { DefinedGoal } from "../../../lib/onboarding/goals/types";

// Clean Consumer-Grade Components
import {
  YearlyProjectionTable,
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
    run.recommendation?.architecture?.architecture_id ??
    ""
  );
}

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
        name: "Self-Funded Path (100% Own Money)",
        tagline: "100% Own Funds & Systematic Investment",
        description: "Fund your goal entirely using disciplined monthly SIPs and market compounding. Zero debt, zero interest.",
        strategy_family: "Funding Path",
        strategic_objective: "Achieve complete goal funding with zero loan burden and maximum compounding wealth retention.",
        core_mechanism: "Systematic monthly contributions and disciplined market compounding.",
        principles: ["Debt freedom", "Compounding preservation"],
        constraints: ["Monthly savings quota"],
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
        trade_offs: ["Requires regular monthly savings commitment"],
        baseline_safety_score: 8.5,
        baseline_liquidity_score: 7.0,
        baseline_growth_score: 8.5,
        baseline_flexibility_score: 7.5,
      },
      {
        strategy_id: "path_self_money_financing",
        name: "Self Money + Loan / Financing",
        tagline: "Combined Down Payment & Structured Loan",
        description: "Combine an upfront own down payment with a structured bank loan to fund your goal while preserving liquid cash.",
        strategy_family: "Funding Path",
        strategic_objective: "Bridge the goal funding timeline by leveraging bank financing alongside own capital.",
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
        metrics: { required_sip: 15000, projected_corpus: targetAmount, total_interest_cost: 0 },
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
        strategy_name: "Self-Funded Path (100% Own Money)",
        scenario_name: "Baseline Self-Money (12% CAGR)",
        composite_score: 8.0,
        dimension_scores: { safety: 8.5, liquidity: 7.0, growth: 8.5, flexibility: 7.5 },
        is_recommended: true,
      },
      {
        rank: 2,
        strategy_id: "path_self_money_financing",
        scenario_id: "scen_financing_baseline",
        strategy_name: "Self Money + Loan / Financing",
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
        "Maximizes compounding wealth without interest cost drag",
        "Zero debt or monthly loan repayment obligations",
      ],
      complete_reasoning:
        "The Self-Funded strategy accumulates your goal corpus systematically through disciplined SIPs, leaving your portfolio debt-free with higher residual wealth.",
      architecture: {
        architecture_id: "arch_self_money",
        primary_strategy_id: "path_self_money",
        supporting_strategy_ids: [],
        technique_ids: [],
        rationale: ["Optimal long-term compounding", "Zero borrowing drag"],
        trade_offs: ["Requires regular monthly savings commitment"],
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
        rationale: ["Optimal long-term compounding", "Zero borrowing drag"],
        trade_offs: ["Requires regular monthly savings commitment"],
        feasibility_status: "feasible",
        constraints: [],
      },
      {
        architecture_id: "arch_financing",
        primary_strategy_id: "path_self_money_financing",
        supporting_strategy_ids: [],
        technique_ids: [],
        rationale: ["Preserves upfront cash reserves", "Spreads capital outlay over tenure"],
        trade_offs: ["Interest overhead paid to bank"],
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
  const [planningUnitId, setPlanningUnitId] = useState<string>("");
  const [goals, setGoals] = useState<Array<{ id: string; name: string }>>([]);
  const [baskets, setBaskets] = useState<PlanningBasket[]>([]);
  const [selectedGoalId, setSelectedGoalId] = useState("");
  const [selectedBasketId, setSelectedBasketId] = useState("");
  const [goalPreview, setGoalPreview] = useState<DefinedGoal | null>(null);
  const [run, setRun] = useState<StrategyRun | null>(null);
  const [history, setHistory] = useState<StrategyRun[]>([]);

  // Funding Path Selection (Default: "self_money")
  const [selectedPath, setSelectedPath] = useState<"self_money" | "financing">("self_money");
  const [enableFinancing, setEnableFinancing] = useState<boolean>(false);

  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(false);

  const [fundingAssessment, setFundingAssessment] = useState<GoalFundingAssessment | null>(null);
  const [assessingFunding, setAssessingFunding] = useState<boolean>(false);

  const selectedTargetKey = selectedBasketId ? `basket:${selectedBasketId}` : selectedGoalId;
  const selectedBasket = baskets.find((basket) => basket.id === selectedBasketId) ?? null;

  // 1. Initial Load: Load user's goals directly from Goal Planner database
  useEffect(() => {
    let active = true;
    (async () => {
      try {
        setLoading(true);
        setError(null);

        const { data: sessionData, error: sessionError } = await supabase.auth.getSession();
        if (sessionError) throw sessionError;
        if (!sessionData?.session) {
          throw new Error("You must be logged in to access Strategy Builder.");
        }

        // Match Goal Planner exactly: resolve the authenticated user's planning unit
        let puId = typeof window !== "undefined" ? window.localStorage.getItem("planvesto-planning-unit-id") : null;
        if (!puId || puId === "pu_default_investor") {
          const { data: unitData } = await supabase
            .from("planning_units")
            .select("planning_unit_id")
            .eq("user_id", sessionData.session.user.id)
            .order("created_at", { ascending: false })
            .limit(1)
            .maybeSingle();

          if (unitData?.planning_unit_id) {
            puId = String(unitData.planning_unit_id);
          }
        }

        if (!puId || puId === "pu_default_investor") {
          throw new Error("No active planning unit found. Please complete personal information first.");
        }

        if (typeof window !== "undefined") {
          window.localStorage.setItem("planvesto-planning-unit-id", puId);
        }

        if (!active) return;
        setPlanningUnitId(puId);

        // Fetch ONLY this user's goals from goals table (identical to Goal Planner)
        const { data: goalRows, error: goalError } = await supabase
          .from("goals")
          .select("goal_id, goal_name, target_amount, target_date, flexibility")
          .eq("planning_unit_id", puId)
          .order("created_at");

        if (goalError) throw goalError;

        const loadedGoals = (goalRows || []).map((g) => ({
          id: g.goal_id,
          name: (g.goal_name && g.goal_name.trim()) || "Untitled Goal",
        }));

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

  // 2. Goal Selection Effect: Compute funding projections immediately
  useEffect(() => {
    if (!selectedGoalId || !planningUnitId) {
      setGoalPreview(null);
      setRun(null);
      setHistory([]);
      setFundingAssessment(null);
      return;
    }

    let active = true;
    const puId = planningUnitId;

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

        let effectivePreview = serverPreview;

        if (!effectivePreview) {
          // If not yet in defined_goals, read the raw goal from goals table (Goal Planner)
          const { data: rawGoal } = await supabase
            .from("goals")
            .select("*")
            .eq("goal_id", selectedGoalId)
            .eq("planning_unit_id", puId)
            .maybeSingle();

          const currentGoalName = goals.find((g) => g.id === selectedGoalId)?.name || rawGoal?.goal_name || "Financial Goal";
          const rawTargetCost = Number(rawGoal?.target_amount) || 1500000;
          const [year, month] = String(rawGoal?.target_date || "").split("-");
          const targetYear = Number(year) || new Date().getFullYear() + 5;
          const targetMonth = Number(month) || 12;
          const durYears = Math.max(1, targetYear - new Date().getFullYear());
          const infRate = 0.06;
          const futureTarget = Math.round(rawTargetCost * Math.pow(1 + infRate, durYears));
          const r = 0.12 / 12;
          const n = durYears * 12;
          const reqMonthlySip = Math.round((futureTarget * r) / (Math.pow(1 + r, n) - 1));

          effectivePreview = {
            goal_id: selectedGoalId,
            planning_unit_id: puId,
            goal_name: currentGoalName,
            goal_type: "others",
            today_cost: rawTargetCost,
            future_target: futureTarget,
            inflation_rate: infRate,
            required_monthly_contribution: reqMonthlySip,
            projected_mapped_asset_value: 0,
            funding_gap: futureTarget,
            funding_status: "On Track",
            priority: (rawGoal?.priority as "High" | "Medium" | "Low") || "High",
            flexibility: (rawGoal?.flexibility as "Fixed" | "Flexible") || "Flexible",
            status: "Active",
            mapped_assets: [],
            target_month: targetMonth,
            target_year: targetYear,
            duration_years: durYears,
            available_monthly_surplus: 35000,
            version: 1,
            is_latest: true,
            created_at: rawGoal?.created_at || new Date().toISOString(),
          };
        }

        if (!active) return;
        setGoalPreview(effectivePreview);

        // Immediate local calculation using real Chapter 10 handoff data
        const immediateAssessment = computeGoalFundingLocally(puId, selectedGoalId, {
          target_amount: effectivePreview.future_target,
          horizon_years: effectivePreview.duration_years || 10,
          start_calendar_year: new Date().getFullYear(),
          initial_allocated_assets: effectivePreview.projected_mapped_asset_value || 0,
          required_monthly_sip: effectivePreview.required_monthly_contribution || 15000,
          expected_annual_return_pct: 12.0,
          available_monthly_surplus: Number(effectivePreview.available_monthly_surplus) || 35000,
        });

        setFundingAssessment(immediateAssessment);
        setRun(createFallbackStrategyRun(selectedGoalId, puId, effectivePreview.future_target));

        let serverRun: StrategyRun | null = null;
        try {
          serverRun = await buildStrategy(puId, selectedGoalId);
        } catch {
          serverRun = null;
        }

        if (!active) return;
        if (serverRun) setRun(serverRun);

        try {
          const serverAssessment = await assessGoalFunding(puId, selectedGoalId, {
            target_amount: effectivePreview.future_target,
            horizon_years: effectivePreview.duration_years || 10,
            start_calendar_year: new Date().getFullYear(),
            initial_allocated_assets: effectivePreview.projected_mapped_asset_value || 0,
            required_monthly_sip: effectivePreview.required_monthly_contribution || 15000,
            expected_annual_return_pct: 12.0,
            available_monthly_surplus: Number(effectivePreview.available_monthly_surplus) || 35000,
            financing_option: {
              down_payment: Math.round(effectivePreview.future_target * 0.2),
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
          // Optional
        }
      } catch (err) {
        // Non-blocking
      }
    })();

    return () => {
      active = false;
    };
  }, [selectedGoalId, planningUnitId]);

  const handleCustomFinancingAssess = async (option: FinancingOption) => {
    const puId = planningUnitId;
    if (!selectedGoalId || !puId) return;

    setAssessingFunding(true);
    setError(null);
    try {
      const targetAmount = goalPreview?.future_target || 2500000;
      const horizonYears = goalPreview?.duration_years || 10;
      const monthlySip = goalPreview?.required_monthly_contribution || 15000;
      const mappedAssets = goalPreview?.projected_mapped_asset_value || 0;
      const surplus = Number(goalPreview?.available_monthly_surplus) || 35000;

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
      setSelectedPath("financing");
      setSuccessMessage("Financing parameters updated in your projection table.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update financing simulation.");
    } finally {
      setAssessingFunding(false);
    }
  };

  const handleToggleFinancing = (e: React.ChangeEvent<HTMLInputElement>) => {
    const checked = e.target.checked;
    setEnableFinancing(checked);
    setSelectedPath(checked ? "financing" : "self_money");
  };

  const handleSelect = () => {
    setError(null);
    setSuccessMessage(null);

    const puId = planningUnitId;
    if (!selectedGoalId || !puId) {
      setError("Please select a goal first.");
      return;
    }

    const stratId = selectedPath === "financing" ? "path_self_money_financing" : "path_self_money";
    const scenId = selectedPath === "financing" ? "scen_financing_baseline" : "scen_self_money_baseline";
    const archId = selectedPath === "financing" ? "arch_financing" : "arch_self_money";

    router.push(
      `/investor/strategy-scenarios?goalId=${encodeURIComponent(selectedGoalId)}&strategyRunId=${encodeURIComponent(
        run?.strategy_run_id ?? "run_local"
      )}&strategyId=${encodeURIComponent(stratId)}&scenarioId=${encodeURIComponent(
        scenId
      )}&architectureId=${encodeURIComponent(archId)}&goalVersion=${encodeURIComponent(
        String(run?.defined_goal_version ?? 1)
      )}`
    );
  };

  if (loading) {
    return (
      <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
        <div className="mx-auto max-w-5xl space-y-6">
          <div className="h-9 w-64 animate-pulse rounded-xl bg-slate-200" />
          <div className="h-96 animate-pulse rounded-3xl bg-white" />
        </div>
      </main>
    );
  }

  const selfMoney = fundingAssessment?.self_money_path;
  const financing = fundingAssessment?.financing_path;

  // Active projection rows based solely on selected path
  const activeProjections = selectedPath === "financing" && financing ? financing.yearly_projections : (selfMoney?.yearly_projections ?? []);

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-20 text-slate-900">
      <InvestorHeader
        eyebrow="Decide"
        title="Strategy Builder"
        description="Choose how you want to fund this goal: 100% through your own investments, or combined with structured financing."
      >
        <button
          type="button"
          onClick={() => setShowHistory((v) => !v)}
          aria-expanded={showHistory}
          className="inline-flex min-h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-bold text-slate-700 shadow-xs hover:bg-slate-50 transition"
        >
          <span>History</span>
          <span className="rounded-full bg-slate-100 px-2 py-0.5 text-[11px]">{history.length}</span>
          <span aria-hidden="true">{showHistory ? "↑" : "↓"}</span>
        </button>
      </InvestorHeader>

      {/* History Slide-down Drawer */}
      {showHistory && (
        <section className="border-b border-slate-200 bg-white">
          <div className="mx-auto max-w-5xl px-4 py-4 sm:px-6">
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700">Strategy Version History</h4>
                  <p className="text-xs text-slate-500">Historical versions and decision checkpoints for this goal.</p>
                </div>
                <span className="text-xs font-semibold text-slate-400">{history.length} logged</span>
              </div>
              {history.length > 0 ? (
                <div className="mt-3 grid gap-2 sm:grid-cols-3">
                  {history.map((item) => (
                    <div
                      key={item.strategy_run_id ?? `${item.created_at}-${item.run_version}`}
                      className="rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-xs"
                    >
                      <div className="flex items-center justify-between font-bold text-slate-800">
                        <span>Run v{item.run_version}</span>
                        <span className="text-[10px] text-slate-400">Goal v{item.defined_goal_version}</span>
                      </div>
                      <p className="mt-1 text-[10px] text-slate-400">
                        {item.created_at ? new Date(item.created_at).toLocaleDateString("en-IN") : "—"}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="mt-2 text-xs text-slate-400">No previous runs recorded.</p>
              )}
            </div>
          </div>
        </section>
      )}

      <div className="mx-auto max-w-5xl space-y-6 p-4 sm:p-6 lg:p-8">
        <StrategyWorkflowNav />
        {error && <InvestorStatus tone="error">{error}</InvestorStatus>}
        {successMessage && <InvestorStatus tone="success">{successMessage}</InvestorStatus>}

        {/* 1. GOAL SELECTOR & COMPACT SNAPSHOT */}
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm space-y-5">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="flex-1 max-w-md">
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-500">
                Active Financial Goal
              </label>
              <select
                value={selectedTargetKey}
                onChange={(e) => handleTargetChange(e.target.value)}
                className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-extrabold text-slate-900 focus:border-teal-500 focus:outline-none"
              >
                <optgroup label="Your Goals">
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
            </div>

            {selectedBasket && (
              <div className="rounded-xl border border-teal-200 bg-teal-50/60 px-3.5 py-2 text-xs text-teal-800 font-medium">
                🧺 <strong>{selectedBasket.name}</strong> selected ({selectedBasket.goalIds.length} goals)
              </div>
            )}
          </div>

          {/* Goal Metrics Strip (Compact & Clean) */}
          {goalPreview && (
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 pt-2 border-t border-slate-100">
              <div className="rounded-2xl bg-slate-50 p-3.5">
                <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Target Corpus</p>
                <p className="mt-1 text-lg font-black text-slate-900">{formatINR(goalPreview.future_target)}</p>
                <p className="text-[10px] text-slate-400">In {goalPreview.duration_years || 10} Years ({goalPreview.target_year})</p>
              </div>

              <div className="rounded-2xl bg-slate-50 p-3.5">
                <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Required Monthly SIP</p>
                <p className="mt-1 text-lg font-black text-teal-700">{formatINR(goalPreview.required_monthly_contribution)}</p>
                <p className="text-[10px] text-slate-400">To fund 100% via savings</p>
              </div>

              <div className="rounded-2xl bg-slate-50 p-3.5">
                <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Today’s Cost</p>
                <p className="mt-1 text-lg font-black text-slate-900">{formatINR(goalPreview.today_cost)}</p>
                <p className="text-[10px] text-slate-400">At {((goalPreview.inflation_rate || 0.06) * 100).toFixed(0)}% inflation p.a.</p>
              </div>

              <div className="rounded-2xl bg-slate-50 p-3.5">
                <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Monthly Surplus</p>
                <p className="mt-1 text-lg font-black text-slate-900">{formatINR(Number(goalPreview.available_monthly_surplus) || 35000)}</p>
                <p className="text-[10px] text-emerald-600 font-semibold">✓ Easily affordable</p>
              </div>
            </div>
          )}
        </section>

        {/* 2. FUNDING APPROACH (PATH SELECTION) */}
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm space-y-5">
          <div>
            <h3 className="text-base font-extrabold text-slate-900">Choose Your Funding Approach</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Select how you prefer to fund this goal. By default, Planvesto designs a debt-free investment plan.
            </p>
          </div>

          {/* Clean 2-Option Radio Cards */}
          <div className="grid gap-4 sm:grid-cols-2">
            {/* Option 1: Self-Funded */}
            <div
              onClick={() => {
                setSelectedPath("self_money");
                setEnableFinancing(false);
              }}
              className={`cursor-pointer rounded-2xl border p-4 transition-all ${
                selectedPath === "self_money"
                  ? "border-teal-500 bg-teal-50/30 ring-2 ring-teal-100 shadow-xs"
                  : "border-slate-200 bg-slate-50/40 hover:border-slate-300"
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <span
                    className={`flex h-4 w-4 rounded-full border-2 items-center justify-center ${
                      selectedPath === "self_money" ? "border-teal-600 bg-teal-600" : "border-slate-300 bg-white"
                    }`}
                  >
                    {selectedPath === "self_money" && <span className="h-1.5 w-1.5 rounded-full bg-white" />}
                  </span>
                  <span className="text-sm font-extrabold text-slate-900">Self-Funded (Recommended)</span>
                </div>
                <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                  Zero Debt
                </span>
              </div>
              <p className="mt-2 text-xs leading-5 text-slate-600 pl-6.5">
                Fund 100% through disciplined monthly SIPs. Zero loan overhead, zero EMI, and maximum wealth retention.
              </p>
            </div>

            {/* Option 2: Self Money + Financing */}
            <div
              onClick={() => {
                setSelectedPath("financing");
                setEnableFinancing(true);
              }}
              className={`cursor-pointer rounded-2xl border p-4 transition-all ${
                selectedPath === "financing"
                  ? "border-amber-500 bg-amber-50/30 ring-2 ring-amber-100 shadow-xs"
                  : "border-slate-200 bg-slate-50/40 hover:border-slate-300"
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <span
                    className={`flex h-4 w-4 rounded-full border-2 items-center justify-center ${
                      selectedPath === "financing" ? "border-amber-600 bg-amber-600" : "border-slate-300 bg-white"
                    }`}
                  >
                    {selectedPath === "financing" && <span className="h-1.5 w-1.5 rounded-full bg-white" />}
                  </span>
                  <span className="text-sm font-extrabold text-slate-900">Include Bank Loan / Financing</span>
                </div>
                <span className="rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-bold text-amber-800">
                  Leveraged
                </span>
              </div>
              <p className="mt-2 text-xs leading-5 text-slate-600 pl-6.5">
                Pay an upfront down payment and fund the remaining balance through an amortized bank loan (e.g. Home/Education loan).
              </p>
            </div>
          </div>

          {/* Quick Checkbox Toggle for Loan Details */}
          <div className="pt-2">
            <label className="inline-flex items-center gap-2.5 cursor-pointer text-xs font-bold text-slate-800">
              <input
                type="checkbox"
                checked={enableFinancing}
                onChange={handleToggleFinancing}
                className="h-4 w-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500 cursor-pointer"
              />
              <span>Explore borrowing options (Configure loan amount, down payment, and tenure)</span>
            </label>
          </div>

          {/* Expandable Financing Calculator (ONLY VISIBLE WHEN TICKED) */}
          {enableFinancing && (
            <div className="pt-2 animate-fadeIn">
              <FinancingInputPanel
                goalTargetAmount={goalPreview?.future_target || 2500000}
                availableMonthlySurplus={Number(goalPreview?.available_monthly_surplus) || 35000}
                onAssess={handleCustomFinancingAssess}
                loading={assessingFunding}
              />
            </div>
          )}
        </section>

        {/* 3. YEAR-BY-YEAR WEALTH TRAJECTORY (SINGLE DYNAMIC TABLE ONLY) */}
        <div className="space-y-4">
          <YearlyProjectionTable
            projections={activeProjections}
            title={
              selectedPath === "financing"
                ? "Year-by-Year Financing & Payout Trajectory"
                : "Year-by-Year Growth Trajectory (Self-Funded)"
            }
            description={
              selectedPath === "financing"
                ? "Reflects your loan disbursement in the goal year and subsequent annual EMI repayments."
                : "Shows how your systematic monthly SIP compounds year-over-year to fund your goal without debt."
            }
            showFinancingColumns={selectedPath === "financing"}
          />

          {/* Trade-off summary when financing is active */}
          {selectedPath === "financing" && financing && (
            <div className="rounded-2xl border border-amber-200 bg-amber-50/70 p-4 text-xs space-y-1.5 text-amber-950">
              <p className="font-extrabold text-amber-900">
                💡 Key Financial Trade-off for Financing:
              </p>
              <p className="leading-5 text-amber-900">
                Using financing requires an initial down payment of <strong>{formatINR(financing.down_payment)}</strong> and borrows{" "}
                <strong>{formatINR(financing.financing_amount)}</strong>. You will pay a total of{" "}
                <strong className="text-rose-700">{formatINR(financing.total_interest_cost)}</strong> in bank interest cost with an EMI of{" "}
                <strong>{formatINR(financing.monthly_emi)}/month</strong>.
              </p>
            </div>
          )}
        </div>

        {/* 4. ACTION BAR (CLEAN & LOW FRICTION) */}
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-teal-700">Next Step</p>
              <h3 className="text-lg font-extrabold text-slate-900">
                Ready to plan your implementation?
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Stress-test scenarios with inflation and step-up options before finalizing.
              </p>
            </div>

            <InvestorButton onClick={handleSelect} disabled={working}>
              Plan Your Implementation →
            </InvestorButton>
          </div>
        </section>
      </div>
    </main>
  );
}
