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

  const rMonthly = numLoanRate / 12 / 100;
  const nMonths = numTenureYears * 12;
  const estimatedEmi =
    rMonthly > 0 && nMonths > 0
      ? (calculatedLoanAmount * rMonthly * Math.pow(1 + rMonthly, nMonths)) /
        (Math.pow(1 + rMonthly, nMonths) - 1)
      : nMonths > 0
      ? calculatedLoanAmount / nMonths
      : 0;

  const totalInterest = Math.max(0, Math.round(estimatedEmi * nMonths - calculatedLoanAmount));
  const isEmiAffordable = availableMonthlySurplus > 0 && estimatedEmi <= availableMonthlySurplus;

  const handleUpdate = () => {
    onAssess({
      down_payment: numDownPayment,
      loan_annual_interest_rate_pct: numLoanRate,
      loan_tenure_months: numTenureYears * 12,
    });
  };

  return (
    <div className="rounded-2xl border border-amber-200 bg-amber-50/50 p-5 space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-amber-200/60 pb-3">
        <div>
          <h4 className="text-sm font-extrabold text-amber-950">
            Loan &amp; Financing Calculator
          </h4>
          <p className="text-xs text-amber-800">
            Adjust your down payment and loan tenure to see how it affects your monthly EMI and total interest.
          </p>
        </div>
        <span className="self-start rounded-full bg-white px-3 py-1 text-xs font-bold text-amber-900 border border-amber-200 sm:self-auto">
          Interactive Simulation
        </span>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {/* 1. Down Payment */}
        <div className="rounded-xl border border-slate-200 bg-white p-3.5 space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold text-slate-700">Own Down Payment</label>
            <span className="text-[11px] font-bold text-teal-700">
              {Math.round(downPaymentRatio)}% of goal
            </span>
          </div>
          <div className="relative">
            <span className="absolute left-3 top-2 text-xs font-bold text-slate-400">₹</span>
            <input
              type="number"
              min={0}
              max={goalTargetAmount}
              value={downPayment}
              onChange={(e) => setDownPayment(e.target.value)}
              className="w-full rounded-lg border border-slate-200 bg-white pl-7 pr-3 py-1.5 text-xs font-bold text-slate-900 focus:border-teal-500 focus:outline-none"
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
                className={`rounded-md border px-2 py-0.5 text-[10px] font-semibold transition ${
                  Math.round(downPaymentRatio) === pct
                    ? "border-teal-600 bg-teal-600 text-white"
                    : "border-slate-200 bg-slate-50 text-slate-600 hover:bg-slate-100"
                }`}
              >
                {pct}%
              </button>
            ))}
          </div>
          <p className="text-[10px] text-slate-500">
            Loan Needed: <strong className="text-slate-800">{formatINR(calculatedLoanAmount)}</strong>
          </p>
        </div>

        {/* 2. Interest Rate */}
        <div className="rounded-xl border border-slate-200 bg-white p-3.5 space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold text-slate-700">Interest Rate</label>
            <span className="text-xs font-bold text-slate-900">{loanRatePct}% p.a.</span>
          </div>
          <div className="relative">
            <input
              type="number"
              step={0.1}
              min={3}
              max={25}
              value={loanRatePct}
              onChange={(e) => setLoanRatePct(e.target.value)}
              className="w-full rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-bold text-slate-900 focus:border-teal-500 focus:outline-none"
            />
            <span className="absolute right-3 top-2 text-xs font-semibold text-slate-400">%</span>
          </div>
          <div className="flex flex-wrap gap-1">
            {["7.5", "8.5", "9.5", "11.0"].map((r) => (
              <button
                key={r}
                type="button"
                onClick={() => setLoanRatePct(r)}
                className={`rounded-md border px-2 py-0.5 text-[10px] font-semibold transition ${
                  loanRatePct === r
                    ? "border-teal-600 bg-teal-600 text-white"
                    : "border-slate-200 bg-slate-50 text-slate-600 hover:bg-slate-100"
                }`}
              >
                {r}%
              </button>
            ))}
          </div>
          <p className="text-[10px] text-slate-500">Benchmark bank lending rate</p>
        </div>

        {/* 3. Loan Tenure */}
        <div className="rounded-xl border border-slate-200 bg-white p-3.5 space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold text-slate-700">Repayment Period</label>
            <span className="text-xs font-bold text-slate-900">{tenureYears} Years</span>
          </div>
          <div className="relative">
            <input
              type="number"
              min={1}
              max={30}
              value={tenureYears}
              onChange={(e) => setTenureYears(e.target.value)}
              className="w-full rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-bold text-slate-900 focus:border-teal-500 focus:outline-none"
            />
            <span className="absolute right-3 top-2 text-xs font-semibold text-slate-400">yrs</span>
          </div>
          <div className="flex flex-wrap gap-1">
            {["5", "10", "15", "20"].map((y) => (
              <button
                key={y}
                type="button"
                onClick={() => setTenureYears(y)}
                className={`rounded-md border px-2 py-0.5 text-[10px] font-semibold transition ${
                  tenureYears === y
                    ? "border-teal-600 bg-teal-600 text-white"
                    : "border-slate-200 bg-slate-50 text-slate-600 hover:bg-slate-100"
                }`}
              >
                {y}y
              </button>
            ))}
          </div>
          <p className="text-[10px] text-slate-500">Total {numTenureYears * 12} monthly installments</p>
        </div>
      </div>

      {/* Summary Banner with Recalculate CTA */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 rounded-xl bg-white p-3.5 border border-amber-200">
        <div className="flex flex-wrap items-center gap-4 text-xs">
          <div>
            <span className="text-slate-400 block text-[10px] font-semibold">Monthly EMI</span>
            <span className="text-base font-extrabold text-slate-900">
              {formatINR(estimatedEmi)}/mo
            </span>
          </div>
          <div className="border-l border-slate-200 pl-3">
            <span className="text-slate-400 block text-[10px] font-semibold">Total Borrowing Cost</span>
            <span className="text-xs font-bold text-rose-700">
              +{formatINR(totalInterest)} (Interest)
            </span>
          </div>
          <div className="border-l border-slate-200 pl-3">
            <span className="text-slate-400 block text-[10px] font-semibold">Affordability Status</span>
            {isEmiAffordable ? (
              <span className="inline-flex items-center gap-1 font-bold text-emerald-700">
                <span>✓</span> Fits in your monthly budget
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 font-bold text-rose-600">
                <span>⚠️</span> Exceeds surplus by {formatINR(Math.max(0, estimatedEmi - availableMonthlySurplus))}
              </span>
            )}
          </div>
        </div>

        <button
          type="button"
          onClick={handleUpdate}
          disabled={loading}
          className="rounded-xl bg-amber-600 px-5 py-2 text-xs font-bold text-white shadow-xs transition hover:bg-amber-700 disabled:opacity-50 cursor-pointer"
        >
          {loading ? "Updating Table…" : "Apply to Projections Table →"}
        </button>
      </div>
    </div>
  );
}
