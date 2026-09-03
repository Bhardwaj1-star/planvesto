import Link from "next/link";

export default function Page() {
  return (
    <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
      <div className="mx-auto max-w-5xl">
        <Link
          href="/investor"
          className="text-sm font-bold text-slate-500 hover:text-slate-900"
        >
          ← Dashboard
        </Link>

        <div className="mt-10 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">
            Planvesto
          </p>

          <h1 className="mt-3 text-3xl font-extrabold text-slate-950">
            Coming into the planning flow
          </h1>

          <p className="mt-3 text-sm text-slate-500">
            This screen is part of the investor decision journey and will be
            built next.
          </p>
        </div>
      </div>
    </main>
  );
}