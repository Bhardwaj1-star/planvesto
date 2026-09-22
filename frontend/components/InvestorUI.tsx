import type { ButtonHTMLAttributes, ReactNode } from "react";

export function InvestorCard({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <section className={"rounded-3xl border border-slate-200 bg-white shadow-sm " + className}>{children}</section>;
}

export function InvestorPageHeader({
  eyebrow, title, description, children,
}: { eyebrow?: string; title: string; description?: string; children?: ReactNode }) {
  return (
    <header className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
      <div>
        {eyebrow && <p className="text-xs font-bold uppercase tracking-[0.16em] text-teal-700">{eyebrow}</p>}
        <h1 className="mt-1 text-3xl font-extrabold tracking-tight text-slate-950">{title}</h1>
        {description && <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">{description}</p>}
      </div>
      {children}
    </header>
  );
}

export function InvestorButton({ children, variant = "primary", className = "", ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { className?: string; variant?: "primary" | "secondary" }) {
  const base = "inline-flex min-h-11 items-center justify-center rounded-xl px-5 py-3 text-sm font-bold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50";
  const tone = variant === "primary" ? "bg-navy-900 text-white hover:bg-slate-800" : "border border-slate-200 bg-white text-slate-700 hover:bg-slate-50";
  return <button {...props} className={base + " " + tone + " " + className}>{children}</button>;
}

export function InvestorStatus({ children, tone = "neutral" }: { children: ReactNode; tone?: "neutral" | "error" | "success" | "warning" }) {
  const tones = { neutral: "border-slate-200 bg-slate-50 text-slate-600", error: "border-red-200 bg-red-50 text-red-700", success: "border-emerald-200 bg-emerald-50 text-emerald-700", warning: "border-amber-200 bg-amber-50 text-amber-700" };
  return <div role="status" className={"rounded-2xl border px-5 py-4 text-sm " + tones[tone]}>{children}</div>;
}