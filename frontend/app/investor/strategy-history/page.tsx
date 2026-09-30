"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import InvestorHeader from "../../../components/InvestorHeader";
import { loadGoalPlannerData } from "../../../lib/onboarding/persistence";
import { getLatestStrategyRun, getPlanningUnitId, type StrategyRun } from "../../../lib/api/strategy";
import { getCurrentPrimaryStrategy, getStrategyVersionHistory, type StrategyVersion } from "../../../lib/api/strategy-version";

type GoalOption = { id: string; name: string };

export default function StrategyHistoryPage() {
  const [goals, setGoals] = useState<GoalOption[]>([]);
  const [selectedGoalId, setSelectedGoalId] = useState("");
  const [run, setRun] = useState<StrategyRun | null>(null);
  const [versions, setVersions] = useState<StrategyVersion[]>([]);
  const [primary, setPrimary] = useState<Awaited<ReturnType<typeof getCurrentPrimaryStrategy>>>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const data = await loadGoalPlannerData();
        const nextGoals = (data?.goals ?? []).map((goal) => ({ id: goal.id, name: goal.name || "Untitled Goal" }));
        if (!active) return;
        setGoals(nextGoals);
        const requested = new URLSearchParams(window.location.search).get("goalId");
        setSelectedGoalId(nextGoals.find((goal) => goal.id === requested)?.id ?? nextGoals[0]?.id ?? "");
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : "Unable to load goals.");
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!selectedGoalId) { setRun(null); setVersions([]); setPrimary(null); return; }
    let active = true;
    (async () => {
      setLoading(true); setError(null);
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
        const latest = await getLatestStrategyRun(planningUnitId, selectedGoalId);
        if (!active) return;
        setRun(latest);
        setPrimary(await getCurrentPrimaryStrategy(planningUnitId));
        const strategyId = latest?.selected_strategy_id ?? latest?.recommendation.recommended_strategy_id;
        setVersions(strategyId ? await getStrategyVersionHistory(planningUnitId, strategyId) : []);
      } catch (err) {
        if (active) { setRun(null); setVersions([]); setError(err instanceof Error ? err.message : "Unable to load strategy history."); }
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, [selectedGoalId]);

  const selectedGoalName = goals.find((goal) => goal.id === selectedGoalId)?.name ?? "Select a goal";

  if (loading && !goals.length) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-6xl space-y-5"><div className="h-9 w-72 animate-pulse rounded-xl bg-slate-200" /><div className="h-48 animate-pulse rounded-3xl bg-white" /><div className="h-72 animate-pulse rounded-3xl bg-white" /></div></main>;

  return (
    <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900">
      <InvestorHeader eyebrow="Review" title="Strategy History" description="Choose a goal to see the strategy decisions and versions created for that goal.">
        <div className="flex gap-2">
          <Link href="/investor/strategy-edit" className="rounded-xl border border-slate-200 bg-white px-3.5 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50">Edit Strategy</Link>
          <Link href="/investor/strategy-builder" className="rounded-xl bg-navy-900 px-3.5 py-2 text-xs font-bold text-white hover:bg-navy-800">Strategy Builder</Link>
        </div>
      </InvestorHeader>
      <div className="mx-auto max-w-6xl space-y-6 p-6 lg:p-10">
        {error && <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">{error}</div>}

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <label className="block max-w-xl"><span className="text-sm font-bold text-slate-700">Goal</span><select value={selectedGoalId} onChange={(e) => setSelectedGoalId(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm"><option value="">Select goal</option>{goals.map((goal) => <option key={goal.id} value={goal.id}>{goal.name}</option>)}</select></label>
          <p className="mt-3 text-xs text-slate-500">Showing history for: <strong className="text-slate-700">{selectedGoalName}</strong></p>
        </section>

        {primary && <section className="rounded-3xl border border-teal-200 bg-white p-6 shadow-sm"><p className="text-xs font-bold uppercase tracking-wide text-teal-700">Current Primary Strategy</p><div className="mt-3 grid gap-4 md:grid-cols-3"><div><p className="text-xs text-slate-400">Strategy</p><p className="mt-1 font-bold">{primary.strategy_id}</p></div><div><p className="text-xs text-slate-400">Version</p><p className="mt-1 font-bold">{primary.strategy_version_id}</p></div><div><p className="text-xs text-slate-400">Updated</p><p className="mt-1 font-bold">{new Date(primary.updated_at).toLocaleString("en-IN")}</p></div></div></section>}

        {run && <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Latest Strategy Run</h2><div className="mt-4 flex flex-wrap gap-3 text-xs text-slate-500"><span className="rounded-full bg-slate-100 px-3 py-1">Run v{run.run_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Goal version {run.defined_goal_version}</span><span className="rounded-full bg-slate-100 px-3 py-1">Status: {run.status}</span></div></section>}

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><div className="flex items-center justify-between"><div><h2 className="text-lg font-bold">Strategy Versions</h2><p className="mt-1 text-sm text-slate-500">Every strategy edit creates a new version; older versions remain preserved.</p></div></div><div className="mt-5 overflow-x-auto"><table className="w-full min-w-[720px] text-left text-sm"><thead className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400"><tr><th className="px-3 py-3">Version</th><th className="px-3 py-3">Source</th><th className="px-3 py-3">Parent</th><th className="px-3 py-3">Status</th><th className="px-3 py-3">Library</th><th className="px-3 py-3">Created</th></tr></thead><tbody>{versions.map((version) => <tr key={version.strategy_version_id ?? `${version.strategy_id}-${version.version}`} className="border-b border-slate-100"><td className="px-3 py-4 font-bold">v{version.version}</td><td className="px-3 py-4">{version.source}</td><td className="px-3 py-4">{version.parent_version ? `v${version.parent_version}` : "—"}</td><td className="px-3 py-4"><span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold">{version.status}</span></td><td className="px-3 py-4">{version.library_version}</td><td className="px-3 py-4 text-slate-500">{new Date(version.created_at).toLocaleString("en-IN")}</td></tr>)}</tbody></table>{!versions.length && <p className="py-10 text-center text-sm text-slate-500">No strategy versions found for this goal.</p>}</div></section>
      </div>
    </main>
  );
}
