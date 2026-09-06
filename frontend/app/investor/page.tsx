"use client";

import Link from "next/link";

const sections = [
  {
    eyebrow: "Financial State",
    title: "Financial State",
    description: "Know where are you today and what is your current financial situation.",
    href: "/investor/financial-state",
    action: "Open Financial State",
  },
  {
    eyebrow: "Goals",
    title: "Goals",
    description: "Know where do you want to get to.",
    href: "/investor/goal-planner",
    action: "Open Goal Planner",
  },
];

export default function InvestorDashboard() {
  return (
    <main className="min-w-0">
          <header className="border-b border-slate-200 bg-white">
            <div className="flex min-h-[80px] items-center justify-between gap-6 px-5 lg:px-8">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-400">
                  Investor Dashboard
                </p>
                <h1 className="mt-1 text-2xl font-extrabold tracking-tight text-slate-950 sm:text-3xl">
                  Your financial plan
                </h1>
              </div>

              <Link
                href="/investor/onboarding"
                className="hidden rounded-xl bg-slate-950 px-4 py-2.5 text-sm font-bold text-white transition hover:bg-slate-800 sm:inline-flex"
              >
                Continue financial plan
              </Link>
            </div>
          </header>

          <div className="p-5 lg:p-8">
            <section className="grid gap-6 xl:grid-cols-2" aria-label="Financial planning overview">
              {sections.map((section) => (
                <Link
                  key={section.href}
                  href={section.href}
                  className="group rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-md lg:p-8"
                >
                  <p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">
                    {section.eyebrow}
                  </p>
                  <h2 className="mt-3 text-2xl font-extrabold tracking-tight text-slate-950">
                    {section.title}
                  </h2>
                  <p className="mt-3 max-w-xl text-sm leading-6 text-slate-500">
                    {section.description}
                  </p>
                  <p className="mt-8 text-sm font-bold text-teal-700 group-hover:text-teal-900">
                    {section.action} <span aria-hidden="true">→</span>
                  </p>
                </Link>
              ))}
            </section>
          </div>
    </main>
  );
}