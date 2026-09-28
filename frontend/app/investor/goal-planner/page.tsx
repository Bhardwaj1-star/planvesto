"use client";

import { useEffect, useState, useId } from "react";
import Link from "next/link";
import InvestorHeader from "../../../components/InvestorHeader";
import { supabase } from "../../../lib/supabase";
import { apiRequest, ApiError } from "../../../lib/api/client";
import { formatINR, formatTargetMonthYear } from "../../../lib/onboarding/goals/goals";
import {
  goalFlexibilities,
  goalStatuses,
  goalTypes,
  returnFrequencies,
  type AssetMappingAllocationType,
  type DefinedGoal,
  type FundingStatus,
  type GoalDynamicDetails,
  type GoalFlexibility,
  type GoalInput,
  type GoalStatus,
  type ReturnFrequency,
} from "../../../lib/onboarding/goals/types";

type AssetRecord = { asset_id: string; asset_name: string; current_value: number };
type LiabilityRecord = { id: string; name: string; outstandingAmount: number; interestRate: number | null; emi: number | null; endDate: string | null };
type FormAssetMapping = { id: string; asset_id: string; allocation_type: AssetMappingAllocationType; allocation_value: string; expected_return: string; return_frequency: ReturnFrequency };
type DynamicDetails = Pick<GoalDynamicDetails, "lifeExpectancy" | "desiredLifestyleMonthlyExpense" | "desiredPassiveIncomeAmount" | "educationForWhom" | "marriageForWhom" | "vacationFrequency" | "vacationType" | "selectedLiabilityId" | "philanthropyContributionAmount" | "otherGoalName">;
type GoalFormData = { goal_id: string | null; goal_type: string; today_cost: string; target_date: string; flexibility: GoalFlexibility | ""; status: GoalStatus; inflation_rate: string; dynamic_details: DynamicDetails; asset_mappings: FormAssetMapping[] };

const DEFAULT_INFLATION_PERCENT = "6.0";
const SPECIAL_GOALS = new Set(["Retirement / Financial Freedom", "Passive Income", "Debt Repayment", "Philanthropy"]);
const emptyDynamicDetails = (): DynamicDetails => ({ lifeExpectancy: "", desiredLifestyleMonthlyExpense: "", desiredPassiveIncomeAmount: "", educationForWhom: "", marriageForWhom: "", vacationFrequency: "", vacationType: "", selectedLiabilityId: "", philanthropyContributionAmount: "", otherGoalName: "" });

function createEmptyForm(): GoalFormData {
  return { goal_id: null, goal_type: "", today_cost: "", target_date: "", flexibility: "Flexible", status: "Active", inflation_rate: DEFAULT_INFLATION_PERCENT, dynamic_details: emptyDynamicDetails(), asset_mappings: [] };
}

function definedGoalToForm(goal: DefinedGoal): GoalFormData {
  const metadata = (goal.version_metadata || {}) as Record<string, unknown>;
  const raw = (metadata.dynamic_details || {}) as Partial<DynamicDetails>;
  return {
    goal_id: goal.goal_id,
    goal_type: goal.goal_type,
    today_cost: String(goal.today_cost || ""),
    target_date: `${goal.target_year}-${String(goal.target_month).padStart(2, "0")}`,
    flexibility: goal.flexibility || "Flexible",
    status: goal.status || "Active",
    inflation_rate: (goal.inflation_rate * 100).toFixed(1),
    dynamic_details: { ...emptyDynamicDetails(), ...raw },
    asset_mappings: goal.mapped_assets.map((m) => ({ id: m.mapping_id || crypto.randomUUID(), asset_id: m.asset_id, allocation_type: m.allocation_type, allocation_value: String(m.allocation_value), expected_return: m.expected_return != null ? (m.expected_return * 100).toFixed(1) : "", return_frequency: (m.return_frequency as ReturnFrequency) || "annual" })),
  };
}

function isSpecialGoal(goalType: string) { return SPECIAL_GOALS.has(goalType); }

function getAvailableAssets(allAssets: AssetRecord[], existingGoals: DefinedGoal[], currentGoalId: string | null) {
  const allocated = new Map<string, number>();
  for (const goal of existingGoals) {
    if (currentGoalId && goal.goal_id === currentGoalId) continue;
    for (const mapping of goal.mapped_assets || []) {
      const asset = allAssets.find((a) => a.asset_id === mapping.asset_id);
      if (!asset || asset.current_value <= 0) continue;
      const share = mapping.allocation_type === "percentage"
        ? Number(mapping.allocation_value) / 100
        : Number(mapping.allocation_value) / asset.current_value;
      if (Number.isFinite(share) && share > 0) allocated.set(mapping.asset_id, (allocated.get(mapping.asset_id) || 0) + share);
    }
  }
  return allAssets.filter((asset) => (allocated.get(asset.asset_id) || 0) < 1 - 1e-9);
}

function DynamicField({ label, value, onChange, type = "text", placeholder }: { label: string; value: string; onChange: (value: string) => void; type?: string; placeholder?: string }) {
  return <div><label className="block text-xs font-bold uppercase tracking-wider text-slate-500">{label}</label><input type={type} value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-sm font-medium text-navy-900 outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-100" /></div>;
}

export default function GoalPlannerPage() {
  const [goals, setGoals] = useState<DefinedGoal[]>([]);
  const [assets, setAssets] = useState<AssetRecord[]>([]);
  const [liabilities, setLiabilities] = useState<LiabilityRecord[]>([]);
  const [planningUnitId, setPlanningUnitId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [isPreviewing, setIsPreviewing] = useState(false);
  const [cancellingGoalId, setCancellingGoalId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [lastSavedGoalId, setLastSavedGoalId] = useState<string | null>(null);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [formData, setFormData] = useState<GoalFormData>(createEmptyForm());
  const [previewResult, setPreviewResult] = useState<DefinedGoal | null>(null);

  useEffect(() => {
    let active = true;
    async function loadData() {
      try {
        setIsLoading(true); setError(null);
        const { data: sessionData, error: sessionError } = await supabase.auth.getSession();
        if (sessionError) throw sessionError;
        if (!sessionData?.session) throw new Error("You must be logged in to access the Goal Planner.");
        let puId = typeof window !== "undefined" ? window.localStorage.getItem("planvesto-planning-unit-id") : null;
        if (!puId) {
          const { data } = await supabase.from("planning_units").select("planning_unit_id").eq("user_id", sessionData.session.user.id).order("created_at", { ascending: false }).limit(1).maybeSingle();
          if (data?.planning_unit_id) puId = String(data.planning_unit_id);
        }
        if (!puId) throw new Error("No planning unit found. Please complete personal information first.");
        if (typeof window !== "undefined") window.localStorage.setItem("planvesto-planning-unit-id", puId);
        if (active) setPlanningUnitId(puId);
        const [{ data: assetRows, error: assetError }, { data: liabilityRows }] = await Promise.all([
          supabase.from("assets").select("asset_id, asset_name, current_value").eq("planning_unit_id", puId).order("created_at"),
          supabase.from("liabilities").select("liability_id, liability_name, outstanding_amount, interest_rate, emi_amount, end_date").eq("planning_unit_id", puId).order("created_at"),
        ]);
        if (assetError) throw assetError;
        if (active) {
          setAssets((assetRows || []).map((a) => ({ asset_id: a.asset_id, asset_name: a.asset_name, current_value: Number(a.current_value) || 0 })));
          setLiabilities((liabilityRows || []).map((l) => ({ id: l.liability_id, name: l.liability_name, outstandingAmount: Number(l.outstanding_amount || 0), interestRate: l.interest_rate == null ? null : Number(l.interest_rate), emi: l.emi_amount == null ? null : Number(l.emi_amount), endDate: l.end_date || null })));
        }
        const { data: goalRows, error: goalError } = await supabase.from("goals").select("goal_id, goal_name, target_amount, target_date, flexibility").eq("planning_unit_id", puId).order("created_at");
        if (goalError) throw goalError;
        const loaded: DefinedGoal[] = [];
        for (const g of goalRows || []) {
          try {
            const dg = await apiRequest<DefinedGoal>(`/api/goals/${g.goal_id}/defined/latest?planning_unit_id=${puId}`);
            if (dg.status !== "Cancelled") loaded.push(dg);
          } catch (e) {
            if (e instanceof ApiError && e.status === 404) {
              const [year, month] = String(g.target_date || "").split("-");
              const payload: GoalInput = { planning_unit_id: puId, goal_id: g.goal_id, goal_name: g.goal_name || "Untitled Goal", goal_type: goalTypes.includes(g.goal_name as never) ? g.goal_name : "Others", today_cost: Number(g.target_amount) || 100000, target_month: Number(month) || 12, target_year: Number(year) || new Date().getFullYear() + 3, inflation_rate: 0.06, priority: "Important", flexibility: g.flexibility || "Flexible", status: "Active", asset_mappings: [], dynamic_details: {} };
              loaded.push(await apiRequest<DefinedGoal>("/api/goals", { method: "POST", body: JSON.stringify(payload) }));
            }
          }
        }
        if (active) setGoals(loaded);
      } catch (e) { if (active) setError(e instanceof Error ? e.message : "Unable to load goal planner data."); }
      finally { if (active) setIsLoading(false); }
    }
    loadData();
    return () => { active = false; };
  }, []);

  function updateDynamic(changes: Partial<DynamicDetails>) { setFormData((p) => ({ ...p, dynamic_details: { ...p.dynamic_details, ...changes } })); }
  function buildGoalInputPayload(): GoalInput | null {
    if (!planningUnitId) { setFormError("Planning unit is missing. Please refresh the page."); return null; }
    const goalType = formData.goal_type;
    if (!goalType) { setFormError("Please select a goal."); return null; }
    const d = formData.dynamic_details;
    const goalName = goalType === "Others" ? d.otherGoalName.trim() : goalType;
    if (!goalName) { setFormError("Please provide a goal name."); return null; }
    let costNum = Number(formData.today_cost);
    if (isSpecialGoal(goalType)) {
      if (goalType === "Retirement / Financial Freedom") costNum = Number(d.desiredLifestyleMonthlyExpense) * 12;
      if (goalType === "Passive Income") costNum = Number(d.desiredPassiveIncomeAmount) * 12;
      if (goalType === "Philanthropy") costNum = Number(d.philanthropyContributionAmount);
      if (goalType === "Debt Repayment") costNum = liabilities.find((l) => l.id === d.selectedLiabilityId)?.outstandingAmount || 0;
    }
    if (!Number.isFinite(costNum) || costNum <= 0) { setFormError("Please enter the required goal amount."); return null; }
    if (!formData.target_date) { setFormError("Please select a target month and year."); return null; }
    const [year, month] = formData.target_date.split("-").map(Number);
    if (!year || !month) { setFormError("Invalid target month or year."); return null; }
    const inflationPercent = Number(formData.inflation_rate);
    if (!Number.isFinite(inflationPercent) || inflationPercent < 0) { setFormError("Please enter a valid inflation rate."); return null; }
    const inflation = inflationPercent / 100;
    return { planning_unit_id: planningUnitId, goal_id: formData.goal_id, goal_name: goalName, goal_type: goalType, today_cost: costNum, target_month: month, target_year: year, inflation_rate: inflation, priority: "Important", flexibility: formData.flexibility || "Flexible", status: formData.status || "Active", asset_mappings: formData.asset_mappings.map((m) => ({ asset_id: m.asset_id, allocation_type: m.allocation_type, allocation_value: Number(m.allocation_value), expected_return: m.expected_return ? Number(m.expected_return) / 100 : null, return_frequency: m.return_frequency })), dynamic_details: d };
  }
  function handleStartAdding() { setFormError(null); setPreviewResult(null); setFormData(createEmptyForm()); setIsFormOpen(true); }
  function handleStartEditing(goal: DefinedGoal) { setFormError(null); setPreviewResult(null); setFormData(definedGoalToForm(goal)); setIsFormOpen(true); }
  function handleCancelForm() { setIsFormOpen(false); setPreviewResult(null); setFormError(null); }
  function handleAddMappingRow() {
    const availableAssets = getAvailableAssets(assets, goals, formData.goal_id);
    if (!availableAssets.length) return;
    setFormData((p) => ({ ...p, asset_mappings: [...p.asset_mappings, { id: crypto.randomUUID(), asset_id: availableAssets[0].asset_id, allocation_type: "percentage", allocation_value: "100", expected_return: "", return_frequency: "annual" }] }));
  }
  function handleRemoveMappingRow(id: string) { setFormData((p) => ({ ...p, asset_mappings: p.asset_mappings.filter((m) => m.id !== id) })); }
  function handleUpdateMappingRow(id: string, changes: Partial<FormAssetMapping>) { setFormData((p) => ({ ...p, asset_mappings: p.asset_mappings.map((m) => m.id === id ? { ...m, ...changes } : m) })); }
  async function handleCalculatePreview() { setFormError(null); const payload = buildGoalInputPayload(); if (!payload) return; try { setIsPreviewing(true); setPreviewResult(await apiRequest<DefinedGoal>("/api/goals/calculate", { method: "POST", body: JSON.stringify(payload) })); } catch (e) { setFormError(e instanceof Error ? e.message : "Unable to calculate goal preview."); } finally { setIsPreviewing(false); } }
  async function handleSaveGoal() {
    setFormError(null); const payload = buildGoalInputPayload(); if (!payload) return;
    try { setIsSaving(true); const saved = await apiRequest<DefinedGoal>("/api/goals", { method: "POST", body: JSON.stringify(payload) }); setLastSavedGoalId(saved.goal_id); setGoals((prev) => { const i = prev.findIndex((g) => g.goal_id === saved.goal_id); if (i < 0) return [...prev, saved]; const next = [...prev]; next[i] = saved; return next; }); setSuccessMessage(formData.goal_id ? `Goal "${saved.goal_name}" updated successfully (v${saved.version}).` : `Goal "${saved.goal_name}" created successfully (v${saved.version}).`); handleCancelForm(); }
    catch (e) { setFormError(e instanceof ApiError ? e.detail || "Failed to save goal." : e instanceof Error ? e.message : "Unable to save goal."); } finally { setIsSaving(false); }
  }
  async function handleCancelGoal(goal: DefinedGoal) {
    if (!window.confirm(`Are you sure you want to mark "${goal.goal_name}" as Cancelled?`)) return;
    try { setCancellingGoalId(goal.goal_id); const payload: GoalInput = { planning_unit_id: goal.planning_unit_id, goal_id: goal.goal_id, investor_id: goal.investor_id, goal_name: goal.goal_name, goal_type: goal.goal_type, today_cost: goal.today_cost, target_month: goal.target_month, target_year: goal.target_year, inflation_rate: goal.inflation_rate, priority: "Important", flexibility: goal.flexibility, status: "Cancelled", asset_mappings: goal.mapped_assets.map((m) => ({ asset_id: m.asset_id, allocation_type: m.allocation_type, allocation_value: m.allocation_value, expected_return: m.expected_return, return_frequency: m.return_frequency })), dynamic_details: goal.version_metadata?.dynamic_details || {} }; const updated = await apiRequest<DefinedGoal>("/api/goals", { method: "POST", body: JSON.stringify(payload) }); setGoals((prev) => prev.filter((g) => g.goal_id !== updated.goal_id)); setSuccessMessage(`Goal "${goal.goal_name}" marked as Cancelled (v${updated.version}).`); }
    catch (e) { setError(e instanceof Error ? e.message : "Unable to cancel goal."); } finally { setCancellingGoalId(null); }
  }
  if (isLoading) return <main className="flex min-h-screen items-center justify-center bg-slate-25"><div className="text-sm font-semibold text-slate-500">Loading your goals...</div></main>;
  const shortfall = goals.filter((g) => g.funding_status === "Shortfall").length; const onTrack = goals.filter((g) => g.funding_status === "On Track").length; const overfunded = goals.filter((g) => g.funding_status === "Overfunded").length;
  const availableAssets = getAvailableAssets(assets, goals, formData.goal_id);
  return <main className="min-h-screen bg-slate-25 text-slate-900"><InvestorHeader eyebrow="Plan" title="Goal Planner" description="Plan your milestones with backend accuracy"><div className="hidden sm:flex items-center gap-4"><Link href="/investor/financial-state" className="text-sm font-semibold text-teal-700">Financial State</Link><Link href="/investor/strategy-builder" className="text-sm font-semibold text-slate-600">Strategy Builder</Link></div></InvestorHeader><div className="mx-auto w-full max-w-[1120px] px-5 py-10 lg:px-8 lg:py-14"><div className="mb-8 flex flex-col justify-between gap-5 sm:flex-row sm:items-end"><div><p className="text-xs font-bold uppercase tracking-[0.16em] text-teal-700">Goal Planner</p><h1 className="mt-2 text-3xl font-extrabold tracking-tight text-navy-900 sm:text-4xl">Financial Goals &amp; Asset Mapping</h1><p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">Create the same goal-specific form used during onboarding, then map assets and preview the existing Goal Engine calculation.</p></div>{!isFormOpen && <button type="button" onClick={handleStartAdding} className="inline-flex items-center justify-center gap-2 rounded-xl bg-teal-700 px-5 py-3 text-sm font-bold text-white">+ Add Goal</button>}</div>{error && <div className="mb-6 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-700">{error}</div>}{successMessage && <div className="mb-6 flex flex-col gap-3 rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700 sm:flex-row sm:items-center sm:justify-between"><span>{successMessage}</span>{lastSavedGoalId && <Link href={`/investor/strategy-builder?goalId=${encodeURIComponent(lastSavedGoalId)}`} className="rounded-lg bg-navy-900 px-4 py-2 text-xs font-bold text-white">Continue to Strategy →</Link>}</div>}{!isFormOpen && <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4"><Metric label="Total Goals" value={goals.length} /><Metric label="Shortfall Goals" value={shortfall} /><Metric label="On Track Goals" value={onTrack} /><Metric label="Overfunded Goals" value={overfunded} /></div>}{!isFormOpen && goals.length === 0 && <div className="rounded-[28px] border border-dashed border-slate-300 bg-white p-12 text-center"><h2 className="text-xl font-extrabold text-navy-900">No goals defined yet</h2><button type="button" onClick={handleStartAdding} className="mt-6 rounded-xl bg-navy-900 px-6 py-3 text-sm font-bold text-white">+ Add Goal</button></div>}{!isFormOpen && goals.length > 0 && <section className="space-y-4">{goals.map((goal) => <GoalCard key={goal.goal_id} goal={goal} cancelling={cancellingGoalId === goal.goal_id} onEdit={() => handleStartEditing(goal)} onCancel={() => handleCancelGoal(goal)} />)}</section>}{isFormOpen && <GoalForm formData={formData} liabilities={liabilities} assets={availableAssets} formError={formError} isSaving={isSaving} isPreviewing={isPreviewing} previewResult={previewResult} updateForm={setFormData} updateDynamic={updateDynamic} onAddAsset={handleAddMappingRow} onRemoveAsset={handleRemoveMappingRow} onUpdateAsset={handleUpdateMappingRow} onCalculate={handleCalculatePreview} onSave={handleSaveGoal} onCancel={handleCancelForm} />}</div></main>;
}
function Metric({ label, value }: { label: string; value: number }) { return <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><p className="text-xs font-bold uppercase tracking-[0.14em] text-slate-400">{label}</p><p className="mt-2 text-3xl font-extrabold text-navy-900">{value}</p></div>; }
function GoalCard({ goal, cancelling, onEdit, onCancel }: { goal: DefinedGoal; cancelling: boolean; onEdit: () => void; onCancel: () => void }) { return <article className={`rounded-2xl border bg-white p-6 shadow-sm ${goal.funding_status === "Shortfall" ? "border-rose-200" : "border-slate-200"}`}><div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between"><div><div className="flex flex-wrap items-center gap-2.5"><h3 className="text-xl font-extrabold text-navy-900">{goal.goal_name}</h3><span className="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-bold text-slate-600">v{goal.version}</span><FundingStatusBadge status={goal.funding_status} /></div><p className="mt-1 text-sm text-slate-500">{goal.goal_type} · Target: {formatTargetMonthYear(goal.target_month, goal.target_year)} · {goal.duration_years} yrs</p></div><div className="flex items-center gap-2 text-sm font-bold"><Link href={`/investor/strategy-builder?goalId=${encodeURIComponent(goal.goal_id)}`} className="rounded-lg bg-navy-900 px-3 py-1.5 text-xs font-bold text-white hover:opacity-90">Plan Strategy →</Link><button type="button" onClick={onEdit} className="rounded-lg px-3 py-1.5 text-teal-700 hover:bg-teal-50">Edit</button><button type="button" disabled={cancelling} onClick={onCancel} className="rounded-lg px-3 py-1.5 text-slate-500 hover:bg-rose-50 disabled:opacity-50">{cancelling ? "Cancelling..." : "Cancel Goal"}</button></div></div><div className="mt-4 flex flex-wrap gap-2 text-xs font-semibold"><span className="rounded-full bg-slate-100 px-3 py-1 text-slate-600">{goal.flexibility}</span><span className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">Status: {goal.status}</span><span className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">Inflation: {(goal.inflation_rate * 100).toFixed(1)}%</span><span className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">{goal.mapped_assets.length} asset{goal.mapped_assets.length === 1 ? "" : "s"} mapped</span></div><div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4"><Snapshot label="Today's Cost" value={formatINR(goal.today_cost)} /><Snapshot label="Future Target" value={formatINR(goal.future_target)} /><Snapshot label="Projected Assets" value={formatINR(goal.projected_mapped_asset_value)} /><Snapshot label="Funding Gap" value={formatINR(goal.funding_gap)} /></div></article>; }
function Snapshot({ label, value }: { label: string; value: string }) { return <div className="rounded-xl border border-slate-100 bg-slate-50/70 p-3.5"><p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">{label}</p><p className="mt-1 text-base font-extrabold text-navy-900">{value}</p></div>; }
function FundingStatusBadge({ status }: { status: FundingStatus }) { const cls = status === "Shortfall" ? "border-rose-200 bg-rose-50 text-rose-700" : status === "On Track" ? "border-teal-200 bg-teal-50 text-teal-800" : "border-blue-200 bg-blue-50 text-blue-800"; return <span className={`inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-black uppercase tracking-wider ${cls}`}>{status}</span>; }

function GoalForm({ formData, liabilities, assets, formError, isSaving, isPreviewing, previewResult, updateForm, updateDynamic, onAddAsset, onRemoveAsset, onUpdateAsset, onCalculate, onSave, onCancel }: { formData: GoalFormData; liabilities: LiabilityRecord[]; assets: AssetRecord[]; formError: string | null; isSaving: boolean; isPreviewing: boolean; previewResult: DefinedGoal | null; updateForm: React.Dispatch<React.SetStateAction<GoalFormData>>; updateDynamic: (changes: Partial<DynamicDetails>) => void; onAddAsset: () => void; onRemoveAsset: (id: string) => void; onUpdateAsset: (id: string, changes: Partial<FormAssetMapping>) => void; onCalculate: () => void; onSave: () => void; onCancel: () => void }) {
  const type = formData.goal_type; const d = formData.dynamic_details; const special = isSpecialGoal(type); const selectedLiability = liabilities.find((l) => l.id === d.selectedLiabilityId);
  return <section className="rounded-[28px] border border-slate-200 bg-white shadow-soft"><div className="border-b border-slate-200 px-5 py-5 sm:px-7"><div className="flex items-start justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-700">{formData.goal_id ? "Edit Goal" : "Create Goal"}</p><h2 className="mt-1 text-2xl font-extrabold tracking-tight text-navy-900">{type ? "Shape your goal" : "Select a goal"}</h2><p className="mt-1 text-sm text-slate-500">{type ? "Only the information relevant to the selected goal is shown." : "Start by selecting the goal you are planning for."}</p></div><button type="button" onClick={onCancel} className="rounded-lg px-3 py-2 text-sm font-bold text-slate-500 hover:bg-slate-100">Cancel</button></div></div>{formError && <div className="mx-5 mt-5 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-700 sm:mx-7">{formError}</div>}<div className="space-y-5 p-5 sm:p-7"><div className="rounded-2xl border border-slate-200 bg-slate-50/60 p-4 sm:p-5"><h3 className="text-sm font-extrabold text-navy-900">Select a Goal</h3><div className="mt-4"><label className="block text-xs font-bold uppercase tracking-wider text-slate-500">Goal</label><select value={type} onChange={(e) => updateForm((p) => ({ ...p, goal_type: e.target.value, dynamic_details: emptyDynamicDetails(), asset_mappings: [], goal_id: p.goal_id }))} className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-sm font-medium text-navy-900"><option value="">Select a goal</option>{goalTypes.map((g) => <option key={g} value={g}>{g}</option>)}</select></div></div>
      {type ? <>
        {type === "Others" && <DynamicSection title="Goal details"><DynamicField label="Goal Name" value={d.otherGoalName} onChange={(v) => updateDynamic({ otherGoalName: v })} placeholder="e.g. Family milestone" /></DynamicSection>}
        {type === "Retirement / Financial Freedom" && <DynamicSection title="Retirement / Financial Freedom"><div className="grid gap-4 sm:grid-cols-2"><DynamicField label="Life Expectancy" type="number" value={d.lifeExpectancy} onChange={(v) => updateDynamic({ lifeExpectancy: v })} placeholder="e.g. 85" /><DynamicField label="Desired Lifestyle Monthly Expense" type="number" value={d.desiredLifestyleMonthlyExpense} onChange={(v) => updateDynamic({ desiredLifestyleMonthlyExpense: v })} placeholder="₹ per month" /></div></DynamicSection>}
        {type === "Passive Income" && <DynamicSection title="Passive Income"><DynamicField label="Desired Amount" type="number" value={d.desiredPassiveIncomeAmount} onChange={(v) => updateDynamic({ desiredPassiveIncomeAmount: v })} placeholder="₹ per month" /></DynamicSection>}
        {type === "Education" && <DynamicSection title="Education"><Choice label="For Whom" value={d.educationForWhom} options={["Self", "Spouse", "Children"]} onChange={(v) => updateDynamic({ educationForWhom: v as DynamicDetails["educationForWhom"] })} /></DynamicSection>}
        {type === "Marriage" && <DynamicSection title="Marriage"><Choice label="For Whom" value={d.marriageForWhom} options={["Self", "Spouse", "Child", "Other"]} onChange={(v) => updateDynamic({ marriageForWhom: v as DynamicDetails["marriageForWhom"] })} /></DynamicSection>}
        {type === "Dream Home" && <DynamicSection title="Dream Home"><DynamicField label="Preferred Location" value={(d as DynamicDetails & { preferredLocation?: string }).preferredLocation || ""} onChange={(v) => updateDynamic({ preferredLocation: v } as Partial<DynamicDetails>)} placeholder="City / area" /></DynamicSection>}
        {type === "Vehicle" && <DynamicSection title="Vehicle"><div className="grid gap-4 sm:grid-cols-2"><DynamicField label="Vehicle Type" value={(d as DynamicDetails & { vehicleType?: string }).vehicleType || ""} onChange={(v) => updateDynamic({ vehicleType: v } as Partial<DynamicDetails>)} placeholder="e.g. SUV, Sedan, Bike" /><Choice label="Condition" value={(d as DynamicDetails & { vehicleCondition?: string }).vehicleCondition || ""} options={["New", "Used"]} onChange={(v) => updateDynamic({ vehicleCondition: v } as Partial<DynamicDetails>)} /></div></DynamicSection>}
        {type === "Vacation" && <DynamicSection title="Vacation"><div className="grid gap-4 sm:grid-cols-2"><DynamicField label="Frequency" value={d.vacationFrequency} onChange={(v) => updateDynamic({ vacationFrequency: v })} placeholder="e.g. Once a year" /><Choice label="Domestic / International" value={d.vacationType} options={["Domestic", "International"]} onChange={(v) => updateDynamic({ vacationType: v as DynamicDetails["vacationType"] })} /></div></DynamicSection>}
        {type === "Wealth Creation" && <DynamicSection title="Wealth Creation"><DynamicField label="Target Wealth / Corpus" type="number" value={(d as DynamicDetails & { targetWealthCorpus?: string }).targetWealthCorpus || ""} onChange={(v) => updateDynamic({ targetWealthCorpus: v } as Partial<DynamicDetails>)} placeholder="₹" /></DynamicSection>}
        {type === "Debt Repayment" && <DynamicSection title="Debt Repayment"><label className="block text-xs font-bold uppercase tracking-wider text-slate-500">Select Liability</label><select value={d.selectedLiabilityId} onChange={(e) => updateDynamic({ selectedLiabilityId: e.target.value })} className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-sm font-medium text-navy-900"><option value="">Select an existing liability</option>{liabilities.map((l) => <option key={l.id} value={l.id}>{l.name} · {formatINR(l.outstandingAmount)}</option>)}</select>{selectedLiability && <p className="mt-2 text-xs text-slate-500">Outstanding {formatINR(selectedLiability.outstandingAmount)}{selectedLiability.interestRate != null ? ` · ${selectedLiability.interestRate}% interest` : ""}{selectedLiability.emi != null ? ` · EMI ${formatINR(selectedLiability.emi)}` : ""}{selectedLiability.endDate ? ` · Ends ${selectedLiability.endDate}` : ""}</p>}</DynamicSection>}
        {type === "Philanthropy" && <DynamicSection title="Philanthropy"><DynamicField label="Contribution Amount" type="number" value={d.philanthropyContributionAmount} onChange={(v) => updateDynamic({ philanthropyContributionAmount: v })} placeholder="₹" /></DynamicSection>}
        {!special && <DynamicField label="Today's Cost" type="number" value={formData.today_cost} onChange={(v) => updateForm((p) => ({ ...p, today_cost: v }))} placeholder="₹" />}
        <div className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5"><div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"><div><label className="block text-xs font-bold uppercase tracking-wider text-slate-500">Target Month &amp; Year</label><input type="month" value={formData.target_date} onChange={(e) => updateForm((p) => ({ ...p, target_date: e.target.value }))} className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-sm font-medium text-navy-900" /></div><div><label className="block text-xs font-bold uppercase tracking-wider text-slate-500">Flexibility</label><select value={formData.flexibility} onChange={(e) => updateForm((p) => ({ ...p, flexibility: e.target.value as GoalFlexibility }))} className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-sm font-medium text-navy-900">{goalFlexibilities.map((f) => <option key={f} value={f}>{f}</option>)}</select></div><DynamicField label="Inflation Rate (%)" type="number" value={formData.inflation_rate} onChange={(v) => updateForm((p) => ({ ...p, inflation_rate: v }))} placeholder="e.g. 6" /></div></div>
        {type && <div className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5"><div className="flex items-start justify-between gap-3"><div><h3 className="text-sm font-extrabold text-navy-900">Funding assets</h3><p className="mt-0.5 text-xs text-slate-500">Map existing assets intended to fund this goal.</p></div>{assets.length > 0 && <button type="button" onClick={onAddAsset} className="rounded-lg border border-teal-600 bg-white px-3 py-2 text-xs font-bold text-teal-700">+ Map asset</button>}</div>{formData.asset_mappings.map((m, i) => <AssetMappingRow key={m.id} index={i} mapping={m} assets={assets} onChange={(c) => onUpdateAsset(m.id, c)} onRemove={() => onRemoveAsset(m.id)} />)}{!formData.asset_mappings.length && <p className="mt-4 rounded-xl border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-slate-500">No assets mapped to this goal.</p>}</div>}
        {type && <div className="rounded-2xl border border-teal-200 bg-teal-50/50 p-4 sm:p-5"><div className="flex items-center justify-between"><div><h3 className="text-sm font-extrabold text-navy-900">Calculation preview</h3><p className="mt-0.5 text-xs text-slate-500">Existing Goal Engine calculation; no calculation logic changed.</p></div><button type="button" disabled={isPreviewing || isSaving} onClick={onCalculate} className="rounded-lg border border-teal-600 bg-white px-3 py-2 text-xs font-bold text-teal-800">{isPreviewing ? "Calculating..." : "Calculate"}</button></div>{previewResult && <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-4"><Snapshot label="Duration" value={`${previewResult.duration_years} yrs`} /><Snapshot label="Future Target" value={formatINR(previewResult.future_target)} /><Snapshot label="Projected Assets" value={formatINR(previewResult.projected_mapped_asset_value)} /><Snapshot label="Funding Gap" value={formatINR(previewResult.funding_gap)} /></div>}</div>}
        <div className="flex justify-end gap-2 border-t border-slate-200 pt-4"><button type="button" onClick={onCancel} className="rounded-xl border border-slate-200 bg-white px-5 py-2.5 text-sm font-bold text-navy-900">Cancel</button><button type="button" disabled={isSaving || isPreviewing} onClick={onSave} className="rounded-xl bg-teal-700 px-6 py-2.5 text-sm font-bold text-white disabled:opacity-60">{isSaving ? "Saving..." : formData.goal_id ? "Save changes" : "Save goal"}</button></div>
      </> : <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-6 text-center"><p className="text-sm font-semibold text-slate-600">Select a goal above to continue.</p></div>}
    </div>
  </section>;
}
function DynamicSection({ title, children }: { title: string; children: React.ReactNode }) { return <div className="rounded-2xl border border-teal-100 bg-teal-50/30 p-4 sm:p-5"><h3 className="text-sm font-extrabold text-navy-900">{title}</h3><div className="mt-4">{children}</div></div>; }
function Choice({ label, value, options, onChange }: { label: string; value: string; options: readonly string[]; onChange: (value: string) => void }) { return <fieldset><legend className="mb-2 text-xs font-bold uppercase tracking-wider text-slate-500">{label}</legend><div className="grid grid-cols-2 gap-2 sm:grid-cols-3">{options.map((o) => <label key={o} className={`flex cursor-pointer items-center gap-2 rounded-lg border bg-white px-3 py-2.5 text-xs font-semibold ${value === o ? "border-teal-500 ring-2 ring-teal-50" : "border-slate-200"}`}><input type="radio" checked={value === o} onChange={() => onChange(o)} className="h-3.5 w-3.5 accent-teal-600" />{o}</label>)}</div></fieldset>; }
function AssetMappingRow({ index, mapping, assets, onChange, onRemove }: { index: number; mapping: FormAssetMapping; assets: AssetRecord[]; onChange: (changes: Partial<FormAssetMapping>) => void; onRemove: () => void }) { const assetId = useId(); return <div className="mt-3 rounded-xl border border-slate-200 bg-white p-4"><div className="grid gap-3 sm:grid-cols-5 sm:items-end"><div className="sm:col-span-2"><label htmlFor={assetId} className="block text-xs font-bold uppercase tracking-wider text-slate-400">Asset #{index + 1}</label><select id={assetId} value={mapping.asset_id} onChange={(e) => onChange({ asset_id: e.target.value })} className="mt-1 w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-medium text-navy-900">{assets.map((a) => <option key={a.asset_id} value={a.asset_id}>{a.asset_name} ({formatINR(a.current_value)})</option>)}</select></div><div><label className="block text-xs font-bold uppercase tracking-wider text-slate-400">Type</label><select value={mapping.allocation_type} onChange={(e) => onChange({ allocation_type: e.target.value as AssetMappingAllocationType })} className="mt-1 w-full rounded-lg border border-slate-200 px-3 py-2 text-xs"><option value="percentage">Percentage (%)</option><option value="currency">Rupees (₹)</option></select></div><div><label className="block text-xs font-bold uppercase tracking-wider text-slate-400">Allocation</label><input type="number" value={mapping.allocation_value} onChange={(e) => onChange({ allocation_value: e.target.value })} className="mt-1 w-full rounded-lg border border-slate-200 px-3 py-2 text-xs" /></div><div className="flex items-center gap-2"><div className="flex-1"><label className="block text-xs font-bold uppercase tracking-wider text-slate-400">Expected Return %</label><input type="number" value={mapping.expected_return} onChange={(e) => onChange({ expected_return: e.target.value })} className="mt-1 w-full rounded-lg border border-slate-200 px-3 py-2 text-xs" /></div><button type="button" onClick={onRemove} className="mt-4 rounded-lg p-2 text-slate-400 hover:bg-rose-50 hover:text-rose-600">✕</button></div></div></div>; }
