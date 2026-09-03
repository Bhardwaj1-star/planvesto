"use client";

import { useState } from "react";
import { useMobileMenuClose } from "../../hooks/useMobileMenuClose";

export default function DecidePage() {
  const [menuOpen, setMenuOpen] = useState(false);

  useMobileMenuClose(setMenuOpen);

  return (
    <>


<header className="fixed inset-x-0 top-0 z-50 border-b border-slate-200/70 bg-white/90 backdrop-blur-xl">

    <div className="mx-auto flex h-20 max-w-[1200px] items-center justify-between px-5 lg:px-8">

        <a
            href="/"
            className="flex items-center gap-2.5"
            aria-label="Planvesto Home"
        >

            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-900">

                <svg
                    className="h-5 w-5 text-white"
                    viewBox="0 0 24 24"
                    fill="none"
                >
                    <path
                        d="M5 17L10 12L13 15L19 8"
                        stroke="currentColor"
                        strokeWidth="2.2"
                        strokeLinecap="round"
                        strokeLinejoin="round" />

                    <path
                        d="M15 8H19V12"
                        stroke="currentColor"
                        strokeWidth="2.2"
                        strokeLinecap="round"
                        strokeLinejoin="round" />

                </svg>

            </div>

            <span className="text-xl font-extrabold tracking-tight text-navy-900">
                planvesto
            </span>

        </a>


        <nav
            className="hidden items-center gap-8 lg:flex"
            aria-label="Main navigation"
        >

            <a className="text-sm font-medium text-slate-600 transition hover:text-navy-900" href="/">
                Home
            </a>

            <a
                href="/plan"
                className="text-sm font-medium text-slate-600 transition hover:text-navy-900"
            >
                Plan
            </a>

            <a
                href="/invest"
                className="text-sm font-medium text-slate-600 transition hover:text-navy-900"
            >
                Invest
            </a>

            <a
                href="/protect"
                className="text-sm font-medium text-slate-600 transition hover:text-navy-900"
            >
                Protect
            </a>

            <a
                href="/decide"
                className="text-sm font-bold text-navy-900"
            >
                Decide
            </a>

            <a
                href="/learn"
                className="text-sm font-medium text-slate-600 transition hover:text-navy-900"
            >
                Learn
            </a>

            <a
                href="/about"
                className="text-sm font-medium text-slate-600 transition hover:text-navy-900"
            >
                About
            </a>

        </nav>


        <div className="hidden items-center gap-3 lg:flex">

            <a
                href="/login"
                className="rounded-xl px-4 py-2.5 text-sm font-semibold text-navy-900 transition hover:bg-slate-100"
            >
                Login
            </a>

            <a
                href="#start"
                className="rounded-xl bg-navy-900 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-navy-800"
            >
                Start Planning
            </a>

        </div>


        <button
            id="menuButton"
            type="button" onClick={() => setMenuOpen(!menuOpen)}
            className="rounded-lg p-2 text-navy-900 lg:hidden"
            aria-label="Open navigation menu"
            aria-expanded={menuOpen}
        >

            <svg
                className="h-6 w-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
            >

                <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M4 6h16M4 12h16M4 18h16" />

            </svg>

        </button>

    </div>


    <div
        id="mobileMenu" className={`mobile-menu border-t border-slate-200 bg-white lg:hidden ${menuOpen ? "" : "hidden"}`}
    >

        <nav className="mx-auto max-w-[1200px] px-5 py-5">

            <div className="flex flex-col gap-1">

                <a
                    href="/plan"
                    className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50"
                >
                    Plan
                </a>

                <a
                    href="/invest"
                    className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50"
                >
                    Invest
                </a>

                <a
                    href="/protect"
                    className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50"
                >
                    Protect
                </a>

                <a
                    href="/decide"
                    className="rounded-lg bg-slate-50 px-3 py-3 text-sm font-bold text-navy-900"
                >
                    Decide
                </a>

                <a
                    href="/learn"
                    className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50"
                >
                    Learn
                </a>

                <a
                    href="/about"
                    className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50"
                >
                    About
                </a>


                <div className="mt-3 grid grid-cols-2 gap-3 border-t border-slate-100 pt-4">

                    <a
                        href="/login"
                        className="rounded-xl border border-slate-200 px-4 py-3 text-center text-sm font-semibold text-navy-900"
                    >
                        Login
                    </a>

                    <a
                        href="#start"
                        className="rounded-xl bg-navy-900 px-4 py-3 text-center text-sm font-semibold text-white"
                    >
                        Start Planning
                    </a>

                </div>

            </div>

        </nav>

    </div>

</header>


<main>




<section className="hero-grid relative overflow-hidden pt-32 lg:pt-40">

    <div className="absolute inset-x-0 top-0 -z-10 h-[560px] bg-gradient-to-b from-teal-50/80 to-transparent"></div>


    <div className="mx-auto max-w-[1200px] px-5 pb-20 lg:px-8 lg:pb-28">

        <div className="grid items-center gap-14 lg:grid-cols-[1fr_0.9fr]">

            <div>

                <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-teal-100 bg-teal-50 px-3.5 py-2">

                    <span className="h-2 w-2 rounded-full bg-teal-600"></span>

                    <span className="text-xs font-semibold tracking-wide text-teal-700">
                        Financial decisions
                    </span>

                </div>


                <h1 className="max-w-3xl text-5xl font-extrabold leading-[1.06] tracking-[-0.04em] text-navy-900 sm:text-6xl">

                    Don't just choose an option.

                    <span className="gradient-text">
                        Understand the decision.
                    </span>

                </h1>


                <p className="mt-7 max-w-2xl text-lg leading-8 text-slate-600">
                    Compare financial strategies, see what could happen under
                    different scenarios and understand the trade-offs before
                    deciding what to do.
                </p>


                <div className="mt-9 flex flex-col gap-3 sm:flex-row">

                    <a
                        href="#start"
                        className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-navy-900/10 transition hover:bg-navy-800"
                    >
                        Explore Your Decision

                        <svg
                            className="h-4 w-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >

                            <path
                                d="M5 12h14M13 6l6 6-6 6"
                                strokeWidth="1.8"
                                strokeLinecap="round"
                                strokeLinejoin="round" />

                        </svg>

                    </a>


                    <a
                        href="#how-it-works"
                        className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-6 py-3.5 text-sm font-semibold text-navy-900 transition hover:bg-slate-50"
                    >
                        How it works
                    </a>

                </div>

            </div>


            

            <div className="relative">

                <div className="absolute -inset-5 rounded-[32px] bg-teal-100/50 blur-3xl"></div>


                <div className="relative rounded-[28px] border border-slate-200 bg-white p-6 shadow-soft sm:p-7">

                    <div className="flex items-center justify-between border-b border-slate-100 pb-5">

                        <div>

                            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                                Example decision
                            </p>

                            <h2 className="mt-1 text-lg font-bold text-navy-900">
                                Retirement funding
                            </h2>

                        </div>

                        <span className="rounded-xl bg-teal-50 px-3 py-2 text-xs font-bold text-teal-700">
                            Compare
                        </span>

                    </div>


                    <div className="mt-6 space-y-3">

                        <div className="rounded-2xl border border-teal-200 bg-teal-50 p-4">

                            <div className="flex items-center justify-between">

                                <div>

                                    <p className="text-xs font-semibold uppercase tracking-wider text-teal-700">
                                        Option A
                                    </p>

                                    <p className="mt-1 text-sm font-bold text-navy-900">
                                        Increase contribution
                                    </p>

                                </div>

                                <span className="rounded-lg bg-white px-2.5 py-1 text-xs font-bold text-teal-700">
                                    Selected
                                </span>

                            </div>

                            <div className="mt-4 grid grid-cols-2 gap-3">

                                <div>

                                    <p className="text-[11px] text-slate-400">
                                        Monthly change
                                    </p>

                                    <p className="mt-1 text-sm font-bold text-navy-900">
                                        +₹10,000
                                    </p>

                                </div>

                                <div>

                                    <p className="text-[11px] text-slate-400">
                                        Goal impact
                                    </p>

                                    <p className="mt-1 text-sm font-bold text-navy-900">
                                        Improved
                                    </p>

                                </div>

                            </div>

                        </div>


                        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">

                            <div className="flex items-center justify-between">

                                <div>

                                    <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                                        Option B
                                    </p>

                                    <p className="mt-1 text-sm font-bold text-navy-900">
                                        Retain current funding
                                    </p>

                                </div>

                                <span className="text-xs font-semibold text-slate-400">
                                    Alternative
                                </span>

                            </div>

                        </div>


                        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">

                            <div className="flex items-center justify-between">

                                <div>

                                    <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                                        Option C
                                    </p>

                                    <p className="mt-1 text-sm font-bold text-navy-900">
                                        Change retirement assumptions
                                    </p>

                                </div>

                                <span className="text-xs font-semibold text-slate-400">
                                    Alternative
                                </span>

                            </div>

                        </div>

                    </div>


                    <div className="mt-5 border-t border-slate-100 pt-5">

                        <div className="flex items-start gap-3">

                            <div className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-navy-900 text-white">

                                <svg
                                    className="h-3.5 w-3.5"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >

                                    <path
                                        d="M12 8v4l3 2"
                                        strokeWidth="1.8"
                                        strokeLinecap="round"
                                        strokeLinejoin="round" />

                                    <circle
                                        cx="12"
                                        cy="12"
                                        r="8"
                                        strokeWidth="1.8" />

                                </svg>

                            </div>

                            <p className="text-xs leading-5 text-slate-500">
                                The right decision depends on goals,
                                constraints, assumptions and the consequences
                                of each alternative.
                            </p>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>




<section className="border-y border-slate-200 bg-white">

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid divide-y divide-slate-200 md:grid-cols-3 md:divide-x md:divide-y-0">

            <div className="px-0 py-10 md:px-8 md:first:pl-0">

                <p className="text-3xl font-extrabold tracking-tight text-navy-900">
                    Compare
                </p>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    Look at relevant alternatives instead of evaluating one option in isolation.
                </p>

            </div>


            <div className="px-0 py-10 md:px-8">

                <p className="text-3xl font-extrabold tracking-tight text-navy-900">
                    Test
                </p>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    Understand how different assumptions and scenarios can change the outcome.
                </p>

            </div>


            <div className="px-0 py-10 md:px-8 md:pr-0">

                <p className="text-3xl font-extrabold tracking-tight text-navy-900">
                    Decide
                </p>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    Move from analysis to a clear financial plan and practical actions.
                </p>

            </div>

        </div>

    </div>

</section>




<section className="py-24 lg:py-32">

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[0.8fr_1.2fr] lg:items-start">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    The problem
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    Financial decisions are rarely about one number.
                </h2>

                <p className="mt-5 text-lg leading-8 text-slate-600">
                    A change that improves one part of your financial life can
                    affect another. Increasing investment, for example, can
                    change liquidity. Increasing protection can change surplus.
                    Changing a goal can change the required funding.
                </p>

            </div>


            <div className="grid gap-4 sm:grid-cols-2">

                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-navy-900">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >

                            <path
                                d="M5 19V9M12 19V5M19 19v-8"
                                strokeWidth="1.8"
                                strokeLinecap="round" />

                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Goals
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        What outcome are you actually trying to achieve?
                    </p>

                </div>


                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-50 text-teal-700">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >

                            <path
                                d="M12 3v18M7 8h8a3 3 0 010 6H9a3 3 0 000 6h8"
                                strokeWidth="1.8"
                                strokeLinecap="round" />

                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Cash flow
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        What can you actually afford without weakening the plan?
                    </p>

                </div>


                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-navy-900">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >

                            <path
                                d="M12 3l8 4v5c0 4.8-3.4 7.9-8 9-4.6-1.1-8-4.2-8-9V7l8-4z"
                                strokeWidth="1.8"
                                strokeLinejoin="round" />

                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Risk
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        What risks and constraints need to be respected?
                    </p>

                </div>


                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-navy-900">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >

                            <path
                                d="M4 19h16M6 16V8M10 16V5M14 16v-4M18 16V7"
                                strokeWidth="1.8"
                                strokeLinecap="round" />

                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Trade-offs
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        What do you gain, give up or change with each alternative?
                    </p>

                </div>

            </div>

        </div>

    </div>

</section>




<section
    id="scenarios"
    className="bg-white py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="max-w-3xl">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                Scenarios
            </p>

            <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                Don't only ask "what should I do?"
            </h2>

            <p className="mt-5 text-lg leading-8 text-slate-600">
                Ask what happens if you choose one path instead of another.
            </p>

        </div>


        <div className="mt-14 grid gap-5 lg:grid-cols-3">

            <div className="rounded-[24px] border border-slate-200 bg-slate-50 p-7">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white text-navy-900 shadow-sm">

                    <span className="text-sm font-extrabold">
                        01
                    </span>

                </div>

                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Baseline
                </h3>

                <p className="mt-3 text-sm leading-7 text-slate-500">
                    Establish the current financial position and assumptions
                    against which alternatives can be considered.
                </p>

            </div>


            <div className="rounded-[24px] border border-teal-100 bg-teal-50 p-7">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white text-teal-700 shadow-sm">

                    <span className="text-sm font-extrabold">
                        02
                    </span>

                </div>

                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Change an assumption
                </h3>

                <p className="mt-3 text-sm leading-7 text-slate-500">
                    Test a strategy or changed assumption and see how the
                    resulting financial position could differ.
                </p>

            </div>


            <div className="rounded-[24px] border border-slate-200 bg-slate-50 p-7">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white text-navy-900 shadow-sm">

                    <span className="text-sm font-extrabold">
                        03
                    </span>

                </div>

                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Compare outcomes
                </h3>

                <p className="mt-3 text-sm leading-7 text-slate-500">
                    See the consequences and trade-offs before selecting a path.
                </p>

            </div>

        </div>


        

        <div className="mt-8 overflow-hidden rounded-[28px] border border-slate-200 bg-white shadow-card">

            <div className="border-b border-slate-200 bg-slate-50 px-6 py-5 sm:px-8">

                <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">

                    <div>

                        <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
                            Illustrative comparison
                        </p>

                        <h3 className="mt-1 text-lg font-bold text-navy-900">
                            Retirement funding alternatives
                        </h3>

                    </div>

                    <span className="text-xs font-medium text-slate-400">
                        Example only
                    </span>

                </div>

            </div>


            <div className="overflow-x-auto">

                <table className="w-full min-w-[680px] border-collapse text-left">

                    <thead>

                        <tr className="border-b border-slate-200">

                            <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-400 sm:px-8">
                                Consideration
                            </th>

                            <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-teal-700">
                                Increase funding
                            </th>

                            <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-400">
                                Current funding
                            </th>

                            <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-400">
                                Change horizon
                            </th>

                        </tr>

                    </thead>


                    <tbody className="divide-y divide-slate-100">

                        <tr>

                            <td className="px-6 py-5 text-sm font-semibold text-navy-900 sm:px-8">
                                Monthly cash flow
                            </td>

                            <td className="px-6 py-5 text-sm text-slate-600">
                                Lower surplus
                            </td>

                            <td className="px-6 py-5 text-sm text-slate-600">
                                Higher surplus
                            </td>

                            <td className="px-6 py-5 text-sm text-slate-600">
                                Unchanged
                            </td>

                        </tr>


                        <tr>

                            <td className="px-6 py-5 text-sm font-semibold text-navy-900 sm:px-8">
                                Retirement funding
                            </td>

                            <td className="px-6 py-5 text-sm text-slate-600">
                                Higher
                            </td>

                            <td className="px-6 py-5 text-sm text-slate-600">
                                Current
                            </td>

                            <td className="px-6 py-5 text-sm text-slate-600">
                                Adjusted
                            </td>

                        </tr>


                        <tr>

                            <td className="px-6 py-5 text-sm font-semibold text-navy-900 sm:px-8">
                                Liquidity
                            </td>

                            <td className="px-6 py-5 text-sm text-slate-600">
                                Potentially lower
                            </td>

                            <td className="px-6 py-5 text-sm text-slate-600">
                                Higher
                            </td>

                            <td className="px-6 py-5 text-sm text-slate-600">
                                Depends
                            </td>

                        </tr>


                        <tr>

                            <td className="px-6 py-5 text-sm font-semibold text-navy-900 sm:px-8">
                                Goal outcome
                            </td>

                            <td className="px-6 py-5 text-sm text-slate-600">
                                Potentially improved
                            </td>

                            <td className="px-6 py-5 text-sm text-slate-600">
                                Baseline
                            </td>

                            <td className="px-6 py-5 text-sm text-slate-600">
                                Depends
                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </div>

    </div>

</section>




<section
    id="how-it-works"
    className="scroll-mt-32 bg-navy-900 py-24 text-white lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[0.8fr_1.2fr]">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-300">
                    How it works
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] sm:text-5xl">
                    From problem to financial decision.
                </h2>

                <p className="mt-6 max-w-lg text-base leading-7 text-slate-300">
                    Planvesto's decision process connects the financial problem,
                    possible strategies and scenario outcomes before arriving
                    at a selected financial plan.
                </p>

            </div>


            <div className="space-y-7">

                <div className="decision-line flex gap-5">

                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        01
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Understand the problem
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Identify the financial issue, goal or constraint that requires a decision.
                        </p>

                    </div>

                </div>


                <div className="decision-line flex gap-5">

                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        02
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Consider applicable strategies
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Identify strategies that are relevant to the specific situation.
                        </p>

                    </div>

                </div>


                <div className="decision-line flex gap-5">

                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        03
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Evaluate scenarios
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Compare what the different strategies could mean under the relevant assumptions.
                        </p>

                    </div>

                </div>


                <div className="decision-line flex gap-5">

                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        04
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Compare the trade-offs
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Consider goals, risk, liquidity, cash flow and other constraints together.
                        </p>

                    </div>

                </div>


                <div className="decision-line flex gap-5">

                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        05
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Select the financial plan
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Move from alternatives to a selected financial decision.
                        </p>

                    </div>

                </div>


                <div className="flex gap-5">

                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-teal-600 text-sm font-bold">
                        06
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Understand and act
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            See why the decision was selected and what actions follow from it.
                        </p>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>




<section className="py-24 lg:py-32">

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-2 lg:items-center">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    Explain the decision
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    A decision should come with a reason.
                </h2>

                <p className="mt-5 text-lg leading-8 text-slate-600">
                    Planvesto is designed so that a financial decision can be
                    understood in terms of the evidence, assumptions,
                    alternatives and scenario results behind it.
                </p>

            </div>


            <div className="rounded-[28px] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">

                <div className="border-b border-slate-100 pb-6">

                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Why this decision?
                    </p>

                    <h3 className="mt-2 text-xl font-bold text-navy-900">
                        Increase retirement funding
                    </h3>

                </div>


                <div className="mt-6 space-y-5">

                    <div className="flex gap-4">

                        <div className="mt-1 h-2.5 w-2.5 shrink-0 rounded-full bg-teal-600"></div>

                        <div>

                            <p className="text-sm font-bold text-navy-900">
                                Goal requirement
                            </p>

                            <p className="mt-1 text-sm leading-6 text-slate-500">
                                The projected retirement position indicates a funding requirement.
                            </p>

                        </div>

                    </div>


                    <div className="flex gap-4">

                        <div className="mt-1 h-2.5 w-2.5 shrink-0 rounded-full bg-teal-600"></div>

                        <div>

                            <p className="text-sm font-bold text-navy-900">
                                Strategy comparison
                            </p>

                            <p className="mt-1 text-sm leading-6 text-slate-500">
                                Multiple relevant strategies were considered against the stated constraints.
                            </p>

                        </div>

                    </div>


                    <div className="flex gap-4">

                        <div className="mt-1 h-2.5 w-2.5 shrink-0 rounded-full bg-teal-600"></div>

                        <div>

                            <p className="text-sm font-bold text-navy-900">
                                Scenario outcome
                            </p>

                            <p className="mt-1 text-sm leading-6 text-slate-500">
                                The selected strategy produced the preferred overall financial outcome in the example.
                            </p>

                        </div>

                    </div>


                    <div className="flex gap-4">

                        <div className="mt-1 h-2.5 w-2.5 shrink-0 rounded-full bg-teal-600"></div>

                        <div>

                            <p className="text-sm font-bold text-navy-900">
                                Financial constraints
                            </p>

                            <p className="mt-1 text-sm leading-6 text-slate-500">
                                The decision also considers the effect on cash flow and liquidity.
                            </p>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>




<section className="bg-white py-24 lg:py-32">

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="mx-auto max-w-3xl text-center">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                Financial decision first
            </p>

            <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                Decide what needs to happen before deciding what to buy.
            </h2>

            <p className="mt-5 text-lg leading-8 text-slate-600">
                A financial plan defines the strategy. Products are an
                implementation layer that comes after the financial decision.
            </p>

        </div>


        <div className="mx-auto mt-14 max-w-4xl">

            <div className="grid items-center gap-4 md:grid-cols-[1fr_auto_1fr_auto_1fr]">

                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 text-center">

                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Step 1
                    </p>

                    <h3 className="mt-3 font-bold text-navy-900">
                        Financial problem
                    </h3>

                </div>


                <div className="hidden text-2xl text-slate-300 md:block">
                    →
                </div>


                <div className="rounded-2xl border border-teal-100 bg-teal-50 p-6 text-center">

                    <p className="text-xs font-bold uppercase tracking-wider text-teal-700">
                        Step 2
                    </p>

                    <h3 className="mt-3 font-bold text-navy-900">
                        Financial strategy
                    </h3>

                </div>


                <div className="hidden text-2xl text-slate-300 md:block">
                    →
                </div>


                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 text-center">

                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Step 3
                    </p>

                    <h3 className="mt-3 font-bold text-navy-900">
                        Implementation
                    </h3>

                </div>

            </div>

        </div>

    </div>

</section>




<section className="py-24 lg:py-32">

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    From decision to action
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    A financial decision should lead somewhere.
                </h2>

                <p className="mt-5 text-lg leading-8 text-slate-600">
                    Once a decision is made, the next step is to translate it
                    into practical actions and keep track of what changes.
                </p>

            </div>


            <div className="space-y-3">

                <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-card">

                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-navy-900 text-sm font-bold text-white">
                        01
                    </div>

                    <div className="flex-1">

                        <p className="text-sm font-bold text-navy-900">
                            Selected financial plan
                        </p>

                        <p className="mt-1 text-xs text-slate-400">
                            What was decided?
                        </p>

                    </div>

                    <span className="text-slate-300">
                        →
                    </span>

                </div>


                <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-card">

                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-sm font-bold text-navy-900">
                        02
                    </div>

                    <div className="flex-1">

                        <p className="text-sm font-bold text-navy-900">
                            Implementation actions
                        </p>

                        <p className="mt-1 text-xs text-slate-400">
                            What needs to change?
                        </p>

                    </div>

                    <span className="text-slate-300">
                        →
                    </span>

                </div>


                <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-card">

                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-sm font-bold text-navy-900">
                        03
                    </div>

                    <div className="flex-1">

                        <p className="text-sm font-bold text-navy-900">
                            Review
                        </p>

                        <p className="mt-1 text-xs text-slate-400">
                            Has the financial position changed?
                        </p>

                    </div>

                    <span className="text-slate-300">
                        →
                    </span>

                </div>


                <div className="flex items-center gap-4 rounded-2xl border border-teal-100 bg-teal-50 p-5">

                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-teal-600 text-sm font-bold text-white">
                        04
                    </div>

                    <div className="flex-1">

                        <p className="text-sm font-bold text-navy-900">
                            Reassess when needed
                        </p>

                        <p className="mt-1 text-xs text-slate-500">
                            A new situation can create a new decision.
                        </p>

                    </div>

                    <span className="text-teal-700">
                        ✓
                    </span>

                </div>

            </div>

        </div>

    </div>

</section>




<section
    id="start"
    className="scroll-mt-32 pb-24 lg:pb-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="relative overflow-hidden rounded-[32px] bg-navy-900 px-7 py-14 sm:px-12 lg:px-16 lg:py-16">

            <div className="absolute -right-20 -top-20 h-72 w-72 rounded-full bg-teal-500/10 blur-3xl"></div>


            <div className="relative max-w-3xl">

                <p className="text-sm font-bold uppercase tracking-widest text-teal-300">
                    Start planning
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-white sm:text-5xl">
                    Make financial decisions with the whole picture in view.
                </h2>

                <p className="mt-5 max-w-2xl text-base leading-7 text-slate-300">
                    Understand the problem, compare the alternatives,
                    evaluate the consequences and move forward with a clear plan.
                </p>


                <div className="mt-8 flex flex-col gap-3 sm:flex-row">

                    <a
                        href="/login"
                        className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-6 py-3.5 text-sm font-bold text-navy-900 transition hover:bg-slate-100"
                    >
                        Start Planning
                        <span>→</span>
                    </a>


                    <a
                        href="/plan"
                        className="inline-flex items-center justify-center rounded-xl border border-white/20 px-6 py-3.5 text-sm font-bold text-white transition hover:bg-white/10"
                    >
                        Explore Financial Planning
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

                <a
                    href="/"
                    className="flex items-center gap-2.5"
                >

                    <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-900">

                        <svg
                            className="h-5 w-5 text-white"
                            viewBox="0 0 24 24"
                            fill="none"
                        >

                            <path
                                d="M5 17L10 12L13 15L19 8"
                                stroke="currentColor"
                                strokeWidth="2.2"
                                strokeLinecap="round"
                                strokeLinejoin="round" />

                            <path
                                d="M15 8H19V12"
                                stroke="currentColor"
                                strokeWidth="2.2"
                                strokeLinecap="round"
                                strokeLinejoin="round" />

                        </svg>

                    </div>

                    <span className="text-xl font-extrabold tracking-tight text-navy-900">
                        planvesto
                    </span>

                </a>


                <p className="mt-5 max-w-sm text-sm leading-7 text-slate-500">
                    A financial decision platform designed to help you
                    understand your options before you act.
                </p>

            </div>


            <div>

                <h3 className="text-sm font-bold text-navy-900">
                    Plan
                </h3>

                <ul className="mt-5 space-y-3 text-sm text-slate-500">

                    <li>
                        <a
                            href="/plan"
                            className="transition hover:text-navy-900"
                        >
                            Financial Planning
                        </a>
                    </li>

                    <li>
                        <a
                            href="/plan#financial-health"
                            className="transition hover:text-navy-900"
                        >
                            Financial Health
                        </a>
                    </li>

                    <li>
                        <a
                            href="/plan#goals"
                            className="transition hover:text-navy-900"
                        >
                            Goals
                        </a>
                    </li>

                    <li>
                        <a
                            href="/plan#retirement"
                            className="transition hover:text-navy-900"
                        >
                            Retirement
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
                        <a
                            href="/invest"
                            className="transition hover:text-navy-900"
                        >
                            Invest
                        </a>
                    </li>

                    <li>
                        <a
                            href="/protect"
                            className="transition hover:text-navy-900"
                        >
                            Protect
                        </a>
                    </li>

                    <li>
                        <a
                            href="/decide"
                            className="font-semibold text-navy-900"
                        >
                            Decide
                        </a>
                    </li>

                    <li>
                        <a
                            href="/learn"
                            className="transition hover:text-navy-900"
                        >
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
                        <a
                            href="/about"
                            className="transition hover:text-navy-900"
                        >
                            About Planvesto
                        </a>
                    </li>

                    <li>
                        <a
                            href="/contact"
                            className="transition hover:text-navy-900"
                        >
                            Contact
                        </a>
                    </li>

                    <li>
                        <a
                            href="/login"
                            className="transition hover:text-navy-900"
                        >
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

                <a
                    href="/privacy"
                    className="transition hover:text-navy-900"
                >
                    Privacy Policy
                </a>

                <a
                    href="/terms"
                    className="transition hover:text-navy-900"
                >
                    Terms &amp; Conditions
                </a>

                <a
                    href="/disclaimer"
                    className="transition hover:text-navy-900"
                >
                    Disclaimer
                </a>

            </div>

        </div>

    </div>

</footer>



    </>
  );
}
