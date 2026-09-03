import Link from "next/link";

export default function InvestmentPlanningPage() {
  return (
    <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
      <div className="mx-auto max-w-6xl">
        <Link href="/investor" className="text-sm font-bold text-slate-500">
          ← Dashboard
        </Link>

        <p className="mt-10 text-xs font-bold uppercase tracking-[0.15em] text-slate-400">
          Planning Engine
        </p>

        <h1 className="mt-2 text-4xl font-extrabold tracking-tight">
          Investment Planning
        </h1>

        <p className="mt-4 max-w-2xl text-sm leading-6 text-slate-500">
          Build investment decisions around your goals, financial position,
          time horizon and required outcomes.
        </p>

        <div className="mt-10 grid gap-5 md:grid-cols-2">
          <PlanningCard
            title="Portfolio"
            description="Understand the portfolio structure required for your financial objectives."
            href="/investor/investment-planning/portfolio"
          />

          <PlanningCard
            title="Products"
            description="Move from an investment requirement toward suitable product decisions."
            href="/investor/investment-planning/products"
          />
        </div>
      </div>
    </main>
  );
}

function PlanningCard({
  title,
  description,
  href,
}: {
  title: string;
  description: string;
  href: string;
}) {
  return (
    <Link
      href={href}
      className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
    >
      <h2 className="text-xl font-extrabold">{title}</h2>
      <p className="mt-2 text-sm leading-6 text-slate-500">
        {description}
      </p>
      <p className="mt-6 text-sm font-bold">Open →</p>
    </Link>
  );
}