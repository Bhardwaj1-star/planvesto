"use client";

import { useEffect, useId, useMemo, useState } from "react";
import Link from "next/link";
import { InvestorProfileMenu } from "../../../components/InvestorProfileMenu";
import { supabase } from "../../../lib/supabase";
import { apiRequest, ApiError } from "../../../lib/api/client";
import { formatINR, formatTargetMonthYear } from "../../../lib/onboarding/goals/goals";
import {
  goalFlexibilities,
  goalPriorities,
  goalStatuses,
  goalTypes,
  returnFrequencies,
  type AssetMappingAllocationType,
  type AssetMappingInput,
  type DefinedGoal,
  type FundingStatus,
  type GoalFlexibility,
  type GoalInput,
  type GoalPriority,
  type GoalStatus,
  type ReturnFrequency,
} from "../../../lib/onboarding/goals/types";

type AssetRecord = { asset_id: string; asset_name: string; current_value: number };
type DependentRecord = { dependent_id: string; name: string; date_of_birth: string | null };
type Mapping = { id: string; asset_id: string; allocation_type: AssetMappingAllocationType; allocation_value: string; expected_return: string; return_frequency: ReturnFrequency };

type FormData = {
  goal_id: string | null;
  goal_type: string;
  goal_name: string;
  priority: GoalPriority;
  flexibility: GoalFlexibility;
  status: GoalStatus;
  current_cost: string;
  target_date: string;
  inflation_rate: string;
  current_age: string;
  retirement_age: string;
  life_expectancy: string;
  current_monthly_expense: string;
  post_retirement_return_rate: string;
  dependent_id: string;
  child_age: string;
  education_start_age: string;
  current_education_cost: string;
  education_duration_years: string;
  education_inflation_rate: string;
  current_trip_cost: string;
  years_to_first_trip: string;
  repeat_every_years: string;
  number_of_trips: string;
  travel_inflation_rate: string;
  asset_mappings: Mapping[];
};

const DEFAULT_INFLATION = "6";
const SPECIALIZED = new Set(["Retirement", "Child Education", "Travel"]);

function nextMonthDate(years: number) {
  const d = new Date();
  d.setMonth(d.getMonth() + Math.max(1, Math.round(years * 12)));
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
}

function ageFromDob(dob: string | null) {
  if (!dob) return "";
  const birth = new Date(dob);
  if (Number.isNaN(birth.getTime())) return "";
  const now = new Date();
  let age = now.getFullYear() - birth.getFullYear();
  const beforeBirthday = now.getMonth() < birth.getMonth() || (now.getMonth() === birth.getMonth() && now.getDate() < birth.getDate());
  if (beforeBirthday) age -= 1;
  return String(Math.max(0, age));
}

function yearsUntil(dateValue: string) {
  if (!dateValue) return 0;
  const [year, month] = dateValue.split("-").map(Number);
  const now = new Date();
  return Math.max(0, (year - now.getFullYear()) + (month - (now.getMonth() + 1)) / 12);
}

function emptyForm(): FormData {
  return {
    goal_id: null, goal_type: "", goal_name: "", priority: "Important", flexibility: "Flexible", status: "Active",
    current_cost: "", target_date: nextMonthDate(5), inflation_rate: DEFAULT_INFLATION,
    current_age: "", retirement_age: "60", life_expectancy: "85", current_monthly_expense: "",
    post_retirement_return_rate: "8", dependent_id: "", child_age: "", education_start_age: "18",
    current_education_cost: "", education_duration_years: "4", education_inflation_rate: "8",
    current_trip_cost: "", years_to_first_trip: "1", repeat_every_years: "1", number_of_trips: "5", travel_inflation_rate: "6",
    asset_mappings: [],
  };
}

function goalInputFromDefined(g: DefinedGoal): FormData {
  const meta = g.version_metadata?.specialized_data as Record<string, unknown> | undefined;
  return { ...emptyForm(), goal_id: g.goal_id, goal_type: g.goal_type, goal_name: g.goal_name, priority: g.priority as GoalPriority, flexibility: g.flexibility as GoalFlexibility, status: g.status as GoalStatus, current_cost: String(g.today_cost), target_date: `${g.target_year}-${String(g.target_month).padStart(2, "0")}`, inflation_rate: String((g.inflation_rate * 100).toFixed(1)), current_age: String(meta?.current_age ?? ""), retirement_age: String(meta?.target_age ?? ""), life_expectancy: String(meta?.life_expectancy ?? "85"), current_monthly_expense: String(meta?.current_monthly_expense ?? ""), post_retirement_return_rate: String(meta?.post_retirement_return_rate ?? "8"), dependent_id: String(meta?.dependent_id ?? ""), child_age: String(meta?.child_age ?? ""), education_start_age: String(meta?.education_start_age ?? "18"), current_education_cost: String(meta?.current_education_cost ?? ""), education_duration_years: String(meta?.education_duration_years ?? "4"), education_inflation_rate: String(meta?.education_inflation_rate ?? "8"), current_trip_cost: String(meta?.current_trip_cost ?? ""), years_to_first_trip: String(meta?.years_to_first_trip ?? "1"), repeat_every_years: String(meta?.repeat_every_years ?? "1"), number_of_trips: String(meta?.number_of_trips ?? "5"), travel_inflation_rate: String(meta?.travel_inflation_rate ?? "6"), asset_mappings: g.mapped_assets.map((m) => ({ id: m.mapping_id || crypto.randomUUID(), asset_id: m.asset_id, allocation_type: m.allocation_type, allocation_value: String(m.allocation_value), expected_return: String((m.expected_return * 100).toFixed(1)), return_frequency: (m.return_frequency as ReturnFrequency) || "annual" })) };
}

export default function GoalPlannerPage() {
  const [goals, setGoals] = useState<DefinedGoal[]>([]);
  const [assets, setAssets] = useState<AssetRecord[]>([]);
  const [dependents, setDependents] = useState<DependentRecord[]>([]);
  const [planningUnitId, setPlanningUnitId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [isPreviewing, setIsPreviewing] = useState(false);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [step, setStep] = useState<1 | 2>(1);
  const [form, setForm] = useState<FormData>(emptyForm());
  const [preview, setPreview] = useState<DefinedGoal | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    async function load() {
      try {
        const { data: sessionData, error: sessionError } = await supabase.auth.getSession();
        if (sessionError) throw sessionError;
        const session = sessionData.session;
        if (!session) throw new Error("You must be logged in to access the Goal Planner.");
        let pu = typeof window !== "undefined" ? localStorage.getItem("planvesto-planning-unit-id") : null;
        if (!pu) {
          const { data, error: puError } = await supabase.from("planning_units").select("planning_unit_id").eq("user_id", session.user.id).order("created_at", { ascending: false }).limit(1).maybeSingle();
          if (puError) throw puError;
          pu = data?.planning_unit_id ? String(data.planning_unit_id) : null;
          if (pu) localStorage.setItem("planvesto-planning-unit-id", pu);
        }
        if (!pu) throw new Error("No planning unit found. Please complete personal information first.");
        if (active) setPlanningUnitId(pu);

        const [assetRes, depRes, goalRes] = await Promise.all([
          supabase.from("assets").select("asset_id, asset_name, current_value").eq("planning_unit_id", pu).order("created_at"),
          supabase.from("dependents").select("dependent_id, name, date_of_birth").eq("planning_unit_id", pu).order("created_at"),
          supabase.from("goals").select("goal_id").eq("planning_unit_id", pu).order("created_at"),
        ]);
        if (assetRes.error) throw assetRes.error;
        if (depRes.error) throw depRes.error;
        if (goalRes.error) throw goalRes.error;
        if (!active) return;
        setAssets((assetRes.data || []).map((a) => ({ asset_id: a.asset_id, asset_name: a.asset_name, current_value: Number(a.current_value) || 0 })));
        setDependents((depRes.data || []).map((d) => ({ dependent_id: d.dependent_id, name: d.name, date_of_birth: d.date_of_birth })));
        const loaded: DefinedGoal[] = [];
        for (const row of goalRes.data || []) {
          try {
            const dg = await apiRequest<DefinedGoal>(`/api/goals/${row.goal_id}/defined/latest?planning_unit_id=${pu}`);
            if (dg.status !== "Cancelled") loaded.push(dg);
          } catch (e) {
            if (!(e instanceof ApiError && e.status === 404)) continue;
          }
        }
        setGoals(loaded);
      } catch (e) {
        if (active) setError(e instanceof Error ? e.message : "Unable to load goal planner data.");
      } finally {
        if (active) setIsLoading(false);
      }
    }
    load();
    return () => { active = false; };
  }, []);

  const selectedDependent = useMemo(() => dependents.find((d) => d.dependent_id === form.dependent_id), [dependents, form.dependent_id]);

  function update<K extends keyof FormData>(key: K, value: FormData[K]) { setForm((p) => ({ ...p, [key]: value })); }

  function startAdd() { setSuccess(null); setError(null); setFormError(null); setPreview(null); setForm(emptyForm()); setStep(1); setIsFormOpen(true); }
  function startEdit(goal: DefinedGoal) { setSuccess(null); setError(null); setFormError(null); setPreview(null); setForm(goalInputFromDefined(goal)); setStep(2); setIsFormOpen(true); }
  function cancelForm() { setIsFormOpen(false); setPreview(null); setFormError(null); }

  function selectGoal(type: string) {
    setForm((p) => ({ ...p, goal_type: type, goal_name: type, dependent_id: "", child_age: "" }));
    setFormError(null);
    setStep(2);
  }

  function buildPayload(): GoalInput | null {
    if (!planningUnitId || !form.goal_type) { setFormError("Please select a goal type."); return null; }
    const specialized = SPECIALIZED.has(form.goal_type);
    let todayCost = Number(form.current_cost);
    let targetDate = form.target_date;
    let specializedData: Record<string, unknown> = {};

    if (form.goal_type === "Retirement") {
      const currentAge = Number(form.current_age), retirementAge = Number(form.retirement_age), life = Number(form.life_expectancy), expense = Number(form.current_monthly_expense);
      if (!(currentAge > 0 && retirementAge > currentAge && life > retirementAge && expense > 0)) { setFormError("Enter valid current age, retirement age, life expectancy and monthly expense."); return null; }
      todayCost = expense * 12;
      targetDate = nextMonthDate(retirementAge - currentAge);
      specializedData = { current_age: currentAge, retirement_age: retirementAge, life_expectancy: life, current_monthly_expense: expense, expense_inflation_rate: Number(form.inflation_rate) / 100, post_retirement_return_rate: Number(form.post_retirement_return_rate) / 100 };
    } else if (form.goal_type === "Child Education") {
      const childAge = Number(form.child_age), startAge = Number(form.education_start_age), cost = Number(form.current_education_cost);
      if (!form.dependent_id || !(childAge >= 0) || !(startAge > childAge) || !(cost > 0)) { setFormError("Select a dependent and enter valid education details."); return null; }
      todayCost = cost;
      targetDate = nextMonthDate(startAge - childAge);
      specializedData = { dependent_id: form.dependent_id, child_age: childAge, education_start_age: startAge, current_education_cost: cost, education_duration_years: Number(form.education_duration_years) || 4, education_inflation_rate: Number(form.education_inflation_rate) / 100 };
    } else if (form.goal_type === "Travel") {
      const tripCost = Number(form.current_trip_cost), first = Number(form.years_to_first_trip), repeat = Number(form.repeat_every_years), trips = Number(form.number_of_trips);
      if (!(tripCost > 0 && first > 0 && repeat > 0 && trips >= 1)) { setFormError("Enter valid travel cost, first-trip timing, repeat interval and number of trips."); return null; }
      todayCost = tripCost;
      targetDate = nextMonthDate(first);
      specializedData = { current_trip_cost: tripCost, years_to_first_trip: first, repeat_every_years: repeat, number_of_trips: Math.floor(trips), travel_inflation_rate: Number(form.travel_inflation_rate) / 100 };
    } else {
      const cost = Number(form.current_cost);
      if (!(cost > 0) || !form.target_date) { setFormError("Enter the current cost and target date."); return null; }
      todayCost = cost;
      specializedData = specialized ? { current_cost: cost, years_to_goal: yearsUntil(form.target_date), inflation_rate: Number(form.inflation_rate) / 100 } : {};
    }

    const [yearStr, monthStr] = targetDate.split("-");
    const targetYear = Number(yearStr), targetMonth = Number(monthStr);
    if (!(targetYear >= 1900 && targetMonth >= 1 && targetMonth <= 12)) { setFormError("Invalid target date."); return null; }

    const mappings: AssetMappingInput[] = [];
    for (const m of form.asset_mappings) {
      const allocation = Number(m.allocation_value);
      if (!m.asset_id || !(allocation > 0) || (m.allocation_type === "percentage" && allocation > 100)) { setFormError("Check the mapped asset allocations."); return null; }
      mappings.push({ asset_id: m.asset_id, allocation_type: m.allocation_type, allocation_value: allocation, expected_return: m.expected_return ? Number(m.expected_return) / 100 : null, return_frequency: m.return_frequency });
    }
    return { planning_unit_id: planningUnitId, goal_id: form.goal_id, goal_name: form.goal_name, goal_type: form.goal_type, today_cost: todayCost, target_month: targetMonth, target_year: targetYear, inflation_rate: specialized ? null : Number(form.inflation_rate) / 100, priority: form.priority, flexibility: form.flexibility, status: form.status, asset_mappings: mappings, specialized_data: specializedData };
  }

  async function calculate() {
    setFormError(null); const payload = buildPayload(); if (!payload) return;
    try { setIsPreviewing(true); setPreview(await apiRequest<DefinedGoal>("/api/goals/calculate", { method: "POST", body: JSON.stringify(payload) })); }
    catch (e) { setFormError(e instanceof Error ? e.message : "Unable to calculate goal."); }
    finally { setIsPreviewing(false); }
  }

  async function save() {
    setFormError(null); const payload = buildPayload(); if (!payload) return;
    try {
      setIsSaving(true);
      const saved = await apiRequest<DefinedGoal>("/api/goals", { method: "POST", body: JSON.stringify(payload) });
      setGoals((prev) => { const i = prev.findIndex((g) => g.goal_id === saved.goal_id); if (i < 0) return [...prev, saved]; const next = [...prev]; next[i] = saved; return next; });
      setSuccess(form.goal_id ? `Goal "${saved.goal_name}" updated successfully.` : `Goal "${saved.goal_name}" created successfully.`);
      cancelForm();
    } catch (e) { setFormError(e instanceof ApiError ? e.detail : e instanceof Error ? e.message : "Unable to save goal."); }
    finally { setIsSaving(false); }
  }

  function addMapping() { if (!assets.length) return; update("asset_mappings", [...form.asset_mappings, { id: crypto.randomUUID(), asset_id: assets[0].asset_id, allocation_type: "percentage", allocation_value: "100", expected_return: "", return_frequency: "annual" }]); }
  function removeMapping(id: string) { update("asset_mappings", form.asset_mappings.filter((m) => m.id !== id)); }
  function changeMapping(id: string, changes: Partial<Mapping>) { update("asset_mappings", form.asset_mappings.map((m) => m.id === id ? { ...m, ...changes } : m)); }

  if (isLoading) return <main className="flex min-h-screen items-center justify-center bg-slate-25 text-sm font-semibold text-slate-500"><div className="flex flex-col items-center gap-3"><div className="h-8 w-8 animate-spin rounded-full border-2 border-teal-600 border-t-transparent" /><p>Loading your goals...</p></div></main>;

  return (
    <main className="min-h-screen bg-slate-25 text-slate-900">
      <header className="border-b border-slate-200 bg-white"><div className="mx-auto flex h-20 max-w-[1200px] items-center justify-between px-5 lg:px-8"><div><span className="text-xs font-bold uppercase tracking-[0.16em] text-teal-700">Goal Planner</span><p className="text-sm font-semibold text-slate-500">Plan your milestones with backend accuracy</p></div><div className="flex items-center gap-4"><Link href="/investor/financial-state" className="text-sm font-semibold text-teal-700 hover:text-teal-900">Financial State</Link><Link href="/investor/strategy-builder" className="text-sm font-semibold text-slate-600 hover:text-navy-900">Strategy Builder</Link><InvestorProfileMenu /></div></div></header>
      <div className="mx-auto w-full max-w-[1120px] px-5 py-10 lg:px-8 lg:py-14">
        <div className="mb-8 flex flex-col justify-between gap-5 sm:flex-row sm:items-end"><div><p className="text-xs font-bold uppercase tracking-[0.16em] text-teal-700">Goal Planner</p><h1 className="mt-2 text-3xl font-extrabold tracking-tight text-navy-900 sm:text-4xl">Financial Goals &amp; Asset Mapping</h1><p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">Define life milestones, connect your existing assets, and let the Planvesto Goal Engine project future requirements and funding gaps.</p></div>{!isFormOpen && <button type="button" onClick={startAdd} className="inline-flex items-center justify-center gap-2 rounded-xl bg-teal-700 px-5 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-teal-800"><span className="text-base font-black">+</span> Add Goal</button>}</div>
        {error && <div className="mb-6 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-700">{error}</div>}
        {success && <div className="mb-6 rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700">{success}</div>}

        {!isFormOpen && <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4"><Metric title="Total Goals" value={goals.length} /><Metric title="Shortfall Goals" value={goals.filter((g) => g.funding_status === "Shortfall").length} tone="rose" /><Metric title="On Track Goals" value={goals.filter((g) => g.funding_status === "On Track").length} tone="teal" /><Metric title="Overfunded Goals" value={goals.filter((g) => g.funding_status === "Overfunded").length} tone="blue" /></div>}

        {!isFormOpen && goals.length === 0 && <section className="rounded-[28px] border border-dashed border-slate-300 bg-white p-12 text-center shadow-soft"><div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-teal-50 text-2xl font-extrabold text-teal-700">🎯</div><h2 className="mt-4 text-xl font-extrabold text-navy-900">No goals defined yet</h2><p className="mx-auto mt-2 max-w-md text-sm text-slate-500">Add your first financial goal to calculate the future requirement and funding status.</p><button type="button" onClick={startAdd} className="mt-6 rounded-xl bg-navy-900 px-6 py-3 text-sm font-bold text-white">+ Add Goal</button></section>}

        {!isFormOpen && goals.length > 0 && <div className="space-y-4">{goals.map((goal) => <GoalCard key={goal.goal_id} goal={goal} onEdit={() => startEdit(goal)} />)}</div>}

        {isFormOpen && <section className="rounded-[28px] border border-slate-200 bg-white shadow-soft"><div className="border-b border-slate-200 px-5 py-5 sm:px-7"><div className="flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-700">{form.goal_id ? "Edit Goal" : "Create Goal"}</p><h2 className="mt-1 text-2xl font-extrabold tracking-tight text-navy-900">{step === 1 ? "What is the goal?" : form.goal_name}</h2><p className="mt-1 text-sm text-slate-500">{step === 1 ? "Select the goal first. We will only ask for information relevant to it." : "Enter only the information required for this goal."}</p></div><button type="button" onClick={cancelForm} className="rounded-lg px-3 py-2 text-sm font-bold text-slate-500 hover:bg-slate-100">Cancel</button></div></div>
          {formError && <div className="mx-5 mt-5 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-700 sm:mx-7">{formError}</div>}
          <div className="space-y-5 p-5 sm:p-7">
            {step === 1 ? <GoalSelection selected={form.goal_type} onSelect={selectGoal} /> : <>
              <SpecializedFields form={form} update={update} dependents={dependents} selectedDependent={selectedDependent} />
              <CommonGoalSettings form={form} update={update} />
              <AssetSection assets={assets} mappings={form.asset_mappings} onAdd={addMapping} onRemove={removeMapping} onChange={changeMapping} />
              <div className="rounded-2xl border border-teal-200 bg-teal-50/50 p-4 sm:p-5"><div className="flex items-center justify-between gap-3"><div><h3 className="text-sm font-extrabold text-navy-900">Calculation preview</h3><p className="mt-0.5 text-xs text-slate-500">Check the Goal Engine output before saving.</p></div><button type="button" disabled={isPreviewing || isSaving} onClick={calculate} className="rounded-lg border border-teal-600 bg-white px-3 py-2 text-xs font-bold text-teal-800">{isPreviewing ? "Calculating..." : "Calculate"}</button></div>{preview && <Preview result={preview} />}</div>
              <div className="sticky bottom-0 z-10 -mx-5 flex flex-col-reverse gap-2 border-t border-slate-200 bg-white/95 px-5 py-4 backdrop-blur sm:-mx-7 sm:flex-row sm:justify-end sm:px-7"><button type="button" onClick={() => form.goal_id ? cancelForm() : setStep(1)} className="rounded-xl border border-slate-200 bg-white px-5 py-2.5 text-sm font-bold text-navy-900">{form.goal_id ? "Cancel" : "Back"}</button><button type="button" disabled={isSaving || isPreviewing} onClick={save} className="rounded-xl bg-teal-700 px-6 py-2.5 text-sm font-bold text-white disabled:opacity-60">{isSaving ? "Saving..." : form.goal_id ? "Save changes" : "Save goal"}</button></div>
            </>}
          </div>
        </section>}
      </div>
    </main>
  );
}

function Metric({ title, value, tone = "slate" }: { title: string; value: number; tone?: "slate" | "rose" | "teal" | "blue" }) { const styles = { slate: "border-slate-200 bg-white text-navy-900", rose: "border-rose-200 bg-rose-50/60 text-rose-700", teal: "border-teal-200 bg-teal-50/60 text-teal-800", blue: "border-blue-200 bg-blue-50/60 text-blue-800" }; return <div className={`rounded-2xl border p-5 shadow-sm ${styles[tone]}`}><p className="text-xs font-bold uppercase tracking-[0.14em] opacity-70">{title}</p><p className="mt-2 text-3xl font-extrabold">{value}</p></div>; }

function GoalSelection({ selected, onSelect }: { selected: string; onSelect: (value: string) => void }) { return <div className="rounded-2xl border border-slate-200 bg-slate-50/60 p-4 sm:p-6"><div className="mb-5"><h3 className="text-sm font-extrabold text-navy-900">Choose a goal</h3><p className="mt-1 text-xs text-slate-500">This is the only information asked on the first step.</p></div><div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{goalTypes.map((type) => <button key={type} type="button" onClick={() => onSelect(type)} className={`rounded-xl border px-4 py-4 text-left text-sm font-bold transition ${selected === type ? "border-teal-600 bg-teal-50 text-teal-800" : "border-slate-200 bg-white text-navy-900 hover:border-teal-300"}`}>{type}</button>)}</div></div>; }

function SpecializedFields({ form, update, dependents, selectedDependent }: { form: FormData; update: <K extends keyof FormData>(key: K, value: FormData[K]) => void; dependents: DependentRecord[]; selectedDependent?: DependentRecord }) {
  const field = (label: string, key: keyof FormData, placeholder = "") => <div><label className="block text-xs font-bold uppercase tracking-wider text-slate-500">{label}</label><input type="number" min="0" value={String(form[key] ?? "")} placeholder={placeholder} onChange={(e) => update(key, e.target.value as never)} className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-sm font-medium text-navy-900 outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-100" /></div>;
  if (form.goal_type === "Retirement") return <div className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5"><h3 className="text-sm font-extrabold text-navy-900">Retirement requirement</h3><p className="mt-1 text-xs text-slate-500">No target amount is required. The required retirement corpus is calculated from your lifestyle and retirement horizon.</p><div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{field("Current age", "current_age")}{field("Retirement age", "retirement_age", "60")}{field("Life expectancy", "life_expectancy", "85")}{field("Current monthly expense", "current_monthly_expense")}{field("Lifestyle inflation (%)", "inflation_rate", "6")}{field("Post-retirement return (%)", "post_retirement_return_rate", "8")}</div></div>;
  if (form.goal_type === "Child Education") return <div className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5"><h3 className="text-sm font-extrabold text-navy-900">Education requirement</h3><p className="mt-1 text-xs text-slate-500">Select the dependent; age is taken from the existing dependent DOB and is not entered manually.</p><div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3"><div><label className="block text-xs font-bold uppercase tracking-wider text-slate-500">Child / dependent</label><select value={form.dependent_id} onChange={(e) => { const d = dependents.find((x) => x.dependent_id === e.target.value); update("dependent_id", e.target.value); update("child_age", ageFromDob(d?.date_of_birth || null)); }} className="mt-1.5 w-full rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-sm font-medium text-navy-900"><option value="">Select dependent</option>{dependents.map((d) => <option key={d.dependent_id} value={d.dependent_id}>{d.name}</option>)}</select>{selectedDependent && <p className="mt-1 text-xs text-slate-400">Current age: {form.child_age || "—"}</p>}</div>{field("Education start age", "education_start_age", "18")}{field("Current education cost", "current_education_cost")}{field("Education duration (years)", "education_duration_years", "4")}{field("Education inflation (%)", "education_inflation_rate", "8")}</div></div>;
  if (form.goal_type === "Travel") return <div className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5"><h3 className="text-sm font-extrabold text-navy-900">Recurring travel requirement</h3><p className="mt-1 text-xs text-slate-500">Travel is treated as a recurring goal instead of a one-time target.</p><div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{field("Current cost per trip", "current_trip_cost")}{field("Years to first trip", "years_to_first_trip", "1")}{field("Repeat every (years)", "repeat_every_years", "1")}{field("Number of trips", "number_of_trips", "5")}{field("Travel inflation (%)", "travel_inflation_rate", "6")}</div></div>;
  return <div className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5"><h3 className="text-sm font-extrabold text-navy-900">Goal requirement</h3><p className="mt-1 text-xs text-slate-500">Enter the current cost and when you want the goal. The future requirement is calculated automatically.</p><div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3"><div><label className="block text-xs font-bold uppercase tracking-wider text-slate-500">Current cost</label><input type="number" min="1" value={form.current_cost} onChange={(e) => update("current_cost", e.target.value)} className="mt-1.5 w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm" /></div><div><label className="block text-xs font-bold uppercase tracking-wider text-slate-500">Target month</label><input type="month" value={form.target_date} onChange={(e) => update("target_date", e.target.value)} className="mt-1.5 w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm" /></div><div>{field("Inflation (%)", "inflation_rate", "6")}</div></div></div>;
}

function CommonGoalSettings({ form, update }: { form: FormData; update: <K extends keyof FormData>(key: K, value: FormData[K]) => void }) { return <div className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5"><div className="grid gap-4 sm:grid-cols-3"><div><label className="block text-xs font-bold uppercase tracking-wider text-slate-500">Priority</label><select value={form.priority} onChange={(e) => update("priority", e.target.value as GoalPriority)} className="mt-1.5 w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm">{goalPriorities.map((x) => <option key={x}>{x}</option>)}</select></div><div><label className="block text-xs font-bold uppercase tracking-wider text-slate-500">Flexibility</label><select value={form.flexibility} onChange={(e) => update("flexibility", e.target.value as GoalFlexibility)} className="mt-1.5 w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm">{goalFlexibilities.map((x) => <option key={x}>{x}</option>)}</select></div><div><label className="block text-xs font-bold uppercase tracking-wider text-slate-500">Status</label><select value={form.status} onChange={(e) => update("status", e.target.value as GoalStatus)} className="mt-1.5 w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm">{goalStatuses.map((x) => <option key={x}>{x}</option>)}</select></div></div></div>; }

function AssetSection({ assets, mappings, onAdd, onRemove, onChange }: { assets: AssetRecord[]; mappings: Mapping[]; onAdd: () => void; onRemove: (id: string) => void; onChange: (id: string, changes: Partial<Mapping>) => void }) { return <div className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5"><div className="flex items-center justify-between"><div><h3 className="text-sm font-extrabold text-navy-900">Funding assets</h3><p className="mt-1 text-xs text-slate-500">Map existing assets intended to fund this goal.</p></div>{assets.length > 0 && <button type="button" onClick={onAdd} className="rounded-lg border border-teal-600 bg-white px-3 py-2 text-xs font-bold text-teal-700">+ Map asset</button>}</div>{mappings.length === 0 ? <p className="mt-4 rounded-xl border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-slate-500">No assets mapped to this goal.</p> : <div className="mt-4 space-y-2">{mappings.map((m, i) => <AssetRow key={m.id} index={i} mapping={m} assets={assets} onChange={(c) => onChange(m.id, c)} onRemove={() => onRemove(m.id)} />)}</div>}</div>; }

function AssetRow({ index, mapping, assets, onChange, onRemove }: { index: number; mapping: Mapping; assets: AssetRecord[]; onChange: (c: Partial<Mapping>) => void; onRemove: () => void }) { const a = assets.find((x) => x.asset_id === mapping.asset_id); const id = useId(); return <div className="rounded-xl border border-slate-200 bg-slate-50 p-4"><div className="grid gap-3 sm:grid-cols-5"><div className="sm:col-span-2"><label className="block text-xs font-bold uppercase tracking-wider text-slate-400">Asset #{index + 1}</label><select id={id} value={mapping.asset_id} onChange={(e) => onChange({ asset_id: e.target.value })} className="mt-1 w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs">{assets.map((x) => <option key={x.asset_id} value={x.asset_id}>{x.asset_name} ({formatINR(x.current_value)})</option>)}</select></div><div><label className="block text-xs font-bold uppercase tracking-wider text-slate-400">Type</label><select value={mapping.allocation_type} onChange={(e) => onChange({ allocation_type: e.target.value as AssetMappingAllocationType })} className="mt-1 w-full rounded-lg border border-slate-200 bg-white px-2 py-2 text-xs"><option value="percentage">Percentage</option><option value="currency">Rupees</option></select></div><div><label className="block text-xs font-bold uppercase tracking-wider text-slate-400">Allocation</label><input type="number" min="0" value={mapping.allocation_value} onChange={(e) => onChange({ allocation_value: e.target.value })} className="mt-1 w-full rounded-lg border border-slate-200 bg-white px-2 py-2 text-xs" /></div><div><label className="block text-xs font-bold uppercase tracking-wider text-slate-400">Expected return %</label><input type="number" min="0" value={mapping.expected_return} placeholder="Default" onChange={(e) => onChange({ expected_return: e.target.value })} className="mt-1 w-full rounded-lg border border-slate-200 bg-white px-2 py-2 text-xs" /></div></div><div className="mt-2 flex justify-between text-[11px] text-slate-400"><span>Balance: {a ? formatINR(a.current_value) : "—"}</span><button type="button" onClick={onRemove} className="font-bold text-rose-600">Remove</button></div></div>; }

function Preview({ result }: { result: DefinedGoal }) { return <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-4">{[["Duration", `${result.duration_years} yrs`], ["Future target", formatINR(result.future_target)], ["Projected assets", formatINR(result.projected_mapped_asset_value)], ["Funding gap", formatINR(result.funding_gap)]].map(([k, v]) => <div key={k} className="rounded-xl border border-teal-100 bg-white px-3 py-3"><p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">{k}</p><p className={`mt-1 text-base font-extrabold ${k === "Funding gap" && result.funding_gap > 0 ? "text-rose-700" : "text-navy-900"}`}>{v}</p></div>)}</div>; }

function GoalCard({ goal, onEdit }: { goal: DefinedGoal; onEdit: () => void }) { return <article className={`rounded-2xl border bg-white p-6 shadow-sm ${goal.funding_status === "Shortfall" ? "border-rose-200/90" : "border-slate-200"}`}><div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between"><div><div className="flex flex-wrap items-center gap-2.5"><h3 className="text-xl font-extrabold text-navy-900">{goal.goal_name}</h3><span className="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-bold text-slate-600">v{goal.version}</span><FundingBadge status={goal.funding_status} /></div><p className="mt-1 text-sm text-slate-500">{goal.goal_type} · Target {formatTargetMonthYear(goal.target_month, goal.target_year)}</p></div><button type="button" onClick={onEdit} className="rounded-lg border border-slate-200 px-3 py-2 text-xs font-bold text-navy-900">Edit</button></div><div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4"><Snapshot title="Today's Cost" value={formatINR(goal.today_cost)} /><Snapshot title="Future Target" value={formatINR(goal.future_target)} /><Snapshot title="Projected Assets" value={formatINR(goal.projected_mapped_asset_value)} /><Snapshot title="Funding Gap" value={formatINR(goal.funding_gap)} danger={goal.funding_gap > 0} /></div></article>; }
function Snapshot({ title, value, danger }: { title: string; value: string; danger?: boolean }) { return <div className="rounded-xl border border-slate-100 bg-slate-50/70 p-3.5"><p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">{title}</p><p className={`mt-1 text-base font-extrabold ${danger ? "text-rose-700" : "text-navy-900"}`}>{value}</p></div>; }
function FundingBadge({ status }: { status: FundingStatus }) { const c = status === "Shortfall" ? "border-rose-200 bg-rose-50 text-rose-700" : status === "On Track" ? "border-teal-200 bg-teal-50 text-teal-800" : "border-blue-200 bg-blue-50 text-blue-800"; return <span className={`inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-black uppercase tracking-wider ${c}`}>{status}</span>; }
