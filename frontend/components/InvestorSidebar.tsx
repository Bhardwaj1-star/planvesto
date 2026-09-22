"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

type NavItem = { label: string; href: string; exact?: boolean };
type NavGroup = { label: string; items: NavItem[] };

const navigation: NavGroup[] = [
  {
    label: "Overview",
    items: [{ label: "Dashboard", href: "/investor/financial-state" }],
  },
  {
    label: "Plan",
    items: [
      { label: "Financial Position", href: "/investor/moneywheel" },
      { label: "Budgeting", href: "/investor/budgeting" },
      { label: "Goals", href: "/investor/goal-planner" },
    ],
  },
  {
    label: "Decide",
    items: [{ label: "Strategy", href: "/investor/strategy-builder" }],
  },
  {
    label: "Implement",
    items: [{ label: "Action Plan", href: "/investor/action-plan" }],
  },
  {
    label: "Review",
    items: [
      { label: "Goal History", href: "/investor/goal-history" },
      { label: "Strategy History", href: "/investor/strategy-history" },
      { label: "Investor Diary", href: "/investor/diary" },
    ],
  },
  {
    label: "Account",
    items: [{ label: "Profile", href: "/investor/profile" }],
  },
];

const contextualRoutes = [
  "/investor/strategy-scenarios",
  "/investor/strategy-approval",
  "/investor/strategy-edit",
];

function isItemActive(pathname: string | null, item: NavItem) {
  if (!pathname) return false;
  return item.exact ? pathname === item.href : pathname.startsWith(item.href);
}

export default function InvestorSidebar() {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  if (pathname?.startsWith("/investor/onboarding")) return null;

  const strategyContextActive =
    pathname === "/investor/strategy-builder" ||
    contextualRoutes.some((route) => pathname?.startsWith(route));

  return (
    <aside
      className={`${isCollapsed ? "w-16" : "w-64"} shrink-0 border-r border-slate-200 bg-white transition-[width] duration-200`}
    >
      <div className="sticky top-0 flex h-screen flex-col">
        <div
          className={`${isCollapsed ? "justify-center px-2" : "justify-between px-4"} flex h-20 items-center border-b border-slate-200`}
        >
          <Link
            href="/investor/financial-state"
            className="flex items-center gap-2.5"
            aria-label="Planvesto Dashboard"
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-900">
              <svg className="h-5 w-5 text-white" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M5 17L10 12L13 15L19 8" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M15 8H19V12" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            {!isCollapsed && <span className="text-xl font-extrabold tracking-tight text-navy-900">planvesto</span>}
          </Link>

          <button
            type="button"
            onClick={() => setIsCollapsed((current) => !current)}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-navy-900"
            aria-label={isCollapsed ? "Expand investor navigation" : "Collapse investor navigation"}
            title={isCollapsed ? "Expand navigation" : "Collapse navigation"}
          >
            <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d={isCollapsed ? "M9 6L15 12L9 18" : "M15 6L9 12L15 18"} stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
        </div>

        <nav
          className={`${isCollapsed ? "p-2" : "p-4"} flex-1 overflow-y-auto`}
          aria-label="Investor navigation"
        >
          {navigation.map((group) => (
            <section key={group.label} className={`${isCollapsed ? "mb-2" : "mb-5"}`}>
              {!isCollapsed && (
                <h2 className="mb-2 px-3 text-[11px] font-bold uppercase tracking-[0.14em] text-slate-400">
                  {group.label}
                </h2>
              )}

              <div className="space-y-1">
                {group.items.map((item) => {
                  const active =
                    item.label === "Strategy"
                      ? strategyContextActive
                      : isItemActive(pathname, item);

                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      aria-current={active ? "page" : undefined}
                      title={isCollapsed ? item.label : undefined}
                      className={[
                        "flex items-center rounded-xl py-2.5 text-sm font-semibold transition",
                        isCollapsed ? "justify-center px-2" : "px-3",
                        active
                          ? "bg-navy-900 text-white shadow-sm"
                          : "text-slate-600 hover:bg-slate-100 hover:text-navy-900",
                      ].join(" ")}
                    >
                      <span className={isCollapsed ? "sr-only" : undefined}>{item.label}</span>
                      {isCollapsed && (
                        <span aria-hidden="true" className="text-base">
                          {item.label.slice(0, 1)}
                        </span>
                      )}
                    </Link>
                  );
                })}
              </div>
            </section>
          ))}
        </nav>

        <div className={`${isCollapsed ? "p-2" : "p-4"} border-t border-slate-200`}>
          <Link
            href="/"
            className={`${isCollapsed ? "justify-center px-2" : "px-3"} flex rounded-xl py-2.5 text-sm font-semibold text-slate-500 transition hover:bg-slate-100 hover:text-navy-900`}
            title={isCollapsed ? "Back to Planvesto" : undefined}
          >
            <span className={isCollapsed ? "sr-only" : undefined}>Back to Planvesto</span>
            {isCollapsed && <span aria-hidden="true">↩</span>}
          </Link>
        </div>
      </div>
    </aside>
  );
}
