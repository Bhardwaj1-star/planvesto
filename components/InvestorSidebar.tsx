"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navigation = [
  {
    label: "Dashboard",
    href: "/investor",
  },
  {
    label: "Personal Management",
    href: "/investor/personal-management",
  },
  {
    label: "Investment Planning",
    href: "/investor/investment-planning",
  },
  {
    label: "Risk Planning",
    href: "/investor/risk-planning",
  },
];

export default function InvestorSidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-64 shrink-0 border-r border-slate-200 bg-white lg:block">
      <div className="sticky top-0 flex h-screen flex-col">
        {/* Logo */}
        <div className="flex h-20 items-center border-b border-slate-200 px-6">
          <Link
            href="/investor"
            className="flex items-center gap-2.5"
            aria-label="Planvesto Investor Dashboard"
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-900">
              <svg
                className="h-5 w-5 text-white"
                viewBox="0 0 24 24"
                fill="none"
              >
                <path
                  d="M5 17L10 12L13 15L19 8"
                  stroke="currentColor"
                  strokeWidth="2.2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />

                <path
                  d="M15 8H19V12"
                  stroke="currentColor"
                  strokeWidth="2.2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>

            <span className="text-xl font-extrabold tracking-tight text-navy-900">
              planvesto
            </span>
          </Link>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-2 overflow-y-auto p-4">
          {navigation.map((item) => {
            const isActive =
              item.href === "/investor"
                ? pathname === "/investor"
                : pathname.startsWith(item.href);

            return (
              <Link
                key={item.href}
                href={item.href}
                className={[
                  "block rounded-xl px-4 py-3 text-sm font-semibold transition",
                  isActive
                    ? "bg-navy-900 text-white"
                    : "text-slate-600 hover:bg-slate-100 hover:text-navy-900",
                ].join(" ")}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* Bottom */}
        <div className="border-t border-slate-200 p-4">
          <Link
            href="/"
            className="block rounded-xl px-4 py-3 text-sm font-semibold text-slate-500 transition hover:bg-slate-100 hover:text-navy-900"
          >
            Back to Planvesto
          </Link>
        </div>
      </div>
    </aside>
  );
}