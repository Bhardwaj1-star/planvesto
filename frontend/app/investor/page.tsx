"use client";

import Link from "next/link";
import InvestorSidebar from "../../components/InvestorSidebar";

const demo = {
  investorName: "Investor",

  netWorth: "₹20.0L",
  netWorthChange: "+8.4%",
  income: "₹1.50L",
  expenses: "₹95K",
  surplus: "₹55K",

  goals: [
    {
      name: "Emergency Fund",
      category: "Safety",
      target: "₹5.0L",
      current: "₹3.2L",
      progress: 64,
      status: "On track",
    },
    {
      name: "Home Purchase",
      category: "Lifestyle",
      target: "₹25.0L",
      current: "₹8.5L",
      progress: 34,
      status: "Needs attention",
    },
    {
      name: "Child Education",
      category: "Future",
      target: "₹15.0L",
      current: "₹4.5L",
      progress: 30,
      status: "Planning required",
    },
  ],

  assets: [
    { name: "Equity", value: "₹8.5L", percentage: 42 },
    { name: "Fixed Income", value: "₹5.0L", percentage: 25 },
    { name: "Cash & Bank", value: "₹4.0L", percentage: 20 },
    { name: "Gold", value: "₹2.5L", percentage: 13 },
  ],

  liabilities: [
    { name: "Home Loan", value: "₹18.0L", percentage: 72 },
    { name: "Personal Loan", value: "₹4.0L", percentage: 16 },
    { name: "Credit Card", value: "₹3.0L", percentage: 12 },
  ],

  attention: [
    {
      title: "Emergency fund is below your target",
      description:
        "You have ₹3.2L against a planned safety reserve of ₹5L.",
      action: "Review goal",
      href: "/investor/personal-management/goals",
    },
    {
      title: "Debt is using a significant part of cash flow",
      description:
        "Your current EMI obligations deserve attention before taking new commitments.",
      action: "Review debt",
      href: "/investor/personal-management/debt",
    },
    {
      title: "Investment strategy needs review",
      description:
        "Your current portfolio should be evaluated against your goals and time horizon.",
      action: "Review investments",
      href: "/investor/investment-planning",
    },
  ],
};

export default function InvestorDashboard() {
  return (
    <div className="min-h-screen bg-[#f6f8fb] text-slate-900">
      <div className="flex min-h-screen">
        <InvestorSidebar />

        <main className="min-w-0 flex-1">
          {/* Top bar */}
          <header className="border-b border-slate-200 bg-white">
            <div className="flex min-h-[80px] items-center justify-between gap-6 px-5 lg:px-8">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-400">
                  Investor Dashboard
                </p>

                <h1 className="mt-1 text-2xl font-extrabold tracking-tight text-slate-950 sm:text-3xl">
                  Welcome, {demo.investorName}
                </h1>
              </div>

              <div className="hidden items-center gap-3 sm:flex">
                <div className="text-right">
                  <p className="text-xs text-slate-400">
                    Financial position
                  </p>
                  <p className="mt-1 text-sm font-bold text-slate-700">
                    September 2026
                  </p>
                </div>

                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-900 text-sm font-bold text-white">
                  I
                </div>
              </div>
            </div>
          </header>

          <div className="space-y-6 p-5 lg:p-8">
            {/* Intro */}
            <section className="relative overflow-hidden rounded-3xl bg-slate-950 p-6 text-white shadow-sm lg:p-8">
              <div className="relative z-10 max-w-2xl">
                <p className="text-xs font-bold uppercase tracking-[0.18em] text-slate-400">
                  Your financial picture
                </p>

                <h2 className="mt-3 text-2xl font-extrabold tracking-tight sm:text-3xl">
                  Understand where you stand before deciding what to do next.
                </h2>

                <p className="mt-3 max-w-xl text-sm leading-6 text-slate-300">
                  Your dashboard brings your goals, cash flow, assets and
                  liabilities together so every financial decision starts
                  from the same picture.
                </p>

                <div className="mt-6 flex flex-wrap gap-3">
                  <Link
                    href="/investor/personal-management"
                    className="rounded-xl bg-white px-4 py-2.5 text-sm font-bold text-slate-950 transition hover:bg-slate-100"
                  >
                    Review finances →
                  </Link>

                  <Link
                    href="/investor/investment-planning"
                    className="rounded-xl border border-slate-700 px-4 py-2.5 text-sm font-bold text-white transition hover:bg-slate-800"
                  >
                    Investment planning
                  </Link>
                </div>
              </div>

              <div className="absolute -right-24 -top-24 h-72 w-72 rounded-full bg-slate-800 opacity-70 blur-2xl" />
              <div className="absolute -bottom-32 right-24 h-64 w-64 rounded-full bg-slate-800 opacity-50 blur-3xl" />
            </section>

            {/* Financial snapshot */}
            <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
              <MetricCard
                label="Net Worth"
                value={demo.netWorth}
                meta={`${demo.netWorthChange} this period`}
                emphasis
              />

              <MetricCard
                label="Monthly Income"
                value={demo.income}
                meta="Current inflow"
              />

              <MetricCard
                label="Monthly Expenses"
                value={demo.expenses}
                meta="Current outflow"
              />

              <MetricCard
                label="Monthly Surplus"
                value={demo.surplus}
                meta="Available after expenses"
              />

              <MetricCard
                label="Goal Progress"
                value="42%"
                meta="Overall funding progress"
              />
            </section>

            {/* Goals */}
            <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm lg:p-7">
              <SectionHeading
                eyebrow="Goals"
                title="What are you trying to achieve?"
                description="Your most important financial goals and their current funding position."
                action={
                  <Link
                    href="/investor/personal-management/goals"
                    className="text-sm font-bold text-slate-700 hover:text-slate-950"
                  >
                    View all →
                  </Link>
                }
              />

              <div className="mt-7 grid gap-4 lg:grid-cols-3">
                {demo.goals.map((goal) => (
                  <GoalCard key={goal.name} goal={goal} />
                ))}
              </div>
            </section>

            {/* Position */}
            <section className="grid gap-6 xl:grid-cols-2">
              <BreakupCard
                title="Where your money is"
                subtitle="Asset allocation"
                total="₹20.0L"
                items={demo.assets}
              />

              <BreakupCard
                title="What you owe"
                subtitle="Outstanding liabilities"
                total="₹25.0L"
                items={demo.liabilities}
              />
            </section>

            {/* Cash flow */}
            <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm lg:p-7">
              <SectionHeading
                eyebrow="Cash Flow"
                title="Your monthly money movement"
                description="The amount coming in, going out and remaining available for future decisions."
              />

              <div className="mt-7 grid gap-4 lg:grid-cols-3">
                <CashFlowCard
                  label="Income"
                  value={demo.income}
                  percentage={100}
                  description="Monthly inflow"
                />

                <CashFlowCard
                  label="Expenses"
                  value={demo.expenses}
                  percentage={63}
                  description="63% of monthly income"
                />

                <CashFlowCard
                  label="Surplus"
                  value={demo.surplus}
                  percentage={37}
                  description="37% available after expenses"
                />
              </div>

              <div className="mt-5 rounded-2xl bg-slate-50 p-5">
                <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-wide text-slate-400">
                      Highest expense category
                    </p>
                    <p className="mt-1 text-base font-extrabold text-slate-900">
                      Housing & EMI
                    </p>
                  </div>

                  <p className="text-lg font-extrabold text-slate-900">
                    ₹40,000 / month
                  </p>
                </div>
              </div>
            </section>

            {/* Attention */}
            <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm lg:p-7">
              <SectionHeading
                eyebrow="Attention"
                title="What needs your attention?"
                description="These are the areas that may influence your next financial decisions."
              />

              <div className="mt-7 divide-y divide-slate-100">
                {demo.attention.map((item) => (
                  <div
                    key={item.title}
                    className="flex flex-col gap-4 py-5 first:pt-0 last:pb-0 sm:flex-row sm:items-center sm:justify-between"
                  >
                    <div className="flex gap-4">
                      <div className="mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-slate-100 text-sm font-extrabold text-slate-700">
                        !
                      </div>

                      <div>
                        <h3 className="text-sm font-extrabold text-slate-900">
                          {item.title}
                        </h3>

                        <p className="mt-1 max-w-2xl text-sm leading-6 text-slate-500">
                          {item.description}
                        </p>
                      </div>
                    </div>

                    <Link
                      href={item.href}
                      className="shrink-0 text-sm font-bold text-slate-700 hover:text-slate-950"
                    >
                      {item.action} →
                    </Link>
                  </div>
                ))}
              </div>
            </section>

            {/* Planning paths */}
            <section>
              <div className="mb-4">
                <p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">
                  Planvesto Planning
                </p>

                <h2 className="mt-1 text-xl font-extrabold tracking-tight text-slate-950">
                  Where do you want to work next?
                </h2>
              </div>

              <div className="grid gap-4 md:grid-cols-3">
                <PlanningCard
                  number="01"
                  title="Personal Management"
                  description="Manage goals, cash flow, strategy and debt."
                  href="/investor/personal-management"
                />

                <PlanningCard
                  number="02"
                  title="Investment Planning"
                  description="Build investment decisions around your financial goals."
                  href="/investor/investment-planning"
                />

                <PlanningCard
                  number="03"
                  title="Risk Planning"
                  description="Understand protection requirements before selecting policies."
                  href="/investor/risk-planning"
                />
              </div>
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}

function MetricCard({
  label,
  value,
  meta,
  emphasis = false,
}: {
  label: string;
  value: string;
  meta: string;
  emphasis?: boolean;
}) {
  return (
    <div
      className={`rounded-2xl border p-5 shadow-sm ${
        emphasis
          ? "border-slate-900 bg-slate-950 text-white"
          : "border-slate-200 bg-white"
      }`}
    >
      <p
        className={`text-xs font-bold uppercase tracking-wide ${
          emphasis ? "text-slate-400" : "text-slate-400"
        }`}
      >
        {label}
      </p>

      <p className="mt-3 text-2xl font-extrabold tracking-tight">
        {value}
      </p>

      <p
        className={`mt-2 text-xs ${
          emphasis ? "text-slate-400" : "text-slate-500"
        }`}
      >
        {meta}
      </p>
    </div>
  );
}

function SectionHeading({
  eyebrow,
  title,
  description,
  action,
}: {
  eyebrow: string;
  title: string;
  description: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
      <div>
        <p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">
          {eyebrow}
        </p>

        <h2 className="mt-2 text-xl font-extrabold tracking-tight text-slate-950">
          {title}
        </h2>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
          {description}
        </p>
      </div>

      {action}
    </div>
  );
}

function GoalCard({
  goal,
}: {
  goal: {
    name: string;
    category: string;
    target: string;
    current: string;
    progress: number;
    status: string;
  };
}) {
  return (
    <Link
      href="/investor/personal-management/goals"
      className="group rounded-2xl border border-slate-200 p-5 transition hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-md"
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-bold uppercase tracking-wide text-slate-400">
            {goal.category}
          </p>

          <h3 className="mt-2 text-base font-extrabold text-slate-950">
            {goal.name}
          </h3>
        </div>

        <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[10px] font-bold text-slate-600">
          {goal.status}
        </span>
      </div>

      <div className="mt-7 flex items-end justify-between">
        <div>
          <p className="text-xs text-slate-400">Current</p>
          <p className="mt-1 text-lg font-extrabold text-slate-900">
            {goal.current}
          </p>
        </div>

        <div className="text-right">
          <p className="text-xs text-slate-400">Target</p>
          <p className="mt-1 text-sm font-bold text-slate-700">
            {goal.target}
          </p>
        </div>
      </div>

      <div className="mt-5">
        <div className="flex justify-between text-xs font-bold">
          <span className="text-slate-400">Progress</span>
          <span className="text-slate-700">{goal.progress}%</span>
        </div>

        <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
          <div
            className="h-full rounded-full bg-slate-900 transition-all"
            style={{ width: `${goal.progress}%` }}
          />
        </div>
      </div>

      <p className="mt-5 text-xs font-bold text-slate-500 group-hover:text-slate-900">
        Open goal →
      </p>
    </Link>
  );
}

function BreakupCard({
  title,
  subtitle,
  total,
  items,
}: {
  title: string;
  subtitle: string;
  total: string;
  items: {
    name: string;
    value: string;
    percentage: number;
  }[];
}) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm lg:p-7">
      <SectionHeading
        eyebrow={title}
        title={total}
        description={subtitle}
      />

      <div className="mt-7 space-y-5">
        {items.map((item) => (
          <div key={item.name}>
            <div className="flex items-center justify-between gap-4">
              <p className="text-sm font-bold text-slate-700">
                {item.name}
              </p>

              <div className="text-right">
                <span className="text-sm font-extrabold text-slate-900">
                  {item.value}
                </span>

                <span className="ml-2 text-xs font-semibold text-slate-400">
                  {item.percentage}%
                </span>
              </div>
            </div>

            <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full bg-slate-800"
                style={{ width: `${item.percentage}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function CashFlowCard({
  label,
  value,
  percentage,
  description,
}: {
  label: string;
  value: string;
  percentage: number;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-200 p-5">
      <div className="flex items-center justify-between">
        <p className="text-xs font-bold uppercase tracking-wide text-slate-400">
          {label}
        </p>

        <span className="text-xs font-bold text-slate-400">
          {percentage}%
        </span>
      </div>

      <p className="mt-3 text-2xl font-extrabold text-slate-950">
        {value}
      </p>

      <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-slate-800"
          style={{ width: `${percentage}%` }}
        />
      </div>

      <p className="mt-3 text-xs text-slate-500">
        {description}
      </p>
    </div>
  );
}

function PlanningCard({
  number,
  title,
  description,
  href,
}: {
  number: string;
  title: string;
  description: string;
  href: string;
}) {
  return (
    <Link
      href={href}
      className="group rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:border-slate-300 hover:shadow-md"
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-extrabold tracking-widest text-slate-400">
          {number}
        </span>

        <span className="text-slate-400 transition group-hover:translate-x-1 group-hover:text-slate-900">
          →
        </span>
      </div>

      <h3 className="mt-8 text-lg font-extrabold text-slate-950">
        {title}
      </h3>

      <p className="mt-2 text-sm leading-6 text-slate-500">
        {description}
      </p>
    </Link>
  );
}