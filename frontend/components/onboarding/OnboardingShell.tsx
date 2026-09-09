"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useOnboardingNavigation } from "./OnboardingProvider";

type OnboardingShellProps = {
  currentStep: number;
  title: string;
  subtitle: string;
  children: React.ReactNode;
  badge?: string;
  stepContext?: string;
};

export default function OnboardingShell({
  currentStep,
  title,
  subtitle,
  children,
  badge,
  stepContext,
}: OnboardingShellProps) {
  const pathname = usePathname();
  const { steps, completedSteps, goToStep } = useOnboardingNavigation(currentStep);

  const totalSteps = steps.length;
  const progressPercent = Math.round((currentStep / totalSteps) * 100);

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900">
      {/* Sticky Top Header */}
      <header className="sticky top-0 z-40 border-b border-slate-200/80 bg-white/95 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6 lg:px-8">
          {/* Brand Logo */}
          <Link
            href="/investor"
            className="flex items-center gap-2.5 transition hover:opacity-90"
            aria-label="Back to Investor Dashboard"
          >
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-navy-900 text-white shadow-sm">
              <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 17L10 12L13 15L19 8" />
                <path d="M15 8H19V12" />
              </svg>
            </div>
            <span className="text-lg font-extrabold tracking-tight text-navy-900">planvesto</span>
          </Link>

          {/* Stepper Navigation for Desktop */}
          <nav aria-label="Onboarding Steps" className="hidden md:flex items-center gap-1 lg:gap-1.5">
            {steps.map((step) => {
              const isActive = step.number === currentStep;
              const isDone = completedSteps.includes(step.number);
              const isClickable = isDone || step.number <= currentStep;

              return (
                <button
                  key={step.slug}
                  type="button"
                  onClick={() => isClickable && goToStep(step.number)}
                  disabled={!isClickable}
                  className={`group flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-xs font-semibold transition ${
                    isActive
                      ? "bg-navy-900 text-white shadow-sm"
                      : isDone
                      ? "text-slate-700 hover:bg-slate-100"
                      : "cursor-not-allowed text-slate-400"
                  }`}
                  title={`${step.title}${isDone ? " (Completed)" : ""}`}
                >
                  <span
                    className={`flex h-4 w-4 items-center justify-center rounded-full text-[10px] font-bold ${
                      isActive
                        ? "bg-teal-400 text-navy-900"
                        : isDone
                        ? "bg-teal-100 text-teal-800"
                        : "bg-slate-200 text-slate-500"
                    }`}
                  >
                    {isDone && !isActive ? (
                      <svg className="h-2.5 w-2.5" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M2.5 6L5 8.5L9.5 3.5" />
                      </svg>
                    ) : (
                      step.number
                    )}
                  </span>
                  <span className="hidden lg:inline">{step.title}</span>
                </button>
              );
            })}
          </nav>

          {/* Header Action: Exit & Progress */}
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex flex-col items-end">
              <span className="text-xs font-bold text-navy-900">
                Step {currentStep} of {totalSteps}
              </span>
              <span className="text-[11px] text-slate-500">{progressPercent}% complete</span>
            </div>
            <Link
              href="/investor"
              className="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 shadow-sm transition hover:bg-slate-50 hover:text-navy-900"
            >
              <span>Save &amp; Exit</span>
            </Link>
          </div>
        </div>

        {/* Linear Progress Bar */}
        <div className="h-1 w-full bg-slate-100">
          <div
            className="h-full bg-gradient-to-r from-teal-500 to-teal-600 transition-all duration-300 ease-out"
            style={{ width: `${progressPercent}%` }}
            role="progressbar"
            aria-valuenow={progressPercent}
            aria-valuemin={0}
            aria-valuemax={100}
          />
        </div>
      </header>

      {/* Main Guided Content */}
      <main className="mx-auto w-full max-w-4xl px-4 py-8 sm:px-6 lg:px-8 lg:py-12">
        {/* Step Intro Header */}
        <div className="mb-8">
          <div className="flex flex-wrap items-center gap-2 mb-2.5">
            <span className="inline-flex items-center rounded-full bg-teal-50 px-2.5 py-0.5 text-xs font-bold uppercase tracking-wider text-teal-800 border border-teal-200/60">
              Step {currentStep} of {totalSteps}
            </span>
            {badge && (
              <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-semibold text-slate-700">
                {badge}
              </span>
            )}
            {stepContext && (
              <span className="text-xs text-slate-400 hidden sm:inline">· {stepContext}</span>
            )}
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight text-navy-900 sm:text-3xl">
            {title}
          </h1>
          <p className="mt-2 text-sm leading-relaxed text-slate-600 sm:text-base">
            {subtitle}
          </p>
        </div>

        {/* Step Body */}
        {children}
      </main>
    </div>
  );
}
