import Link from "next/link";

const items = [
  ["Goals", "Define and manage the financial outcomes you are working toward.", "/investor/personal-management/goals"],
  ["Budget & Cash Flow", "Understand income, expenses and monthly surplus.", "/investor/personal-management/budget"],
  ["Strategy", "Translate your financial position into an actionable strategy.", "/investor/personal-management/strategy"],
  ["Debt Management", "Review liabilities, EMIs and debt priorities.", "/investor/personal-management/debt"],
];

export default function PersonalManagementPage() {
  return <PlanningPage title="Personal Management" description="Build the financial foundation on which your investment and risk decisions depend." items={items} />;
}

function PlanningPage({
  title,
  description,
  items,
}: {
  title: string;
  description: string;
  items: string[][];
}) {
  return (
    <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
      <div className="mx-auto max-w-6xl">
        <Link href="/investor" className="text-sm font-bold text-slate-500 hover:text-slate-900">
          ← Dashboard
        </Link>

        <p className="mt-10 text-xs font-bold uppercase tracking-[0.15em] text-slate-400">
          Planning
        </p>

        <h1 className="mt-2 text-4xl font-extrabold tracking-tight text-slate-950">
          {title}
        </h1>

        <p className="mt-4 max-w-2xl text-sm leading-6 text-slate-500">
          {description}
        </p>

        <div className="mt-10 grid gap-5 md:grid-cols-2">
          {items.map(([name, text, href], index) => (
            <Link
              key={name}
              href={href}
              className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
            >
              <p className="text-xs font-bold text-slate-400">
                0{index + 1}
              </p>
              <h2 className="mt-6 text-xl font-extrabold text-slate-950">
                {name}
              </h2>
              <p className="mt-2 text-sm leading-6 text-slate-500">
                {text}
              </p>
              <p className="mt-6 text-sm font-bold text-slate-700">
                Open →
              </p>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}