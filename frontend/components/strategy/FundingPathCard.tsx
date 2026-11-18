"use client";

import React from "react";

interface FinancingDetails {
  downPayment: number;
  financingAmount: number;
  monthlyEmi: number;
  totalInterestCost: number;
  totalRepayment: number;
  emiAffordable: boolean;
  loanTenureMonths: number;
  interestRatePct: number;
}

interface FundingPathCardProps {
  type: "self_money" | "financing";
  totalContributions: number;
  projectedCorpus: number;
  goalAmountFunded: number;
  remainingCorpus: number;
  isFullyFunded: boolean;
  explanation: string;
  financingDetails?: FinancingDetails;
  selected?: boolean;
  onSelect?: () => void;
}

function formatINR(value: number | null | undefined): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return "—";
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

export default function FundingPathCard({
  type,
  totalContributions,
  projectedCorpus,
  goalAmountFunded,
  remainingCorpus,
  isFullyFunded,
  explanation,
  financingDetails,
  selected = false,
  onSelect,
}: FundingPathCardProps) {
  const isFinancing = type === "financing";

  return (
    <article
      className={`relative rounded-3xl border bg-white p-6 shadow-sm transition-all ${
        selected
          ? "border-teal-500 ring-2 ring-teal-100"
          : "border-slate-200 hover:border-slate-300"
      }`}
    >
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <span
            className={`inline-block rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wide ${
              isFinancing
                ? "bg-amber-50 text-amber-800 border border-amber-200"
                : "bg-teal-50 text-teal-800 border border-teal-200"
            }`}
          >
            {isFinancing ? "Path 2: Self Money + Financing" : "Path 1: Self Money (100% Own Funds)"}
          </span>
          <h3 className="mt-2 text-xl font-extrabold text-slate-900">
            {isFinancing ? "Structured Financing & Down Payment" : "Systematic Accumulation & Compounding"}
          </h3>
          <p className="mt-1 text-xs text-slate-500">
            {isFinancing
              ? "Combines upfront equity down payment with amortized debt facility."
              : "Disciplined SIPs and full compound wealth retention without loan interest."}
          </p>
        </div>

        <div className="flex items-center gap-2">
          {isFullyFunded ? (
            <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-bold text-emerald-700 border border-emerald-200">
              ✓ Fully Funded
            </span>
          ) : (
            <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-bold text-amber-700 border border-amber-200">
              ⚠️ Partial Coverage
            </span>
          )}
        </div>
      </div>

      {/* Primary Metrics Grid */}
      <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <div className="rounded-2xl bg-slate-50 p-3.5">
          <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
            {isFinancing ? "Total Cash Outflow" : "Total Own Savings"}
          </p>
          <p className="mt-1 text-base font-extrabold text-slate-900">
            {formatINR(totalContributions)}
          </p>
          <p className="text-[10px] text-slate-400">
            {isFinancing ? "Down payment + all EMIs" : "Principal invested"}
          </p>
        </div>

        <div className="rounded-2xl bg-slate-50 p-3.5">
          <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Corpus at Target Date
          </p>
          <p className="mt-1 text-base font-extrabold text-slate-900">
            {formatINR(projectedCorpus)}
          </p>
          <p className="text-[10px] text-slate-400">Value accumulated</p>
        </div>

        <div className="rounded-2xl bg-slate-50 p-3.5">
          <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Goal Amount Funded
          </p>
          <p className="mt-1 text-base font-extrabold text-teal-700">
            {formatINR(goalAmountFunded)}
          </p>
          <p className="text-[10px] text-slate-400">Disbursed for goal</p>
        </div>

        <div className="rounded-2xl bg-slate-50 p-3.5">
          <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Remaining Net Wealth
          </p>
          <p className="mt-1 text-base font-extrabold text-emerald-700">
            {formatINR(remainingCorpus)}
          </p>
          <p className="text-[10px] text-slate-400">Post-goal surplus</p>
        </div>
      </div>

      {/* Financing Details Specific Sub-Panel */}
      {isFinancing && financingDetails && (
        <div className="mt-4 rounded-2xl border border-amber-200/80 bg-amber-50/40 p-4">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-amber-200/50 pb-2">
            <span className="text-xs font-extrabold uppercase tracking-wider text-amber-900">
              Loan & Repayment Structure (§11.6)
            </span>
            {financingDetails.emiAffordable ? (
              <span className="flex items-center gap-1 rounded-full bg-emerald-100 px-2.5 py-0.5 text-[11px] font-bold text-emerald-800">
                <span>✓</span> EMI Within Surplus Limit
              </span>
            ) : (
              <span className="flex items-center gap-1 rounded-full bg-rose-100 px-2.5 py-0.5 text-[11px] font-bold text-rose-800">
                <span>⚠️</span> EMI Exceeds Current Surplus
              </span>
            )}
          </div>

          <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-4 text-xs">
            <div>
              <span className="text-slate-500 block text-[10px] uppercase font-semibold">Down Payment</span>
              <span className="font-extrabold text-slate-900">{formatINR(financingDetails.downPayment)}</span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px] uppercase font-semibold">Loan Principal</span>
              <span className="font-extrabold text-slate-900">{formatINR(financingDetails.financingAmount)}</span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px] uppercase font-semibold">Monthly EMI</span>
              <span className="font-extrabold text-slate-900">{formatINR(financingDetails.monthlyEmi)}/mo</span>
              <span className="text-[10px] text-slate-500 block">for {financingDetails.loanTenureMonths} mos @ {financingDetails.interestRatePct}%</span>
            </div>
            <div>
              <span className="text-slate-500 block text-[10px] uppercase font-semibold text-rose-700">Borrowing Interest Drag</span>
              <span className="font-extrabold text-rose-700">{formatINR(financingDetails.totalInterestCost)}</span>
            </div>
          </div>
        </div>
      )}

      {/* Narrative Explanation */}
      <p className="mt-4 text-xs leading-5 text-slate-600 bg-slate-50/80 p-3 rounded-xl border border-slate-100">
        <strong className="text-slate-800">Operational Summary:</strong> {explanation}
      </p>

      {/* Select button if provided */}
      {onSelect && (
        <div className="mt-4 flex justify-end">
          <button
            type="button"
            onClick={onSelect}
            className={`rounded-xl px-4 py-2 text-xs font-bold transition-all ${
              selected
                ? "bg-teal-600 text-white"
                : "border border-slate-200 bg-white text-slate-700 hover:bg-slate-50"
            }`}
          >
            {selected ? "Active Funding Path ✓" : "Inspect this Path"}
          </button>
        </div>
      )}
    </article>
  );
}
