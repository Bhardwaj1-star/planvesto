"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { InvestorProfileMenu } from "../../../components/InvestorProfileMenu";
import {
  loadGoalPlannerData,
  saveGoalPlannerData,
  type GoalPlannerData,
  type GoalPlannerGoal,
} from "../../../lib/onboarding/persistence";

const goalOptions = [
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

const criticalityOptions = ["Critical", "Important", "Aspirational"] as const;
const flexibilityOptions = ["Fixed", "Flexible"] as const;
const assumedInflation = 6;
const expectedReturn = 10;

type DraftGoal = GoalPlannerGoal & { option: string; customName: string };

function createDraftGoal(): DraftGoal {
  return {
    id: `goal-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    name: "",
    option: "",
    customName: "",
    targetAmount: "",
    targetDate: "",
    priority: "",
    flexibility: "",
    funding: [],
  };
}

function toDraft(goal: GoalPlannerGoal): DraftGoal {
  const option = goalOptions.includes(goal.name as (typeof goalOptions)[number]) ? goal.name : "Other";
  return { ...goal, option, customName: option === "Other" ? goal.name : "" };
}

function monthsRemaining(targetDate: string) {
  if (!targetDate) return 0;
  const [year, month] = targetDate.split("-").map(Number);
  const now = new Date();
  return Math.max(0, (year - now.getFullYear()) * 12 + month - (now.getMonth() + 1));
}

function currency(value: number) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);
}

function projectedValues(goal: GoalPlannerGoal, data: GoalPlannerData) {
  const years = monthsRemaining(goal.targetDate) / 12;
  const projectedGoal = (Number(goal.targetAmount) || 0) * Math.pow(1 + assumedInflation / 100, years);
  const projectedAssets = goal.funding.reduce((total, allocation) => {
    const asset = data.assets.find((item) => item.id === allocation.assetId);
    return total + (Number(asset?.currentValue) || 0) * ((Number(allocation.allocationPercentage) || 0) / 100) * Math.pow(1 + expectedReturn / 100, years);
  }, 0);
  return { projectedGoal, projectedAssets, shortfall: projectedGoal - projectedAssets };
}

export default function GoalPlannerPage() {
  const [data, setData] = useState<GoalPlannerData>({ goals: [], assets: [] });
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);

  // Form state
  const [editingDraft, setEditingDraft] = useState<DraftGoal | null>(null);
  const [editingGoalId, setEditingGoalId] = useState<string | null>(null);

  const isFormOpen = editingDraft !== null;

  useEffect(() => {
    let active = true;
    loadGoalPlannerData()
      .then((loaded) => {
        if (!active) return;
        setData(loaded);
        setError(null);
      })
      .catch((cause: unknown) => {
        if (active) setError(cause instanceof Error ? cause.message : "Unable to load goals.");
      })
      .finally(() => {
        if (active) setIsLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  function startAdding() {
    setSaved(false);
    setEditingDraft(createDraftGoal());
    setEditingGoalId(null);
  }

  function startEditing(goal: GoalPlannerGoal) {
    setSaved(false);
    setEditingDraft(toDraft(goal));
    setEditingGoalId(goal.id);
  }

  function cancelForm() {
    setEditingDraft(null);
    setEditingGoalId(null);
  }

  function updateDraft(changes: Partial<DraftGoal>) {
    setEditingDraft((current) => current ? { ...current, ...changes } : current);
  }

  function updateFunding(assetId: string, changes: { checked?: boolean; percentage?: string }) {
    setEditingDraft((current) => {
      if (!current) return current;
      const existing = current.funding.find((allocation) => allocation.assetId === assetId);
      if (changes.checked === false) return { ...current, funding: current.funding.filter((allocation) => allocation.assetId !== assetId) };
      if (existing) return { ...current, funding: current.funding.map((allocation) => allocation.assetId === assetId ? { ...allocation, allocationPercentage: changes.percentage ?? allocation.allocationPercentage } : allocation) };
      return { ...current, funding: [...current.funding, { assetId, allocationPercentage: changes.percentage ?? "100" }] };
    });
  }

  async function saveGoal() {
    if (!editingDraft) return;
    setIsSaving(true);
    setSaved(false);
    setError(null);
    try {
      const goal = editingDraft;
      if (!goal.name.trim() || !goal.targetAmount || Number(goal.targetAmount) < 0 || !goal.targetDate || !goal.priority || !goal.flexibility || (goal.option === "Other" && !goal.customName.trim())) {
        throw new Error("Complete the required fields before saving.");
      }
      const { option: _option, customName: _customName, ...cleanGoal } = goal;
      const payload = editingGoalId
        ? data.goals.map((g) => g.id === editingGoalId ? { ...cleanGoal, name: cleanGoal.name.trim() } : g)
        : [...data.goals, { ...cleanGoal, name: cleanGoal.name.trim() }];
      const savedData = await saveGoalPlannerData(payload);
      setData(savedData);
      setSaved(true);
      cancelForm();
    } catch (cause: unknown) {
      setError(cause instanceof Error ? cause.message : "Unable to save goal.");
    } finally {
      setIsSaving(false);
    }
  }

  async function removeGoal(id: string) {
    setSaved(false);
    setError(null);
    try {
      const nextGoals = data.goals.filter((goal) => goal.id !== id);
      const savedData = await saveGoalPlannerData(nextGoals);
      setData(savedData);
      if (editingGoalId === id) cancelForm();
    } catch (cause: unknown) {
      setError(cause instanceof Error ? cause.message : "Unable to delete goal.");
    }
  }

  if (isLoading) return <main className="flex min-h-screen items-center justify-center bg-slate-25 text-sm font-semibold text-slate-500">Loading your goals...</main>;

  return (
    <main className="min-h-screen bg-slate-25 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex h-20 max-w-[1200px] items-center justify-between px-5 lg:px-8">
          <p className="text-sm font-semibold text-slate-500">Plan your next milestones</p>
          <div className="flex items-center gap-4">
            <Link href="/investor/financial-state" className="text-sm font-semibold text-teal-700 hover:text-teal-900">
              Financial State
            </Link>
            <InvestorProfileMenu />
          </div>
        </div>
      </header>

      <div className="mx-auto w-full max-w-[1120px] px-5 py-10 lg:px-8 lg:py-14">
        <div className="mb-8 flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.16em] text-teal-700">Step 5</p>
            <h1 className="mt-3 text-3xl font-extrabold tracking-tight text-navy-900 sm:text-4xl">Goal Planner</h1>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">Turn the things that matter into clear financial targets and connect them to the assets you already own.</p>
          </div>
          {!isFormOpen && (
            <button type="button" onClick={startAdding} className="inline-flex items-center justify-center gap-2 rounded-xl border border-teal-600 px-5 py-3 text-sm font-bold text-teal-700 hover:bg-teal-50">+ Add Goal</button>
          )}
        </div>

        {error && <p className="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700" role="alert">{error}</p>}
        {saved && <p className="mb-5 rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700" role="status">Goal saved successfully.</p>}

        {/* ---- Saved goals list ---- */}
        {!isFormOpen && data.goals.length === 0 && (
          <section className="rounded-[28px] border border-dashed border-slate-300 bg-white p-10 text-center shadow-soft">
            <h2 className="text-xl font-extrabold text-navy-900">No goals added yet</h2>
            <p className="mt-2 text-sm text-slate-500">Add your first goal to start planning its future value.</p>
            <button type="button" onClick={startAdding} className="mt-6 rounded-xl bg-navy-900 px-5 py-3 text-sm font-bold text-white hover:bg-navy-800">Add Goal</button>
          </section>
        )}

        {!isFormOpen && data.goals.length > 0 && (
          <div className="space-y-4">
            {data.goals.map((goal, index) => {
              const values = projectedValues(goal, data);
              return (
                <section key={goal.id} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <h3 className="font-extrabold text-navy-900">{goal.name || `Goal ${index + 1}`}</h3>
                      <p className="mt-1 text-sm text-slate-500">
                        {goal.targetDate && `Target: ${goal.targetDate}`}
                        {goal.targetAmount && ` · ${currency(Number(goal.targetAmount))}`}
                      </p>
                    </div>
                    <div className="flex shrink-0 gap-3 text-sm font-bold">
                      <button type="button" onClick={() => startEditing(goal)} className="text-teal-700 underline decoration-teal-200 underline-offset-4 hover:text-teal-800">Edit</button>
                      <button type="button" onClick={() => removeGoal(goal.id)} className="text-slate-500 underline decoration-slate-200 underline-offset-4 hover:text-red-600">Remove</button>
                    </div>
                  </div>
                  <div className="mt-4 flex flex-wrap gap-2 text-xs font-semibold">
                    {goal.priority && (
                      <span className={`rounded-full px-3 py-1 ${goal.priority === "Critical" ? "bg-red-50 text-red-700" : goal.priority === "Important" ? "bg-teal-50 text-teal-700" : "bg-slate-100 text-slate-600"}`}>{goal.priority}</span>
                    )}
                    {goal.flexibility && (
                      <span className={`rounded-full px-3 py-1 ${goal.flexibility === "Fixed" ? "bg-amber-50 text-amber-800" : "bg-slate-100 text-slate-600"}`}>{goal.flexibility}</span>
                    )}
                    {goal.funding.length > 0 && (
                      <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">{goal.funding.length} asset{goal.funding.length > 1 ? "s" : ""} mapped</span>
                    )}
                  </div>
                  <div className="mt-4 grid gap-3 sm:grid-cols-3">
                    <Metric label="Projected Goal Value" value={currency(values.projectedGoal)} />
                    <Metric label="Projected Asset Value" value={currency(values.projectedAssets)} />
                    <Metric label="Shortfall" value={currency(values.shortfall)} tone={values.shortfall > 0 ? "text-red-600" : "text-teal-700"} />
                  </div>
                </section>
              );
            })}
          </div>
        )}

        {/* ---- Goal Form ---- */}
        {isFormOpen && editingDraft && (
          <section className="rounded-[28px] border border-teal-200 bg-teal-50/50 p-6 shadow-soft sm:p-8">
            <div className="mb-6 flex items-start justify-between gap-4 border-b border-teal-100 pb-5">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.14em] text-teal-700">{editingGoalId ? "Edit goal" : "New goal"}</p>
                <h2 className="mt-2 text-xl font-extrabold text-navy-900">Goal information</h2>
              </div>
              <button type="button" onClick={cancelForm} className="text-sm font-bold text-slate-500 underline decoration-slate-300 underline-offset-4 hover:text-navy-900">Cancel</button>
            </div>
            <div className="grid gap-5 md:grid-cols-2">
              <label className="text-sm font-semibold text-navy-900">Goal name
                <select value={editingDraft.option} onChange={(event) => updateDraft({ option: event.target.value, name: event.target.value === "Other" ? editingDraft.customName : event.target.value })} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3.5 text-sm font-normal">
                  <option value="">Select a goal</option>{goalOptions.map((option) => <option key={option}>{option}</option>)}
                </select>
              </label>
              {editingDraft.option === "Other" && <label className="text-sm font-semibold text-navy-900">Custom goal name<input value={editingDraft.customName} onChange={(event) => updateDraft({ customName: event.target.value, name: event.target.value })} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3.5 text-sm font-normal" placeholder="Name your goal" /></label>}
              <label className="text-sm font-semibold text-navy-900">Target amount<input type="number" min="0" value={editingDraft.targetAmount} onChange={(event) => updateDraft({ targetAmount: event.target.value })} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3.5 text-sm font-normal" placeholder="0" /></label>
              <label className="text-sm font-semibold text-navy-900">Target month &amp; year<input type="month" value={editingDraft.targetDate} onChange={(event) => updateDraft({ targetDate: event.target.value })} className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3.5 text-sm font-normal" /></label>
              <label className="text-sm font-semibold text-navy-900">Criticality<select value={editingDraft.priority} onChange={(event) => updateDraft({ priority: event.target.value })} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3.5 text-sm font-normal"><option value="">Select criticality</option>{criticalityOptions.map((option) => <option key={option}>{option}</option>)}</select></label>
              <label className="text-sm font-semibold text-navy-900">Flexibility<select value={editingDraft.flexibility} onChange={(event) => updateDraft({ flexibility: event.target.value })} className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-4 py-3.5 text-sm font-normal"><option value="">Select flexibility</option>{flexibilityOptions.map((option) => <option key={option}>{option}</option>)}</select></label>
            </div>

            {/* Projections */}
            {(editingDraft.targetAmount && editingDraft.targetDate) && (
              <div className="mt-8 rounded-2xl bg-slate-50 p-5">
                <div className="flex flex-wrap gap-x-6 gap-y-2 text-sm font-semibold text-slate-600"><span><em className="not-italic text-slate-400">Assumed Inflation:</em> {assumedInflation}%</span><span><em className="not-italic text-slate-400">Expected Return:</em> {expectedReturn}%</span><span><em className="not-italic text-slate-400">Time Remaining:</em> {monthsRemaining(editingDraft.targetDate)} months</span></div>
                <div className="mt-5 grid gap-3 sm:grid-cols-3">
                  {(() => { const values = projectedValues(editingDraft, data); return <><Metric label="Projected Goal Value" value={currency(values.projectedGoal)} /><Metric label="Projected Asset Value" value={currency(values.projectedAssets)} /><Metric label="Shortfall" value={currency(values.shortfall)} tone={values.shortfall > 0 ? "text-red-600" : "text-teal-700"} /></>; })()}
                </div>
              </div>
            )}

            {/* Map assets */}
            <div className="mt-8 border-t border-teal-100 pt-6">
              <div className="flex items-end justify-between gap-4">
                <div><h3 className="text-lg font-extrabold text-navy-900">Map assets</h3><p className="mt-1 text-sm text-slate-500">Select one or more assets and set each allocation percentage.</p></div>
                <span className="text-xs font-bold uppercase tracking-[0.12em] text-slate-400">{editingDraft.funding.length} mapped</span>
              </div>
              {data.assets.length === 0 ? <p className="mt-5 rounded-xl border border-dashed border-slate-300 px-4 py-5 text-sm text-slate-500">Add assets during onboarding before mapping them to this goal.</p> : (
                <div className="mt-5 space-y-3">{data.assets.map((asset) => {
                  const selectedAssets = new Set(editingDraft.funding.map((a) => a.assetId));
                  const allocation = editingDraft.funding.find((item) => item.assetId === asset.id);
                  return <div key={asset.id} className="flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-4 sm:flex-row sm:items-center sm:justify-between"><label className="flex items-center gap-3 text-sm font-semibold text-navy-900"><input type="checkbox" checked={selectedAssets.has(asset.id)} onChange={(event) => updateFunding(asset.id, { checked: event.target.checked })} className="h-4 w-4 accent-teal-600" />{asset.name}<span className="text-xs font-normal text-slate-400">{currency(Number(asset.currentValue))}</span></label>{allocation && <label className="flex items-center gap-2 text-sm text-slate-600">Allocation <input type="number" min="0" max="100" step="0.001" value={allocation.allocationPercentage} onChange={(event) => updateFunding(asset.id, { percentage: event.target.value })} className="w-24 rounded-lg border border-slate-200 px-3 py-2 text-right" />%</label>}</div>;
                })}</div>
              )}
            </div>

            {/* Form actions */}
            <div className="mt-7 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
              <button type="button" onClick={cancelForm} className="rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-navy-900 transition hover:border-slate-300">Cancel</button>
              <button type="button" disabled={isSaving} onClick={saveGoal} className="rounded-xl bg-teal-700 px-6 py-3.5 text-sm font-bold text-white shadow-sm hover:bg-teal-800 disabled:cursor-not-allowed disabled:opacity-60">{isSaving ? "Saving..." : editingGoalId ? "Save Changes" : "Add Goal"}</button>
            </div>
          </section>
        )}
      </div>
    </main>
  );
}

function Metric({ label, value, tone = "text-navy-900" }: { label: string; value: string; tone?: string }) {
  return <div className="rounded-xl border border-slate-200 bg-white p-4"><p className="text-xs font-semibold text-slate-400">{label}</p><p className={`mt-2 text-lg font-extrabold ${tone}`}>{value}</p></div>;
}