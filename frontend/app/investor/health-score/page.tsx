"use client";

import { useState } from "react";
import Link from "next/link";
import { InvestorProfileMenu } from "../../../components/InvestorProfileMenu";

// ============================================================================
// DATA CONTRACT: FINANCIAL HEALTH SCORE (Presentation Layer Only - No Formulas)
// ============================================================================
// Health Score evaluates overall financial resilience and personal financial
// positioning (Liquidity Reserve, Debt Burden, Savings Discipline, Protection).
// NOTE: It is distinct from investment portfolio SLR (Safety, Liquidity, Return).

export interface HealthDimension {
  id: string;
  name: string;
  score: number; // 0 - 100
  status: "Excellent" | "Strong" | "Moderate" | "Needs Attention";
  explanation: string;
  keyDrivers: string[];
}

export interface ScoreDriver {
  id: string;
  factor: string;
  impactType: "positive" | "negative";
  impactPoints: string;
  explanation: string;
}

export interface ImprovementPriority {
  id: string;
  priorityRank: 1 | 2 | 3;
  dimensionName: string;
  problem: string;
  recommendedAction: string;
  expectedImpact: string;
  actionCtaText: string;
  targetLink: string;
}

export interface TrendDataPoint {
  periodLabel: string;
  score: number;
}

export interface FinancialHealthScoreResponse {
  overallScore: number; // e.g. 76
  scoreMax: number; // 100
  statusLabel: "Excellent" | "Strong" | "Moderate" | "Needs Attention";
  statusSummary: string;
  evaluatedDate: string;
  previousScore: number;
  scoreChange: number;
  trendText: string;
  explanation: {
    statusHeadline: string;
    narrative: string;
    positiveFactors: string[];
    attentionAreas: string[];
  };
  dimensions: HealthDimension[];
  drivers: ScoreDriver[];
  priorities: [ImprovementPriority, ImprovementPriority, ImprovementPriority]; // Exactly 3
  trend: {
    monthly: TrendDataPoint[];
    quarterly: TrendDataPoint[];
  };
}

// ============================================================================
// STATIC UI PREVIEW PLACEHOLDER (NO FORMULAS / NO BACKEND LOGIC)
// ============================================================================

const PLACEHOLDER_HEALTH_SCORE_DATA: FinancialHealthScoreResponse = {
  overallScore: 76,
  scoreMax: 100,
  statusLabel: "Strong",
  statusSummary:
    "Your financial position shows dependable cash flow surplus and minimal high-cost debt, with room to reinforce emergency reserves and long-term protection cover.",
  evaluatedDate: "September 2026",
  previousScore: 71,
  scoreChange: +5,
  trendText: "+5 pts since last evaluation",
  explanation: {
    statusHeadline: "Stable Foundation with Clear Opportunities to Optimize",
    narrative:
      "A score of 76 indicates that your fundamental finances are in good health. Your monthly debt service ratio is well within safe thresholds and your net investable savings rate is robust. Strengthening your instant cash emergency buffer and updating family healthcare cover will help elevate your resilience toward the 'Excellent' benchmark.",
    positiveFactors: [
      "Low Debt Burden: Zero high-interest credit card debt; secured home EMI is only 18% of monthly income.",
      "Healthy Savings Flow: Consistently generating ~32% investable surplus after living expenses.",
      "Disciplined Outflows: Living costs are well-controlled within established budgetary limits.",
    ],
    attentionAreas: [
      "Emergency Reserve Shortfall: Current liquid funds cover 3.8 months (target is 6 months of baseline outflows).",
      "Health Protection Gap: Base family healthcare floater lacks adequate buffer against high medical inflation.",
      "Idle Cash Drag: Significant balance sitting in zero-return current/savings accounts.",
    ],
  },
  dimensions: [
    {
      id: "dim-emergency",
      name: "Emergency Preparedness",
      score: 64,
      status: "Moderate",
      explanation: "Measures liquid reserves available to withstand unexpected job or income interruptions without distress.",
      keyDrivers: [
        "Current reserve covers 3.8 months of household expenses.",
        "Target guideline recommends 6 months of living costs in high-liquidity accounts.",
      ],
    },
    {
      id: "dim-debt",
      name: "Debt Sustainability",
      score: 90,
      status: "Excellent",
      explanation: "Evaluates debt burden, EMI-to-income ratio, and reliance on unsecured borrowing.",
      keyDrivers: [
        "EMI-to-income ratio is 18% (well below the 40% danger threshold).",
        "Zero revolving credit card balances or high-cost personal loans.",
      ],
    },
    {
      id: "dim-savings",
      name: "Savings & Cash Flow Discipline",
      score: 82,
      status: "Strong",
      explanation: "Assesses net surplus generation after living expenses and monthly wealth accumulation rate.",
      keyDrivers: [
        "Investable surplus represents 32% of total post-tax monthly income.",
        "Consistent month-on-month accumulation towards established milestones.",
      ],
    },
    {
      id: "dim-protection",
      name: "Risk & Insurance Protection",
      score: 68,
      status: "Moderate",
      explanation: "Measures insurance shields safeguarding family dependents and accumulated assets from catastrophic shocks.",
      keyDrivers: [
        "Pure term life cover equals 14x annual household expenses.",
        "Medical insurance requires super top-up reinforcement to match rising hospitalization costs.",
      ],
    },
  ],
  drivers: [
    {
      id: "drv-1",
      factor: "Low Debt-to-Income Leverage",
      impactType: "positive",
      impactPoints: "+18 pts",
      explanation: "Keeping monthly EMI commitments below 20% of net income provides immense cash flow flexibility.",
    },
    {
      id: "drv-2",
      factor: "Consistent Monthly Investable Surplus",
      impactType: "positive",
      impactPoints: "+14 pts",
      explanation: "Generating an investable surplus above 30% of income accelerates goal compounding and debt safety.",
    },
    {
      id: "drv-3",
      factor: "Adequate Pure Term Life Protection",
      impactType: "positive",
      impactPoints: "+9 pts",
      explanation: "14x annual expenditure coverage shields your family dependents from unforeseen loss of income.",
    },
    {
      id: "drv-4",
      factor: "Sub-optimal Emergency Cash Buffer",
      impactType: "negative",
      impactPoints: "-10 pts",
      explanation: "3.8 months of liquid reserves leaves you slightly exposed to prolonged income disruptions or emergencies.",
    },
    {
      id: "drv-5",
      factor: "Healthcare Super Top-Up Coverage Gap",
      impactType: "negative",
      impactPoints: "-5 pts",
      explanation: "Base employer floater policy is vulnerable to catastrophic hospitalization claims and co-pays.",
    },
  ],
  priorities: [
    {
      id: "prio-1",
      priorityRank: 1,
      dimensionName: "Emergency Preparedness",
      problem: "Liquid emergency reserve covers only 3.8 months of recurring household expenses.",
      recommendedAction: "Allocate ₹12,000 monthly from current surplus into an instant-access liquid fund or high-yield savings buffer.",
      expectedImpact: "Expands emergency coverage from 3.8 to 6.0 months within 7 months, enhancing financial peace of mind.",
      actionCtaText: "Adjust Budget Buffer",
      targetLink: "/investor/budgeting",
    },
    {
      id: "prio-2",
      priorityRank: 2,
      dimensionName: "Risk & Insurance Protection",
      problem: "Family floater health coverage is vulnerable to high medical inflation and critical illness expenses.",
      recommendedAction: "Institute a ₹15 Lakh Super Top-Up health policy to complement your base health cover.",
      expectedImpact: "Protects long-term investment assets from unexpected hospitalization and out-of-pocket medical bills.",
      actionCtaText: "Review Financial State",
      targetLink: "/investor/financial-state",
    },
    {
      id: "prio-3",
      priorityRank: 3,
      dimensionName: "Savings & Cash Flow Discipline",
      problem: "Idle savings balance is generating sub-inflation returns without deliberate goal mapping.",
      recommendedAction: "Establish automated systematic transfers (STP) of idle capital towards critical long-term milestones.",
      expectedImpact: "Reduces purchasing power erosion and accelerates milestone achievement timelines by 12–18 months.",
      actionCtaText: "Open Goal Planner",
      targetLink: "/investor/goal-planner",
    },
  ],
  trend: {
    monthly: [
      { periodLabel: "Apr", score: 68 },
      { periodLabel: "May", score: 70 },
      { periodLabel: "Jun", score: 71 },
      { periodLabel: "Jul", score: 73 },
      { periodLabel: "Aug", score: 74 },
      { periodLabel: "Sep", score: 76 },
    ],
    quarterly: [
      { periodLabel: "Q3 2025", score: 64 },
      { periodLabel: "Q4 2025", score: 67 },
      { periodLabel: "Q1 2026", score: 70 },
      { periodLabel: "Q2 2026", score: 73 },
      { periodLabel: "Q3 2026", score: 76 },
    ],
  },
};

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export default function InvestorHealthScorePage() {
  // Period control for trend chart: Monthly vs Quarterly
  const [trendPeriod, setTrendPeriod] = useState<"monthly" | "quarterly">("monthly");

  // UI state switcher for demonstrating Normal, Loading, Empty, Error
  const [uiState, setUiState] = useState<"normal" | "loading" | "empty" | "error">("normal");

  // Interactive details modal for priorities
  const [activeModalPriority, setActiveModalPriority] = useState<ImprovementPriority | null>(null);

  const data = PLACEHOLDER_HEALTH_SCORE_DATA;
  const activeTrendPoints = trendPeriod === "monthly" ? data.trend.monthly : data.trend.quarterly;

  // Gauge calculations for the circular score (Radius 70)
  const radius = 72;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (data.overallScore / data.scoreMax) * circumference;

  // ==========================================================================
  // RENDER: LOADING STATE
  // ==========================================================================
  if (uiState === "loading") {
    return (
      <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10" aria-busy="true">
        <div className="mx-auto max-w-6xl space-y-6">
          <div className="flex justify-end gap-2 pb-2">
            <span className="text-xs font-semibold text-slate-400 self-center">UI State Preview:</span>
            <button
              onClick={() => setUiState("normal")}
              className="rounded-lg bg-white px-3 py-1 text-xs font-bold text-slate-700 border border-slate-200"
            >
              Normal
            </button>
            <button
              onClick={() => setUiState("empty")}
              className="rounded-lg bg-white px-3 py-1 text-xs font-bold text-slate-700 border border-slate-200"
            >
              Empty
            </button>
            <button
              onClick={() => setUiState("error")}
              className="rounded-lg bg-white px-3 py-1 text-xs font-bold text-slate-700 border border-slate-200"
            >
              Error
            </button>
          </div>

          <div className="h-8 w-64 animate-pulse rounded-lg bg-slate-200" />
          <div className="h-64 animate-pulse rounded-3xl bg-white shadow-sm" />
          <div className="grid grid-cols-1 gap-5 md:grid-cols-4">
            <div className="h-44 animate-pulse rounded-3xl bg-white shadow-sm" />
            <div className="h-44 animate-pulse rounded-3xl bg-white shadow-sm" />
            <div className="h-44 animate-pulse rounded-3xl bg-white shadow-sm" />
            <div className="h-44 animate-pulse rounded-3xl bg-white shadow-sm" />
          </div>
          <div className="h-80 animate-pulse rounded-3xl bg-white shadow-sm" />
        </div>
      </main>
    );
  }

  // ==========================================================================
  // RENDER: ERROR STATE
  // ==========================================================================
  if (uiState === "error") {
    return (
      <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
        <div className="mx-auto max-w-2xl rounded-3xl border border-red-200 bg-white p-8 text-center shadow-sm">
          <div className="flex justify-end gap-2 pb-4">
            <button
              onClick={() => setUiState("normal")}
              className="rounded-lg bg-navy-900 px-3 py-1 text-xs font-bold text-white"
            >
              Back to Normal
            </button>
          </div>
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-red-50 text-red-600">
            <svg className="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h2 className="mt-4 text-xl font-bold text-slate-900">Health Score Assessment Unavailable</h2>
          <p className="mt-2 text-sm text-slate-600">
            We encountered a temporary issue generating your financial health diagnostic. Please try again.
          </p>
          <button
            onClick={() => setUiState("normal")}
            className="mt-6 inline-flex items-center rounded-xl bg-navy-900 px-6 py-2.5 text-sm font-semibold text-white transition hover:bg-navy-800"
          >
            Retry Diagnosis
          </button>
        </div>
      </main>
    );
  }

  // ==========================================================================
  // RENDER: EMPTY STATE
  // ==========================================================================
  if (uiState === "empty") {
    return (
      <main className="min-h-screen bg-[#f6f8fb] p-6 lg:p-10">
        <div className="mx-auto max-w-2xl rounded-3xl border border-slate-200 bg-white p-10 text-center shadow-sm">
          <div className="flex justify-end gap-2 pb-4">
            <button
              onClick={() => setUiState("normal")}
              className="rounded-lg bg-navy-900 px-3 py-1 text-xs font-bold text-white"
            >
              Show Populated State
            </button>
          </div>
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-teal-50 text-teal-700">
            <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h2 className="mt-4 text-2xl font-black text-slate-950">No Health Score Recorded Yet</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-600 max-w-md mx-auto">
            Your Health Score is generated once your income, expenses, debts, and assets are recorded in your Financial State.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            <Link
              href="/investor/financial-state"
              className="inline-flex items-center rounded-xl bg-teal-700 px-6 py-3 text-sm font-bold text-white transition hover:bg-teal-800"
            >
              Complete Financial State →
            </Link>
          </div>
        </div>
      </main>
    );
  }

  // ==========================================================================
  // RENDER: NORMAL POPULATED STATE
  // ==========================================================================
  return (
    <main className="min-h-screen bg-[#f6f8fb] text-slate-900 pb-20">
      {/* 1. PAGE HEADER */}
      <header className="border-b border-slate-200 bg-white sticky top-0 z-10">
        <div className="mx-auto flex min-h-[80px] max-w-6xl items-center justify-between gap-6 px-6 lg:px-8">
          <div>
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center rounded-md bg-teal-50 px-2 py-0.5 text-xs font-semibold text-teal-700 ring-1 ring-inset ring-teal-600/20">
                Financial Health Assessment
              </span>
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-400">
                Diagnostic Overview
              </p>
            </div>
            <h1 className="mt-1 text-2xl font-extrabold tracking-tight text-slate-950 sm:text-3xl">
              Health Score
            </h1>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center border-r border-slate-200 pr-3">
              <span className="text-xs text-slate-400 font-semibold mr-2">Evaluated:</span>
              <span className="text-xs font-bold text-slate-700 bg-slate-100 px-2.5 py-1 rounded-md">
                {data.evaluatedDate}
              </span>
            </div>

            {/* Quick Demo State Selector */}
            <select
              aria-label="UI Preview State Switcher"
              value={uiState}
              onChange={(e) => setUiState(e.target.value as typeof uiState)}
              className="rounded-lg border border-slate-200 bg-white px-2 py-1.5 text-xs font-semibold text-slate-600 outline-none hover:bg-slate-50"
            >
              <option value="normal">UI: Populated</option>
              <option value="empty">UI: Empty</option>
              <option value="loading">UI: Loading</option>
              <option value="error">UI: Error</option>
            </select>

            <InvestorProfileMenu />
          </div>
        </div>
      </header>

      {/* Supporting Banner / Placeholder Notice */}
      <div className="border-b border-teal-200 bg-teal-50/60 px-6 py-2.5 text-xs text-teal-900">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4">
          <p className="flex items-center gap-2">
            <span className="flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-teal-200 text-teal-800 font-bold text-[10px]">
              ✓
            </span>
            <span>
              Your Health Score provides an overall diagnostic of your financial health and highlights the most important areas for improvement.
            </span>
          </p>
          <span className="shrink-0 font-bold uppercase tracking-wider text-[10px] text-teal-800 bg-teal-100 px-2 py-0.5 rounded">
            Preview / Placeholder Data
          </span>
        </div>
      </div>

      <div className="mx-auto max-w-6xl px-6 pt-8 lg:px-8 space-y-8">
        {/* ================================================================== */}
        {/* 2. OVERALL HEALTH SCORE (Prominent Hero Section)                   */}
        {/* ================================================================== */}
        <section
          aria-labelledby="overall-health-score-title"
          className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-10 shadow-soft"
        >
          <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
            {/* Left Narrative */}
            <div className="max-w-xl space-y-4">
              <div className="flex items-center gap-2.5">
                <span className="rounded-lg bg-emerald-50 border border-emerald-200 px-3 py-1 text-xs font-black uppercase tracking-wider text-emerald-800">
                  Status: {data.statusLabel}
                </span>
                <span className="text-xs font-bold text-teal-700 bg-teal-50 px-2.5 py-1 rounded-lg">
                  {data.trendText}
                </span>
              </div>

              <h2
                id="overall-health-score-title"
                className="text-3xl sm:text-4xl font-black tracking-tight text-slate-950"
              >
                Overall Health Score: {data.overallScore}
                <span className="text-xl sm:text-2xl font-semibold text-slate-400"> / {data.scoreMax}</span>
              </h2>

              <p className="text-sm leading-relaxed text-slate-600">
                {data.statusSummary}
              </p>

              <div className="pt-2">
                <div className="flex items-center gap-3 text-xs font-semibold text-slate-500">
                  <span>Benchmark:</span>
                  <span className="rounded bg-slate-100 px-2 py-0.5 text-slate-700 font-bold">85+ Excellent</span>
                  <span className="rounded bg-teal-50 text-teal-800 px-2 py-0.5 font-bold">70–84 Strong</span>
                  <span className="rounded bg-amber-50 text-amber-800 px-2 py-0.5 font-bold">50–69 Moderate</span>
                </div>
              </div>
            </div>

            {/* Right Visual Circular Score Gauge */}
            <div className="flex flex-col items-center justify-center p-4">
              <div className="relative flex items-center justify-center">
                <svg className="h-44 w-44 transform -rotate-90" viewBox="0 0 160 160">
                  {/* Background Track */}
                  <circle
                    cx="80"
                    cy="80"
                    r={radius}
                    stroke="#E2E8F0"
                    strokeWidth="14"
                    fill="transparent"
                  />
                  {/* Progress Ring */}
                  <circle
                    cx="80"
                    cy="80"
                    r={radius}
                    stroke="#0F766E"
                    strokeWidth="14"
                    strokeDasharray={circumference}
                    strokeDashoffset={strokeDashoffset}
                    strokeLinecap="round"
                    fill="transparent"
                    className="transition-all duration-1000 ease-out"
                  />
                </svg>

                {/* Center Content */}
                <div className="absolute flex flex-col items-center justify-center text-center">
                  <span className="text-4xl font-black text-slate-950">{data.overallScore}</span>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                    out of {data.scoreMax}
                  </span>
                  <span className="mt-1 text-[10px] font-extrabold text-teal-800 bg-teal-50 px-2.5 py-0.5 rounded-full border border-teal-200">
                    {data.statusLabel}
                  </span>
                </div>
              </div>

              <p className="mt-3 text-xs font-semibold text-slate-500 text-center">
                Reflects current position across 4 health dimensions
              </p>
            </div>
          </div>
        </section>

        {/* ================================================================== */}
        {/* 3. HEALTH DIMENSIONS BREAKDOWN                                      */}
        {/* ================================================================== */}
        <section aria-labelledby="health-dimensions-title" className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 id="health-dimensions-title" className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Financial Health Dimensions
            </h2>
            <span className="text-xs font-semibold text-slate-500">
              4 Core Diagnostic Pillars
            </span>
          </div>

          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {data.dimensions.map((dim) => (
              <div
                key={dim.id}
                className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm flex flex-col justify-between hover:border-slate-300 transition"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-900 truncate pr-2">
                      {dim.name}
                    </span>
                    <span
                      className={`shrink-0 rounded-md px-2 py-0.5 text-[10px] font-bold ${
                        dim.status === "Excellent"
                          ? "bg-emerald-50 text-emerald-800 border border-emerald-200"
                          : dim.status === "Strong"
                          ? "bg-teal-50 text-teal-800 border border-teal-200"
                          : dim.status === "Moderate"
                          ? "bg-amber-50 text-amber-800 border border-amber-200"
                          : "bg-rose-50 text-rose-800 border border-rose-200"
                      }`}
                    >
                      {dim.status}
                    </span>
                  </div>

                  <div className="mt-4 flex items-baseline gap-2">
                    <span className="text-3xl font-black text-slate-950">{dim.score}</span>
                    <span className="text-xs font-semibold text-slate-400">/ 100</span>
                  </div>

                  {/* Progress bar */}
                  <div className="mt-2 h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        dim.score >= 80 ? "bg-emerald-600" : dim.score >= 70 ? "bg-teal-600" : "bg-amber-500"
                      }`}
                      style={{ width: `${dim.score}%` }}
                    />
                  </div>

                  <p className="mt-3 text-xs text-slate-600 leading-relaxed">
                    {dim.explanation}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 space-y-1">
                  <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Key Drivers</p>
                  {dim.keyDrivers.map((driver, idx) => (
                    <p key={idx} className="text-xs text-slate-600 leading-normal">• {driver}</p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ================================================================== */}
        {/* 4. KEY DRIVERS: What's Driving Your Score?                         */}
        {/* ================================================================== */}
        <section aria-labelledby="key-drivers-title" className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-8 shadow-sm">
          <div className="border-b border-slate-100 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
              Factor Breakdown
            </span>
            <h2 id="key-drivers-title" className="mt-1 text-xl font-extrabold text-slate-950">
              What&rsquo;s Driving Your Score?
            </h2>
            <p className="mt-0.5 text-xs text-slate-500">
              The major positive and negative factors influencing your overall financial health score.
            </p>
          </div>

          <div className="mt-6 divide-y divide-slate-100">
            {data.drivers.map((driver) => (
              <div key={driver.id} className="py-4 first:pt-0 last:pb-0 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                <div className="flex items-start gap-3">
                  <span
                    className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-lg font-black text-xs ${
                      driver.impactType === "positive"
                        ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                        : "bg-rose-50 text-rose-700 border border-rose-200"
                    }`}
                  >
                    {driver.impactType === "positive" ? "+" : "−"}
                  </span>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">{driver.factor}</h3>
                    <p className="text-xs text-slate-600 mt-0.5 leading-relaxed">{driver.explanation}</p>
                  </div>
                </div>

                <div className="sm:self-center shrink-0">
                  <span
                    className={`inline-flex items-center rounded-lg px-2.5 py-1 text-xs font-extrabold ${
                      driver.impactType === "positive"
                        ? "bg-emerald-50 text-emerald-800"
                        : "bg-rose-50 text-rose-800"
                    }`}
                  >
                    {driver.impactPoints} impact
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ================================================================== */}
        {/* 5. TOP 3 PRIORITIES & 6. ACTIONS                                   */}
        {/* ================================================================== */}
        <section aria-labelledby="top-priorities-title" className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
                Actionable Gap Analysis
              </span>
              <h2 id="top-priorities-title" className="mt-1 text-xl font-extrabold text-slate-950 sm:text-2xl">
                Top 3 Priorities
              </h2>
            </div>
            <span className="text-xs font-semibold text-slate-500">
              Ranked by impact on financial health
            </span>
          </div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            {data.priorities.map((item) => (
              <div
                key={item.id}
                className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm flex flex-col justify-between hover:border-teal-300 transition"
              >
                <div>
                  {/* Priority Header */}
                  <div className="flex items-center justify-between">
                    <span className="flex h-6 w-6 items-center justify-center rounded-lg bg-navy-900 text-white font-bold text-xs">
                      #{item.priorityRank}
                    </span>
                    <span className="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-bold text-slate-700">
                      {item.dimensionName}
                    </span>
                  </div>

                  {/* Problem */}
                  <div className="mt-4">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                      Identified Problem
                    </p>
                    <p className="mt-1 text-sm font-extrabold text-slate-950 leading-snug">
                      {item.problem}
                    </p>
                  </div>

                  {/* Recommended Action */}
                  <div className="mt-4 rounded-2xl bg-slate-50 p-3.5 border border-slate-100">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                      Recommended Action
                    </p>
                    <p className="mt-1 text-xs text-slate-700 font-medium leading-relaxed">
                      {item.recommendedAction}
                    </p>
                  </div>

                  {/* Expected Financial Impact */}
                  <div className="mt-3">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-teal-700">
                      Expected Financial Impact
                    </p>
                    <p className="mt-0.5 text-xs font-bold text-slate-800 leading-snug">
                      {item.expectedImpact}
                    </p>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="mt-6 pt-4 border-t border-slate-100 flex items-center gap-2">
                  <Link
                    href={item.targetLink}
                    className="flex-1 text-center rounded-xl bg-navy-900 py-2.5 text-xs font-bold text-white transition hover:bg-navy-800"
                  >
                    {item.actionCtaText} →
                  </Link>

                  <button
                    type="button"
                    onClick={() => setActiveModalPriority(item)}
                    className="rounded-xl border border-slate-200 px-3 py-2.5 text-xs font-semibold text-slate-600 hover:bg-slate-50 transition"
                  >
                    View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ================================================================== */}
        {/* 7. SCORE TREND (Health Score Trend)                                */}
        {/* ================================================================== */}
        <section aria-labelledby="score-trend-title" className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-8 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-100 pb-5">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
                Progression History
              </span>
              <h2 id="score-trend-title" className="mt-1 text-xl font-extrabold text-slate-950 sm:text-2xl">
                Health Score Trend
              </h2>
              <p className="mt-0.5 text-xs text-slate-500">
                Track how changes in savings, debt payoff, and protection affect your overall score over time.
              </p>
            </div>

            {/* Monthly / Quarterly Controls */}
            <div className="inline-flex rounded-xl bg-slate-100 p-1 border border-slate-200">
              <button
                type="button"
                onClick={() => setTrendPeriod("monthly")}
                className={`rounded-lg px-3.5 py-1.5 text-xs font-bold transition ${
                  trendPeriod === "monthly"
                    ? "bg-white text-navy-900 shadow-xs"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Monthly
              </button>
              <button
                type="button"
                onClick={() => setTrendPeriod("quarterly")}
                className={`rounded-lg px-3.5 py-1.5 text-xs font-bold transition ${
                  trendPeriod === "quarterly"
                    ? "bg-white text-navy-900 shadow-xs"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Quarterly
              </button>
            </div>
          </div>

          {/* Metric Cards & Trend Visualization */}
          <div className="mt-6 space-y-6">
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              <div className="rounded-2xl bg-slate-50 p-4 border border-slate-100">
                <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Current Score</p>
                <p className="mt-1 text-2xl font-black text-slate-950">{data.overallScore}</p>
                <p className="text-xs text-teal-700 font-semibold mt-0.5">{data.statusLabel}</p>
              </div>

              <div className="rounded-2xl bg-slate-50 p-4 border border-slate-100">
                <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Previous Score</p>
                <p className="mt-1 text-2xl font-black text-slate-950">{data.previousScore}</p>
                <p className="text-xs text-slate-500 mt-0.5">Prior evaluation</p>
              </div>

              <div className="rounded-2xl bg-slate-50 p-4 border border-slate-100">
                <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Net Improvement</p>
                <p className="mt-1 text-2xl font-black text-emerald-700">+{data.scoreChange} pts</p>
                <p className="text-xs text-slate-500 mt-0.5">Recent progression</p>
              </div>

              <div className="rounded-2xl bg-slate-50 p-4 border border-slate-100">
                <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Direction</p>
                <p className="mt-1 text-xl font-black text-teal-700">↗ Upward</p>
                <p className="text-xs text-slate-500 mt-0.5">Positive trajectory</p>
              </div>
            </div>

            {/* Clean SVG Trend Chart */}
            <div className="rounded-2xl bg-slate-50/80 p-6 border border-slate-200">
              <div className="h-44 w-full flex items-end justify-between gap-2 px-2 pt-6">
                {activeTrendPoints.map((pt, idx) => {
                  const min = 50;
                  const max = 100;
                  const heightPercent = Math.max(15, Math.min(100, ((pt.score - min) / (max - min)) * 100));

                  return (
                    <div key={idx} className="flex-1 flex flex-col items-center gap-2 group">
                      <span className="text-xs font-bold text-slate-700 group-hover:text-teal-700 transition">
                        {pt.score}
                      </span>
                      <div className="w-full max-w-[48px] bg-slate-200 rounded-t-lg overflow-hidden h-28 flex items-end">
                        <div
                          className="w-full bg-teal-700 transition-all duration-500 rounded-t-lg group-hover:bg-teal-600"
                          style={{ height: `${heightPercent}%` }}
                        />
                      </div>
                      <span className="text-[11px] font-bold text-slate-500 mt-1">
                        {pt.periodLabel}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </section>

        {/* ================================================================== */}
        {/* 8. HEALTH SCORE EXPLANATION (Decision-oriented Narrative)          */}
        {/* ================================================================== */}
        <section aria-labelledby="explanation-title" className="rounded-3xl border border-slate-200 bg-white p-6 lg:p-8 shadow-sm">
          <div className="border-b border-slate-100 pb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
              Understanding Your Results
            </span>
            <h2 id="explanation-title" className="mt-1 text-xl font-extrabold text-slate-950">
              Health Score Explanation
            </h2>
            <p className="mt-0.5 text-xs text-slate-500">
              Clear breakdown of what your score signifies for your financial journey.
            </p>
          </div>

          <div className="mt-6 space-y-6">
            <div className="rounded-2xl bg-teal-50/60 p-5 border border-teal-100">
              <h3 className="text-sm font-black text-teal-950">
                {data.explanation.statusHeadline}
              </h3>
              <p className="mt-2 text-xs leading-relaxed text-slate-700">
                {data.explanation.narrative}
              </p>
            </div>

            <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
              {/* Positive Factors */}
              <div className="rounded-2xl bg-emerald-50/50 p-5 border border-emerald-100">
                <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-900 flex items-center gap-1.5">
                  <span>✓</span>
                  <span>Key Positive Factors</span>
                </h4>
                <ul className="mt-3 space-y-2">
                  {data.explanation.positiveFactors.map((item, idx) => (
                    <li key={idx} className="text-xs text-slate-700 leading-relaxed">
                      • {item}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Attention Areas */}
              <div className="rounded-2xl bg-amber-50/50 p-5 border border-amber-100">
                <h4 className="text-xs font-bold uppercase tracking-wider text-amber-900 flex items-center gap-1.5">
                  <span>⚠️</span>
                  <span>Key Areas Requiring Attention</span>
                </h4>
                <ul className="mt-3 space-y-2">
                  {data.explanation.attentionAreas.map((item, idx) => (
                    <li key={idx} className="text-xs text-slate-700 leading-relaxed">
                      • {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* Footer Navigation Link */}
        <div className="rounded-3xl border border-slate-200 bg-white p-6 text-center shadow-xs">
          <p className="text-xs text-slate-500">
            Address identified priorities through dedicated financial planning modules:
          </p>
          <div className="mt-3 flex flex-wrap justify-center gap-3">
            <Link
              href="/investor/budgeting"
              className="inline-flex items-center rounded-xl border border-slate-200 bg-white px-5 py-2.5 text-xs font-bold text-slate-700 transition hover:bg-slate-50"
            >
              Optimize Cash Flow in Budgeting →
            </Link>
            <Link
              href="/investor/goal-planner"
              className="inline-flex items-center rounded-xl bg-navy-900 px-6 py-2.5 text-xs font-bold text-white transition hover:bg-navy-800"
            >
              Plan Goals in Goal Planner →
            </Link>
          </div>
        </div>
      </div>

      {/* Action / Detail Modal (UI only) */}
      {activeModalPriority && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-xs p-4"
          role="dialog"
          aria-modal="true"
        >
          <div className="w-full max-w-lg rounded-3xl bg-white p-6 sm:p-8 shadow-card space-y-5 animate-fadeIn">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <span className="text-xs font-bold uppercase tracking-wider text-teal-700">
                Priority #{activeModalPriority.priorityRank} · {activeModalPriority.dimensionName}
              </span>
              <button
                type="button"
                onClick={() => setActiveModalPriority(null)}
                className="text-slate-400 hover:text-slate-600 text-lg font-bold"
              >
                ✕
              </button>
            </div>

            <div>
              <h3 className="text-lg font-black text-slate-950">
                {activeModalPriority.problem}
              </h3>
            </div>

            <div className="rounded-2xl bg-teal-50/70 p-4 border border-teal-100">
              <p className="text-xs font-bold uppercase tracking-wider text-teal-900">Recommended Action Plan</p>
              <p className="mt-1 text-sm font-semibold text-slate-800 leading-relaxed">
                {activeModalPriority.recommendedAction}
              </p>
            </div>

            <div className="rounded-2xl bg-slate-50 p-4 border border-slate-100">
              <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Expected Financial Impact</p>
              <p className="mt-1 text-xs font-bold text-teal-700">
                {activeModalPriority.expectedImpact}
              </p>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setActiveModalPriority(null)}
                className="rounded-xl border border-slate-200 px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50"
              >
                Dismiss
              </button>
              <Link
                href={activeModalPriority.targetLink}
                className="rounded-xl bg-navy-900 px-5 py-2 text-xs font-bold text-white hover:bg-navy-800"
              >
                Proceed to Action →
              </Link>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
