"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getGoals, getDefinedGoalVersions, getPlanningUnitId, type DefinedGoalVersionSummary, type GoalSummary } from "../../../lib/api/goals";

function money(value: number) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(value);
}

export default function GoalHistoryPage() {
  const [goals, setGoals] = useState<GoalSummary[]>([]);
  const [goalId, setGoalId] = useState("");
  const [versions, setVersions] = useState<DefinedGoalVersionSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const pu = getPlanningUnitId();
        if (!pu) throw new Error("Planning unit is not available. Please complete onboarding first.");
        const data = await getGoals(pu);
        if (!active) return;
        setGoals(data);
        if (data[0]) setGoalId(data[0].goal_id);
      } catch (err) { if (active) setError(err instanceof Error ? err.message : "Unable to load goals."); }
      finally { if (active) setLoading(false); }
    })();
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!goalId) { setVersions([]); return; }
    let active = true;
    (async () => {
      setWorking(true); setError(null);
      try {
        const pu = getPlanningUnitId();
        if (!pu) throw new Error("Planning unit is not available.");
        const data = await getDefinedGoalVersions(pu, goalId);
        if (active) setVersions(data);
      } catch (err) { if (active) setError(err instanceof Error ? err.message : "Unable to load goal history."); }
      finally { if (active) setWorking(false); }
    })();
    return () => { active = false; };
  }, [goalId]);

  if (loading) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-6xl"><div className="h-10 w-72 animate-pulse rounded-xl bg-slate-200" /><div className="mt-6 h-80 animate-pulse rounded-3xl bg-white" /></div></main>;

  return <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900"><div className="mx-auto max-w-6xl space-y-6 p-6 lg:p-10">
    <header><Link href="/investor/goal-planner" className="text-sm font-semibold text-teal-700">← Goal Planner</Link><p className="mt-6 text-sm font-semibold uppercase tracking-[0.16em] text-teal-700">Goal lifecycle</p><h1 className="mt-1 text-3xl font-extrabold tracking-tight">Goal History</h1><p className="mt-2 max-w-3xl text-sm text-slate-500">Every DefinedGoal calculation is preserved as an immutable version. The latest version is explicitly marked by the backend.</p></header>
    {error && <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">{error}</div>}
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><label className="block max-w-xl"><span className="text-sm font-bold text-slate-700">Goal</span><select value={goalId} onChange={(e) => setGoalId(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm"><option value="">Select goal</option>{goals.map((g) => <option key={g.goal_id} value={g.goal_id}>{g.goal_name}</option>)}</select></label></section>
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><div className="flex items-center justify-between"><div><h2 className="text-lg font-bold">DefinedGoal Versions</h2><p className="mt-1 text-sm text-slate-500">{working ? "Loading…" : `${versions.length} version${versions.length === 1 ? "" : "s"}`}</p></div></div><div className="mt-5 overflow-x-auto"><table className="w-full min-w-[900px] text-left text-sm"><thead className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400"><tr><th className="px-3 py-3">Version</th><th className="px-3 py-3">Status</th><th className="px-3 py-3">Today's Cost</th><th className="px-3 py-3">Future Target</th><th className="px-3 py-3">Mapped Value</th><th className="px-3 py-3">Funding Gap</th><th className="px-3 py-3">Created</th></tr></thead><tbody>{versions.map((v) => <tr key={v.defined_goal_id} className="border-b border-slate-100"><td className="px-3 py-4 font-bold">v{v.version}</td><td className="px-3 py-4"><span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${v.is_latest ? "bg-teal-50 text-teal-700" : "bg-slate-100 text-slate-600"}`}>{v.is_latest ? "Latest" : v.funding_status}</span></td><td className="px-3 py-4">{money(v.today_cost)}</td><td className="px-3 py-4">{money(v.future_target)}</td><td className="px-3 py-4">{money(v.projected_mapped_asset_value)}</td><td className="px-3 py-4">{money(v.funding_gap)}</td><td className="px-3 py-4 text-slate-500">{new Date(v.created_at).toLocaleString("en-IN")}</td></tr>)}</tbody></table>{!versions.length && <p className="py-10 text-center text-sm text-slate-500">No DefinedGoal versions found for this goal.</p>}</div></section>
  </div></main>;
}
