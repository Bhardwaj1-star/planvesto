"use client";

import { useEffect, useState } from "react";
import { loadGoalPlannerData } from "../lib/onboarding/persistence";

type Goal = { id: string; name: string };
type Basket = { id: string; name: string; goalIds: string[] };

const STORAGE_KEY = "planvesto:planning-baskets";

function BasketIcon() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.8">
      <path d="M5 9h14l-1 10H6L5 9Z" />
      <path d="M8 9c.2-3 1.7-5 4-5s3.8 2 4 5M9 13v3M12 13v3M15 13v3" strokeLinecap="round" />
    </svg>
  );
}

export default function PlanningBasketButton() {
  const [open, setOpen] = useState(false);
  const [goals, setGoals] = useState<Goal[]>([]);
  const [baskets, setBaskets] = useState<Basket[]>([]);
  const [name, setName] = useState("");
  const [selectedGoalIds, setSelectedGoalIds] = useState<string[]>([]);

  useEffect(() => {
    if (!open) return;
    try {
      const saved = JSON.parse(window.localStorage.getItem(STORAGE_KEY) || "[]");
      if (Array.isArray(saved)) setBaskets(saved);
    } catch { setBaskets([]); }
    void loadGoalPlannerData().then((data) => {
      setGoals((data?.goals ?? []).map((goal) => ({ id: goal.id, name: goal.name || "Untitled Goal" })));
    }).catch(() => setGoals([]));
  }, [open]);

  const createBasket = () => {
    const trimmed = name.trim();
    if (!trimmed || selectedGoalIds.length === 0) return;
    const basket: Basket = { id: crypto.randomUUID(), name: trimmed, goalIds: selectedGoalIds };
    const next = [...baskets, basket];
    setBaskets(next);
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    setName("");
    setSelectedGoalIds([]);
  };

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        aria-expanded={open}
        aria-label="Open Planning Basket"
        className="inline-flex min-h-10 items-center gap-2 rounded-xl border border-teal-200 bg-teal-50 px-3 py-2 text-xs font-bold text-teal-800 transition hover:bg-teal-100 sm:px-4 sm:text-sm"
      >
        <BasketIcon />
        Planning Basket
      </button>

      {open && (
        <div className="absolute right-0 z-30 mt-2 w-[min(92vw,380px)] rounded-2xl border border-slate-200 bg-white p-4 shadow-xl">
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-sm font-extrabold text-slate-900">Planning Basket</p>
              <p className="mt-1 text-xs leading-5 text-slate-500">Group related goals and work with them together.</p>
            </div>
            <button type="button" onClick={() => setOpen(false)} className="text-slate-400 hover:text-slate-700" aria-label="Close">×</button>
          </div>

          {baskets.length > 0 && (
            <div className="mt-4 space-y-2">
              <p className="text-[11px] font-bold uppercase tracking-wide text-slate-400">Your baskets</p>
              {baskets.map((basket) => (
                <button key={basket.id} type="button" className="w-full rounded-xl border border-slate-200 px-3 py-2 text-left hover:bg-slate-50">
                  <span className="block text-sm font-bold text-slate-800">{basket.name}</span>
                  <span className="text-xs text-slate-500">{basket.goalIds.length} goal{basket.goalIds.length === 1 ? "" : "s"}</span>
                </button>
              ))}
            </div>
          )}

          <div className="mt-4 border-t border-slate-100 pt-4">
            <p className="text-[11px] font-bold uppercase tracking-wide text-slate-400">Create new basket</p>
            <input value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Family Security" className="mt-2 w-full rounded-xl border border-slate-200 px-3 py-2.5 text-sm outline-none focus:border-teal-400" />
            <div className="mt-3 max-h-36 space-y-2 overflow-y-auto">
              {goals.map((goal) => (
                <label key={goal.id} className="flex cursor-pointer items-center gap-2 rounded-lg px-2 py-1.5 text-sm hover:bg-slate-50">
                  <input type="checkbox" checked={selectedGoalIds.includes(goal.id)} onChange={(e) => setSelectedGoalIds((current) => e.target.checked ? [...current, goal.id] : current.filter((id) => id !== goal.id))} />
                  <span>{goal.name}</span>
                </label>
              ))}
            </div>
            <button type="button" onClick={createBasket} disabled={!name.trim() || selectedGoalIds.length === 0} className="mt-3 w-full rounded-xl bg-navy-900 px-4 py-2.5 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-40">
              Create Planning Basket
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
