"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

type NavItem = { label: string; href: string; exact?: boolean };
type NavGroup = { label: string; items: NavItem[] };

const navigation: NavGroup[] = [
  { label: "Overview", items: [{ label: "Dashboard", href: "/investor/financial-state" }] },
  {
    label: "Plan",
    items: [
      { label: "Moneywheel", href: "/investor/moneywheel" },
      { label: "Budgeting", href: "/investor/budgeting" },
      { label: "Goal Planner", href: "/investor/goal-planner" },
    ],
  },
  { label: "Decide", items: [{ label: "Strategy Builder", href: "/investor/strategy-builder" }] },
  { label: "Implement", items: [{ label: "Action Plan", href: "/investor/action-plan" }] },
  {
    label: "Review",
    items: [
      { label: "Goal History", href: "/investor/goal-history" },
      { label: "Strategy History", href: "/investor/strategy-history" },
      { label: "Investor Diary", href: "/investor/diary" },
    ],
  },
  { label: "Account", items: [{ label: "Profile", href: "/investor/profile" }] },
];

const strategyRoutes = [
  { label: "Strategy Builder", href: "/investor/strategy-builder" },
  { label: "Custom Scenarios", href: "/investor/strategy-scenarios" },
  { label: "Strategy Approval", href: "/investor/strategy-approval" },
  { label: "Strategy Edit", href: "/investor/strategy-edit" },
];

function isItemActive(pathname: string | null, item: NavItem) {
  return Boolean(pathname && pathname.startsWith(item.href));
}

export default function InvestorSidebar() {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  if (pathname?.startsWith("/investor/onboarding")) return null;

  const strategyContextActive =
    pathname === "/investor/strategy-builder" ||
    pathname?.startsWith("/investor/strategy-scenarios") ||
    pathname?.startsWith("/investor/strategy-approval") ||
    pathname?.startsWith("/investor/strategy-edit");

  return (
    <>
      <button
        type="button"
        onClick={() => setIsMobileOpen(false)}
        aria-label="Close investor navigation"
        className={`fixed inset-0 z-40 bg-slate-950/40 md:hidden ${isMobileOpen ? "block" : "hidden"}`}
      />
      <button
        type="button"
        onClick={() => setIsMobileOpen((current) => !current)}
        aria-expanded={isMobileOpen}
        aria-controls="investor-sidebar"
        aria-label={isMobileOpen ? "Close investor navigation" : "Open investor navigation"}
        className="fixed left-4 top-4 z-50 flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-700 shadow-sm md:hidden"
      >
        <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d={isMobileOpen ? "M6 6L18 18M18 6L6 18" : "M4 7H20M4 12H20M4 17H20"} stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        </svg>
      </button>
      <aside id="investor-sidebar" className={`fixed inset-y-0 left-0 z-50 w-72 shrink-0 border-r border-slate-200 bg-white transition-transform duration-200 md:static md:z-auto md:h-auto md:translate-x-0 ${isCollapsed ? "md:w-16" : "md:w-64"} ${isMobileOpen ? "translate-x-0" : "-translate-x-full"} md:transition-[width]`}>
      <div className="sticky top-0 flex h-screen flex-col">
        <div className={`${isCollapsed ? "justify-center px-2" : "justify-between px-4"} flex h-20 items-center border-b border-slate-200`}>
          <Link href="/investor/financial-state" className="flex items-center gap-2.5" aria-label="Planvesto Dashboard">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-900">
              <svg className="h-5 w-5 text-white" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M5 17L10 12L13 15L19 8" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M15 8H19V12" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            {!isCollapsed && <span className="text-xl font-extrabold tracking-tight text-navy-900">planvesto</span>}
          </Link>
          <button type="button" onClick={() => { setIsCollapsed((current) => !current); setIsMobileOpen(false); }} className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-navy-900" aria-label={isCollapsed ? "Expand investor navigation" : "Collapse investor navigation"} title={isCollapsed ? "Expand navigation" : "Collapse navigation"}>
            <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d={isCollapsed ? "M9 6L15 12L9 18" : "M15 6L9 12L15 18"} stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
        </div>

        <nav className={`${isCollapsed ? "p-2" : "p-4"} flex-1 overflow-y-auto`} aria-label="Investor navigation">
          {navigation.map((group) => (
            <section key={group.label} className={`${isCollapsed ? "mb-2" : "mb-5"}`}>
              {!isCollapsed && <h2 className="mb-2 px-3 text-[11px] font-bold uppercase tracking-[0.14em] text-slate-400">{group.label}</h2>}
              <div className="space-y-1">
                {group.items.map((item) => {
                  const active = item.label === "Strategy Builder" ? strategyContextActive : isItemActive(pathname, item);
                  return (
                    <div key={item.href}>
                      <Link
                        href={item.href}
                        onClick={() => setIsMobileOpen(false)}
                        aria-current={active ? "page" : undefined}
                        title={isCollapsed ? item.label : undefined}
                        className={[
                          "flex items-center rounded-xl py-2.5 text-sm font-semibold transition",
                          isCollapsed ? "justify-center px-2" : "px-3",
                          active ? "bg-navy-900 text-white shadow-sm" : "text-slate-600 hover:bg-slate-100 hover:text-navy-900",
                        ].join(" ")}
                      >
                        <span className={isCollapsed ? "sr-only" : undefined}>{item.label}</span>
                        {isCollapsed && <span aria-hidden="true" className="text-base">{item.label.slice(0, 1)}</span>}
                      </Link>

                      {item.label === "Strategy Builder" && strategyContextActive && !isCollapsed && (
                        <div className="ml-3 mt-1 space-y-1 border-l border-slate-200 pl-3" aria-label="Strategy workflow">
                          {strategyRoutes.map((route) => {
                            const routeActive = pathname === route.href || pathname?.startsWith(route.href + "/");
                            return (
                              <Link
                                key={route.href}
                                href={route.href}
                                onClick={() => setIsMobileOpen(false)}
                                aria-current={routeActive ? "page" : undefined}
                                className={[
                                  "block rounded-lg px-3 py-2 text-xs font-semibold transition",
                                  routeActive ? "bg-teal-50 text-teal-800" : "text-slate-500 hover:bg-slate-50 hover:text-slate-800",
                                ].join(" ")}
                              >
                                {route.label}
                              </Link>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </section>
          ))}
        </nav>

        <div className={`${isCollapsed ? "p-2" : "p-4"} border-t border-slate-200`}>
          <Link href="/" onClick={() => setIsMobileOpen(false)} className={`${isCollapsed ? "justify-center px-2" : "px-3"} flex rounded-xl py-2.5 text-sm font-semibold text-slate-500 transition hover:bg-slate-100 hover:text-navy-900`} title={isCollapsed ? "Back to Planvesto" : undefined}>
            <span className={isCollapsed ? "sr-only" : undefined}>Back to Planvesto</span>
            {isCollapsed && <span aria-hidden="true">↩</span>}
          </Link>
        </div>
      </div>
      </aside>
    </>
  );
}
