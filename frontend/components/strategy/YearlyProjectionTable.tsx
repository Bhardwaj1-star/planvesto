"use client";

import React from "react";
import type { PathProjectionRow } from "../../lib/api/goal-funding";

interface YearlyProjectionTableProps {
  projections: PathProjectionRow[];
  title?: string;
  description?: string;
  showFinancingColumns?: boolean;
}

function formatINR(value: number | null | undefined): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return "—";
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

export default function YearlyProjectionTable({
  projections,
  title = "Year-by-Year Growth Trajectory",
  description = "Annual breakdown of opening balances, contributions, compounding returns, and target payout.",
  showFinancingColumns = false,
}: YearlyProjectionTableProps) {
  if (!projections || projections.length === 0) {
    return (
      <section className="rounded-3xl border border-dashed border-slate-300 bg-white p-8 text-center">
        <p className="text-sm text-slate-500">No projection data available yet.</p>
      </section>
    );
  }

  const lastIndex = projections.length - 1;

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex flex-col justify-between gap-1 sm:flex-row sm:items-center">
        <div>
          <h3 className="text-lg font-bold text-slate-900">{title}</h3>
          {description && (
            <p className="text-xs text-slate-500 mt-0.5">{description}</p>
          )}
        </div>
        <span className="self-start rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600 sm:self-auto">
          {projections.length} {projections.length === 1 ? "Year" : "Years"} Horizon
        </span>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-slate-200">
        <table className="min-w-[700px] w-full text-left text-xs">
          <thead className="sticky top-0 bg-slate-50 text-[11px] font-bold uppercase tracking-wider text-slate-500 border-b border-slate-200">
            <tr>
              <th className="py-3 px-3 text-center">Year</th>
              <th className="py-3 px-3 text-center">Calendar Year</th>
              <th className="py-3 px-3 text-right">Opening Balance</th>
              {!showFinancingColumns && (
                <>
                  <th className="py-3 px-3 text-right">Annual SIP</th>
                  <th className="py-3 px-3 text-right text-emerald-700">Compounding Growth</th>
                </>
              )}
              {showFinancingColumns && (
                <>
                  <th className="py-3 px-3 text-right text-amber-700">Loan Disbursed</th>
                  <th className="py-3 px-3 text-right text-rose-700">Annual EMI Paid</th>
                </>
              )}
              <th className="py-3 px-3 text-right text-teal-800">Goal Payout</th>
              <th className="py-3 px-3 text-right">Closing Wealth</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {projections.map((row, idx) => {
              const isTargetYear = idx === lastIndex;
              return (
                <tr
                  key={row.year_index}
                  className={`transition-colors ${
                    isTargetYear
                      ? "bg-teal-50/70 font-semibold text-teal-950"
                      : idx % 2 === 1
                      ? "bg-slate-50/40"
                      : "bg-white hover:bg-slate-50"
                  }`}
                >
                  <td className="py-3 px-3 text-center font-bold text-slate-700">
                    Yr {row.year_index}
                  </td>
                  <td className="py-3 px-3 text-center text-slate-500">
                    {row.calendar_year}
                  </td>
                  <td className="py-3 px-3 text-right">
                    {formatINR(row.opening_balance)}
                  </td>
                  {!showFinancingColumns && (
                    <>
                      <td className="py-3 px-3 text-right text-slate-800">
                        {row.annual_contributions > 0
                          ? formatINR(row.annual_contributions)
                          : "—"}
                      </td>
                      <td className="py-3 px-3 text-right text-emerald-600 font-medium">
                        {row.investment_growth > 0
                          ? `+${formatINR(row.investment_growth)}`
                          : "—"}
                      </td>
                    </>
                  )}
                  {showFinancingColumns && (
                    <>
                      <td className="py-3 px-3 text-right text-amber-700 font-medium">
                        {row.financing_disbursement > 0
                          ? `+${formatINR(row.financing_disbursement)}`
                          : "—"}
                      </td>
                      <td className="py-3 px-3 text-right text-rose-600 font-medium">
                        {row.annual_debt_repayment > 0
                          ? `-${formatINR(row.annual_debt_repayment)}`
                          : "—"}
                      </td>
                    </>
                  )}
                  <td className="py-3 px-3 text-right font-bold text-teal-700">
                    {row.goal_withdrawal > 0 ? (
                      <span className="rounded-lg bg-teal-100/90 px-2.5 py-1 text-teal-900">
                        {formatINR(row.goal_withdrawal)}
                      </span>
                    ) : (
                      "—"
                    )}
                  </td>
                  <td className="py-3 px-3 text-right font-bold text-slate-900">
                    {formatINR(row.closing_balance)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="mt-3 flex flex-wrap items-center justify-between gap-2 text-[11px] text-slate-400">
        <span>* Growth compounded systematically based on your investment plan.</span>
        <span className="flex items-center gap-1.5 font-medium text-teal-800">
          <span className="h-2 w-2 rounded-full bg-teal-500"></span>
          Highlighted row indicates goal completion milestone
        </span>
      </div>
    </section>
  );
}
