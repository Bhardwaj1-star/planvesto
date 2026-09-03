import Link from "next/link";

export default function RiskPlanningPage() {
  return (
    <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
      <div className="mx-auto max-w-6xl">
        <Link href="/investor" className="text-sm font-bold text-slate-500">
          ← Dashboard
        </Link>

        <p className="mt-10 text-xs font-bold uppercase tracking-[0.15em] text-slate-400">
          Protection Planning
        </p>

        <h1 className="mt-2 text-4xl font-extrabold tracking-tight">
          Risk Planning
        </h1>

        <p className="mt-4 max-w-2xl text-sm leading-6 text-slate-500">
          Determine what needs to be protected before deciding which
          insurance products to use.
        </p>

        <div className="mt-10 grid gap-5 md:grid-cols-2">
          <PlanningCard
            title="Coverage"
            description="Determine protection requirements based on your financial situation."
            href="/investor/risk-planning/coverage"
          />

          <PlanningCard
            title="Policies"
            description="Review policy decisions after establishing the required protection."
            href="/investor/risk-planning/policies"
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