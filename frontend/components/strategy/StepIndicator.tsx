"use client";

import React from "react";

interface StepIndicatorProps {
  currentStep: number;
  completedSteps: number[];
  onStepClick?: (step: number) => void;
}

const STEPS = [
  { step: 1, label: "Available Money", desc: "Mapped Assets & SIPs" },
  { step: 2, label: "Asset Assessment", desc: "Keep / Reallocate" },
  { step: 3, label: "Recalculate Need", desc: "Self-Money Requirement" },
  { step: 4, label: "Yearly Projections", desc: "Funding Trajectory" },
  { step: 5, label: "Investment Planning", desc: "Asset Allocation" },
  { step: 6, label: "Payment & Withdrawal", desc: "Liquidation Matching" },
  { step: 7, label: "Monitoring", desc: "Checkpoints & Risk" },
];

export default function StepIndicator({
  currentStep,
  completedSteps,
  onStepClick,
}: StepIndicatorProps) {
  return (
    <div className="w-full rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
        <div>
          <p className="text-[11px] font-bold uppercase tracking-wider text-teal-700">
            Strategy Workflow
          </p>
          <h3 className="text-base font-extrabold text-slate-900">
            Goal Funding Strategy Steps
          </h3>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
          Step {currentStep} of {STEPS.length}
        </span>
      </div>

      <div className="overflow-x-auto pb-2">
        <div className="flex min-w-[700px] items-center justify-between gap-1">
          {STEPS.map((s, idx) => {
            const isCompleted = completedSteps.includes(s.step);
            const isCurrent = currentStep === s.step;
            const isClickable = Boolean(onStepClick);

            return (
              <React.Fragment key={s.step}>
                <div
                  onClick={() => isClickable && onStepClick?.(s.step)}
                  className={`flex flex-col items-center text-center transition-all ${
                    isClickable ? "cursor-pointer hover:opacity-80" : ""
                  }`}
                  style={{ width: "12%" }}
                >
                  <div
                    className={`flex h-8 w-8 items-center justify-center rounded-full text-xs font-bold transition-all ${
                      isCurrent
                        ? "bg-teal-600 text-white shadow-sm ring-4 ring-teal-100"
                        : isCompleted
                        ? "bg-emerald-500 text-white"
                        : "bg-slate-100 text-slate-400"
                    }`}
                  >
                    {isCompleted ? "✓" : s.step}
                  </div>
                  <p
                    className={`mt-2 text-[11px] leading-tight ${
                      isCurrent
                        ? "font-extrabold text-teal-900"
                        : isCompleted
                        ? "font-bold text-slate-800"
                        : "font-medium text-slate-400"
                    }`}
                  >
                    {s.label}
                  </p>
                  <p className="mt-0.5 text-[10px] text-slate-400 line-clamp-1">
                    {s.desc}
                  </p>
                </div>

                {idx < STEPS.length - 1 && (
                  <div
                    className={`h-0.5 flex-1 transition-all ${
                      completedSteps.includes(s.step) &&
                      (completedSteps.includes(s.step + 1) || currentStep === s.step + 1)
                        ? "bg-emerald-400"
                        : "bg-slate-200"
                    }`}
                  />
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
}
