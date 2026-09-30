"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getActions, getPlanningUnitId, type ActionPlanItem } from "../../lib/api/action-plan";

export default function DiaryActionPlan() {
  const [actions, setActions] = useState<ActionPlanItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    async function loadActions(): Promise<void> {
      try {
        const planningUnitId = getPlanningUnitId();
        if (!planningUnitId) {
          if (active) setActions([]);
          return;
        }

        const items: ActionPlanItem[] = await getActions(planningUnitId);
        if (active) {
          setActions(
            items
              .filter((item: ActionPlanItem) => item.status !== "completed" && item.status !== "cancelled")
              .slice(0, 3),
          );
        }
      } catch {
        if (active) setActions([]);
      } finally {
        if (active) setLoading(false);
      }
    }

    void loadActions();
    return () => {
      active = false;
    };
  }, []);

  return (
    <section className="mx-auto mt-6 w-full max-w-5xl rounded-[28px] border border-[#d8c8b4] bg-[#f9f5ed] p-6 shadow-sm sm:p-8">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#8c6d48]">What comes next</p>
          <h2 className="mt-1 font-serif text-2xl font-bold text-slate-900">My Action Plan</h2>
          <p className="mt-1 text-xs leading-relaxed text-slate-600">The few things that need your attention after the decisions in your financial plan.</p>
        </div>
        <Link href="/investor/action-plan" className="shrink-0 rounded-xl bg-navy-900 px-4 py-2 text-xs font-bold text-white hover:bg-navy-800">Open Action Plan</Link>
      </div>

      <div className="mt-5 space-y-3">
        {loading ? (
          <div className="rounded-2xl border border-[#ebdccb] bg-white/60 p-4 text-xs text-slate-500">Checking what needs your attention…</div>
        ) : actions.length === 0 ? (
          <div className="rounded-2xl border border-[#ebdccb] bg-white/60 p-4 text-xs text-slate-600">Nothing is waiting right now. Your plan is up to date.</div>
        ) : (
          actions.map((action: ActionPlanItem) => (
            <div key={action.action_id ?? action.created_at + action.title} className="flex items-start gap-3 rounded-2xl border border-[#ebdccb] bg-white/70 p-4">
              <span className="mt-1 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border border-[#c8b79f] text-[10px] text-[#8c6d48]">○</span>
              <div className="min-w-0 flex-1">
                <p className="font-serif text-sm font-bold text-slate-900">{action.title}</p>
                {action.description && <p className="mt-1 text-xs leading-relaxed text-slate-600">{action.description}</p>}
                <div className="mt-2 flex flex-wrap gap-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
                  <span>{action.priority} priority</span>
                  {action.deadline && <span>• Due {new Date(action.deadline).toLocaleDateString("en-IN", { day: "numeric", month: "short" })}</span>}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </section>
  );
}
