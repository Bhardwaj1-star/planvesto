"use client";

import React, { useState, useEffect } from "react";
import type { FinancingOption } from "../../lib/api/goal-funding";

interface FinancingInputPanelProps {
  goalTargetAmount: number;
  availableMonthlySurplus: number;
  onAssess: (option: FinancingOption) => void;
  loading?: boolean;
  defaultDownPaymentPct?: number;
  defaultLoanRatePct?: number;
  defaultTenureYears?: number;
}

function formatINR(value: number | null | undefined): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return "—";
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

export default function FinancingInputPanel({
  goalTargetAmount,
  availableMonthlySurplus,
  onAssess,
  loading = false,
  defaultDownPaymentPct = 20,
  defaultLoanRatePct = 8.5,
  defaultTenureYears = 10,
}: FinancingInputPanelProps) {
  const initialDownPayment = Math.round((goalTargetAmount * defaultDownPaymentPct) / 100);

  const [downPayment, setDownPayment] = useState<string>(String(initialDownPayment));
  const [loanRatePct, setLoanRatePct] = useState<string>(String(defaultLoanRatePct));
  const [tenureYears, setTenureYears] = useState<string>(String(defaultTenureYears));

  // Sync when goalTargetAmount changes
  useEffect(() => {
    if (goalTargetAmount > 0) {
      setDownPayment(String(Math.round((goalTargetAmount * defaultDownPaymentPct) / 100)));
    }
  }, [goalTargetAmount, defaultDownPaymentPct]);

  const numDownPayment = Number(downPayment) || 0;
  const numLoanRate = Number(loanRatePct) || 0;
  const numTenureYears = Number(tenureYears) || 0;

  const calculatedLoanAmount = Math.max(0, goalTargetAmount - numDownPayment);
  const downPaymentRatio = goalTargetAmount > 0 ? (numDownPayment / goalTargetAmount) * 100 : 0;

  // Approximate monthly EMI preview for instantaneous feedback
  const rMonthly = numLoanRate / 12 / 100;
  const nMonths = numTenureYears * 12;
  const estimatedEmi =
    rMonthly > 0 && nMonths > 0
      ? (calculatedLoanAmount * rMonthly * Math.pow(1 + rMonthly, nMonths)) /
        (Math.pow(1 + rMonthly, nMonths) - 1)
      : nMonths > 0
      ? calculatedLoanAmount / nMonths
      : 0;

  const isEmiAffordable = availableMonthlySurplus > 0 && estimatedEmi <= availableMonthlySurplus;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onAssess({
      down_payment: numDownPayment,
      loan_annual_interest_rate_pct: numLoanRate,
      loan_tenure_months: numTenureYears * 12,
    });
  };

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col justify-between gap-2 border-b border-slate-100 pb-4 sm:flex-row sm:items-center">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-amber-700">
            Step 4 &amp; §11.6 Financing Assessment
          </span>
          <h3 className="text-lg font-extrabold text-slate-900">
            Evaluate "Self Money + Financing" Path
          </h3>
          <p className="mt-0.5 text-xs text-slate-500">
            Configure borrowing terms to simulate loan principal, monthly EMI obligation, and interest drag.
          </p>
        </div>
        <span className="self-start rounded-full bg-amber-50 px-3 py-1 text-xs font-bold text-amber-800 border border-amber-200 sm:self-auto">
          Interactive Financing Sandbox
        </span>
      </div>

      <form onSubmit={handleSubmit} className="mt-5 space-y-6">
        <div className="grid gap-5 md:grid-cols-3">
          {/* 1. Down Payment */}
          <div className="rounded-2xl border border-slate-200 bg-slate-50/70 p-4 space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-700">
                Own Down Payment
              </label>
              <span className="rounded-full bg-slate-200/80 px-2 py-0.5 text-[10px] font-bold text-slate-700">
                {downPaymentRatio.toFixed(0)}% of goal
              </span>
            </div>
            <div className="relative">
              <span className="absolute left-3.5 top-2.5 text-sm font-bold text-slate-400">₹</span>
              <input
                type="number"
                min={0}
                max={goalTargetAmount}
                value={downPayment}
                onChange={(e) => setDownPayment(e.target.value)}
                className="w-full rounded-xl border border-slate-200 bg-white pl-8 pr-4 py-2 text-sm font-bold text-slate-900 focus:border-teal-500 focus:outline-none"
              />
            </div>
            <div className="flex flex-wrap gap-1">
              {[10, 20, 30, 50].map((pct) => (
                <button
                  key={pct}
                  type="button"
                  onClick={() =>
                    setDownPayment(String(Math.round((goalTargetAmount * pct) / 100)))
                  }
                  className={`rounded-lg border px-2 py-0.5 text-[10px] font-semibold transition ${
                    Math.round(downPaymentRatio) === pct
                      ? "border-teal-600 bg-teal-600 text-white"
                      : "border-slate-200 bg-white text-slate-600 hover:bg-slate-100"
                  }`}
                >
                  {pct}% ({formatINR((goalTargetAmount * pct) / 100)})
                </button>
              ))}
            </div>
            <p className="text-[11px] text-slate-400">
              Loan Principal required: <strong>{formatINR(calculatedLoanAmount)}</strong>
            </p>
          </div>

          {/* 2. Interest Rate */}
          <div className="rounded-2xl border border-slate-200 bg-slate-50/70 p-4 space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-700">
                Annual Interest Rate
              </label>
              <span className="text-xs font-extrabold text-slate-800">{loanRatePct}% p.a.</span>
            </div>
            <div className="relative">
              <input
                type="number"
                step={0.1}
                min={3}
                max={25}
                value={loanRatePct}
                onChange={(e) => setLoanRatePct(e.target.value)}
                className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-bold text-slate-900 focus:border-teal-500 focus:outline-none"
              />
              <span className="absolute right-3.5 top-2.5 text-sm font-semibold text-slate-400">%</span>
            </div>
            <div className="flex flex-wrap gap-1">
              {["7.5", "8.5", "9.5", "11.0"].map((r) => (
                <button
                  key={r}
                  type="button"
                  onClick={() => setLoanRatePct(r)}
                  className={`rounded-lg border px-2.5 py-0.5 text-[10px] font-semibold transition ${
                    loanRatePct === r
                      ? "border-teal-600 bg-teal-600 text-white"
                      : "border-slate-200 bg-white text-slate-600 hover:bg-slate-100"
                  }`}
                >
                  {r}%
                </button>
              ))}
            </div>
            <p className="text-[11px] text-slate-400">
              Standard benchmark reducing-balance lending rate.
            </p>
          </div>

          {/* 3. Loan Tenure */}
          <div className="rounded-2xl border border-slate-200 bg-slate-50/70 p-4 space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-700">
                Repayment Tenure
              </label>
              <span className="text-xs font-extrabold text-slate-800">{tenureYears} Years</span>
            </div>
            <div className="relative">
              <input
                type="number"
                min={1}
                max={30}
                value={tenureYears}
                onChange={(e) => setTenureYears(e.target.value)}
                className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-bold text-slate-900 focus:border-teal-500 focus:outline-none"
              />
              <span className="absolute right-3.5 top-2.5 text-xs font-semibold text-slate-400">yrs</span>
            </div>
            <div className="flex flex-wrap gap-1">
              {["3", "5", "10", "15", "20"].map((y) => (
                <button
                  key={y}
                  type="button"
                  onClick={() => setTenureYears(y)}
                  className={`rounded-lg border px-2.5 py-0.5 text-[10px] font-semibold transition ${
                    tenureYears === y
                      ? "border-teal-600 bg-teal-600 text-white"
                      : "border-slate-200 bg-white text-slate-600 hover:bg-slate-100"
                  }`}
                >
                  {y}y
                </button>
              ))}
            </div>
            <p className="text-[11px] text-slate-400">
              Total of {numTenureYears * 12} monthly EMI payments.
            </p>
          </div>
        </div>

        {/* Quick Instant Preview & Affordability Bar */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-slate-50 p-4">
          <div className="flex flex-wrap items-center gap-4 text-xs">
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-bold">Estimated Monthly EMI</span>
              <span className="text-base font-extrabold text-slate-900">
                {formatINR(estimatedEmi)}/month
              </span>
            </div>
            <div className="border-l border-slate-200 pl-4">
              <span className="text-slate-400 block text-[10px] uppercase font-bold">Surplus Capacity</span>
              <span className="text-sm font-bold text-slate-800">
                {formatINR(availableMonthlySurplus)}/month
              </span>
            </div>
            <div className="border-l border-slate-200 pl-4">
              <span className="text-slate-400 block text-[10px] uppercase font-bold">Affordability Status</span>
              {isEmiAffordable ? (
                <span className="inline-flex items-center gap-1 font-bold text-emerald-700">
                  <span>✓</span> Affordable within surplus
                </span>
              ) : (
                <span className="inline-flex items-center gap-1 font-bold text-rose-600">
                  <span>⚠️</span> Exceeds surplus by {formatINR(Math.max(0, estimatedEmi - availableMonthlySurplus))}
                </span>
              )}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || numDownPayment <= 0 && calculatedLoanAmount <= 0}
            className="rounded-xl bg-teal-600 px-6 py-2.5 text-xs font-bold text-white shadow-sm transition hover:bg-teal-700 disabled:opacity-50"
          >
            {loading ? "Calculating Path…" : "Simulate Financing Path →"}
          </button>
        </div>
      </form>
    </section>
  );
}
