"use client";

import { useEffect, useState } from "react";
import { InvestorProfileMenu } from "../../../components/InvestorProfileMenu";
import { supabase } from "../../../lib/supabase";
import { ApiError, apiRequest } from "../../../lib/api/client";
import { formatINR, formatTargetMonthYear } from "../../../lib/onboarding/goals/goals";
import { goalFlexibilities, goalPriorities, goalStatuses, type AssetMappingAllocationType, type AssetMappingInput, type DefinedGoal, type GoalInput, type GoalType } from "../../../lib/onboarding/goals/types";

type Asset = { asset_id: string; asset_name: string; current_value: number };
type Dependent = { dependent_id: string; name: string; date_of_birth: string; relationship?: string | null };
type Mapping = AssetMappingInput & { id: string; expected_return_text: string };
type Form = {
  goal_id: string | null; goal_type: GoalType | ""; goal_name: string; today_cost: string; target_date: string; inflation_rate: string;
  priority: string; flexibility: string; status: string; retirement_age: string; life_expectancy: string; post_retirement_return: string;
  dependent_id: string; education_start_age: string; education_inflation_rate: string; repeat_every_years: string; number_of_trips: string;
  travel_inflation_rate: string; asset_mappings: Mapping[];
};

const specializedTypes: GoalType[] = ["Retirement", "Child Education", "Travel"];
const genericTypes: GoalType[] = ["Emergency Fund", "Child Marriage", "Home Purchase", "Vehicle", "Business", "Wealth Creation", "Other"];

function emptyForm(): Form {
  const d = new Date();
  return { goal_id: null, goal_type: "", goal_name: "", today_cost: "", target_date: `${d.getFullYear() + 5}-${String(d.getMonth() + 1).padStart(2, "0")}`, inflation_rate: "6", priority: "Important", flexibility: "Flexible", status: "Active", retirement_age: "60", life_expectancy: "85", post_retirement_return: "8", dependent_id: "", education_start_age: "18", education_inflation_rate: "8", repeat_every_years: "2", number_of_trips: "5", travel_inflation_rate: "6", asset_mappings: [] };
}

function toForm(goal: DefinedGoal): Form {
  const d = (goal.version_metadata?.goal_details || {}) as Record<string, unknown>;
  return { ...emptyForm(), goal_id: goal.goal_id, goal_type: goal.goal_type as GoalType, goal_name: goal.goal_name, today_cost: String(goal.today_cost), target_date: `${goal.target_year}-${String(goal.target_month).padStart(2, "0")}`, inflation_rate: String((goal.inflation_rate * 100).toFixed(1)), priority: goal.priority, flexibility: goal.flexibility, status: goal.status, retirement_age: String(d.retirement_age ?? 60), life_expectancy: String(d.life_expectancy ?? 85), post_retirement_return: String(Number(d.post_retirement_return ?? .08) * 100), dependent_id: String(d.dependent_id ?? ""), education_start_age: String(d.education_start_age ?? 18), education_inflation_rate: String(Number(d.education_inflation_rate ?? .08) * 100), repeat_every_years: String(d.repeat_every_years ?? 2), number_of_trips: String(d.number_of_trips ?? 5), travel_inflation_rate: String(Number(d.travel_inflation_rate ?? .06) * 100), asset_mappings: goal.mapped_assets.map((m, i) => ({ id: m.mapping_id || `m-${i}`, asset_id: m.asset_id, allocation_type: m.allocation_type, allocation_value: m.allocation_value, expected_return: m.expected_return, expected_return_text: m.expected_return ? String(m.expected_return * 100) : "", return_frequency: m.return_frequency })) };
}

export default function GoalPlannerPage() {
  const [planningUnitId, setPlanningUnitId] = useState<string | null>(null);
  const [goals, setGoals] = useState<DefinedGoal[]>([]);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [dependents, setDependents] = useState<Dependent[]>([]);
  const [form, setForm] = useState<Form>(emptyForm());
  const [open, setOpen] = useState(false);
  const [preview, setPreview] = useState<DefinedGoal | null>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const { data: s, error: se } = await supabase.auth.getSession(); if (se) throw se; if (!s.session) throw new Error("You must be logged in to access the Goal Planner.");
        let pu = localStorage.getItem("planvesto-planning-unit-id");
        if (!pu) { const { data, error: e } = await supabase.from("planning_units").select("planning_unit_id").eq("user_id", s.session.user.id).order("created_at", { ascending: false }).limit(1).maybeSingle(); if (e) throw e; pu = data?.planning_unit_id ? String(data.planning_unit_id) : null; if (pu) localStorage.setItem("planvesto-planning-unit-id", pu); }
        if (!pu) throw new Error("No planning unit found. Please complete personal information first.");
        const [{ data: a, error: ae }, { data: d, error: de }, { data: rows, error: ge }] = await Promise.all([
          supabase.from("assets").select("asset_id, asset_name, current_value").eq("planning_unit_id", pu).order("created_at"),
          supabase.from("dependents").select("dependent_id, name, date_of_birth, relationship").eq("planning_unit_id", pu).order("created_at"),
          supabase.from("goals").select("goal_id, goal_name, target_amount, target_date, priority, flexibility").eq("planning_unit_id", pu).order("created_at")
        ]);
        if (ae) throw ae; if (de) throw de; if (ge) throw ge;
        const loaded: DefinedGoal[] = [];
        for (const row of rows || []) { try { const g = await apiRequest<DefinedGoal>(`/api/goals/${row.goal_id}/defined/latest?planning_unit_id=${pu}`); if (g.status !== "Cancelled") loaded.push(g); } catch (e) { if (e instanceof ApiError && e.status === 404) { try { loaded.push(await apiRequest<DefinedGoal>("/api/goals", { method: "POST", body: JSON.stringify({ planning_unit_id: pu, goal_id: row.goal_id, goal_name: row.goal_name || "Untitled Goal", goal_type: "Other", today_cost: Number(row.target_amount) || 100000, target_month: Number((row.target_date || "").split("-")[1]) || 12, target_year: Number((row.target_date || "").split("-")[0]) || new Date().getFullYear() + 3, inflation_rate: .06, priority: row.priority || "Important", flexibility: row.flexibility || "Flexible", status: "Active", asset_mappings: [] }) })); } catch {} } } }
        if (alive) { setPlanningUnitId(pu); setAssets((a || []).map(x => ({ ...x, current_value: Number(x.current_value) || 0 }))); setDependents((d || []) as Dependent[]); setGoals(loaded); }
      } catch (e) { if (alive) setError(e instanceof Error ? e.message : "Unable to load Goal Planner."); } finally { if (alive) setLoading(false); }
    })(); return () => { alive = false; };
  }, []);

  const patch = (p: Partial<Form>) => setForm(x => ({ ...x, ...p }));
  const specialized = specializedTypes.includes(form.goal_type as GoalType);

  function addMapping() { if (!assets.length) return; const a = assets[0]; patch({ asset_mappings: [...form.asset_mappings, { id: crypto.randomUUID(), asset_id: a.asset_id, allocation_type: "percentage", allocation_value: 100, expected_return: null, expected_return_text: "", return_frequency: "annual" }] }); }

  function buildPayload(): GoalInput | null {
    if (!planningUnitId || !form.goal_type) { setFormError("Select a goal type."); return null; }
    if (!form.goal_name.trim()) { setFormError("Enter a goal name."); return null; }
    const details: Record<string, string | number | boolean | null | string[]> = {};
    if (form.goal_type === "Retirement") { details.retirement_age = Number(form.retirement_age); details.life_expectancy = Number(form.life_expectancy); details.post_retirement_return = Number(form.post_retirement_return) / 100; }
    if (form.goal_type === "Child Education") { if (!form.dependent_id) { setFormError("Select the child from Dependents."); return null; } details.dependent_id = form.dependent_id; details.education_start_age = Number(form.education_start_age); details.current_cost = Number(form.today_cost); details.education_inflation_rate = Number(form.education_inflation_rate) / 100; }
    if (form.goal_type === "Travel") { details.current_trip_cost = Number(form.today_cost); details.repeat_every_years = Number(form.repeat_every_years); details.number_of_trips = Number(form.number_of_trips); details.travel_inflation_rate = Number(form.travel_inflation_rate) / 100; }
    const mappings: AssetMappingInput[] = form.asset_mappings.map(m => ({ asset_id: m.asset_id, allocation_type: m.allocation_type, allocation_value: Number(m.allocation_value), expected_return: m.expected_return_text ? Number(m.expected_return_text) / 100 : null, return_frequency: m.return_frequency }));
    if (mappings.some(m => !Number.isFinite(m.allocation_value) || m.allocation_value <= 0 || (m.allocation_type === "percentage" && m.allocation_value > 100))) { setFormError("Check asset allocation values."); return null; }
    const [year, month] = form.target_date.split("-").map(Number);
    return { planning_unit_id: planningUnitId, goal_id: form.goal_id, goal_name: form.goal_name.trim(), goal_type: form.goal_type, today_cost: specialized ? null : Number(form.today_cost), target_month: specialized ? null : month, target_year: specialized ? null : year, inflation_rate: specialized ? null : Number(form.inflation_rate) / 100, priority: form.priority, flexibility: form.flexibility, status: form.status, goal_details: details, asset_mappings: mappings };
  }

  async function calculate(save: boolean) { setFormError(null); const payload = buildPayload(); if (!payload) return; setBusy(true); try { const result = await apiRequest<DefinedGoal>(save ? "/api/goals" : "/api/goals/calculate", { method: "POST", body: JSON.stringify(payload) }); if (save) { setGoals(prev => { const i = prev.findIndex(g => g.goal_id === result.goal_id); if (i < 0) return [...prev, result]; const n = [...prev]; n[i] = result; return n; }); setOpen(false); setPreview(null); } else setPreview(result); } catch (e) { setFormError(e instanceof Error ? e.message : "Goal calculation failed."); } finally { setBusy(false); } }

  if (loading) return <main className="flex min-h-screen items-center justify-center text-sm font-semibold text-slate-500">Loading Goal Planner…</main>;
  return <main className="min-h-screen bg-slate-25 text-slate-900"><header className="border-b border-slate-200 bg-white"><div className="mx-auto flex h-20 max-w-[1200px] items-center justify-between px-5"><div><p className="text-xs font-bold uppercase tracking-widest text-teal-700">Goal Planner</p><p className="text-sm font-semibold text-slate-500">Goal-type driven planning</p></div><InvestorProfileMenu /></div></header><div className="mx-auto max-w-[1120px] px-5 py-10">
    {error && <div className="mb-5 rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm font-semibold text-rose-700">{error}</div>}
    {!open && <div className="mb-8 flex items-end justify-between gap-4"><div><h1 className="text-3xl font-extrabold text-navy-900">Financial Goals</h1><p className="mt-2 text-sm text-slate-500">Retirement, education and recurring travel use dedicated calculations; other goals remain target-based.</p></div><button onClick={() => { patch(emptyForm()); setOpen(true); setError(null); }} className="rounded-xl bg-teal-700 px-5 py-3 text-sm font-bold text-white">+ Add Goal</button></div>}
    {open && <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><div className="mb-6 flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-widest text-teal-700">{form.goal_id ? "Edit goal" : "New goal"}</p><h2 className="mt-1 text-2xl font-extrabold">Define the requirement</h2></div><button onClick={() => setOpen(false)} className="text-sm font-bold text-slate-500">Cancel</button></div>
      {formError && <div className="mb-5 rounded-xl border border-rose-200 bg-rose-50 p-3 text-sm font-semibold text-rose-700">{formError}</div>}
      <div className="grid gap-4 sm:grid-cols-2"><Field label="Goal type"><select value={form.goal_type} onChange={e => { const t = e.target.value as GoalType; patch({ goal_type: t, goal_name: t }); }} className="input"><option value="">Select goal type</option>{specializedTypes.map(t => <option key={t}>{t}</option>)}{genericTypes.map(t => <option key={t}>{t}</option>)}</select></Field><Field label="Goal name"><input className="input" value={form.goal_name} onChange={e => patch({ goal_name: e.target.value })} placeholder="e.g. Retirement at 60" /></Field></div>
      {form.goal_type === "Retirement" && <div className="mt-5 rounded-2xl border border-teal-200 bg-teal-50/50 p-5"><h3 className="font-extrabold">Retirement requirement</h3><p className="mt-1 text-xs text-slate-500">Current age and monthly expenses are taken from existing investor and expense data.</p><div className="mt-4 grid gap-4 sm:grid-cols-3"><Field label="Retirement age"><input className="input" type="number" min="1" value={form.retirement_age} onChange={e => patch({ retirement_age: e.target.value })}/></Field><Field label="Life expectancy"><input className="input" type="number" min="1" value={form.life_expectancy} onChange={e => patch({ life_expectancy: e.target.value })}/></Field><Field label="Post-retirement return %"><input className="input" type="number" min="0" step="0.1" value={form.post_retirement_return} onChange={e => patch({ post_retirement_return: e.target.value })}/></Field></div></div>}
      {form.goal_type === "Child Education" && <div className="mt-5 rounded-2xl border border-teal-200 bg-teal-50/50 p-5"><h3 className="font-extrabold">Education requirement</h3><p className="mt-1 text-xs text-slate-500">Child age is derived from the selected dependent's date of birth.</p><div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4"><Field label="Dependent"><select className="input" value={form.dependent_id} onChange={e => patch({ dependent_id: e.target.value })}><option value="">Select child</option>{dependents.map(d => <option key={d.dependent_id} value={d.dependent_id}>{d.name}{d.relationship ? ` · ${d.relationship}` : ""}</option>)}</select></Field><Field label="Current education cost"><input className="input" type="number" min="1" value={form.today_cost} onChange={e => patch({ today_cost: e.target.value })}/></Field><Field label="Education start age"><input className="input" type="number" min="1" value={form.education_start_age} onChange={e => patch({ education_start_age: e.target.value })}/></Field><Field label="Education inflation %"><input className="input" type="number" min="0" step="0.1" value={form.education_inflation_rate} onChange={e => patch({ education_inflation_rate: e.target.value })}/></Field></div></div>}
      {form.goal_type === "Travel" && <div className="mt-5 rounded-2xl border border-teal-200 bg-teal-50/50 p-5"><h3 className="font-extrabold">Recurring travel requirement</h3><p className="mt-1 text-xs text-slate-500">The planner calculates the inflated cost across repeated trips.</p><div className="mt-4 grid gap-4 sm:grid-cols-4"><Field label="Current trip cost"><input className="input" type="number" min="1" value={form.today_cost} onChange={e => patch({ today_cost: e.target.value })}/></Field><Field label="Repeat every (years)"><input className="input" type="number" min="1" value={form.repeat_every_years} onChange={e => patch({ repeat_every_years: e.target.value })}/></Field><Field label="Number of trips"><input className="input" type="number" min="1" value={form.number_of_trips} onChange={e => patch({ number_of_trips: e.target.value })}/></Field><Field label="Travel inflation %"><input className="input" type="number" min="0" step="0.1" value={form.travel_inflation_rate} onChange={e => patch({ travel_inflation_rate: e.target.value })}/></Field></div></div>}
      {form.goal_type && !specialized && <div className="mt-5 grid gap-4 sm:grid-cols-3"><Field label="Today's cost"><input className="input" type="number" min="1" value={form.today_cost} onChange={e => patch({ today_cost: e.target.value })}/></Field><Field label="Target month"><input className="input" type="month" value={form.target_date} onChange={e => patch({ target_date: e.target.value })}/></Field><Field label="Inflation %"><input className="input" type="number" min="0" step="0.1" value={form.inflation_rate} onChange={e => patch({ inflation_rate: e.target.value })}/></Field></div>}
      <div className="mt-5 grid gap-4 sm:grid-cols-3"><Field label="Priority"><select className="input" value={form.priority} onChange={e => patch({ priority: e.target.value })}>{goalPriorities.map(x => <option key={x}>{x}</option>)}</select></Field><Field label="Flexibility"><select className="input" value={form.flexibility} onChange={e => patch({ flexibility: e.target.value })}>{goalFlexibilities.map(x => <option key={x}>{x}</option>)}</select></Field><Field label="Status"><select className="input" value={form.status} onChange={e => patch({ status: e.target.value })}>{goalStatuses.map(x => <option key={x}>{x}</option>)}</select></Field></div>
      <div className="mt-5 rounded-2xl border border-slate-200 p-5"><div className="flex items-center justify-between"><div><h3 className="font-extrabold">Funding assets</h3><p className="text-xs text-slate-500">Optional existing assets mapped to this goal.</p></div><button onClick={addMapping} className="rounded-lg border border-teal-600 px-3 py-2 text-xs font-bold text-teal-700">+ Map asset</button></div>{form.asset_mappings.map(m => <div key={m.id} className="mt-3 grid gap-2 sm:grid-cols-5"><select className="input" value={m.asset_id} onChange={e => patch({ asset_mappings: form.asset_mappings.map(x => x.id === m.id ? { ...x, asset_id: e.target.value } : x) })}>{assets.map(a => <option key={a.asset_id} value={a.asset_id}>{a.asset_name} ({formatINR(a.current_value)})</option>)}</select><select className="input" value={m.allocation_type} onChange={e => patch({ asset_mappings: form.asset_mappings.map(x => x.id === m.id ? { ...x, allocation_type: e.target.value as AssetMappingAllocationType } : x) })}><option value="percentage">%</option><option value="currency">₹</option></select><input className="input" type="number" min="0" value={m.allocation_value} onChange={e => patch({ asset_mappings: form.asset_mappings.map(x => x.id === m.id ? { ...x, allocation_value: Number(e.target.value) } : x) })}/><input className="input" type="number" min="0" step="0.1" placeholder="Return %" value={m.expected_return_text} onChange={e => patch({ asset_mappings: form.asset_mappings.map(x => x.id === m.id ? { ...x, expected_return_text: e.target.value } : x) })}/><button onClick={() => patch({ asset_mappings: form.asset_mappings.filter(x => x.id !== m.id) })} className="text-xs font-bold text-rose-600">Remove</button></div>)}</div>
      {preview && <div className="mt-5 grid grid-cols-2 gap-3 rounded-2xl border border-teal-200 bg-teal-50 p-5 sm:grid-cols-4"><Metric label="Required target" value={formatINR(preview.future_target)}/><Metric label="Target" value={formatTargetMonthYear(preview.target_month, preview.target_year)}/><Metric label="Funding gap" value={formatINR(preview.funding_gap)}/><Metric label="Monthly contribution" value={formatINR((preview as DefinedGoal & { required_monthly_contribution?: number }).required_monthly_contribution || 0)}/></div>}
      <div className="mt-6 flex justify-end gap-3"><button disabled={busy} onClick={() => calculate(false)} className="rounded-xl border border-teal-600 px-5 py-2.5 text-sm font-bold text-teal-700">{busy ? "Calculating…" : "Calculate"}</button><button disabled={busy} onClick={() => calculate(true)} className="rounded-xl bg-teal-700 px-6 py-2.5 text-sm font-bold text-white">{busy ? "Saving…" : "Save goal"}</button></div>
    </section>}
    {!open && <section className="space-y-4">{goals.map(g => <article key={g.goal_id} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><div className="flex items-start justify-between gap-3"><div><h2 className="text-xl font-extrabold">{g.goal_name}</h2><p className="text-sm text-slate-500">{g.goal_type} · Target {formatTargetMonthYear(g.target_month, g.target_year)}</p></div><button onClick={() => { setForm(toForm(g)); setOpen(true); }} className="text-sm font-bold text-teal-700">Edit</button></div><div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4"><Metric label="Future target" value={formatINR(g.future_target)}/><Metric label="Projected assets" value={formatINR(g.projected_mapped_asset_value)}/><Metric label="Funding gap" value={formatINR(g.funding_gap)}/><Metric label="Status" value={g.funding_status}/></div></article>)}</section>}
    {!open && goals.length === 0 && <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center text-sm text-slate-500">No goals defined yet.</div>}
  </div></main>;
}

function Field({ label, children }: { label: string; children: React.ReactNode }) { return <label className="block"><span className="text-xs font-bold uppercase tracking-wider text-slate-500">{label}</span>{children}</label>; }
function Metric({ label, value }: { label: string; value: string }) { return <div className="rounded-xl border border-slate-100 bg-white p-3"><p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">{label}</p><p className="mt-1 text-sm font-extrabold text-navy-900">{value}</p></div>; }
