"use client";

import React from "react";
import type {
  SelfMoneyPathResult,
  FinancingPathResult,
  FundingComparisonMatrix,
} from "../../lib/api/goal-funding";

interface FundingPathComparisonProps {
  selfMoneyPath: SelfMoneyPathResult;
  financingPath: FinancingPathResult;
  comparisonMatrix: FundingComparisonMatrix;
  onSelectPath?: (pathType: "self_money" | "financing") => void;
  selectedPath?: "self_money" | "financing";
}

function formatINR(value: number | null | undefined): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return "—";
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

export default function FundingPathComparison({
  selfMoneyPath,
  financingPath,
  comparisonMatrix,
  onSelectPath,
  selectedPath = "self_money",
}: FundingPathComparisonProps) {
  const outflowDiff = comparisonMatrix.own_money_outflow_difference;
  const interestDrag = comparisonMatrix.financing_cost_drag;
  const residualDiff = comparisonMatrix.remaining_corpus_difference;

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm space-y-6">
      <div className="flex flex-col justify-between gap-2 border-b border-slate-100 pb-4 sm:flex-row sm:items-center">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
            Chapter 11 §11.7
          </span>
          <h3 className="text-lg font-extrabold text-slate-900">
            Side-by-Side Funding Paths Comparison
          </h3>
          <p className="mt-0.5 text-xs text-slate-500">
            Objective evaluation of capital outflow, interest cost drag, and wealth retention. The investor decides.
          </p>
        </div>
        <span className="self-start rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600 sm:self-auto">
          Deterministic Comparison Engine
        </span>
      </div>

      {/* Comparison Matrix Table */}
      <div className="overflow-x-auto rounded-2xl border border-slate-200">
        <table className="min-w-[650px] w-full text-left text-xs">
          <thead className="bg-slate-50 text-[11px] font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200">
            <tr>
              <th className="py-3 px-4 w-2/5">Decision Dimension</th>
              <th className="py-3 px-4 w-3/10 text-center bg-teal-50/50 text-teal-900">
                Path 1: Self Money
              </th>
              <th className="py-3 px-4 w-3/10 text-center bg-amber-50/50 text-amber-900">
                Path 2: Self Money + Financing
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {/* Total Own Outflow */}
            <tr className="hover:bg-slate-50">
              <td className="py-3 px-4 font-bold text-slate-700">
                Total Own Capital Outflow
                <span className="block text-[10px] font-normal text-slate-400">
                  Principal accumulated vs Down payment + all repayments
                </span>
              </td>
              <td className="py-3 px-4 text-center font-extrabold text-emerald-700 bg-teal-50/20">
                {formatINR(selfMoneyPath.total_own_contributions)}
                <span className="block text-[10px] text-emerald-600 font-semibold">
                  (Zero interest cost)
                </span>
              </td>
              <td className="py-3 px-4 text-center font-extrabold text-slate-800 bg-amber-50/20">
                {formatINR(financingPath.down_payment + financingPath.total_repayment)}
                <span className="block text-[10px] text-rose-600 font-semibold">
                  (+{formatINR(interestDrag)} loan interest)
                </span>
              </td>
            </tr>

            {/* Goal Funded */}
            <tr className="hover:bg-slate-50">
              <td className="py-3 px-4 font-bold text-slate-700">
                Goal Realization Amount
                <span className="block text-[10px] font-normal text-slate-400">
                  Total capital available for goal payment
                </span>
              </td>
              <td className="py-3 px-4 text-center font-bold text-slate-800 bg-teal-50/20">
                {formatINR(selfMoneyPath.goal_amount_funded)}
              </td>
              <td className="py-3 px-4 text-center font-bold text-slate-800 bg-amber-50/20">
                {formatINR(financingPath.goal_amount_funded)}
              </td>
            </tr>

            {/* Remaining Wealth After Goal */}
            <tr className="hover:bg-slate-50">
              <td className="py-3 px-4 font-bold text-slate-700">
                Residual Wealth After Goal
                <span className="block text-[10px] font-normal text-slate-400">
                  Remaining investment corpus post-payout
                </span>
              </td>
              <td className="py-3 px-4 text-center font-extrabold text-emerald-700 bg-teal-50/20">
                {formatINR(selfMoneyPath.remaining_corpus)}
                {residualDiff > 0 && (
                  <span className="block text-[10px] text-emerald-600 font-semibold">
                    +{formatINR(residualDiff)} retained
                  </span>
                )}
              </td>
              <td className="py-3 px-4 text-center font-bold text-slate-700 bg-amber-50/20">
                {formatINR(financingPath.remaining_corpus)}
              </td>
            </tr>

            {/* Monthly Debt Commitment */}
            <tr className="hover:bg-slate-50">
              <td className="py-3 px-4 font-bold text-slate-700">
                Monthly Debt Service (EMI)
                <span className="block text-[10px] font-normal text-slate-400">
                  Recurring monthly liability
                </span>
              </td>
              <td className="py-3 px-4 text-center font-extrabold text-emerald-700 bg-teal-50/20">
                ₹0 / month
                <span className="block text-[10px] text-emerald-600 font-semibold">
                  Zero debt commitment
                </span>
              </td>
              <td className="py-3 px-4 text-center font-bold text-rose-700 bg-amber-50/20">
                {formatINR(financingPath.monthly_emi)}/mo
                <span className="block text-[10px] text-slate-500">
                  for {financingPath.loan_tenure_months} months
                </span>
              </td>
            </tr>

            {/* Borrowing Cost Drag */}
            <tr className="hover:bg-slate-50">
              <td className="py-3 px-4 font-bold text-slate-700">
                Financing Cost Drag (Total Interest)
                <span className="block text-[10px] font-normal text-slate-400">
                  Financing overhead paid to lenders
                </span>
              </td>
              <td className="py-3 px-4 text-center font-extrabold text-emerald-700 bg-teal-50/20">
                ₹0
              </td>
              <td className="py-3 px-4 text-center font-bold text-rose-700 bg-amber-50/20">
                {formatINR(financingPath.total_interest_cost)}
              </td>
            </tr>

            {/* Funding Status Badge */}
            <tr className="hover:bg-slate-50">
              <td className="py-3 px-4 font-bold text-slate-700">
                Feasibility &amp; Coverage
              </td>
              <td className="py-3 px-4 text-center bg-teal-50/20">
                <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[11px] font-bold text-emerald-800">
                  {selfMoneyPath.is_fully_funded ? "✓ 100% Funded" : "⚠️ Partial"}
                </span>
              </td>
              <td className="py-3 px-4 text-center bg-amber-50/20">
                <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[11px] font-bold text-emerald-800">
                  {financingPath.is_fully_funded ? "✓ 100% Funded" : "⚠️ Partial"}
                </span>
              </td>
            </tr>

            {/* Path Selection Controls */}
            {onSelectPath && (
              <tr>
                <td className="py-3 px-4 font-bold text-slate-500">
                  Select for Execution
                </td>
                <td className="py-3 px-4 text-center bg-teal-50/30">
                  <button
                    type="button"
                    onClick={() => onSelectPath("self_money")}
                    className={`rounded-xl px-4 py-2 text-xs font-bold transition-all ${
                      selectedPath === "self_money"
                        ? "bg-teal-700 text-white shadow-sm"
                        : "border border-teal-600 bg-white text-teal-700 hover:bg-teal-50"
                    }`}
                  >
                    {selectedPath === "self_money" ? "Selected Path ✓" : "Choose Self Money"}
                  </button>
                </td>
                <td className="py-3 px-4 text-center bg-amber-50/30">
                  <button
                    type="button"
                    onClick={() => onSelectPath("financing")}
                    className={`rounded-xl px-4 py-2 text-xs font-bold transition-all ${
                      selectedPath === "financing"
                        ? "bg-amber-800 text-white shadow-sm"
                        : "border border-amber-600 bg-white text-amber-800 hover:bg-amber-50"
                    }`}
                  >
                    {selectedPath === "financing" ? "Selected Path ✓" : "Choose Financing"}
                  </button>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Trade-off Summary Callout */}
      <div className="rounded-2xl border border-amber-200 bg-amber-50/60 p-4">
        <h4 className="text-xs font-extrabold uppercase tracking-wider text-amber-900">
          Core Trade-off Summary (§11.7)
        </h4>
        <div className="mt-2 text-xs leading-5 text-amber-950 whitespace-pre-line font-medium">
          {comparisonMatrix.trade_off_summary}
        </div>
      </div>

      {/* Investor Decision Prompt */}
      <div className="rounded-2xl border border-navy-900 bg-navy-950 p-4 text-white">
        <div className="flex items-center gap-2">
          <span className="text-teal-400 font-bold text-base">⚖️</span>
          <h4 className="text-xs font-extrabold uppercase tracking-wider text-teal-300">
            Investor Decision Prompt (§11.7 Invariant)
          </h4>
        </div>
        <p className="mt-2 text-xs leading-5 text-slate-200">
          {comparisonMatrix.investor_decision_prompt}
        </p>
      </div>
    </section>
  );
}
