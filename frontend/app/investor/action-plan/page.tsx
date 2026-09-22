"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import {
  confirmActionDecision,
  createAction,
  getActions,
  getDecisionHistory,
  getPlanningUnitId,
  type ActionDecision,
  type ActionPlanItem,
} from "../../../lib/api/action-plan";

const DECISIONS: ActionDecision[] = ["add", "modify", "complete", "cancel", "delete"];

function formatDate(value: string | null) {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

function statusClass(status: ActionPlanItem["status"]) {
  if (status === "completed") return "bg-emerald-50 text-emerald-700";
  if (status === "cancelled") return "bg-slate-100 text-slate-500";
  if (status === "confirmed") return "bg-teal-50 text-teal-700";
  return "bg-amber-50 text-amber-700";
}

export default function ActionPlanPage() {
  const [actions, setActions] = useState<ActionPlanItem[]>([]);
  const [history, setHistory] = useState<Array<{ action_id: string; decision: string; confirmed_at: string; decision_id: string | null }>>([]);
  const [selectedDecision, setSelectedDecision] = useState<Record<string, ActionDecision>>({});
  const [workingId, setWorkingId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [strategyVersionId, setStrategyVersionId] = useState("");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<"high" | "medium" | "low">("medium");
  const [deadline, setDeadline] = useState("");
  const [creating, setCreating] = useState(false);

  const refresh = async () => {
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId) throw new Error("Planning unit is not available. Please complete onboarding first.");
    const [nextActions, nextHistory] = await Promise.all([getActions(planningUnitId), getDecisionHistory(planningUnitId)]);
    setActions(nextActions);
    setHistory(nextHistory.map((item) => ({ action_id: item.action_id, decision: item.decision, confirmed_at: item.confirmed_at, decision_id: item.decision_id })));
  };

  useEffect(() => {
    if (typeof window !== "undefined") setStrategyVersionId(new URLSearchParams(window.location.search).get("strategyVersionId") ?? "");
  }, []);

  useEffect(() => {
    let active = true;
    (async () => {
      try { await refresh(); }
      catch (err) { if (active) setError(err instanceof Error ? err.message : "Unable to load Action Plan."); }
      finally { if (active) setLoading(false); }
    })();
    return () => { active = false; };
  }, []);

  const historyByAction = useMemo(() => {
    const map = new Map<string, typeof history>();
    for (const item of history) map.set(item.action_id, [...(map.get(item.action_id) ?? []), item]);
    return map;
  }, [history]);

  const handleCreate = async () => {
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId) return setError("Planning unit is not available.");
    if (!strategyVersionId.trim()) return setError("Strategy Version is required. Continue here from Strategy Approval or enter the approved version.");
    if (!title.trim()) return setError("Action title is required.");
    setCreating(true); setError(null);
    try {
      await createAction({ planning_unit_id: planningUnitId, strategy_version_id: strategyVersionId.trim(), title: title.trim(), description: description.trim() || null, priority, deadline: deadline || null });
      setTitle(""); setDescription(""); setDeadline("");
      await refresh();
    } catch (err) { setError(err instanceof Error ? err.message : "Unable to create implementation action."); }
    finally { setCreating(false); }
  };

  const handleDecision = async (action: ActionPlanItem) => {
    const decision = selectedDecision[action.action_id ?? ""];
    if (!action.action_id || !decision) return;
    const planningUnitId = getPlanningUnitId();
    if (!planningUnitId) return setError("Planning unit is not available.");
    setWorkingId(action.action_id); setError(null);
    try {
      await confirmActionDecision(planningUnitId, action, decision);
      await refresh();
    } catch (err) { setError(err instanceof Error ? err.message : "Action decision failed."); }
    finally { setWorkingId(null); }
  };

  if (loading) return <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10"><div className="mx-auto max-w-6xl space-y-6"><div className="h-10 w-64 animate-pulse rounded-xl bg-slate-200" /><div className="h-72 animate-pulse rounded-3xl bg-white" /></div></main>;

  return <main className="min-h-screen bg-[#f6f8fb] pb-16 text-slate-900"><div className="mx-auto max-w-6xl space-y-6 p-6 lg:p-10">
    <header><p className="text-sm font-semibold uppercase tracking-[0.16em] text-teal-700">Implementation</p><h1 className="mt-1 text-3xl font-extrabold tracking-tight">Action Plan</h1><p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">Turn an approved Strategy Version into concrete implementation actions. Decisions are recorded as immutable history by the backend.</p></header>
    {error && <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">{error}</div>}
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-lg font-bold">Add implementation action</h2><p className="mt-1 text-sm text-slate-500">Create an actionable item for the approved Strategy Version. You can add, modify, complete or cancel it later.</p><div className="mt-5 grid gap-4 md:grid-cols-2"><label className="block md:col-span-2"><span className="text-sm font-bold">Strategy Version ID</span><input value={strategyVersionId} onChange={(e) => setStrategyVersionId(e.target.value)} placeholder="Approved Strategy Version ID" className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm" /></label><label className="block md:col-span-2"><span className="text-sm font-bold">Action title</span><input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g. Set up the monthly investment instruction" className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm" /></label><label className="block md:col-span-2"><span className="text-sm font-bold">Description</span><textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3} placeholder="What needs to be done?" className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm" /></label><label className="block"><span className="text-sm font-bold">Priority</span><select value={priority} onChange={(e) => setPriority(e.target.value as typeof priority)} className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-3 text-sm"><option value="high">High</option><option value="medium">Medium</option><option value="low">Low</option></select></label><label className="block"><span className="text-sm font-bold">Deadline</span><input type="date" value={deadline} onChange={(e) => setDeadline(e.target.value)} className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-3 text-sm" /></label></div><button onClick={() => void handleCreate()} disabled={creating} className="mt-5 w-full rounded-xl bg-navy-900 px-4 py-3 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-50">{creating ? "Creating…" : "Add Action"}</button></section>
    {!actions.length ? <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center"><h2 className="text-xl font-bold">No actions yet</h2><p className="mt-2 text-sm text-slate-500">Create the first implementation action above for the approved Strategy Version.</p><Link href="/investor/strategy-approval" className="mt-6 inline-flex rounded-xl border border-slate-200 px-5 py-3 text-sm font-bold text-slate-700">Review Strategy Approval</Link></section> : <section className="space-y-4">{actions.map((action) => { const id = action.action_id ?? ""; const historyItems = historyByAction.get(id) ?? []; return <article key={id} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"><div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between"><div className="min-w-0"><div className="flex flex-wrap items-center gap-2"><span className={`rounded-full px-3 py-1 text-xs font-bold capitalize ${statusClass(action.status)}`}>{action.status}</span><span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold capitalize text-slate-600">{action.priority} priority</span></div><h2 className="mt-3 text-xl font-extrabold">{action.title}</h2>{action.description && <p className="mt-1 text-sm leading-6 text-slate-600">{action.description}</p>}<div className="mt-4 flex flex-wrap gap-4 text-xs text-slate-500"><span>Deadline: <b className="text-slate-700">{formatDate(action.deadline)}</b></span><span>Created: <b className="text-slate-700">{formatDate(action.created_at)}</b></span><span>Strategy Version: <b className="text-slate-700">{action.strategy_version_id}</b></span></div></div>{action.status !== "completed" && action.status !== "cancelled" && <div className="w-full md:w-72"><label className="block text-xs font-bold uppercase tracking-wide text-slate-400">Decision</label><select value={selectedDecision[id] ?? ""} onChange={(e) => setSelectedDecision((prev) => ({ ...prev, [id]: e.target.value as ActionDecision }))} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm"><option value="">Choose action</option>{DECISIONS.map((decision) => <option key={decision} value={decision}>{decision}</option>)}</select><button onClick={() => void handleDecision(action)} disabled={!selectedDecision[id] || workingId === id} className="mt-2 w-full rounded-xl bg-navy-900 px-4 py-2.5 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-50">{workingId === id ? "Saving…" : "Confirm Decision"}</button></div>}</div>{historyItems.length > 0 && <details className="mt-5 border-t border-slate-100 pt-4"><summary className="cursor-pointer text-sm font-bold text-slate-700">Decision history ({historyItems.length})</summary><div className="mt-3 space-y-2">{historyItems.map((item) => <div key={item.decision_id ?? `${item.action_id}-${item.confirmed_at}`} className="flex items-center justify-between rounded-xl bg-slate-50 px-4 py-3 text-xs"><span className="font-bold capitalize text-slate-700">{item.decision}</span><span className="text-slate-500">{formatDate(item.confirmed_at)}</span></div>)}</div></details>}</article>; })}</section>}
  </div></main>;
}
