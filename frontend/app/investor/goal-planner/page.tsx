"use client";

import { useEffect, useState, useId } from "react";
import Link from "next/link";
import { InvestorProfileMenu } from "../../../components/InvestorProfileMenu";
import { supabase } from "../../../lib/supabase";
import {
  formatINR,
  formatTargetMonthYear,
} from "../../../lib/onboarding/goals/goals";
import {
  goalFlexibilities,
  goalPriorities,
  goalStatuses,
  goalTypes,
  returnFrequencies,
  type AssetMappingAllocationType,
  type AssetMappingInput,
  type DefinedGoal,
  type DefinedGoalAssetMapping,
  type FundingStatus,
  type GoalFlexibility,
  type GoalInput,
  type GoalPriority,
  type GoalStatus,
  type GoalType,
  type ReturnFrequency,
} from "../../../lib/onboarding/goals/types";

// ============================================================================
// TYPES & DEFAULTS
// ============================================================================

type AssetRecord = {
  asset_id: string;
  asset_name: string;
  current_value: number;
};

type FormAssetMapping = {
  id: string;
  asset_id: string;
  allocation_type: AssetMappingAllocationType;
  allocation_value: string;
  expected_return: string;
  return_frequency: ReturnFrequency;
};

type GoalFormData = {
  goal_id: string | null;
  goal_name: string;
  preset_name: string;
  custom_name: string;
  goal_type: GoalType | "";
  today_cost: string;
  inflation_rate: string;
  target_date: string; // YYYY-MM
  priority: GoalPriority | "";
  flexibility: GoalFlexibility | "";
  status: GoalStatus;
  asset_mappings: FormAssetMapping[];
};

const DEFAULT_INFLATION_PERCENT = "6.0";

const PRESET_GOAL_NAMES = [
  "Retirement",
  "Child Education",
  "Child Marriage",
  "Dream Home",
  "Vehicle",
  "Travel",
  "Wealth Creation",
  "Emergency Fund",
  "Other",
] as const;

function deriveGoalType(goalName: string): GoalType {
  const normalized = goalName.trim();
  const aliases: Record<string, GoalType> = { "Dream Home": "Home Purchase" };
  if (aliases[normalized]) return aliases[normalized];
  if (goalTypes.includes(normalized as GoalType)) return normalized as GoalType;
  return "Other";
}

function createEmptyForm(): GoalFormData {
  const nextYear = new Date().getFullYear() + 5;
  const month = String(new Date().getMonth() + 1).padStart(2, "0");
  return {
    goal_id: null,
    goal_name: "",
    preset_name: "",
    custom_name: "",
    goal_type: "",
    today_cost: "",
    inflation_rate: DEFAULT_INFLATION_PERCENT,
    target_date: `${nextYear}-${month}`,
    priority: "Important",
    flexibility: "Flexible",
    status: "Active",
    asset_mappings: [],
  };
}

function definedGoalToForm(goal: DefinedGoal): GoalFormData {
  const isPreset = PRESET_GOAL_NAMES.includes(
    goal.goal_name as (typeof PRESET_GOAL_NAMES)[number]
  );
  const targetDateStr = `${goal.target_year}-${String(goal.target_month).padStart(2, "0")}`;

  return {
    goal_id: goal.goal_id,
    goal_name: goal.goal_name,
    preset_name: isPreset ? goal.goal_name : "Other",
    custom_name: isPreset ? "" : goal.goal_name,
    goal_type: (goal.goal_type as GoalType) || "",
    today_cost: String(goal.today_cost),
    inflation_rate: (goal.inflation_rate * 100).toFixed(1),
    target_date: targetDateStr,
    priority: (goal.priority as GoalPriority) || "Important",
    flexibility: (goal.flexibility as GoalFlexibility) || "Flexible",
    status: (goal.status as GoalStatus) || "Active",
    asset_mappings: goal.mapped_assets.map((m) => ({
      id: m.mapping_id || `map-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
      asset_id: m.asset_id,
      allocation_type: m.allocation_type,
      allocation_value: String(m.allocation_value),
      expected_return: m.expected_return != null ? (m.expected_return * 100).toFixed(1) : "",
      return_frequency: (m.return_frequency as ReturnFrequency) || "annual",
    })),
  };
}


export default function GoalPlannerPage() {
  const [goals, setGoals] = useState<DefinedGoal[]>([]);
  const [assets, setAssets] = useState<AssetRecord[]>([]);
  const [planningUnitId, setPlanningUnitId] = useState<string | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);

  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [isPreviewing, setIsPreviewing] = useState(false);
  const [cancellingGoalId, setCancellingGoalId] = useState<string | null>(null);

  const [error, setError] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [lastSavedGoalId, setLastSavedGoalId] = useState<string | null>(null);

  // Form State
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [formData, setFormData] = useState<GoalFormData>(createEmptyForm());
  const [previewResult, setPreviewResult] = useState<DefinedGoal | null>(null);

  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  // 1. Initial Load: Authenticate, resolve planning unit, load assets & DefinedGoals
  useEffect(() => {
    let active = true;

    async function loadData() {
      try {
        setIsLoading(true);
        if (!backendUrl) throw new Error("Backend URL is not configured.");
        setError(null);

        const { data: sessionData, error: sessionError } = await supabase.auth.getSession();
        if (sessionError) throw sessionError;
        const session = sessionData?.session;

        if (!session) {
          throw new Error("You must be logged in to access the Goal Planner.");
        }

        const token = session.access_token;
        if (active) setAccessToken(token);

        // Resolve planning unit ID
        let resolvedPuId =
          typeof window !== "undefined"
            ? window.localStorage.getItem("planvesto-planning-unit-id")
            : null;

        if (!resolvedPuId) {
          const { data: puData, error: puError } = await supabase
            .from("planning_units")
            .select("planning_unit_id")
            .eq("user_id", session.user.id)
            .order("created_at", { ascending: false })
            .limit(1)
            .maybeSingle();

          if (puError) throw puError;
          if (puData?.planning_unit_id) {
            resolvedPuId = String(puData.planning_unit_id);
            if (typeof window !== "undefined") {
              window.localStorage.setItem("planvesto-planning-unit-id", resolvedPuId);
            }
          }
        }

        if (!resolvedPuId) {
          throw new Error("No planning unit found. Please complete personal information first.");
        }

        if (active) setPlanningUnitId(resolvedPuId);

        // Fetch assets for asset mapping
        const { data: assetsData, error: assetsError } = await supabase
          .from("assets")
          .select("asset_id, asset_name, current_value")
          .eq("planning_unit_id", resolvedPuId)
          .order("created_at");

        if (assetsError) throw assetsError;
        const loadedAssets: AssetRecord[] = (assetsData || []).map((a) => ({
          asset_id: a.asset_id,
          asset_name: a.asset_name,
          current_value: Number(a.current_value) || 0,
        }));

        if (active) setAssets(loadedAssets);

        // Fetch existing goals
        const { data: goalRows, error: goalsQueryError } = await supabase
          .from("goals")
          .select("goal_id, goal_name, target_amount, target_date, priority, flexibility")
          .eq("planning_unit_id", resolvedPuId)
          .order("created_at");

        if (goalsQueryError) throw goalsQueryError;

        // For each goal, retrieve the authoritative latest DefinedGoal
        const definedGoalsList: DefinedGoal[] = [];

        for (const g of goalRows || []) {
          try {
            const resp = await fetch(
              `${backendUrl}/api/goals/${g.goal_id}/defined/latest?planning_unit_id=${resolvedPuId}`,
              {
                headers: {
                  Authorization: `Bearer ${token}`,
                },
              }
            );

            if (resp.ok) {
              const dg: DefinedGoal = await resp.json();
              // Cancelled goals remain in history, but must not appear in the active Goal Planner.
              if (dg.status !== "Cancelled") {
                definedGoalsList.push(dg);
              }
            } else if (resp.status === 404) {
              // Legacy goal without DefinedGoal snapshot: initialize it via backend
              const [yearStr, monthStr] = (g.target_date || "").split("-");
              const targetYear = parseInt(yearStr, 10) || new Date().getFullYear() + 3;
              const targetMonth = parseInt(monthStr, 10) || 12;

              const initPayload: GoalInput = {
                planning_unit_id: resolvedPuId,
                goal_id: g.goal_id,
                goal_name: g.goal_name || "Untitled Goal",
                goal_type: "Other",
                today_cost: Number(g.target_amount) || 100000,
                target_month: targetMonth,
                target_year: targetYear,
                inflation_rate: 0.06,
                priority: g.priority || "Important",
                flexibility: g.flexibility || "Flexible",
                status: "Active",
                asset_mappings: [],
              };

              const postResp = await fetch(`${backendUrl}/api/goals`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(initPayload),
              });

              if (postResp.ok) {
                const newDg: DefinedGoal = await postResp.json();
                definedGoalsList.push(newDg);
              }
            }
          } catch {
            // If individual retrieval fails, proceed with remaining goals
          }
        }

        if (active) {
          setGoals(definedGoalsList);
        }
      } catch (err: unknown) {
        if (active) {
          setError(err instanceof Error ? err.message : "Unable to load goal planner data.");
        }
      } finally {
        if (active) {
          setIsLoading(false);
        }
      }
    }

    loadData();

    return () => {
      active = false;
    };
  }, [backendUrl]);

  // Helper to build GoalInput payload from form state
  function buildGoalInputPayload(forCalculate = false): GoalInput | null {
    if (!planningUnitId) {
      setFormError("Planning unit is missing. Please refresh the page.");
      return null;
    }

    const goalName =
      formData.preset_name === "Other"
        ? formData.custom_name.trim()
        : formData.preset_name.trim() || formData.goal_name.trim();

    if (!goalName) {
      setFormError("Please provide a name for the goal.");
      return null;
    }

    const goalType = deriveGoalType(goalName);

    const costNum = Number(formData.today_cost);
    if (!Number.isFinite(costNum) || costNum <= 0) {
      setFormError("Please enter a valid today's cost greater than zero.");
      return null;
    }

    if (!formData.target_date) {
      setFormError("Please select a target month and year.");
      return null;
    }

    const [yearStr, monthStr] = formData.target_date.split("-");
    const targetYear = parseInt(yearStr, 10);
    const targetMonth = parseInt(monthStr, 10);

    if (isNaN(targetYear) || isNaN(targetMonth) || targetMonth < 1 || targetMonth > 12) {
      setFormError("Invalid target month or year.");
      return null;
    }

    // Inflation rate: User input % -> decimal (e.g. 6% -> 0.06)
    let inflationDecimal: number | null = null;
    if (formData.inflation_rate.trim()) {
      const parsedRate = parseFloat(formData.inflation_rate);
      if (Number.isFinite(parsedRate) && parsedRate >= 0) {
        inflationDecimal = Number((parsedRate / 100).toFixed(4));
      }
    }

    // Asset mappings
    const assetMappings: AssetMappingInput[] = [];
    for (let i = 0; i < formData.asset_mappings.length; i++) {
      const m = formData.asset_mappings[i];
      if (!m.asset_id) {
        setFormError(`Asset mapping #${i + 1} has no asset selected.`);
        return null;
      }

      const allocVal = parseFloat(m.allocation_value);
      if (!Number.isFinite(allocVal) || allocVal <= 0) {
        setFormError(`Asset mapping #${i + 1} has an invalid allocation value.`);
        return null;
      }

      if (m.allocation_type === "percentage" && allocVal > 100) {
        setFormError(`Asset mapping #${i + 1} percentage cannot exceed 100%.`);
        return null;
      }

      let expReturnDecimal: number | null = null;
      if (m.expected_return.trim()) {
        const parsedExp = parseFloat(m.expected_return);
        if (Number.isFinite(parsedExp) && parsedExp >= 0) {
          expReturnDecimal = Number((parsedExp / 100).toFixed(4));
        }
      }

      assetMappings.push({
        asset_id: m.asset_id,
        allocation_type: m.allocation_type,
        allocation_value: allocVal,
        expected_return: expReturnDecimal,
        return_frequency: m.return_frequency || "annual",
      });
    }

    return {
      planning_unit_id: planningUnitId,
      goal_id: forCalculate ? formData.goal_id : formData.goal_id,
      goal_name: goalName,
      goal_type: goalType,
      today_cost: costNum,
      target_month: targetMonth,
      target_year: targetYear,
      inflation_rate: inflationDecimal,
      priority: formData.priority || "Important",
      flexibility: formData.flexibility || "Flexible",
      status: formData.status || "Active",
      asset_mappings: assetMappings,
    };
  }

  // 2. Actions: Add, Edit, Cancel Form
  function handleStartAdding() {
    setSuccessMessage(null);
    setError(null);
    setFormError(null);
    setPreviewResult(null);
    setFormData(createEmptyForm());
    setIsFormOpen(true);
  }

  function handleStartEditing(goal: DefinedGoal) {
    setSuccessMessage(null);
    setError(null);
    setFormError(null);
    setPreviewResult(null);
    setFormData(definedGoalToForm(goal));
    setIsFormOpen(true);
  }

  function handleCancelForm() {
    setIsFormOpen(false);
    setPreviewResult(null);
    setFormError(null);
  }

  // 3. Asset Mapping Row helpers
  function handleAddMappingRow() {
    if (assets.length === 0) return;
    const defaultAssetId = assets[0].asset_id;
    setFormData((prev) => ({
      ...prev,
      asset_mappings: [
        ...prev.asset_mappings,
        {
          id: `map-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
          asset_id: defaultAssetId,
          allocation_type: "percentage",
          allocation_value: "100",
          expected_return: "",
          return_frequency: "annual",
        },
      ],
    }));
  }

  function handleRemoveMappingRow(id: string) {
    setFormData((prev) => ({
      ...prev,
      asset_mappings: prev.asset_mappings.filter((m) => m.id !== id),
    }));
  }

  function handleUpdateMappingRow(id: string, changes: Partial<FormAssetMapping>) {
    setFormData((prev) => ({
      ...prev,
      asset_mappings: prev.asset_mappings.map((m) =>
        m.id === id ? { ...m, ...changes } : m
      ),
    }));
  }

  // 4. Preview / Calculate via POST /api/goals/calculate
  async function handleCalculatePreview() {
    setFormError(null);
    const payload = buildGoalInputPayload(true);
    if (!payload) return;

    try {
      setIsPreviewing(true);
      const resp = await fetch(`${backendUrl}/api/goals/calculate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify(payload),
      });

      const data = await resp.json();
      if (!resp.ok) {
        throw new Error(data.detail || "Calculation preview failed.");
      }

      setPreviewResult(data as DefinedGoal);
    } catch (err: unknown) {
      setFormError(err instanceof Error ? err.message : "Unable to calculate goal preview.");
    } finally {
      setIsPreviewing(false);
    }
  }

  // 5. Save Goal via POST /api/goals
  async function handleSaveGoal() {
    setFormError(null);
    const payload = buildGoalInputPayload(false);
    if (!payload) return;

    try {
      setIsSaving(true);
      const resp = await fetch(`${backendUrl}/api/goals`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify(payload),
      });

      const responseBody = await resp.json();
      if (!resp.ok) {
        if (resp.status === 401) {
          throw new Error("Your session has expired. Please refresh the page and sign in again.");
        }
        if (resp.status === 403) {
          throw new Error("You do not have permission to modify this planning unit.");
        }
        if (resp.status === 400 || resp.status === 422) {
          throw new Error(responseBody.detail || "Invalid goal input. Please check the values entered.");
        }
        throw new Error(responseBody.detail || "Failed to save goal.");
      }

      const savedDefinedGoal: DefinedGoal = responseBody;
      setLastSavedGoalId(savedDefinedGoal.goal_id);

      // Update local state with the returned authoritative DefinedGoal
      setGoals((prev) => {
        const existingIdx = prev.findIndex((g) => g.goal_id === savedDefinedGoal.goal_id);
        if (existingIdx >= 0) {
          const updated = [...prev];
          updated[existingIdx] = savedDefinedGoal;
          return updated;
        }
        return [...prev, savedDefinedGoal];
      });

      setSuccessMessage(
        formData.goal_id
          ? `Goal "${savedDefinedGoal.goal_name}" updated successfully (v${savedDefinedGoal.version}).`
          : `Goal "${savedDefinedGoal.goal_name}" created successfully (v${savedDefinedGoal.version}).`
      );

      handleCancelForm();
    } catch (err: unknown) {
      setFormError(err instanceof Error ? err.message : "Unable to save goal.");
    } finally {
      setIsSaving(false);
    }
  }

  // 6. Cancel Goal action (Creates new version with status "Cancelled" without hard delete)
  async function handleCancelGoal(goal: DefinedGoal) {
    if (goal.status === "Cancelled") {
      return;
    }

    const confirmCancel = window.confirm(
      `Are you sure you want to mark "${goal.goal_name}" as Cancelled? All version history will remain intact.`
    );
    if (!confirmCancel) return;

    try {
      setCancellingGoalId(goal.goal_id);
      setError(null);

      const cancelPayload: GoalInput = {
        planning_unit_id: goal.planning_unit_id,
        goal_id: goal.goal_id,
        investor_id: goal.investor_id,
        goal_name: goal.goal_name,
        goal_type: goal.goal_type,
        today_cost: goal.today_cost,
        target_month: goal.target_month,
        target_year: goal.target_year,
        inflation_rate: goal.inflation_rate,
        priority: goal.priority,
        flexibility: goal.flexibility,
        status: "Cancelled",
        asset_mappings: goal.mapped_assets.map((m) => ({
          asset_id: m.asset_id,
          allocation_type: m.allocation_type,
          allocation_value: m.allocation_value,
          expected_return: m.expected_return,
          return_frequency: m.return_frequency,
        })),
      };

      const resp = await fetch(`${backendUrl}/api/goals`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify(cancelPayload),
      });

      const result = await resp.json();
      if (!resp.ok) {
        throw new Error(result.detail || "Unable to cancel goal.");
      }

      const updatedGoal: DefinedGoal = result;
      setGoals((prev) =>
        prev.map((g) => (g.goal_id === updatedGoal.goal_id ? updatedGoal : g))
      );
      // Cancelled goals stay in history but are removed from the active planner immediately.
      setGoals((prev) => prev.filter((g) => g.goal_id !== goal.goal_id));

      setSuccessMessage(`Goal "${goal.goal_name}" marked as Cancelled (v${updatedGoal.version}).`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unable to cancel goal.");
    } finally {
      setCancellingGoalId(null);
    }
  }

  // Summary Metrics derived directly from DefinedGoal items
  const totalGoalsCount = goals.length;
  const shortfallGoalsCount = goals.filter((g) => g.funding_status === "Shortfall").length;
  const onTrackGoalsCount = goals.filter((g) => g.funding_status === "On Track").length;
  const overfundedGoalsCount = goals.filter((g) => g.funding_status === "Overfunded").length;

  if (isLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-25 text-sm font-semibold text-slate-500">
        <div className="flex flex-col items-center gap-3">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-teal-600 border-t-transparent" />
          <p>Loading your goals from the DefinedGoal engine...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-25 text-slate-900">
      {/* Header */}
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex h-20 max-w-[1200px] items-center justify-between px-5 lg:px-8">
          <div>
            <span className="text-xs font-bold uppercase tracking-[0.16em] text-teal-700">
              Defined Goal Architecture
            </span>
            <p className="text-sm font-semibold text-slate-500">Plan your milestones with backend accuracy</p>
          </div>
          <div className="flex items-center gap-4">
            <Link
              href="/investor/financial-state"
              className="text-sm font-semibold text-teal-700 hover:text-teal-900"
            >
              Financial State
            </Link>
            <Link
              href="/investor/strategy-builder"
              className="text-sm font-semibold text-slate-600 hover:text-navy-900"
            >
              Strategy Builder
            </Link>
            <InvestorProfileMenu />
          </div>
        </div>
      </header>

      <div className="mx-auto w-full max-w-[1120px] px-5 py-10 lg:px-8 lg:py-14">
        {/* Page Title & Actions */}
        <div className="mb-8 flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.16em] text-teal-700">Goal Planner</p>
            <h1 className="mt-2 text-3xl font-extrabold tracking-tight text-navy-900 sm:text-4xl">
              Financial Goals &amp; Asset Mapping
            </h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
              Define life milestones, connect your existing assets, and let the Planvesto Goal Engine
              authoritatively project future targets, duration, and funding gaps.
            </p>
          </div>
          {!isFormOpen && (
            <button
              type="button"
              onClick={handleStartAdding}
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-teal-700 px-5 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-teal-800"
            >
              <span className="text-base font-black">+</span> Add Goal
            </button>
          )}
        </div>

        {/* Banners */}
        {error && (
          <div className="mb-6 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-700" role="alert">
            {error}
          </div>
        )}
        {successMessage && (
          <div className="mb-6 flex flex-col gap-3 rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700 sm:flex-row sm:items-center sm:justify-between" role="status">
            <span>{successMessage}</span>
            {lastSavedGoalId && (
              <Link
                href={`/investor/strategy-builder?goalId=${encodeURIComponent(lastSavedGoalId)}`}
                className="inline-flex shrink-0 items-center justify-center rounded-lg bg-navy-900 px-4 py-2 text-xs font-bold text-white transition hover:bg-navy-800"
              >
                Continue to Strategy →
              </Link>
            )}
          </div>
        )}

        {/* 11. GOAL SUMMARY METRICS (Derived from DefinedGoal responses) */}
        {!isFormOpen && (
          <section aria-labelledby="goal-summary-heading" className="mb-8">
            <h2 id="goal-summary-heading" className="sr-only">Goal Summary</h2>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <p className="text-xs font-bold uppercase tracking-[0.14em] text-slate-400">Total Goals</p>
                <p className="mt-2 text-3xl font-extrabold text-navy-900">{totalGoalsCount}</p>
                <p className="mt-1 text-xs text-slate-500">Defined planning milestones</p>
              </div>

              <div className="rounded-2xl border border-rose-200 bg-rose-50/60 p-5 shadow-sm">
                <div className="flex items-center justify-between">
                  <p className="text-xs font-bold uppercase tracking-[0.14em] text-rose-700">Shortfall Goals</p>
                  <span className="h-2 w-2 rounded-full bg-rose-500" />
                </div>
                <p className="mt-2 text-3xl font-extrabold text-rose-700">{shortfallGoalsCount}</p>
                <p className="mt-1 text-xs text-rose-600">Requires additional funding</p>
              </div>

              <div className="rounded-2xl border border-teal-200 bg-teal-50/60 p-5 shadow-sm">
                <div className="flex items-center justify-between">
                  <p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-700">On Track Goals</p>
                  <span className="h-2 w-2 rounded-full bg-teal-500" />
                </div>
                <p className="mt-2 text-3xl font-extrabold text-teal-800">{onTrackGoalsCount}</p>
                <p className="mt-1 text-xs text-teal-600">Fully funded to target</p>
              </div>

              <div className="rounded-2xl border border-blue-200 bg-blue-50/60 p-5 shadow-sm">
                <div className="flex items-center justify-between">
                  <p className="text-xs font-bold uppercase tracking-[0.14em] text-blue-700">Overfunded Goals</p>
                  <span className="h-2 w-2 rounded-full bg-blue-500" />
                </div>
                <p className="mt-2 text-3xl font-extrabold text-blue-800">{overfundedGoalsCount}</p>
                <p className="mt-1 text-xs text-blue-600">Surplus asset backing</p>
              </div>
            </div>
          </section>
        )}

        {/* Empty State */}
        {!isFormOpen && goals.length === 0 && (
          <section className="rounded-[28px] border border-dashed border-slate-300 bg-white p-12 text-center shadow-soft">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-teal-50 text-teal-700 font-extrabold text-2xl">
              🎯
            </div>
            <h2 className="mt-4 text-xl font-extrabold text-navy-900">No goals defined yet</h2>
            <p className="mx-auto mt-2 max-w-md text-sm text-slate-500">
              Add your first financial goal to calculate future target values, map assets, and inspect funding status.
            </p>
            <button
              type="button"
              onClick={handleStartAdding}
              className="mt-6 inline-flex items-center gap-2 rounded-xl bg-navy-900 px-6 py-3 text-sm font-bold text-white transition hover:bg-navy-800"
            >
              + Add Goal
            </button>
          </section>
        )}

        {/* 10. GOAL CARDS LIST */}
        {!isFormOpen && goals.length > 0 && (
          <section aria-labelledby="goals-list-heading" className="space-y-4">
            <h2 id="goals-list-heading" className="sr-only">Saved Goals</h2>
            {goals.map((goal) => {
              const isCancelled = goal.status === "Cancelled";
              return (
                <article
                  key={goal.goal_id}
                  className={`rounded-2xl border bg-white p-6 shadow-sm transition ${
                    isCancelled
                      ? "border-slate-200 opacity-60"
                      : goal.funding_status === "Shortfall"
                      ? "border-rose-200/90"
                      : "border-slate-200"
                  }`}
                >
                  <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                      <div className="flex flex-wrap items-center gap-2.5">
                        <h3 className="text-xl font-extrabold text-navy-900">{goal.goal_name}</h3>
                        <span className="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-bold text-slate-600">
                          v{goal.version}
                        </span>
                        <FundingStatusBadge status={goal.funding_status} />
                        {isCancelled && (
                          <span className="rounded-md bg-slate-200 px-2 py-0.5 text-xs font-bold text-slate-700">
                            Cancelled
                          </span>
                        )}
                      </div>
                      <p className="mt-1 text-sm text-slate-500">
                        {goal.goal_type} · Target: {formatTargetMonthYear(goal.target_month, goal.target_year)}
                        {" "}(Duration: {goal.duration_years} yrs)
                      </p>
                    </div>

                    <div className="flex shrink-0 items-center gap-3 text-sm font-bold">
                      <button
                        type="button"
                        onClick={() => handleStartEditing(goal)}
                        className="rounded-lg px-3 py-1.5 text-teal-700 hover:bg-teal-50"
                      >
                        Edit
                      </button>
                      {!isCancelled && (
                        <button
                          type="button"
                          disabled={cancellingGoalId === goal.goal_id}
                          onClick={() => handleCancelGoal(goal)}
                          className="rounded-lg px-3 py-1.5 text-slate-500 hover:bg-rose-50 hover:text-rose-700 disabled:opacity-50"
                        >
                          {cancellingGoalId === goal.goal_id ? "Cancelling..." : "Cancel Goal"}
                        </button>
                      )}
                    </div>
                  </div>

                  {/* Badges */}
                  <div className="mt-4 flex flex-wrap gap-2 text-xs font-semibold">
                    <span
                      className={`rounded-full px-3 py-1 ${
                        goal.priority === "Critical"
                          ? "bg-rose-50 text-rose-700"
                          : goal.priority === "Important"
                          ? "bg-teal-50 text-teal-700"
                          : "bg-slate-100 text-slate-600"
                      }`}
                    >
                      {goal.priority}
                    </span>
                    <span
                      className={`rounded-full px-3 py-1 ${
                        goal.flexibility === "Fixed"
                          ? "bg-amber-50 text-amber-800"
                          : "bg-slate-100 text-slate-600"
                      }`}
                    >
                      {goal.flexibility}
                    </span>
                    <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">
                      Status: {goal.status}
                    </span>
                    <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">
                      Inflation: {(goal.inflation_rate * 100).toFixed(1)}%
                    </span>
                    <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">
                      {goal.mapped_assets.length} asset{goal.mapped_assets.length === 1 ? "" : "s"} mapped
                    </span>
                  </div>

                  {/* Financial Snapshot */}
                  <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
                    <div className="rounded-xl border border-slate-100 bg-slate-50/70 p-3.5">
                      <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Today&apos;s Cost</p>
                      <p className="mt-1 text-base font-extrabold text-navy-900">{formatINR(goal.today_cost)}</p>
                    </div>

                    <div className="rounded-xl border border-slate-100 bg-slate-50/70 p-3.5">
                      <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Future Target</p>
                      <p className="mt-1 text-base font-extrabold text-navy-900">{formatINR(goal.future_target)}</p>
                    </div>

                    <div className="rounded-xl border border-slate-100 bg-slate-50/70 p-3.5">
                      <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Projected Mapped Assets</p>
                      <p className="mt-1 text-base font-extrabold text-teal-800">
                        {formatINR(goal.projected_mapped_asset_value)}
                      </p>
                    </div>

                    <div className="rounded-xl border border-slate-100 bg-slate-50/70 p-3.5">
                      <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Funding Gap</p>
                      <p
                        className={`mt-1 text-base font-extrabold ${
                          goal.funding_gap > 0 ? "text-rose-700" : "text-teal-700"
                        }`}
                      >
                        {formatINR(goal.funding_gap)}
                      </p>
                    </div>
                  </div>

                  {/* Mapped Assets Details Expansion if any */}
                  {goal.mapped_assets.length > 0 && (
                    <div className="mt-4 border-t border-slate-100 pt-3">
                      <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Mapped Asset Details</p>
                      <div className="mt-2 divide-y divide-slate-100">
                        {goal.mapped_assets.map((m, idx) => (
                          <div key={m.mapping_id || idx} className="flex flex-wrap items-center justify-between py-1.5 text-xs text-slate-600">
                            <span className="font-semibold text-navy-900">
                              {m.asset_name || "Asset"}
                            </span>
                            <div className="flex items-center gap-4">
                              <span>
                                Allocation: {m.allocation_type === "currency" ? formatINR(m.allocation_value) : `${m.allocation_value}%`}
                                {" "}({formatINR(m.allocated_amount)})
                              </span>
                              <span>Return: {(m.expected_return * 100).toFixed(1)}% ({m.return_frequency})</span>
                              <span className="font-bold text-teal-800">Proj: {formatINR(m.projected_value)}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </article>
              );
            })}
          </section>
        )}

        {/* 12. GOAL FORM UX (DefinedGoal Compliant) */}
        {isFormOpen && (
          <section
            aria-labelledby="goal-form-heading"
            className="max-h-[calc(100vh-220px)] overflow-y-auto rounded-[28px] border border-teal-200 bg-teal-50/50 p-5 shadow-soft sm:p-6"
          >
            <div className="mb-4 flex items-start justify-between gap-4 border-b border-teal-100 pb-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-700">
                  {formData.goal_id ? "Edit Defined Goal" : "New Defined Goal"}
                </p>
                <h2 id="goal-form-heading" className="mt-1 text-xl font-extrabold text-navy-900">
                  Configure Goal &amp; Asset Mapping
                </h2>
                <p className="mt-1 text-xs text-slate-500">
                  Values are calculated authoritatively by the Planvesto Goal Engine on save or preview.
                </p>
              </div>
              <button
                type="button"
                onClick={handleCancelForm}
                className="text-sm font-bold text-slate-500 hover:text-navy-900"
              >
                ✕ Cancel
              </button>
            </div>

            {formError && (
              <div className="mb-6 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-700" role="alert">
                {formError}
              </div>
            )}

            <div className="space-y-5">
              {/* SECTION 1: GOAL INFORMATION */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-teal-800">
                  1. Goal Information
                </h3>
                <div className="mt-2 grid gap-3 sm:grid-cols-2">
                  <div>
                    <label htmlFor="form-preset-name" className="block text-sm font-semibold text-navy-900">Goal Name</label>
                    <select
                      id="form-preset-name"
                      value={formData.preset_name}
                      onChange={(e) => {
                        const val = e.target.value;
                        setFormData((prev) => ({
                          ...prev,
                          preset_name: val,
                          goal_name: val === "Other" ? prev.custom_name : val,
                        }));
                      }}
                      className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-navy-900 outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-100"
                    >
                      <option value="">Select a common goal</option>
                      {PRESET_GOAL_NAMES.map((opt) => (
                        <option key={opt} value={opt}>
                          {opt}
                        </option>
                      ))}
                    </select>
                  </div>

                  {formData.preset_name === "Other" && (
                    <div>
                      <label htmlFor="form-custom-name" className="block text-sm font-semibold text-navy-900">Custom Goal Name</label>
                      <input
                        id="form-custom-name"
                        type="text"
                        placeholder="e.g. Master's Degree Abroad"
                        value={formData.custom_name}
                        onChange={(e) =>
                          setFormData((prev) => ({
                            ...prev,
                            custom_name: e.target.value,
                            goal_name: e.target.value,
                          }))
                        }
                        className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-navy-900 outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-100"
                      />
                    </div>
                  )}

                </div>
              </div>

              {/* SECTION 2: GOAL COST */}
              <div className="border-t border-teal-100 pt-4">
                <h3 className="text-xs font-bold uppercase tracking-wider text-teal-800">
                  2. Goal Cost &amp; Inflation
                </h3>
                <div className="mt-2 grid gap-3 sm:grid-cols-2">
                  <div>
                    <label htmlFor="form-today-cost" className="block text-sm font-semibold text-navy-900">
                      Today&apos;s Cost (₹)
                    </label>
                    <div className="relative mt-1.5">
                      <span className="pointer-events-none absolute left-4 top-3 text-sm font-bold text-slate-400">
                        ₹
                      </span>
                      <input
                        id="form-today-cost"
                        type="number"
                        min="1"
                        step="1000"
                        placeholder="e.g. 2500000"
                        value={formData.today_cost}
                        onChange={(e) =>
                          setFormData((prev) => ({ ...prev, today_cost: e.target.value }))
                        }
                        className="w-full rounded-xl border border-slate-200 bg-white pl-8 pr-4 py-2.5 text-sm font-medium text-navy-900 outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-100"
                      />
                    </div>
                  </div>

                  <div>
                    <label htmlFor="form-inflation-rate" className="block text-sm font-semibold text-navy-900">
                      Inflation Rate (%)
                    </label>
                    <div className="relative mt-1.5">
                      <input
                        id="form-inflation-rate"
                        type="number"
                        min="0"
                        max="30"
                        step="0.1"
                        placeholder="6.0"
                        value={formData.inflation_rate}
                        onChange={(e) =>
                          setFormData((prev) => ({ ...prev, inflation_rate: e.target.value }))
                        }
                        className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-navy-900 outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-100"
                      />
                      <span className="pointer-events-none absolute right-4 top-3 text-sm font-bold text-slate-400">
                        %
                      </span>
                    </div>
                    <p className="mt-1.5 text-xs text-slate-500">
                      Planvesto uses inflation to estimate what this goal may cost at the target date.
                    </p>
                  </div>
                </div>
              </div>

              {/* SECTION 3: TIMING & CHARACTERISTICS */}
              <div className="border-t border-teal-100 pt-4">
                <h3 className="text-xs font-bold uppercase tracking-wider text-teal-800">3. Timing &amp; Goal Characteristics</h3>
                <div className="mt-2 grid gap-3 sm:grid-cols-4">
                  <div>
                    <label htmlFor="form-target-date" className="block text-sm font-semibold text-navy-900">Target Month &amp; Year</label>
                    <input id="form-target-date" type="month" value={formData.target_date} onChange={(e) => setFormData((prev) => ({ ...prev, target_date: e.target.value }))} className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm font-medium text-navy-900 outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-100" />
                  </div>
                  <div>
                    <label htmlFor="form-priority" className="block text-sm font-semibold text-navy-900">Priority</label>
                    <select id="form-priority" value={formData.priority} onChange={(e) => setFormData((prev) => ({ ...prev, priority: e.target.value as GoalPriority }))} className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm font-medium text-navy-900 outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-100">
                      {goalPriorities.map((p) => <option key={p} value={p}>{p}</option>)}
                    </select>
                  </div>
                  <div>
                    <label htmlFor="form-flexibility" className="block text-sm font-semibold text-navy-900">Flexibility</label>
                    <select id="form-flexibility" value={formData.flexibility} onChange={(e) => setFormData((prev) => ({ ...prev, flexibility: e.target.value as GoalFlexibility }))} className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm font-medium text-navy-900 outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-100">
                      {goalFlexibilities.map((f) => <option key={f} value={f}>{f}</option>)}
                    </select>
                  </div>
                  <div>
                    <label htmlFor="form-status" className="block text-sm font-semibold text-navy-900">Status</label>
                    <select id="form-status" value={formData.status} onChange={(e) => setFormData((prev) => ({ ...prev, status: e.target.value as GoalStatus }))} className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm font-medium text-navy-900 outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-100">
                      {goalStatuses.map((status) => <option key={status} value={status}>{status}</option>)}
                    </select>
                  </div>
                </div>
              </div>

              {/* SECTION 5: ASSET MAPPING */}
              <div className="border-t border-teal-100 pt-4">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                  <div>
                    <h3 className="text-xs font-bold uppercase tracking-wider text-teal-800">
                      5. Asset Mapping
                    </h3>
                    <p className="mt-0.5 text-xs text-slate-500">
                      Connect specific assets to back this goal. One asset may be partially mapped across multiple goals.
                    </p>
                  </div>
                  {assets.length > 0 && (
                    <button
                      type="button"
                      onClick={handleAddMappingRow}
                      className="inline-flex items-center gap-1.5 rounded-lg border border-teal-600 bg-white px-3 py-1.5 text-xs font-bold text-teal-700 hover:bg-teal-50"
                    >
                      + Map Asset
                    </button>
                  )}
                </div>

                {assets.length === 0 ? (
                  <p className="mt-4 rounded-xl border border-dashed border-slate-300 bg-white p-4 text-sm text-slate-500">
                    No assets recorded in this planning unit. You can still save this goal without mapped assets.
                  </p>
                ) : formData.asset_mappings.length === 0 ? (
                  <div className="mt-4 rounded-xl border border-dashed border-slate-300 bg-white p-6 text-center">
                    <p className="text-sm text-slate-500">No assets mapped to this goal yet.</p>
                    <button
                      type="button"
                      onClick={handleAddMappingRow}
                      className="mt-3 inline-flex items-center gap-1.5 text-xs font-bold text-teal-700 underline underline-offset-4 hover:text-teal-900"
                    >
                      + Map an asset to fund this goal
                    </button>
                  </div>
                ) : (
                  <div className="mt-4 space-y-3">
                    {formData.asset_mappings.map((mapping, idx) => (
                      <AssetMappingRow
                        key={mapping.id}
                        index={idx}
                        mapping={mapping}
                        assets={assets}
                        onChange={(changes) => handleUpdateMappingRow(mapping.id, changes)}
                        onRemove={() => handleRemoveMappingRow(mapping.id)}
                      />
                    ))}
                  </div>
                )}
              </div>

              {/* 8. PREVIEW / CALCULATION RESULT (Read-only) */}
              <div className="border-t border-teal-100 pt-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-xs font-bold uppercase tracking-wider text-teal-800">
                      6. Calculation Preview (Read-Only)
                    </h3>
                    <p className="mt-0.5 text-xs text-slate-500">
                      Evaluated dynamically by POST /api/goals/calculate without persisting to the database.
                    </p>
                  </div>
                  <button
                    type="button"
                    disabled={isPreviewing || isSaving}
                    onClick={handleCalculatePreview}
                    className="inline-flex items-center gap-1.5 rounded-xl border border-teal-600 bg-teal-50 px-4 py-2 text-xs font-bold text-teal-800 transition hover:bg-teal-100 disabled:opacity-50"
                  >
                    {isPreviewing ? "Calculating..." : "⚡ Calculate / Preview"}
                  </button>
                </div>

                {previewResult && (
                  <div className="mt-4 rounded-2xl border border-teal-200 bg-white p-5 shadow-sm">
                    <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                      <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                        Preview Engine Output
                      </span>
                      <FundingStatusBadge status={previewResult.funding_status} />
                    </div>

                    <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
                      <div>
                        <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Duration</p>
                        <p className="mt-1 text-lg font-extrabold text-navy-900">{previewResult.duration_years} yrs</p>
                      </div>

                      <div>
                        <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Future Target</p>
                        <p className="mt-1 text-lg font-extrabold text-navy-900">{formatINR(previewResult.future_target)}</p>
                      </div>

                      <div>
                        <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Projected Assets</p>
                        <p className="mt-1 text-lg font-extrabold text-teal-700">
                          {formatINR(previewResult.projected_mapped_asset_value)}
                        </p>
                      </div>

                      <div>
                        <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Funding Gap</p>
                        <p
                          className={`mt-1 text-lg font-extrabold ${
                            previewResult.funding_gap > 0 ? "text-rose-700" : "text-teal-700"
                          }`}
                        >
                          {formatINR(previewResult.funding_gap)}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Form Action Buttons */}
              <div className="sticky bottom-0 flex flex-col-reverse items-stretch gap-3 border-t border-teal-100 bg-teal-50/95 pt-3 pb-1 backdrop-blur sm:flex-row sm:justify-end">
                <button
                  type="button"
                  onClick={handleCancelForm}
                  className="rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-navy-900 transition hover:border-slate-300"
                >
                  Cancel
                </button>

                <button
                  type="button"
                  disabled={isSaving || isPreviewing}
                  onClick={handleSaveGoal}
                  className="rounded-xl bg-teal-700 px-6 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {isSaving ? "Saving to DefinedGoal..." : formData.goal_id ? "Save Changes" : "Save Defined Goal"}
                </button>
              </div>
            </div>
          </section>
        )}
      </div>
    </main>
  );
}

// ============================================================================
// SUB-COMPONENTS
// ============================================================================

function FundingStatusBadge({ status }: { status: FundingStatus }) {
  if (status === "Shortfall") {
    return (
      <span className="inline-flex items-center rounded-md border border-rose-200 bg-rose-50 px-2.5 py-0.5 text-xs font-black uppercase tracking-wider text-rose-700">
        SHORTFALL
      </span>
    );
  }
  if (status === "On Track") {
    return (
      <span className="inline-flex items-center rounded-md border border-teal-200 bg-teal-50 px-2.5 py-0.5 text-xs font-black uppercase tracking-wider text-teal-800">
        ON TRACK
      </span>
    );
  }
  return (
    <span className="inline-flex items-center rounded-md border border-blue-200 bg-blue-50 px-2.5 py-0.5 text-xs font-black uppercase tracking-wider text-blue-800">
      OVERFUNDED
    </span>
  );
}

function AssetMappingRow({
  index,
  mapping,
  assets,
  onChange,
  onRemove,
}: {
  index: number;
  mapping: FormAssetMapping;
  assets: AssetRecord[];
  onChange: (changes: Partial<FormAssetMapping>) => void;
  onRemove: () => void;
}) {
  const assetSelectId = useId();
  const allocTypeId = useId();
  const allocValId = useId();
  const expReturnId = useId();
  const freqId = useId();

  const selectedAsset = assets.find((a) => a.asset_id === mapping.asset_id);

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-xs">
      <div className="grid gap-3 sm:grid-cols-6 sm:items-end">
        {/* Asset */}
        <div className="sm:col-span-2">
          <label htmlFor={assetSelectId} className="block text-xs font-bold uppercase tracking-wider text-slate-400">
            Asset #{index + 1}
          </label>
          <select
            id={assetSelectId}
            value={mapping.asset_id}
            onChange={(e) => onChange({ asset_id: e.target.value })}
            className="mt-1 w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-medium text-navy-900 outline-none focus:border-teal-500"
          >
            {assets.map((a) => (
              <option key={a.asset_id} value={a.asset_id}>
                {a.asset_name} ({formatINR(a.current_value)})
              </option>
            ))}
          </select>
          {selectedAsset && (
            <p className="mt-1 text-[11px] text-slate-400">
              Balance: {formatINR(selectedAsset.current_value)}
            </p>
          )}
        </div>

        {/* Allocation Type */}
        <div>
          <label htmlFor={allocTypeId} className="block text-xs font-bold uppercase tracking-wider text-slate-400">
            Type
          </label>
          <select
            id={allocTypeId}
            value={mapping.allocation_type}
            onChange={(e) =>
              onChange({ allocation_type: e.target.value as AssetMappingAllocationType })
            }
            className="mt-1 w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-medium text-navy-900 outline-none focus:border-teal-500"
          >
            <option value="percentage">Percentage (%)</option>
            <option value="currency">Rupees (₹)</option>
          </select>
        </div>

        {/* Allocation Value */}
        <div>
          <label htmlFor={allocValId} className="block text-xs font-bold uppercase tracking-wider text-slate-400">
            Allocation {mapping.allocation_type === "percentage" ? "(%)" : "(₹)"}
          </label>
          <input
            id={allocValId}
            type="number"
            min="0"
            step={mapping.allocation_type === "percentage" ? "1" : "1000"}
            placeholder={mapping.allocation_type === "percentage" ? "100" : "50000"}
            value={mapping.allocation_value}
            onChange={(e) => onChange({ allocation_value: e.target.value })}
            className="mt-1 w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-medium text-navy-900 outline-none focus:border-teal-500"
          />
        </div>

        {/* Expected Return Override */}
        <div>
          <label htmlFor={expReturnId} className="block text-xs font-bold uppercase tracking-wider text-slate-400">
            Exp. Return (%)
          </label>
          <input
            id={expReturnId}
            type="number"
            min="0"
            max="100"
            step="0.1"
            placeholder="Default"
            value={mapping.expected_return}
            onChange={(e) => onChange({ expected_return: e.target.value })}
            className="mt-1 w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-medium text-navy-900 outline-none focus:border-teal-500"
          />
        </div>

        {/* Return Frequency & Remove */}
        <div className="flex items-center gap-2">
          <div className="flex-1">
            <label htmlFor={freqId} className="block text-xs font-bold uppercase tracking-wider text-slate-400">
              Frequency
            </label>
            <select
              id={freqId}
              value={mapping.return_frequency}
              onChange={(e) => onChange({ return_frequency: e.target.value as ReturnFrequency })}
              className="mt-1 w-full rounded-lg border border-slate-200 bg-white px-2 py-2 text-xs font-medium text-navy-900 outline-none focus:border-teal-500"
            >
              {returnFrequencies.map((f) => (
                <option key={f} value={f}>
                  {f.charAt(0).toUpperCase() + f.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <button
            type="button"
            onClick={onRemove}
            title="Remove mapping"
            className="mt-4 rounded-lg p-2 text-slate-400 hover:bg-rose-50 hover:text-rose-600"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  );
}