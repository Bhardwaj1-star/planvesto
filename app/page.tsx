"use client";

import { useState } from "react";
import { useMobileMenuClose } from "../hooks/useMobileMenuClose";

export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false);
  useMobileMenuClose(setMenuOpen);

  return (
    <>

<header className="fixed inset-x-0 top-0 z-50 border-b border-slate-200/70 bg-white/90 backdrop-blur-xl">
<div className="mx-auto flex h-20 max-w-[1200px] items-center justify-between px-5 lg:px-8">

<a aria-label="Planvesto Home" className="flex items-center gap-2.5" href="/">
<div className="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-900">
<svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<path d="M5 17L10 12L13 15L19 8" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2"></path>
<path d="M15 8H19V12" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2"></path>
</svg>
</div>
<span className="text-xl font-extrabold tracking-tight text-navy-900">
                planvesto
            </span>
</a>

<nav aria-label="Main navigation" className="hidden items-center gap-8 lg:flex">
<a className="text-sm font-bold text-navy-900" href="/">
                Home
            </a>
<a className="text-sm font-medium text-slate-600 transition hover:text-navy-900" href="/plan">
                Plan
            </a>
<a className="text-sm font-medium text-slate-600 transition hover:text-navy-900" href="/invest">
                Invest
            </a>
<a className="text-sm font-medium text-slate-600 transition hover:text-navy-900" href="/protect">
                Protect
            </a>
<a className="text-sm font-medium text-slate-600 transition hover:text-navy-900" href="/decide">
                Decide
            </a>
<a className="text-sm font-medium text-slate-600 transition hover:text-navy-900" href="/learn">
                Learn
            </a>
<a className="text-sm font-medium text-slate-600 transition hover:text-navy-900" href="/about">
                About
            </a>
</nav>

<div className="hidden items-center gap-3 lg:flex">
<a className="rounded-xl px-4 py-2.5 text-sm font-semibold text-navy-900 transition hover:bg-slate-100" href="/login">
                Login
            </a>
<a className="rounded-xl bg-navy-900 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-navy-800" href="/plan">
                Start Planning
            </a>
</div>

<button aria-expanded={menuOpen} aria-label="Open navigation menu" className="rounded-lg p-2 text-navy-900 lg:hidden" id="menuButton" onClick={() => setMenuOpen(!menuOpen)} type="button">
<svg className="h-6 w-6" fill="none" id="menuIcon" stroke="currentColor" viewBox="0 0 24 24">
<path d="M4 6h16M4 12h16M4 18h16" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path>
</svg>
</button>
</div>

<div className={`mobile-menu border-t border-slate-200 bg-white lg:hidden ${menuOpen ? "" : "hidden"}`} id="mobileMenu">
<nav aria-label="Mobile navigation" className="mx-auto max-w-[1200px] px-5 py-5">
<div className="flex flex-col gap-1">
<a className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50" href="/">
                    Home
                </a>
<a className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50" href="/plan">
                    Plan
                </a>
<a className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50" href="/invest">
                    Invest
                </a>
<a className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50" href="/protect">
                    Protect
                </a>
<a className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50" href="/decide">
                    Decide
                </a>
<a className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50" href="/learn">
                    Learn
                </a>
<a className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50" href="/about">
                    About
                </a>
<div className="mt-3 grid grid-cols-2 gap-3 border-t border-slate-100 pt-4">
<a className="rounded-xl border border-slate-200 px-4 py-3 text-center text-sm font-semibold text-navy-900" href="/login">
                        Login
                    </a>
<a className="rounded-xl bg-navy-900 px-4 py-3 text-center text-sm font-semibold text-white" href="/plan">
                        Start Planning
                    </a>
</div>
</div>
</nav>
</div>
</header>
<main>

<section className="hero-grid relative overflow-hidden pt-32 lg:pt-40">
<div className="absolute inset-x-0 top-0 -z-10 h-[520px] bg-gradient-to-b from-teal-50/70 to-transparent"></div>
<div className="mx-auto max-w-[1200px] px-5 pb-20 lg:px-8 lg:pb-28">
<div className="grid items-center gap-14 lg:grid-cols-[1.05fr_0.95fr]">

<div>
<div className="mb-6 inline-flex items-center gap-2 rounded-full border border-teal-100 bg-teal-50 px-3.5 py-2">
<span className="h-2 w-2 rounded-full bg-teal-600"></span>
<span className="text-xs font-semibold tracking-wide text-teal-700">
                        Financial decision support
                    </span>
</div>
<h1 className="max-w-3xl text-5xl font-extrabold leading-[1.05] tracking-[-0.04em] text-navy-900 sm:text-6xl lg:text-[68px]">
                    Make better
                    <span className="gradient-text">financial decisions.</span>
</h1>
<p className="mt-7 max-w-xl text-lg leading-8 text-slate-600 lg:text-xl">
                    Understand where you stand, define what you want to achieve,
                    explore your options, and see what each decision could mean
                    for your financial future.
                </p>
<div className="mt-9 flex flex-col gap-3 sm:flex-row">
<a className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-navy-900/10 transition hover:bg-navy-800" href="/plan">
                        Start Planning

                        <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path d="M5 12h14M13 6l6 6-6 6" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path>
</svg>
</a>
<a className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-6 py-3.5 text-sm font-semibold text-navy-900 transition hover:border-slate-400 hover:bg-slate-50" href="/decide">
                        See How It Works
                    </a>
</div>
<div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-3 text-xs font-medium text-slate-500">
<span className="flex items-center gap-2">
<span className="h-1.5 w-1.5 rounded-full bg-teal-600"></span>
                        Goals
                    </span>
<span className="flex items-center gap-2">
<span className="h-1.5 w-1.5 rounded-full bg-teal-600"></span>
                        Investments
                    </span>
<span className="flex items-center gap-2">
<span className="h-1.5 w-1.5 rounded-full bg-teal-600"></span>
                        Protection
                    </span>
<span className="flex items-center gap-2">
<span className="h-1.5 w-1.5 rounded-full bg-teal-600"></span>
                        Decisions
                    </span>
</div>
</div>

<div className="relative">
<div className="absolute -inset-5 rounded-[32px] bg-teal-100/40 blur-2xl"></div>
<div className="relative rounded-[28px] border border-slate-200 bg-white p-5 shadow-soft sm:p-7">
<div className="flex items-center justify-between border-b border-slate-100 pb-5">
<div>
<p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                                Financial decision
                            </p>
<h2 className="mt-1 text-lg font-bold text-navy-900">
                                Build ₹1 Crore in 10 years
                            </h2>
</div>
<div className="rounded-xl bg-teal-50 px-3 py-2 text-xs font-bold text-teal-700">
                            Explore
                        </div>
</div>
<div className="mt-6 space-y-1">
<div className="decision-line flex gap-4 pb-7">
<div className="relative z-10 flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-navy-900 text-white">
<svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h7l5 5v11a2 2 0 01-2 2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
</svg>
</div>
<div>
<p className="text-sm font-bold text-navy-900">
                                    Understand your starting point
                                </p>
<p className="mt-1 text-sm leading-6 text-slate-500">
                                    Income, expenses, savings, assets, liabilities and existing investments.
                                </p>
</div>
</div>
<div className="decision-line flex gap-4 pb-7">
<div className="relative z-10 flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-teal-600 text-white">
<svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path d="M12 3v18m9-9H3" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
</svg>
</div>
<div>
<p className="text-sm font-bold text-navy-900">
                                    Explore possible paths
                                </p>
<p className="mt-1 text-sm leading-6 text-slate-500">
                                    Increase contributions, add capital, change the timeline, or combine actions.
                                </p>
</div>
</div>
<div className="flex gap-4">
<div className="relative z-10 flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-slate-100 text-navy-900">
<svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path d="M8 12l3 3 5-6" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
</svg>
</div>
<div>
<p className="text-sm font-bold text-navy-900">
                                    Compare before you decide
                                </p>
<p className="mt-1 text-sm leading-6 text-slate-500">
                                    See outcomes, uncertainty and trade-offs across the alternatives.
                                </p>
</div>
</div>
</div>
<div className="mt-7 rounded-2xl bg-slate-50 p-4">
<div className="flex items-center justify-between">
<span className="text-xs font-semibold text-slate-500">
                                Decision principle
                            </span>
<span className="text-xs font-bold text-teal-700">
                                You decide
                            </span>
</div>
<p className="mt-2 text-sm font-semibold leading-6 text-navy-900">
                            Planvesto helps you understand what each choice means.
                        </p>
</div>
</div>
</div>
</div>
</div>
</section>

<section className="border-y border-slate-200 bg-white">
<div className="mx-auto grid max-w-[1200px] gap-0 px-5 sm:grid-cols-3 lg:px-8">
<div className="border-b border-slate-200 py-7 sm:border-b-0 sm:border-r sm:pr-8">
<p className="text-sm font-bold text-navy-900">
                Your financial reality
            </p>
<p className="mt-1 text-sm leading-6 text-slate-500">
                Decisions start with where you actually stand.
            </p>
</div>
<div className="border-b border-slate-200 py-7 sm:border-b-0 sm:px-8 sm:border-r">
<p className="text-sm font-bold text-navy-900">
                Your goals
            </p>
<p className="mt-1 text-sm leading-6 text-slate-500">
                Your desired outcomes shape the path forward.
            </p>
</div>
<div className="py-7 sm:pl-8">
<p className="text-sm font-bold text-navy-900">
                Your decision
            </p>
<p className="mt-1 text-sm leading-6 text-slate-500">
                You remain in control of the final choice.
            </p>
</div>
</div>
</section>

<section className="py-24 lg:py-32">
<div className="mx-auto max-w-[1200px] px-5 lg:px-8">
<div className="max-w-2xl">
<p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                One financial picture
            </p>
<h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                Your financial decisions are connected.
            </h2>
<p className="mt-5 text-lg leading-8 text-slate-600">
                A decision about investing can affect your goals, liquidity and
                risk. A protection decision can affect how much you can invest.
                Planvesto brings these considerations together.
            </p>
</div>
<div className="mt-14 grid gap-5 md:grid-cols-2 lg:grid-cols-4">

<a className="group rounded-2xl border border-slate-200 bg-white p-6 shadow-card transition duration-300 hover:-translate-y-1 hover:border-slate-300 hover:shadow-soft" href="/plan">
<div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-navy-900 text-white">
<svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
</svg>
</div>
<h3 className="mt-6 text-xl font-bold text-navy-900">
                    Plan
                </h3>
<p className="mt-3 text-sm leading-6 text-slate-500">
                    Understand your financial position and define the goals that matter to you.
                </p>
<span className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-navy-900">
                    Explore planning
                    <span className="transition group-hover:translate-x-1">→</span>
</span>
</a>

<a className="group rounded-2xl border border-slate-200 bg-white p-6 shadow-card transition duration-300 hover:-translate-y-1 hover:border-slate-300 hover:shadow-soft" href="/invest">
<div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-teal-600 text-white">
<svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path d="M4 19V5m0 14h16M8 15l3-4 3 2 5-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
</svg>
</div>
<h3 className="mt-6 text-xl font-bold text-navy-900">
                    Invest
                </h3>
<p className="mt-3 text-sm leading-6 text-slate-500">
                    Structure your capital around what your goals require.
                </p>
<span className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-navy-900">
                    Explore investing
                    <span className="transition group-hover:translate-x-1">→</span>
</span>
</a>

<a className="group rounded-2xl border border-slate-200 bg-white p-6 shadow-card transition duration-300 hover:-translate-y-1 hover:border-slate-300 hover:shadow-soft" href="/protect">
<div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-navy-900">
<svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path d="M12 3l8 4v5c0 4.8-3.4 7.9-8 9-4.6-1.1-8-4.2-8-9V7l8-4z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
<path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
</svg>
</div>
<h3 className="mt-6 text-xl font-bold text-navy-900">
                    Protect
                </h3>
<p className="mt-3 text-sm leading-6 text-slate-500">
                    Identify financial risks that could disrupt the plan you are building.
                </p>
<span className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-navy-900">
                    Explore protection
                    <span className="transition group-hover:translate-x-1">→</span>
</span>
</a>

<a className="group rounded-2xl border border-slate-200 bg-white p-6 shadow-card transition duration-300 hover:-translate-y-1 hover:border-slate-300 hover:shadow-soft" href="/decide">
<div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-navy-900 text-white">
<svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path d="M8 12h8M12 8v8" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
<circle cx="12" cy="12" r="9" strokeWidth="1.8"></circle>
</svg>
</div>
<h3 className="mt-6 text-xl font-bold text-navy-900">
                    Decide
                </h3>
<p className="mt-3 text-sm leading-6 text-slate-500">
                    Compare possible paths and understand the trade-offs before choosing.
                </p>
<span className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-navy-900">
                    Explore decisions
                    <span className="transition group-hover:translate-x-1">→</span>
</span>
</a>
</div>
</div>
</section>

<section className="bg-navy-900 py-24 text-white lg:py-32">
<div className="mx-auto max-w-[1200px] px-5 lg:px-8">
<div className="grid gap-16 lg:grid-cols-[0.85fr_1.15fr]">
<div>
<p className="text-sm font-bold uppercase tracking-widest text-teal-300">
                    How it works
                </p>
<h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] sm:text-5xl">
                    From financial reality to a decision.
                </h2>
<p className="mt-6 max-w-lg text-base leading-7 text-slate-300">
                    Planvesto turns a financial question into a set of understandable
                    choices so you can see what may need to change.
                </p>
<a className="mt-8 inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3.5 text-sm font-bold text-navy-900 transition hover:bg-slate-100" href="/decide">
                    See the decision process
                    <span>→</span>
</a>
</div>
<div className="space-y-7">

<div className="flex gap-5">
<div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        01
                    </div>
<div>
<h3 className="text-lg font-bold">
                            Understand where you are
                        </h3>
<p className="mt-2 text-sm leading-6 text-slate-400">
                            Look at your income, expenses, assets, liabilities,
                            liquidity and existing investments.
                        </p>
</div>
</div>

<div className="flex gap-5">
<div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        02
                    </div>
<div>
<h3 className="text-lg font-bold">
                            Define where you want to go
                        </h3>
<p className="mt-2 text-sm leading-6 text-slate-400">
                            Establish the goals, timelines, priorities and flexibility
                            that matter to you.
                        </p>
</div>
</div>

<div className="flex gap-5">
<div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        03
                    </div>
<div>
<h3 className="text-lg font-bold">
                            Explore possible paths
                        </h3>
<p className="mt-2 text-sm leading-6 text-slate-400">
                            Consider changes to contributions, capital, timelines,
                            investments, debt or protection where relevant.
                        </p>
</div>
</div>

<div className="flex gap-5">
<div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        04
                    </div>
<div>
<h3 className="text-lg font-bold">
                            Compare the consequences
                        </h3>
<p className="mt-2 text-sm leading-6 text-slate-400">
                            Understand possible outcomes, uncertainty and trade-offs.
                        </p>
</div>
</div>

<div className="flex gap-5">
<div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-teal-600 text-sm font-bold">
                        05
                    </div>
<div>
<h3 className="text-lg font-bold">
                            Make your decision
                        </h3>
<p className="mt-2 text-sm leading-6 text-slate-400">
                            Choose the path that fits your situation and priorities.
                        </p>
</div>
</div>
</div>
</div>
</div>
</section>

<section className="py-24 lg:py-32">
<div className="mx-auto max-w-[1200px] px-5 lg:px-8">
<div className="text-center">
<p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                Built around your decisions
            </p>
<h2 className="mx-auto mt-4 max-w-3xl text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                See the financial picture before acting.
            </h2>
<p className="mx-auto mt-5 max-w-2xl text-lg leading-8 text-slate-600">
                The value is not a list of products. It is understanding
                how different financial choices affect the whole picture.
            </p>
</div>
<div className="mt-14 grid gap-5 md:grid-cols-2">
<div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-card">
<div className="flex items-start justify-between">
<div className="flex h-11 w-11 items-center justify-center rounded-xl bg-teal-50 text-teal-700">
<svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path d="M4 19V5m0 14h16" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
<path d="M7 15l3-4 3 2 4-6" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
</svg>
</div>
<span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        01
                    </span>
</div>
<h3 className="mt-6 text-xl font-bold text-navy-900">
                    Understand your financial position
                </h3>
<p className="mt-3 text-sm leading-7 text-slate-500">
                    See the factors that shape what you can realistically do,
                    including cash flow, liquidity, assets, liabilities and existing investments.
                </p>
</div>
<div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-card">
<div className="flex items-start justify-between">
<div className="flex h-11 w-11 items-center justify-center rounded-xl bg-navy-900 text-white">
<svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path d="M5 19V5" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
<path d="M5 6c4-3 7 3 14 0v9c-7 3-10-3-14 0" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
</svg>
</div>
<span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        02
                    </span>
</div>
<h3 className="mt-6 text-xl font-bold text-navy-900">
                    Connect decisions to goals
                </h3>
<p className="mt-3 text-sm leading-7 text-slate-500">
                    A goal is more than a number. Its timing, importance,
                    funding and flexibility can change the choices available to you.
                </p>
</div>
<div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-card">
<div className="flex items-start justify-between">
<div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-100 text-navy-900">
<svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path d="M8 12h8M12 8v8" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
<circle cx="12" cy="12" r="9" strokeWidth="1.8"></circle>
</svg>
</div>
<span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        03
                    </span>
</div>
<h3 className="mt-6 text-xl font-bold text-navy-900">
                    Compare alternatives
                </h3>
<p className="mt-3 text-sm leading-7 text-slate-500">
                    See different ways of approaching a financial problem instead
                    of treating one predefined solution as the answer.
                </p>
</div>
<div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-card">
<div className="flex items-start justify-between">
<div className="flex h-11 w-11 items-center justify-center rounded-xl bg-teal-50 text-teal-700">
<svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
<path d="M5 4h14v16H5z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8"></path>
</svg>
</div>
<span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        04
                    </span>
</div>
<h3 className="mt-6 text-xl font-bold text-navy-900">
                    Understand trade-offs
                </h3>
<p className="mt-3 text-sm leading-7 text-slate-500">
                    See how a choice can affect goals, cash flow, liquidity,
                    risk, investments and protection.
                </p>
</div>
</div>
</div>
</section>

<section className="bg-slate-100 py-24 lg:py-28">
<div className="mx-auto max-w-[1200px] px-5 lg:px-8">
<div className="max-w-2xl">
<p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                Designed for clarity
            </p>
<h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                Financial decisions should be easier to understand.
            </h2>
</div>
<div className="mt-12 grid gap-5 md:grid-cols-3">
<article className="rounded-2xl border border-slate-200 bg-white p-7 shadow-card">
<div aria-label="5 out of 5 stars" className="flex gap-1 text-teal-600">
                    ★★★★★
                </div>
<blockquote className="mt-5 text-base font-medium leading-7 text-navy-900">
                    “I finally understood what I was actually choosing between,
                    instead of just being shown another investment.”
                </blockquote>
<div className="mt-7 border-t border-slate-100 pt-5">
<p className="text-sm font-bold text-navy-900">
                        Early user
                    </p>
<p className="mt-1 text-xs text-slate-500">
                        Financial planning
                    </p>
</div>
</article>
<article className="rounded-2xl border border-slate-200 bg-white p-7 shadow-card">
<div aria-label="5 out of 5 stars" className="flex gap-1 text-teal-600">
                    ★★★★★
                </div>
<blockquote className="mt-5 text-base font-medium leading-7 text-navy-900">
                    “The useful part was seeing the trade-off between investing
                    more and changing the goal timeline.”
                </blockquote>
<div className="mt-7 border-t border-slate-100 pt-5">
<p className="text-sm font-bold text-navy-900">
                        Early user
                    </p>
<p className="mt-1 text-xs text-slate-500">
                        Goal planning
                    </p>
</div>
</article>
<article className="rounded-2xl border border-slate-200 bg-white p-7 shadow-card">
<div aria-label="5 out of 5 stars" className="flex gap-1 text-teal-600">
                    ★★★★★
                </div>
<blockquote className="mt-5 text-base font-medium leading-7 text-navy-900">
                    “It made the connection between my investments and the rest
                    of my financial plan much clearer.”
                </blockquote>
<div className="mt-7 border-t border-slate-100 pt-5">
<p className="text-sm font-bold text-navy-900">
                        Early user
                    </p>
<p className="mt-1 text-xs text-slate-500">
                        Investment planning
                    </p>
</div>
</article>
</div>
<p className="mt-5 text-xs text-slate-400">
            Illustrative testimonials shown for design purposes.
        </p>
</div>
</section>

<section className="py-24 lg:py-32">
<div className="mx-auto max-w-[1200px] px-5 lg:px-8">
<div className="relative overflow-hidden rounded-[32px] bg-navy-900 px-7 py-14 sm:px-12 lg:px-16 lg:py-16">
<div className="absolute right-0 top-0 h-72 w-72 rounded-full bg-teal-500/10 blur-3xl"></div>
<div className="relative max-w-3xl">
<p className="text-sm font-bold uppercase tracking-widest text-teal-300">
                    Start with your financial picture
                </p>
<h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-white sm:text-5xl">
                    Your next financial decision deserves more than a guess.
                </h2>
<p className="mt-5 max-w-2xl text-base leading-7 text-slate-300">
                    Understand your position, explore your options and see the
                    consequences before you choose.
                </p>
<div className="mt-8 flex flex-col gap-3 sm:flex-row">
<a className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-6 py-3.5 text-sm font-bold text-navy-900 transition hover:bg-slate-100" href="/plan">
                        Start Planning
                        <span>→</span>
</a>
<a className="inline-flex items-center justify-center rounded-xl border border-white/20 px-6 py-3.5 text-sm font-bold text-white transition hover:bg-white/10" href="/about">
                        About Planvesto
                    </a>
</div>
</div>
</div>
</div>
</section>
</main>

<footer className="border-t border-slate-200 bg-white">
<div className="mx-auto max-w-[1200px] px-5 py-14 lg:px-8">
<div className="grid gap-12 md:grid-cols-2 lg:grid-cols-[1.5fr_1fr_1fr_1fr]">

<div>
<a className="flex items-center gap-2.5" href="/">
<div className="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-900">
<svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<path d="M5 17L10 12L13 15L19 8" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2"></path>
<path d="M15 8H19V12" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2"></path>
</svg>
</div>
<span className="text-xl font-extrabold tracking-tight text-navy-900">
                        planvesto
                    </span>
</a>
<p className="mt-5 max-w-sm text-sm leading-7 text-slate-500">
                    A financial decision platform designed to help you understand
                    your options before you act.
                </p>
</div>

<div>
<h3 className="text-sm font-bold text-navy-900">
                    Plan
                </h3>
<ul className="mt-5 space-y-3 text-sm text-slate-500">
<li>
<a className="transition hover:text-navy-900" href="/plan">
                            Financial Planning
                        </a>
</li>
<li>
<a className="transition hover:text-navy-900" href="/plan#goals">
                            Goals
                        </a>
</li>
<li>
<a className="transition hover:text-navy-900" href="/plan#financial-health">
                            Financial Health
                        </a>
</li>
<li>
<a className="transition hover:text-navy-900" href="/plan#retirement">
                            Retirement Planning
                        </a>
</li>
</ul>
</div>

<div>
<h3 className="text-sm font-bold text-navy-900">
                    Explore
                </h3>
<ul className="mt-5 space-y-3 text-sm text-slate-500">
<li>
<a className="transition hover:text-navy-900" href="/invest">
                            Invest
                        </a>
</li>
<li>
<a className="transition hover:text-navy-900" href="/protect">
                            Protect
                        </a>
</li>
<li>
<a className="transition hover:text-navy-900" href="/decide">
                            Decide
                        </a>
</li>
<li>
<a className="transition hover:text-navy-900" href="/learn">
                            Learn
                        </a>
</li>
</ul>
</div>

<div>
<h3 className="text-sm font-bold text-navy-900">
                    Company
                </h3>
<ul className="mt-5 space-y-3 text-sm text-slate-500">
<li>
<a className="transition hover:text-navy-900" href="/about">
                            About Planvesto
                        </a>
</li>
<li>
<a className="transition hover:text-navy-900" href="/contact">
                            Contact
                        </a>
</li>
<li>
<a className="transition hover:text-navy-900" href="/login">
                            Login
                        </a>
</li>
</ul>
</div>
</div>
<div className="mt-12 flex flex-col gap-5 border-t border-slate-200 pt-7 sm:flex-row sm:items-center sm:justify-between">
<p className="text-xs text-slate-400">
                © <span id="currentYear">{new Date().getFullYear()}</span> Planvesto. All rights reserved.
            </p>
<div className="flex flex-wrap gap-5 text-xs text-slate-400">
<a className="transition hover:text-navy-900" href="/privacy">
                    Privacy Policy
                </a>
<a className="transition hover:text-navy-900" href="/terms">
                    Terms &amp; Conditions
                </a>
<a className="transition hover:text-navy-900" href="/disclaimer">
                    Disclaimer
                </a>
</div>
</div>
</div>
</footer>


    </>
  );
}
