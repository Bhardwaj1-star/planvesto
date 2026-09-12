"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const navigation = [
  { label: "Dashboard", href: "/investor/financial-state" },
  { label: "Moneywheel", href: "/investor/moneywheel" },
  { label: "Budgeting", href: "/investor/budgeting" },
  { label: "Goal Planner", href: "/investor/goal-planner" },
  { label: "Goal History", href: "/investor/goal-history" },
  { label: "Strategy Builder", href: "/investor/strategy-builder" },
  { label: "Custom Scenarios", href: "/investor/strategy-scenarios" },
  { label: "Strategy Approval", href: "/investor/strategy-approval" },
  { label: "Strategy History", href: "/investor/strategy-history" },
  { label: "Strategy Edit", href: "/investor/strategy-edit" },
  { label: "Action Plan", href: "/investor/action-plan" },
  { label: "Investor Diary", href: "/investor/diary" },
  { label: "Profile", href: "/investor/profile" },
];

export default function InvestorSidebar() {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  if (pathname?.startsWith("/investor/onboarding")) return null;

  return (
    <aside className={`${isCollapsed ? "w-16" : "w-64"} shrink-0 border-r border-slate-200 bg-white transition-[width] duration-200`}>
      <div className="sticky top-0 flex h-screen flex-col">
        <div className={`flex h-20 items-center border-b border-slate-200 ${isCollapsed ? "justify-center px-2" : "justify-between px-4"}`}>
          <Link href="/investor/financial-state" className="flex items-center gap-2.5" aria-label="Planvesto Dashboard">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-900"><svg className="h-5 w-5 text-white" viewBox="0 0 24 24" fill="none"><path d="M5 17L10 12L13 15L19 8" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" /><path d="M15 8H19V12" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" /></svg></div>
            {!isCollapsed && <span className="text-xl font-extrabold tracking-tight text-navy-900">planvesto</span>}
          </Link>
          <button type="button" onClick={() => setIsCollapsed((current) => !current)} className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-navy-900" aria-label={isCollapsed ? "Expand investor navigation" : "Collapse investor navigation"} title={isCollapsed ? "Expand navigation" : "Collapse navigation"}><svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d={isCollapsed ? "M9 6L15 12L9 18" : "M15 6L9 12L15 18"} stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" /></svg></button>
        </div>
        <nav className={`flex-1 space-y-2 overflow-y-auto ${isCollapsed ? "p-2" : "p-4"}`} aria-label="Investor navigation">
          {navigation.map((item) => { const isActive = pathname?.startsWith(item.href); return <Link key={item.href} href={item.href} className={["flex items-center rounded-xl py-3 text-sm font-semibold transition", isCollapsed ? "justify-center px-2" : "px-4", isActive ? "bg-navy-900 text-white" : "text-slate-600 hover:bg-slate-100 hover:text-navy-900"].join(" ")}><span className={isCollapsed ? "sr-only" : undefined}>{item.label}</span>{isCollapsed && <span aria-hidden="true" className="text-base">{item.label.slice(0, 1)}</span>}</Link>; })}
        </nav>
        <div className={`border-t border-slate-200 ${isCollapsed ? "p-2" : "p-4"}`}><Link href="/" className={`flex rounded-xl py-3 text-sm font-semibold text-slate-500 transition hover:bg-slate-100 hover:text-navy-900 ${isCollapsed ? "justify-center px-2" : "px-4"}`} title={isCollapsed ? "Back to Planvesto" : undefined}><span className={isCollapsed ? "sr-only" : undefined}>Back to Planvesto</span>{isCollapsed && <span aria-hidden="true">↩</span>}</Link></div>
      </div>
    </aside>
  );
}
