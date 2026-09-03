"use client";

import { useState } from "react";
import { supabase } from "../../lib/supabase";

type StrategyResult = {
  strategy_id: string;
  strategy_name: string;
  annual_return: number;
  monthly_investment: number;
  required_monthly_investment: number;
  projected_corpus: number;
  funding_gap: number;
  total_contribution: number;
  time_horizon_years: number;
  initial_capital: number;
};

export default function StrategyBuilderPage() {
  const [goalAmount, setGoalAmount] = useState("10000000");
  const [timeHorizon, setTimeHorizon] = useState("10");
  const [currentCorpus, setCurrentCorpus] = useState("0");
  const [monthlyInvestment, setMonthlyInvestment] = useState("25000");
  const [existingInvestments, setExistingInvestments] = useState("0");
  const [expectedReturn, setExpectedReturn] = useState("12");

  const [showResult, setShowResult] = useState(false);
  const [results, setResults] = useState<StrategyResult[]>([]);
  const [isBuilding, setIsBuilding] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const buildStrategy = async () => {
    if (isBuilding) return;

    setIsBuilding(true);
    setErrorMessage("");

    try {
      const { data: userData, error: userError } = await supabase.auth.getUser();
      const user = userData.user;

      if (userError || !user) {
        throw new Error("Please log in before building your strategy.");
      }

      const response = await fetch("http://127.0.0.1:8000/api/strategy/build", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: user.id,
          name: user.user_metadata?.full_name || "",
          email: user.email || "",
          goal_amount: Number(goalAmount),
          time_horizon_years: Number(timeHorizon),
          current_corpus: Number(currentCorpus),
          monthly_investment: Number(monthlyInvestment),
          existing_investments: Number(existingInvestments),
          expected_annual_return: Number(expectedReturn),
        }),
      });

      const responseBody = await response.json();
      if (!response.ok) {
        throw new Error(responseBody.detail || "Unable to build your strategy.");
      }

      const strategyResults = responseBody.data?.results;
      if (!Array.isArray(strategyResults)) {
        throw new Error("The strategy response was incomplete. Please try again.");
      }

      setResults(strategyResults);
      setShowResult(true);
    } catch (error) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "Unable to build your strategy. Please try again.",
      );
    } finally {
      setIsBuilding(false);
    }
  };

  const formatCurrency = (value: string | number) => {
    const number = Number(value || 0);
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(number);
  };

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <a href="/" className="text-xl font-bold text-slate-900">
            Planvesto
          </a>

          <a
            href="/investor"
            className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium hover:bg-slate-50"
          >
            Investor Area
          </a>
        </div>
      </header>

      <section className="mx-auto max-w-6xl px-6 py-12">
        <div className="mb-10 max-w-3xl">
          <p className="mb-3 text-sm font-semibold uppercase tracking-wider text-teal-700">
            Strategy Builder
          </p>

          <h1 className="text-4xl font-bold tracking-tight text-slate-950">
            Build your strategy
          </h1>

          <p className="mt-4 text-lg leading-8 text-slate-600">
            Start with your goal, current financial position and investment
            capacity. Explore different paths before making a decision.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-[1fr_0.8fr]">
          {/* INPUT SECTION */}
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-bold">Your starting point</h2>

            <p className="mt-2 text-sm text-slate-500">
              Enter the basic numbers for this strategy.
            </p>

            <div className="mt-8 space-y-6">
              <div>
                <label className="mb-2 block text-sm font-semibold">
                  Goal amount
                </label>

                <input
                  type="number"
                  value={goalAmount}
                  onChange={(e) => setGoalAmount(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-teal-600"
                />

                <p className="mt-1 text-xs text-slate-500">
                  Example: ₹1 Crore
                </p>
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold">
                  Time horizon
                </label>

                <div className="relative">
                  <input
                    type="number"
                    value={timeHorizon}
                    onChange={(e) => setTimeHorizon(e.target.value)}
                    className="w-full rounded-xl border border-slate-300 px-4 py-3 pr-20 outline-none focus:border-teal-600"
                  />

                  <span className="absolute right-4 top-1/2 -translate-y-1/2 text-sm text-slate-500">
                    years
                  </span>
                </div>
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold">
                  Current corpus
                </label>

                <input
                  type="number"
                  value={currentCorpus}
                  onChange={(e) => setCurrentCorpus(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-teal-600"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold">
                  Monthly investment capacity
                </label>

                <input
                  type="number"
                  value={monthlyInvestment}
                  onChange={(e) => setMonthlyInvestment(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-teal-600"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold">
                  Existing investments
                </label>

                <input
                  type="number"
                  value={existingInvestments}
                  onChange={(e) => setExistingInvestments(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-teal-600"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold">
                  Expected annual return
                </label>

                <div className="relative">
                  <input
                    type="number"
                    value={expectedReturn}
                    onChange={(e) => setExpectedReturn(e.target.value)}
                    className="w-full rounded-xl border border-slate-300 px-4 py-3 pr-12 outline-none focus:border-teal-600"
                  />

                  <span className="absolute right-4 top-1/2 -translate-y-1/2 text-sm text-slate-500">
                    %
                  </span>
                </div>

                <p className="mt-1 text-xs text-slate-500">
                  Demo assumption only. Returns are not guaranteed.
                </p>
              </div>

              <button
                onClick={buildStrategy}
                disabled={isBuilding}
                className="w-full rounded-xl bg-slate-950 px-6 py-4 font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isBuilding ? "Building Strategy..." : "Build Strategy"}
              </button>

              {errorMessage && (
                <p className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700" role="alert">
                  {errorMessage}
                </p>
              )}
            </div>
          </section>

          {/* SUMMARY SECTION */}
          <section className="space-y-6">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Your target
              </p>

              <h2 className="mt-2 text-3xl font-bold">
                {formatCurrency(goalAmount)}
              </h2>

              <p className="mt-2 text-slate-500">
                over {timeHorizon || 0} years
              </p>

              <div className="mt-6 grid grid-cols-2 gap-4">
                <div className="rounded-xl bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">Current corpus</p>
                  <p className="mt-1 font-semibold">
                    {formatCurrency(currentCorpus)}
                  </p>
                </div>

                <div className="rounded-xl bg-slate-50 p-4">
                  <p className="text-xs text-slate-500">Monthly capacity</p>
                  <p className="mt-1 font-semibold">
                    {formatCurrency(monthlyInvestment)}
                  </p>
                </div>
              </div>
            </div>

            {!showResult ? (
              <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-8 text-center">
                <h3 className="font-semibold">Strategy results will appear here</h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                  Enter your numbers and select Build Strategy to explore
                  possible paths.
                </p>
              </div>
            ) : (
              <>
                <div className="rounded-2xl border border-teal-100 bg-teal-50 p-6">
                  <p className="text-xs font-semibold uppercase tracking-wider text-teal-700">
                    Strategy preview
                  </p>

                  <h3 className="mt-2 text-2xl font-bold">
                    Explore multiple paths
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-slate-600">
                    This prototype will compare different combinations of
                    monthly contribution, initial capital and time horizon.
                  </p>
                </div>

                <div className="space-y-4">
                  {results.map((result, index) => (
                    <div className="rounded-2xl border border-slate-200 bg-white p-5" key={result.strategy_id}>
                      <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                        Strategy {String(index + 1).padStart(2, "0")}
                      </p>

                      <h3 className="mt-2 text-lg font-bold">{result.strategy_name}</h3>

                      <div className="mt-4 grid gap-2 text-sm text-slate-500 sm:grid-cols-2">
                        <p>Annual return: {result.annual_return}%</p>
                        <p>Time horizon: {result.time_horizon_years} years</p>
                        <p>Monthly investment: {formatCurrency(result.monthly_investment)}</p>
                        <p>Required monthly investment: {formatCurrency(result.required_monthly_investment)}</p>
                        <p>Projected corpus: {formatCurrency(result.projected_corpus)}</p>
                        <p>Funding gap: {formatCurrency(result.funding_gap)}</p>
                        <p>Total contribution: {formatCurrency(result.total_contribution)}</p>
                        <p>Initial capital: {formatCurrency(result.initial_capital)}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </section>
        </div>
      </section>
    </main>
  );
}