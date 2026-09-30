"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";

export default function StrategyWorkflowNav() {
  const pathname = usePathname();
  const [goalId, setGoalId] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      setGoalId(new URLSearchParams(window.location.search).get("goalId"));
    }
  }, []);

  const querySuffix = goalId ? `?goalId=${encodeURIComponent(goalId)}` : "";

  const steps = [
    {
      id: "build",
      label: "Build",
      href: `/investor/strategy-builder${querySuffix}`,
      isActive: Boolean(pathname?.startsWith("/investor/strategy-builder")),
    },
    {
      id: "compare",
      label: "Compare",
      href: `/investor/strategy-scenarios${querySuffix}`,
      isActive: Boolean(pathname?.startsWith("/investor/strategy-scenarios")),
    },
    {
      id: "report-action",
      label: "Report & Action Plan",
      href: `/investor/action-plan${querySuffix}`,
      isActive: Boolean(
        pathname?.startsWith("/investor/action-plan") ||
        pathname?.startsWith("/investor/goal-report") ||
        pathname?.startsWith("/investor/retirement-report") ||
        pathname?.startsWith("/investor/financial-plan")
      ),
    },
  ];

  return (
    <nav aria-label="Strategy workflow" className="overflow-x-auto">
      <ol className="flex min-w-max items-center gap-2 rounded-2xl border border-slate-200 bg-white p-2 shadow-sm">
        {steps.map((step, index) => {
          const active = step.isActive;
          return (
            <li key={step.id} className="flex items-center gap-2">
              <Link
                href={step.href}
                aria-current={active ? "step" : undefined}
                className={[
                  "min-h-10 rounded-xl px-3 py-2 text-xs font-bold transition sm:px-4 sm:text-sm",
                  active
                    ? "bg-navy-900 text-white"
                    : "text-slate-500 hover:bg-slate-50 hover:text-slate-900",
                ].join(" ")}
              >
                <span className={active ? "mr-1 text-slate-300" : "mr-1 text-slate-400"}>
                  {index + 1}.
                </span>
                {step.label}
              </Link>
              {index < steps.length - 1 && (
                <span aria-hidden="true" className="text-slate-300">
                  →
                </span>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
