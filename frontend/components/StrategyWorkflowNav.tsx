"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const steps = [
  { label: "Build & Compare", href: "/investor/strategy-builder" },
  { label: "Custom Scenarios", href: "/investor/strategy-scenarios" },
  { label: "Approval", href: "/investor/strategy-approval" },
];

export default function StrategyWorkflowNav() {
  const pathname = usePathname();
  return (
    <nav aria-label="Strategy workflow" className="overflow-x-auto">
      <ol className="flex min-w-max items-center gap-2 rounded-2xl border border-slate-200 bg-white p-2 shadow-sm">
        {steps.map((step, index) => {
          const active = pathname === step.href || pathname?.startsWith(step.href + "/");
          return <li key={step.href} className="flex items-center gap-2">
            <Link href={step.href} aria-current={active ? "step" : undefined} className={["min-h-10 rounded-xl px-3 py-2 text-xs font-bold transition sm:px-4 sm:text-sm", active ? "bg-navy-900 text-white" : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"].join(" ")}>
              <span className="mr-1 text-slate-400">{index + 1}.</span>{step.label}
            </Link>
            {index < steps.length - 1 && <span aria-hidden="true" className="text-slate-300">→</span>}
          </li>;
        })}
      </ol>
    </nav>
  );
}