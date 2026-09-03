"use client";

import { useState } from "react";
import { useMobileMenuClose } from "../../hooks/useMobileMenuClose";

export default function PlanPage() {
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
                className="text-sm font-bold text-navy-900"
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
                    className="rounded-lg bg-slate-50 px-3 py-3 text-sm font-bold text-navy-900"
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

    <div className="absolute inset-x-0 top-0 -z-10 h-[500px] bg-gradient-to-b from-teal-50/80 to-transparent"></div>

    <div className="mx-auto max-w-[1200px] px-5 pb-20 lg:px-8 lg:pb-28">

        <div className="grid items-center gap-14 lg:grid-cols-[1fr_0.85fr]">

            
            <div>

                <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-teal-100 bg-teal-50 px-3.5 py-2">

                    <span className="h-2 w-2 rounded-full bg-teal-600"></span>

                    <span className="text-xs font-semibold tracking-wide text-teal-700">
                        Financial planning
                    </span>

                </div>


                <h1 className="max-w-3xl text-5xl font-extrabold leading-[1.06] tracking-[-0.04em] text-navy-900 sm:text-6xl">

                    Before deciding what to do with your money,

                    <span className="gradient-text">
                        understand where you stand.
                    </span>

                </h1>


                <p className="mt-7 max-w-2xl text-lg leading-8 text-slate-600">
                    Build a clear picture of your financial position,
                    define the goals that matter, and understand what
                    your current financial reality allows you to do.
                </p>


                <div className="mt-9 flex flex-col gap-3 sm:flex-row">

                    <a
                        href="#start"
                        className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-navy-900/10 transition hover:bg-navy-800"
                    >
                        Start Planning

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
                        How planning works
                    </a>

                </div>

            </div>


            
            <div className="relative">

                <div className="absolute -inset-5 rounded-[32px] bg-teal-100/40 blur-3xl"></div>

                <div className="relative rounded-[28px] border border-slate-200 bg-white p-6 shadow-soft sm:p-7">

                    <div className="flex items-center justify-between border-b border-slate-100 pb-5">

                        <div>

                            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                                Your financial picture
                            </p>

                            <h2 className="mt-1 text-lg font-bold text-navy-900">
                                Current position
                            </h2>

                        </div>

                        <div className="rounded-xl bg-teal-50 px-3 py-2 text-xs font-bold text-teal-700">
                            Overview
                        </div>

                    </div>


                    <div className="mt-6 grid grid-cols-2 gap-3">

                        <div className="rounded-2xl bg-slate-50 p-4">

                            <p className="text-xs font-medium text-slate-400">
                                Monthly income
                            </p>

                            <p className="mt-2 text-lg font-bold text-navy-900">
                                ₹1,50,000
                            </p>

                        </div>


                        <div className="rounded-2xl bg-slate-50 p-4">

                            <p className="text-xs font-medium text-slate-400">
                                Monthly surplus
                            </p>

                            <p className="mt-2 text-lg font-bold text-navy-900">
                                ₹45,000
                            </p>

                        </div>


                        <div className="rounded-2xl bg-slate-50 p-4">

                            <p className="text-xs font-medium text-slate-400">
                                Investments
                            </p>

                            <p className="mt-2 text-lg font-bold text-navy-900">
                                ₹18.5L
                            </p>

                        </div>


                        <div className="rounded-2xl bg-slate-50 p-4">

                            <p className="text-xs font-medium text-slate-400">
                                Liabilities
                            </p>

                            <p className="mt-2 text-lg font-bold text-navy-900">
                                ₹9.2L
                            </p>

                        </div>

                    </div>


                    <div className="mt-5 rounded-2xl border border-teal-100 bg-teal-50 p-5">

                        <div className="flex items-start gap-3">

                            <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-white text-teal-700">

                                <svg
                                    className="h-4 w-4"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth="1.8"
                                        d="M12 8v4l3 2" />

                                    <circle
                                        cx="12"
                                        cy="12"
                                        r="8"
                                        strokeWidth="1.8" />
                                </svg>

                            </div>


                            <div>

                                <p className="text-sm font-bold text-navy-900">
                                    Financial planning starts with context.
                                </p>

                                <p className="mt-1 text-xs leading-5 text-slate-600">
                                    The same investment decision can mean something
                                    very different depending on your complete financial position.
                                </p>

                            </div>

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
                href="#financial-health"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Financial Health
            </a>

            <a
                href="#goals"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Goals
            </a>

            <a
                href="#priorities"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Priorities
            </a>

            <a
                href="#retirement"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Retirement
            </a>

            <a
                href="#how-it-works"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                How It Works
            </a>

        </nav>

    </div>

</section>




<section
    id="financial-health"
    className="scroll-mt-32 py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[0.8fr_1.2fr] lg:items-start">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    01 · Financial health
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    Know your starting point.
                </h2>

                <p className="mt-5 text-lg leading-8 text-slate-600">
                    Good financial decisions start with an accurate picture
                    of your current financial reality.
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
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth="1.8"
                                d="M12 3v18M7 7h7.5a3.5 3.5 0 010 7H8.5a3.5 3.5 0 000 7H17" />
                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Income & expenses
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        Understand how money enters and leaves your household.
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
                                d="M5 19V5M5 19h15"
                                stroke="currentColor"
                                strokeWidth="1.8"
                                strokeLinecap="round" />

                            <path
                                d="M8 15l3-4 3 2 4-6"
                                stroke="currentColor"
                                strokeWidth="1.8"
                                strokeLinecap="round"
                                strokeLinejoin="round" />
                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Surplus & cash flow
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        See how much cash flow is actually available for future decisions.
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
                            <rect
                                x="4"
                                y="4"
                                width="16"
                                height="16"
                                rx="2"
                                strokeWidth="1.8" />

                            <path
                                d="M8 15l2.5-3 2 2 3.5-5"
                                strokeWidth="1.8"
                                strokeLinecap="round"
                                strokeLinejoin="round" />
                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Assets & investments
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        Understand what you already own before deciding what to add.
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
                                d="M7 4h10v16H7z"
                                strokeWidth="1.8"
                                strokeLinejoin="round" />

                            <path
                                d="M10 8h4M10 12h4M10 16h4"
                                strokeWidth="1.8"
                                strokeLinecap="round" />
                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Debt & commitments
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        See which obligations compete with your available financial capacity.
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
                                d="M12 3v18M7 8h8a3 3 0 010 6H9a3 3 0 000 6h8"
                                strokeWidth="1.8"
                                strokeLinecap="round" />
                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Liquidity
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        Know how much money needs to remain readily available.
                    </p>

                </div>


                
                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-navy-900 text-white">

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
                        Overall position
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        Bring the different parts of your financial life into one picture.
                    </p>

                </div>

            </div>

        </div>

    </div>

</section>




<section
    id="goals"
    className="scroll-mt-32 bg-white py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="max-w-3xl">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                02 · Goals
            </p>

            <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                Your money needs a destination.
            </h2>

            <p className="mt-5 text-lg leading-8 text-slate-600">
                A financial goal is not just a number. The amount, timing,
                importance and flexibility of the goal can change the decisions
                available to you.
            </p>

        </div>


        <div className="mt-14 grid gap-5 md:grid-cols-2 lg:grid-cols-3">

            
            <a
                id="retirement"
                href="#start"
                className="scroll-mt-32 group rounded-2xl border border-slate-200 bg-slate-50 p-7 transition hover:-translate-y-1 hover:bg-white hover:shadow-soft"
            >

                <div className="flex items-center justify-between">

                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-navy-900 text-white">

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

                    <span className="text-xs font-semibold text-slate-400">
                        Long term
                    </span>

                </div>

                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Retirement
                </h3>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Build a financial path toward the future lifestyle you want.
                </p>

                <span className="mt-6 inline-flex text-sm font-bold text-navy-900">
                    Explore →
                </span>

            </a>


            
            <a
                href="#start"
                className="group rounded-2xl border border-slate-200 bg-slate-50 p-7 transition hover:-translate-y-1 hover:bg-white hover:shadow-soft"
            >

                <div className="flex items-center justify-between">

                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-teal-50 text-teal-700">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M4 9l8-4 8 4-8 4-8-4z"
                                strokeWidth="1.8"
                                strokeLinejoin="round" />

                            <path
                                d="M7 11v5c2.8 2 7.2 2 10 0v-5"
                                strokeWidth="1.8"
                                strokeLinecap="round" />
                        </svg>

                    </div>

                    <span className="text-xs font-semibold text-slate-400">
                        Family
                    </span>

                </div>

                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Education
                </h3>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Plan for future education expenses without losing sight of other goals.
                </p>

                <span className="mt-6 inline-flex text-sm font-bold text-navy-900">
                    Explore →
                </span>

            </a>


            
            <a
                href="#start"
                className="group rounded-2xl border border-slate-200 bg-slate-50 p-7 transition hover:-translate-y-1 hover:bg-white hover:shadow-soft"
            >

                <div className="flex items-center justify-between">

                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-navy-900">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M3 11l9-7 9 7"
                                strokeWidth="1.8"
                                strokeLinecap="round"
                                strokeLinejoin="round" />

                            <path
                                d="M5 10v10h14V10M9 20v-6h6v6"
                                strokeWidth="1.8"
                                strokeLinejoin="round" />
                        </svg>

                    </div>

                    <span className="text-xs font-semibold text-slate-400">
                        Major purchase
                    </span>

                </div>

                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Home
                </h3>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Understand how a large future purchase fits into the wider financial picture.
                </p>

                <span className="mt-6 inline-flex text-sm font-bold text-navy-900">
                    Explore →
                </span>

            </a>


            
            <a
                href="#start"
                className="group rounded-2xl border border-slate-200 bg-slate-50 p-7 transition hover:-translate-y-1 hover:bg-white hover:shadow-soft"
            >

                <div className="flex items-center justify-between">

                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-navy-900 text-white">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M4 19V9l4 3V7l4 3V5l8 5v9H4z"
                                strokeWidth="1.8"
                                strokeLinejoin="round" />
                        </svg>

                    </div>

                    <span className="text-xs font-semibold text-slate-400">
                        Long term
                    </span>

                </div>

                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Wealth creation
                </h3>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Build capital while keeping your broader financial priorities visible.
                </p>

                <span className="mt-6 inline-flex text-sm font-bold text-navy-900">
                    Explore →
                </span>

            </a>


            
            <a
                href="#start"
                className="group rounded-2xl border border-slate-200 bg-slate-50 p-7 transition hover:-translate-y-1 hover:bg-white hover:shadow-soft"
            >

                <div className="flex items-center justify-between">

                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-teal-50 text-teal-700">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M4 12h16M6 8h12M8 16h8"
                                strokeWidth="1.8"
                                strokeLinecap="round" />
                        </svg>

                    </div>

                    <span className="text-xs font-semibold text-slate-400">
                        Lifestyle
                    </span>

                </div>

                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Lifestyle goals
                </h3>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Account for the things you want to enjoy today and in the future.
                </p>

                <span className="mt-6 inline-flex text-sm font-bold text-navy-900">
                    Explore →
                </span>

            </a>


            
            <a
                href="#start"
                className="group rounded-2xl border border-slate-200 bg-slate-50 p-7 transition hover:-translate-y-1 hover:bg-white hover:shadow-soft"
            >

                <div className="flex items-center justify-between">

                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-navy-900">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <circle
                                cx="5"
                                cy="12"
                                r="1.5"
                                fill="currentColor" />

                            <circle
                                cx="12"
                                cy="12"
                                r="1.5"
                                fill="currentColor" />

                            <circle
                                cx="19"
                                cy="12"
                                r="1.5"
                                fill="currentColor" />
                        </svg>

                    </div>

                    <span className="text-xs font-semibold text-slate-400">
                        Flexible
                    </span>

                </div>

                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Other goals
                </h3>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Add the financial objectives that are specific to your life.
                </p>

                <span className="mt-6 inline-flex text-sm font-bold text-navy-900">
                    Explore →
                </span>

            </a>

        </div>

    </div>

</section>




<section
    id="priorities"
    className="scroll-mt-32 py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[1fr_1fr] lg:items-center">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    03 · Priorities
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    Not every part of a goal is equally fixed.
                </h2>

                <p className="mt-5 text-lg leading-8 text-slate-600">
                    Sometimes the amount can change. Sometimes the date can change.
                    Sometimes the contribution can change. Understanding this
                    creates more possible financial paths.
                </p>

            </div>


            <div className="rounded-[28px] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">

                <div className="space-y-6">

                    <div className="flex gap-4">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-navy-900 text-sm font-bold text-white">
                            01
                        </div>

                        <div>

                            <h3 className="font-bold text-navy-900">
                                Date flexibility
                            </h3>

                            <p className="mt-1 text-sm leading-6 text-slate-500">
                                Could the timing of the goal move if necessary?
                            </p>

                        </div>

                    </div>


                    <div className="flex gap-4">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-teal-600 text-sm font-bold text-white">
                            02
                        </div>

                        <div>

                            <h3 className="font-bold text-navy-900">
                                Amount flexibility
                            </h3>

                            <p className="mt-1 text-sm leading-6 text-slate-500">
                                Could the target amount change if circumstances require it?
                            </p>

                        </div>

                    </div>


                    <div className="flex gap-4">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-sm font-bold text-navy-900">
                            03
                        </div>

                        <div>

                            <h3 className="font-bold text-navy-900">
                                Funding flexibility
                            </h3>

                            <p className="mt-1 text-sm leading-6 text-slate-500">
                                Could the contribution or funding approach change?
                            </p>

                        </div>

                    </div>


                    <div className="flex gap-4">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-sm font-bold text-navy-900">
                            04
                        </div>

                        <div>

                            <h3 className="font-bold text-navy-900">
                                Goal priority
                            </h3>

                            <p className="mt-1 text-sm leading-6 text-slate-500">
                                Which goals matter most when resources are limited?
                            </p>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>




<section className="bg-navy-900 py-24 text-white lg:py-32">

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-300">
                    Retirement planning
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] sm:text-5xl">
                    Plan for the life your money needs to support.
                </h2>

                <p className="mt-6 max-w-xl text-base leading-7 text-slate-300">
                    Retirement is not simply a corpus number. It involves
                    timing, future spending, existing resources, contributions,
                    investment growth and the ability to sustain withdrawals.
                </p>

                <a
                    href="#start"
                    className="mt-8 inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3.5 text-sm font-bold text-navy-900 transition hover:bg-slate-100"
                >
                    Explore retirement planning
                    <span>→</span>
                </a>

            </div>


            <div className="rounded-[28px] border border-white/10 bg-white/5 p-6 sm:p-8">

                <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
                    Retirement picture
                </p>

                <div className="mt-6 space-y-5">

                    <div>

                        <div className="flex justify-between text-sm">

                            <span className="text-slate-300">
                                Current investments
                            </span>

                            <span className="font-bold text-white">
                                ₹35L
                            </span>

                        </div>

                        <div className="mt-2 h-2 rounded-full bg-white/10">

                            <div className="h-2 w-[38%] rounded-full bg-teal-500"></div>

                        </div>

                    </div>


                    <div>

                        <div className="flex justify-between text-sm">

                            <span className="text-slate-300">
                                Future contributions
                            </span>

                            <span className="font-bold text-white">
                                ₹45K / month
                            </span>

                        </div>

                        <div className="mt-2 h-2 rounded-full bg-white/10">

                            <div className="h-2 w-[57%] rounded-full bg-teal-500"></div>

                        </div>

                    </div>


                    <div>

                        <div className="flex justify-between text-sm">

                            <span className="text-slate-300">
                                Retirement horizon
                            </span>

                            <span className="font-bold text-white">
                                20 years
                            </span>

                        </div>

                        <div className="mt-2 h-2 rounded-full bg-white/10">

                            <div className="h-2 w-[75%] rounded-full bg-teal-500"></div>

                        </div>

                    </div>

                </div>


                <div className="mt-7 border-t border-white/10 pt-6">

                    <p className="text-sm leading-6 text-slate-300">
                        The purpose is not to predict one guaranteed future.
                        It is to understand the financial path and what may
                        need to change.
                    </p>

                </div>

            </div>

        </div>

    </div>

</section>




<section
    id="how-it-works"
    className="scroll-mt-32 bg-white py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="text-center">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                How planning works
            </p>

            <h2 className="mx-auto mt-4 max-w-3xl text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                Build the picture before building the strategy.
            </h2>

        </div>


        <div className="mx-auto mt-16 max-w-3xl space-y-8">

            
            <div className="step-line flex gap-5">

                <div className="relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-navy-900 text-xs font-bold text-white">
                    01
                </div>

                <div className="pb-4">

                    <h3 className="text-xl font-bold text-navy-900">
                        Understand your current reality
                    </h3>

                    <p className="mt-2 text-sm leading-7 text-slate-500">
                        Bring together the financial information that describes
                        your current position.
                    </p>

                </div>

            </div>


            
            <div className="step-line flex gap-5">

                <div className="relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-teal-600 text-xs font-bold text-white">
                    02
                </div>

                <div className="pb-4">

                    <h3 className="text-xl font-bold text-navy-900">
                        Define your goals
                    </h3>

                    <p className="mt-2 text-sm leading-7 text-slate-500">
                        Establish what you want, when you want it and how important
                        or flexible each goal is.
                    </p>

                </div>

            </div>


            
            <div className="step-line flex gap-5">

                <div className="relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-slate-100 text-xs font-bold text-navy-900">
                    03
                </div>

                <div className="pb-4">

                    <h3 className="text-xl font-bold text-navy-900">
                        Understand the gaps
                    </h3>

                    <p className="mt-2 text-sm leading-7 text-slate-500">
                        See what your current resources and cash flow can support
                        relative to your desired outcomes.
                    </p>

                </div>

            </div>


            
            <div className="step-line flex gap-5">

                <div className="relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-slate-100 text-xs font-bold text-navy-900">
                    04
                </div>

                <div className="pb-4">

                    <h3 className="text-xl font-bold text-navy-900">
                        Create possible paths
                    </h3>

                    <p className="mt-2 text-sm leading-7 text-slate-500">
                        Different combinations of contributions, capital, timing,
                        priorities and other financial actions may create different paths.
                    </p>

                </div>

            </div>


            
            <div className="flex gap-5">

                <div className="relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-navy-900 text-xs font-bold text-white">
                    05
                </div>

                <div>

                    <h3 className="text-xl font-bold text-navy-900">
                        Move into decision-making
                    </h3>

                    <p className="mt-2 text-sm leading-7 text-slate-500">
                        Once the planning picture is clear, you can move into
                        investment, protection and strategy decisions.
                    </p>

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
                    Start planning
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-white sm:text-5xl">
                    Start with where you are.
                </h2>

                <p className="mt-5 max-w-2xl text-base leading-7 text-slate-300">
                    Build your financial picture first. Your goals and decisions
                    become easier to understand when the starting point is clear.
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
                        href="/decide"
                        className="inline-flex items-center justify-center rounded-xl border border-white/20 px-6 py-3.5 text-sm font-bold text-white transition hover:bg-white/10"
                    >
                        See how decisions work
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
                            href="#financial-health"
                            className="transition hover:text-navy-900"
                        >
                            Financial Health
                        </a>
                    </li>

                    <li>
                        <a
                            href="#goals"
                            className="transition hover:text-navy-900"
                        >
                            Goals
                        </a>
                    </li>

                    <li>
                        <a
                            href="#retirement"
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
