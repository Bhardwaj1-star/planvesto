"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import PlanningBasketButton from "./PlanningBasketButton";

const WORKFLOW_STAGES = [
  { href: "/investor/strategy-builder", label: "1. Strategy Builder", root: "/investor/strategy-builder" },
  { href: "/investor/strategy-comparison", label: "2. Comparison", root: "/investor/strategy-comparison" },
  { href: "/investor/strategy-scenarios", label: "3. Implementation", root: "/investor/strategy-scenarios" },
  { href: "/investor/strategy-history", label: "4. History", root: "/investor/strategy-history" },
];

export default function StrategyWorkflowNav() {
  const pathname = usePathname() || "";
  const isStrategyBuilder = pathname.startsWith("/investor/strategy-builder");

  return (
    <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
      <nav aria-label="Strategy Navigation" className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs">
        {WORKFLOW_STAGES.map((stage, idx) => {
          const isActive = pathname.startsWith(stage.root);
          return (
            <div key={stage.href} className="flex items-center gap-1.5 shrink-0">
              <Link
                href={stage.href}
                className={`rounded-xl px-3.5 py-2 font-bold transition-all ${
                  isActive
                    ? "bg-navy-900 text-white shadow-xs"
                    : "text-slate-500 hover:bg-slate-100 hover:text-slate-800"
                }`}
              >
                {stage.label}
              </Link>
              {idx < WORKFLOW_STAGES.length - 1 && (
                <span className="text-slate-300 font-semibold select-none">›</span>
              )}
            </div>
          );
        })}
      </nav>

      {isStrategyBuilder && (
        <div className="shrink-0">
          <PlanningBasketButton />
        </div>
      )}
    </div>
  );
}
