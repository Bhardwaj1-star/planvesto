"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import InvestorHeader from "../../../components/InvestorHeader";
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

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
      <InvestorHeader
        eyebrow="Review"
        title="Goal History"
        description="Every DefinedGoal calculation is preserved as an immutable version. The latest version is explicitly marked by the backend."
      />
      <div className="mx-auto max-w-6xl space-y-6 p-6 lg:p-10">
        <div>
          <Link href="/investor/goal-planner" className="inline-flex items-center gap-1.5 text-sm font-semibold text-teal-700 hover:underline">
            ← Back to Goal Planner
          </Link>
        </div>
        {error && <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">{error}</div>}
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><label className="block max-w-xl"><span className="text-sm font-bold text-slate-700">Goal</span><select value={goalId} onChange={(e) => setGoalId(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm"><option value="">Select goal</option>{goals.map((g) => <option key={g.goal_id} value={g.goal_id}>{g.goal_name}</option>)}</select></label></section>
      </div>
    </main>
  );
}
