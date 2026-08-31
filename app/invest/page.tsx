"use client";

import { useState } from "react";
import { useMobileMenuClose } from "../../hooks/useMobileMenuClose";

export default function InvestPage() {
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
                    xmlns="http://www.w3.org/2000/svg"
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
                className="text-sm font-bold text-navy-900"
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
                className="text-sm font-medium text-slate-600 transition hover:text-navy-900"
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
                    className="rounded-lg bg-slate-50 px-3 py-3 text-sm font-bold text-navy-900"
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
                    className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50"
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

    <div className="absolute inset-x-0 top-0 -z-10 h-[520px] bg-gradient-to-b from-teal-50/80 to-transparent"></div>


    <div className="mx-auto max-w-[1200px] px-5 pb-20 lg:px-8 lg:pb-28">

        <div className="grid items-center gap-14 lg:grid-cols-[1fr_0.9fr]">

            
            <div>

                <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-teal-100 bg-teal-50 px-3.5 py-2">

                    <span className="h-2 w-2 rounded-full bg-teal-600"></span>

                    <span className="text-xs font-semibold tracking-wide text-teal-700">
                        Investment planning
                    </span>

                </div>


                <h1 className="max-w-3xl text-5xl font-extrabold leading-[1.06] tracking-[-0.04em] text-navy-900 sm:text-6xl">

                    Invest for what your money

                    <span className="gradient-text">
                        needs to accomplish.
                    </span>

                </h1>


                <p className="mt-7 max-w-2xl text-lg leading-8 text-slate-600">
                    Your investments should fit your goals, time horizon,
                    financial position, liquidity needs, risk and what you
                    already own.
                </p>


                <div className="mt-9 flex flex-col gap-3 sm:flex-row">

                    <a
                        href="#start"
                        className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-navy-900/10 transition hover:bg-navy-800"
                    >
                        Start Investment Planning

                        <svg
                            className="h-4 w-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth="2"
                                d="M5 12h14M13 6l6 6-6 6" />
                        </svg>

                    </a>


                    <a
                        href="#how-it-works"
                        className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-6 py-3.5 text-sm font-semibold text-navy-900 transition hover:bg-slate-50"
                    >
                        How investing works
                    </a>

                </div>

            </div>


            
            <div className="relative">

                <div className="absolute -inset-5 rounded-[32px] bg-teal-100/50 blur-3xl"></div>


                <div className="relative rounded-[28px] border border-slate-200 bg-white p-6 shadow-soft sm:p-7">

                    <div className="flex items-center justify-between border-b border-slate-100 pb-5">

                        <div>

                            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                                Investment picture
                            </p>

                            <h2 className="mt-1 text-lg font-bold text-navy-900">
                                Current portfolio
                            </h2>

                        </div>

                        <span className="rounded-xl bg-teal-50 px-3 py-2 text-xs font-bold text-teal-700">
                            Example
                        </span>

                    </div>


                    <div className="mt-6">

                        <div className="flex items-end justify-between">

                            <div>

                                <p className="text-xs font-medium text-slate-400">
                                    Portfolio value
                                </p>

                                <p className="mt-1 text-3xl font-extrabold tracking-tight text-navy-900">
                                    ₹28.4L
                                </p>

                            </div>

                            <span className="rounded-lg bg-teal-50 px-2.5 py-1.5 text-xs font-bold text-teal-700">
                                100%
                            </span>

                        </div>


                        
                        <div className="mt-7">

                            <div className="flex h-3 overflow-hidden rounded-full bg-slate-100">

                                <div
                                    className="allocation-bar w-[55%] bg-navy-900"
                                    title="Growth assets"
                                ></div>

                                <div
                                    className="allocation-bar w-[30%] bg-teal-600"
                                    title="Stability assets"
                                ></div>

                                <div
                                    className="allocation-bar w-[15%] bg-slate-300"
                                    title="Liquidity"
                                ></div>

                            </div>


                            <div className="mt-5 grid grid-cols-3 gap-3">

                                <div>

                                    <div className="flex items-center gap-2">

                                        <span className="h-2 w-2 rounded-full bg-navy-900"></span>

                                        <span className="text-xs font-medium text-slate-500">
                                            Growth
                                        </span>

                                    </div>

                                    <p className="mt-1 text-sm font-bold text-navy-900">
                                        55%
                                    </p>

                                </div>


                                <div>

                                    <div className="flex items-center gap-2">

                                        <span className="h-2 w-2 rounded-full bg-teal-600"></span>

                                        <span className="text-xs font-medium text-slate-500">
                                            Stability
                                        </span>

                                    </div>

                                    <p className="mt-1 text-sm font-bold text-navy-900">
                                        30%
                                    </p>

                                </div>


                                <div>

                                    <div className="flex items-center gap-2">

                                        <span className="h-2 w-2 rounded-full bg-slate-300"></span>

                                        <span className="text-xs font-medium text-slate-500">
                                            Liquidity
                                        </span>

                                    </div>

                                    <p className="mt-1 text-sm font-bold text-navy-900">
                                        15%
                                    </p>

                                </div>

                            </div>

                        </div>


                        <div className="mt-7 rounded-2xl border border-slate-200 p-4">

                            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                                What matters
                            </p>

                            <p className="mt-2 text-sm font-semibold leading-6 text-navy-900">
                                Allocation should reflect the job your money needs to perform.
                            </p>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>




<section className="sticky top-20 z-40 border-y border-slate-200 bg-white/95 backdrop-blur-xl">

    <div className="mx-auto max-w-[1200px] overflow-x-auto px-5 lg:px-8">

        <nav className="flex min-w-max items-center gap-7 py-4">

            <a
                href="#requirement"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Investment Requirement
            </a>

            <a
                href="#risk"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Risk
            </a>

            <a
                href="#allocation"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Allocation
            </a>

            <a
                href="#selection"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Selection
            </a>

            <a
                href="#validation"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Validation
            </a>

        </nav>

    </div>

</section>




<section
    id="requirement"
    className="scroll-mt-32 py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[0.8fr_1.2fr] lg:items-start">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    01 · Investment requirement
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    Start with what the money needs to do.
                </h2>

                <p className="mt-5 text-lg leading-8 text-slate-600">
                    The right investment depends on the purpose of the money.
                    A retirement investment and a short-term liquidity reserve
                    do not necessarily have the same job.
                </p>

            </div>


            <div className="grid gap-4 sm:grid-cols-2">

                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-navy-900 text-white">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <circle
                                cx="12"
                                cy="12"
                                r="9"
                                strokeWidth="1.8" />

                            <path
                                d="M12 7v5l3 2"
                                strokeWidth="1.8"
                                strokeLinecap="round" />
                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Time horizon
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        When will the money be needed?
                    </p>

                </div>


                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-teal-50 text-teal-700">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M4 19V5M4 19h16"
                                strokeWidth="1.8"
                                strokeLinecap="round" />

                            <path
                                d="M8 15l3-4 3 2 5-7"
                                strokeWidth="1.8"
                                strokeLinecap="round"
                                strokeLinejoin="round" />
                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Required outcome
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        What financial outcome does the investment need to support?
                    </p>

                </div>


                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-100 text-navy-900">

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
                        What level of financial risk fits your circumstances?
                    </p>

                </div>


                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-100 text-navy-900">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M5 7h14M5 12h14M5 17h9"
                                strokeWidth="1.8"
                                strokeLinecap="round" />
                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Liquidity
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        How much flexibility does the money need to retain?
                    </p>

                </div>

            </div>

        </div>

    </div>

</section>




<section
    id="risk"
    className="scroll-mt-32 bg-white py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[1fr_1fr] lg:items-center">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    02 · Risk
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    Risk is about more than how you feel about markets.
                </h2>

                <p className="mt-5 text-lg leading-8 text-slate-600">
                    Investment decisions need to consider both your willingness
                    to take risk and your financial ability to absorb it.
                </p>

            </div>


            <div className="rounded-[28px] border border-slate-200 bg-slate-50 p-6 sm:p-8">

                <div className="space-y-6">

                    <div>

                        <div className="flex items-center justify-between">

                            <h3 className="font-bold text-navy-900">
                                Risk capacity
                            </h3>

                            <span className="text-xs font-bold text-teal-700">
                                Financial ability
                            </span>

                        </div>

                        <p className="mt-2 text-sm leading-6 text-slate-500">
                            How much financial loss or volatility can your
                            overall circumstances reasonably absorb?
                        </p>

                    </div>


                    <div className="h-px bg-slate-200"></div>


                    <div>

                        <div className="flex items-center justify-between">

                            <h3 className="font-bold text-navy-900">
                                Risk tolerance
                            </h3>

                            <span className="text-xs font-bold text-teal-700">
                                Personal willingness
                            </span>

                        </div>

                        <p className="mt-2 text-sm leading-6 text-slate-500">
                            How comfortable are you with uncertainty and
                            fluctuations in investment outcomes?
                        </p>

                    </div>


                    <div className="h-px bg-slate-200"></div>


                    <div>

                        <div className="flex items-center justify-between">

                            <h3 className="font-bold text-navy-900">
                                Investment context
                            </h3>

                            <span className="text-xs font-bold text-teal-700">
                                Full picture
                            </span>

                        </div>

                        <p className="mt-2 text-sm leading-6 text-slate-500">
                            Goals, horizon, liquidity, existing investments
                            and financial circumstances all matter.
                        </p>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>




<section
    id="allocation"
    className="scroll-mt-32 py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="max-w-3xl">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                03 · Asset allocation
            </p>

            <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                Decide what role each part of the portfolio should play.
            </h2>

            <p className="mt-5 text-lg leading-8 text-slate-600">
                Asset allocation connects your investment requirement with
                the different types of assets that may be used to fulfil it.
            </p>

        </div>


        <div className="mt-14 grid gap-5 md:grid-cols-3">

            
            <div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-card">

                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-navy-900 text-white">

                    <svg
                        className="h-5 w-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            d="M4 19V5M4 19h16"
                            strokeWidth="1.8"
                            strokeLinecap="round" />

                        <path
                            d="M8 15l3-4 3 2 5-7"
                            strokeWidth="1.8"
                            strokeLinecap="round"
                            strokeLinejoin="round" />
                    </svg>

                </div>

                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Growth
                </h3>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Assets intended to provide long-term growth potential,
                    with corresponding uncertainty and volatility.
                </p>

            </div>


            
            <div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-card">

                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-teal-50 text-teal-700">

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

                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Stability
                </h3>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Assets that may play a role in reducing portfolio
                    volatility or supporting stability.
                </p>

            </div>


            
            <div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-card">

                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-navy-900">

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

                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Liquidity
                </h3>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Resources that need to remain accessible when money
                    may be required in the near term.
                </p>

            </div>

        </div>


        
        <div className="mt-8 rounded-[28px] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">

            <div className="grid gap-8 lg:grid-cols-[0.8fr_1.2fr] lg:items-center">

                <div>

                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Illustrative example
                    </p>

                    <h3 className="mt-3 text-2xl font-extrabold tracking-tight text-navy-900">
                        One portfolio can have different jobs.
                    </h3>

                    <p className="mt-4 text-sm leading-7 text-slate-500">
                        Allocation is not simply about choosing a percentage
                        for each asset class. It is about matching capital
                        to the requirements of the financial plan.
                    </p>

                </div>


                <div>

                    <div className="flex h-5 overflow-hidden rounded-full bg-slate-100">

                        <div className="w-[50%] bg-navy-900"></div>

                        <div className="w-[30%] bg-teal-600"></div>

                        <div className="w-[20%] bg-slate-300"></div>

                    </div>


                    <div className="mt-5 grid grid-cols-3 gap-5">

                        <div>

                            <p className="text-xs font-medium text-slate-400">
                                Growth
                            </p>

                            <p className="mt-1 text-xl font-extrabold text-navy-900">
                                50%
                            </p>

                        </div>


                        <div>

                            <p className="text-xs font-medium text-slate-400">
                                Stability
                            </p>

                            <p className="mt-1 text-xl font-extrabold text-navy-900">
                                30%
                            </p>

                        </div>


                        <div>

                            <p className="text-xs font-medium text-slate-400">
                                Liquidity
                            </p>

                            <p className="mt-1 text-xl font-extrabold text-navy-900">
                                20%
                            </p>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>




<section
    id="selection"
    className="scroll-mt-32 bg-white py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    04 · Investment selection
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    Products come after the requirement.
                </h2>

                <p className="mt-5 text-lg leading-8 text-slate-600">
                    A product is a vehicle. First understand what role the
                    investment needs to fulfil. Then evaluate products against
                    that role and the overall portfolio.
                </p>

                <a
                    href="/decide"
                    className="mt-8 inline-flex items-center gap-2 text-sm font-bold text-navy-900"
                >
                    Understand the decision process
                    <span>→</span>
                </a>

            </div>


            <div className="rounded-[28px] border border-slate-200 bg-slate-50 p-6 sm:p-8">

                <div className="space-y-4">

                    <div className="flex items-center gap-4 rounded-2xl bg-white p-5 shadow-sm">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-navy-900 text-sm font-bold text-white">
                            01
                        </div>

                        <div>

                            <h3 className="text-sm font-bold text-navy-900">
                                Define the role
                            </h3>

                            <p className="mt-1 text-xs leading-5 text-slate-500">
                                What does this investment need to accomplish?
                            </p>

                        </div>

                    </div>


                    <div className="flex items-center gap-4 rounded-2xl bg-white p-5 shadow-sm">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-teal-600 text-sm font-bold text-white">
                            02
                        </div>

                        <div>

                            <h3 className="text-sm font-bold text-navy-900">
                                Define the requirements
                            </h3>

                            <p className="mt-1 text-xs leading-5 text-slate-500">
                                Risk, liquidity, horizon and portfolio fit.
                            </p>

                        </div>

                    </div>


                    <div className="flex items-center gap-4 rounded-2xl bg-white p-5 shadow-sm">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-sm font-bold text-navy-900">
                            03
                        </div>

                        <div>

                            <h3 className="text-sm font-bold text-navy-900">
                                Evaluate suitable products
                            </h3>

                            <p className="mt-1 text-xs leading-5 text-slate-500">
                                Compare available investment vehicles against the requirement.
                            </p>

                        </div>

                    </div>


                    <div className="flex items-center gap-4 rounded-2xl bg-white p-5 shadow-sm">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-navy-900 text-sm font-bold text-white">
                            04
                        </div>

                        <div>

                            <h3 className="text-sm font-bold text-navy-900">
                                Check the whole portfolio
                            </h3>

                            <p className="mt-1 text-xs leading-5 text-slate-500">
                                Make sure the new investment fits what you already own.
                            </p>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>




<section
    id="validation"
    className="scroll-mt-32 py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="max-w-3xl">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                05 · Validation
            </p>

            <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                Before acting, check what the decision changes.
            </h2>

            <p className="mt-5 text-lg leading-8 text-slate-600">
                An investment can look attractive on its own and still be
                unsuitable for the overall financial plan. The final question
                is how the resulting portfolio fits the plan.
            </p>

        </div>


        <div className="mt-14 grid gap-5 md:grid-cols-2 lg:grid-cols-4">

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                <div className="text-xs font-bold uppercase tracking-wider text-teal-700">
                    Check 01
                </div>

                <h3 className="mt-4 font-bold text-navy-900">
                    Goal impact
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    Does the investment support the intended goal?
                </p>

            </div>


            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                <div className="text-xs font-bold uppercase tracking-wider text-teal-700">
                    Check 02
                </div>

                <h3 className="mt-4 font-bold text-navy-900">
                    Risk impact
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    Does the resulting risk remain appropriate?
                </p>

            </div>


            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                <div className="text-xs font-bold uppercase tracking-wider text-teal-700">
                    Check 03
                </div>

                <h3 className="mt-4 font-bold text-navy-900">
                    Liquidity impact
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    Does enough accessible capital remain available?
                </p>

            </div>


            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                <div className="text-xs font-bold uppercase tracking-wider text-teal-700">
                    Check 04
                </div>

                <h3 className="mt-4 font-bold text-navy-900">
                    Portfolio impact
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    Does the investment fit with the rest of the portfolio?
                </p>

            </div>

        </div>

    </div>

</section>




<section
    id="how-it-works"
    className="scroll-mt-32 bg-navy-900 py-24 text-white lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[0.85fr_1.15fr]">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-300">
                    How investment planning works
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] sm:text-5xl">
                    From purpose to portfolio.
                </h2>

                <p className="mt-6 max-w-lg text-base leading-7 text-slate-300">
                    The process moves from the financial requirement to the
                    portfolio rather than starting with a product.
                </p>

            </div>


            <div className="space-y-7">

                <div className="flex gap-5">

                    <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        01
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Understand the requirement
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Goal, horizon, required outcome, liquidity and financial context.
                        </p>

                    </div>

                </div>


                <div className="flex gap-5">

                    <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        02
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Understand risk
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Consider both financial capacity and willingness to take risk.
                        </p>

                    </div>

                </div>


                <div className="flex gap-5">

                    <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        03
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Build the allocation
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Determine how capital can be distributed across different roles.
                        </p>

                    </div>

                </div>


                <div className="flex gap-5">

                    <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        04
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Select investments
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Evaluate suitable investment vehicles against the defined requirement.
                        </p>

                    </div>

                </div>


                <div className="flex gap-5">

                    <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-teal-600 text-sm font-bold">
                        05
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Validate the portfolio
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Check the resulting effect on goals, risk, liquidity and the overall plan.
                        </p>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>




<section
    id="start"
    className="scroll-mt-32 py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="relative overflow-hidden rounded-[32px] bg-navy-900 px-7 py-14 sm:px-12 lg:px-16 lg:py-16">

            <div className="absolute -right-20 -top-20 h-72 w-72 rounded-full bg-teal-500/10 blur-3xl"></div>


            <div className="relative max-w-3xl">

                <p className="text-sm font-bold uppercase tracking-widest text-teal-300">
                    Start investing with context
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-white sm:text-5xl">
                    Don't start with a product. Start with the purpose.
                </h2>

                <p className="mt-5 max-w-2xl text-base leading-7 text-slate-300">
                    Understand what your money needs to accomplish,
                    then build the investment approach around it.
                </p>


                <div className="mt-8 flex flex-col gap-3 sm:flex-row">

                    <a
                        href="/login"
                        className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-6 py-3.5 text-sm font-bold text-navy-900 transition hover:bg-slate-100"
                    >
                        Start Investment Planning
                        <span>→</span>
                    </a>

                    <a
                        href="/decide"
                        className="inline-flex items-center justify-center rounded-xl border border-white/20 px-6 py-3.5 text-sm font-bold text-white transition hover:bg-white/10"
                    >
                        Compare decisions
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
                            className="font-semibold text-navy-900"
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
                            className="transition hover:text-navy-900"
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
