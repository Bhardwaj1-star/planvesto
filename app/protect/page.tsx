"use client";

import { useState } from "react";
import { useMobileMenuClose } from "../../hooks/useMobileMenuClose";

export default function ProtectPage() {
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
                className="text-sm font-bold text-navy-900"
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
                    className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50"
                >
                    Invest
                </a>

                <a
                    href="/protect"
                    className="rounded-lg bg-slate-50 px-3 py-3 text-sm font-bold text-navy-900"
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

    <div className="absolute inset-x-0 top-0 -z-10 h-[540px] bg-gradient-to-b from-teal-50/80 to-transparent"></div>


    <div className="mx-auto max-w-[1200px] px-5 pb-20 lg:px-8 lg:pb-28">

        <div className="grid items-center gap-14 lg:grid-cols-[1fr_0.9fr]">

            <div>

                <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-teal-100 bg-teal-50 px-3.5 py-2">

                    <span className="h-2 w-2 rounded-full bg-teal-600"></span>

                    <span className="text-xs font-semibold tracking-wide text-teal-700">
                        Risk protection
                    </span>

                </div>


                <h1 className="max-w-3xl text-5xl font-extrabold leading-[1.06] tracking-[-0.04em] text-navy-900 sm:text-6xl">

                    Protect the financial life

                    <span className="gradient-text">
                        you are building.
                    </span>

                </h1>


                <p className="mt-7 max-w-2xl text-lg leading-8 text-slate-600">
                    Identify the financial risks that could affect your goals,
                    understand your existing protection and see where meaningful
                    gaps may remain.
                </p>


                <div className="mt-9 flex flex-col gap-3 sm:flex-row">

                    <a
                        href="#start"
                        className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-navy-900/10 transition hover:bg-navy-800"
                    >
                        Review Your Protection

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
                        How protection works
                    </a>

                </div>

            </div>


            
            <div className="relative">

                <div className="absolute -inset-5 rounded-[32px] bg-teal-100/50 blur-3xl"></div>


                <div className="relative rounded-[28px] border border-slate-200 bg-white p-6 shadow-soft sm:p-7">

                    <div className="flex items-center justify-between border-b border-slate-100 pb-5">

                        <div>

                            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                                Protection picture
                            </p>

                            <h2 className="mt-1 text-lg font-bold text-navy-900">
                                Current position
                            </h2>

                        </div>

                        <span className="rounded-xl bg-teal-50 px-3 py-2 text-xs font-bold text-teal-700">
                            Example
                        </span>

                    </div>


                    <div className="mt-6 space-y-4">

                        <div className="flex items-center justify-between rounded-2xl bg-slate-50 p-4">

                            <div className="flex items-center gap-3">

                                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-navy-900">

                                    <svg
                                        className="h-4 w-4"
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

                                <div>

                                    <p className="text-sm font-bold text-navy-900">
                                        Financial risks
                                    </p>

                                    <p className="text-xs text-slate-400">
                                        Identified exposures
                                    </p>

                                </div>

                            </div>

                            <span className="text-sm font-extrabold text-navy-900">
                                4
                            </span>

                        </div>


                        <div className="flex items-center justify-between rounded-2xl bg-slate-50 p-4">

                            <div className="flex items-center gap-3">

                                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-teal-700">

                                    <svg
                                        className="h-4 w-4"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            d="M5 12l4 4L19 6"
                                            strokeWidth="1.8"
                                            strokeLinecap="round"
                                            strokeLinejoin="round" />
                                    </svg>

                                </div>

                                <div>

                                    <p className="text-sm font-bold text-navy-900">
                                        Existing protection
                                    </p>

                                    <p className="text-xs text-slate-400">
                                        Effective cover
                                    </p>

                                </div>

                            </div>

                            <span className="text-sm font-extrabold text-navy-900">
                                ₹75L
                            </span>

                        </div>


                        <div className="rounded-2xl border border-teal-100 bg-teal-50 p-5">

                            <div className="flex items-center justify-between">

                                <div>

                                    <p className="text-xs font-semibold uppercase tracking-wider text-teal-700">
                                        Protection gap
                                    </p>

                                    <p className="mt-1 text-2xl font-extrabold text-navy-900">
                                        ₹25L
                                    </p>

                                </div>

                                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white text-teal-700">

                                    <svg
                                        className="h-5 w-5"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            d="M12 9v4M12 17h.01"
                                            strokeWidth="2"
                                            strokeLinecap="round" />

                                        <path
                                            d="M10.3 4.5L3.2 17a2 2 0 001.7 3h14.2a2 2 0 001.7-3L13.7 4.5a2 2 0 00-3.4 0z"
                                            strokeWidth="1.7"
                                            strokeLinejoin="round" />
                                    </svg>

                                </div>

                            </div>

                            <p className="mt-3 text-xs leading-5 text-slate-500">
                                Example only. Actual protection requirements
                                depend on your financial circumstances and risks.
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
                href="#risks"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Risks
            </a>

            <a
                href="#need"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Protection Need
            </a>

            <a
                href="#gap"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Protection Gap
            </a>

            <a
                href="#strategy"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Strategy
            </a>

            <a
                href="#monitoring"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Monitoring
            </a>

        </nav>

    </div>

</section>




<section
    id="risks"
    className="scroll-mt-32 py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[0.8fr_1.2fr] lg:items-start">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    01 · Financial risks
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    What could disrupt the plan?
                </h2>

                <p className="mt-5 text-lg leading-8 text-slate-600">
                    Protection starts by understanding the financial consequences
                    of risks affecting your income, family, liabilities, assets
                    and goals.
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
                                d="M12 3v18M7 8h8a3 3 0 010 6H9a3 3 0 000 6h8"
                                strokeWidth="1.8"
                                strokeLinecap="round" />
                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Income risk
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        What happens to the financial plan if an important income source is affected?
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
                                d="M12 3l8 4v5c0 4.8-3.4 7.9-8 9-4.6-1.1-8-4.2-8-9V7l8-4z"
                                strokeWidth="1.8"
                                strokeLinejoin="round" />
                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Family risk
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        How could a major life event affect dependents and their financial goals?
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
                                d="M4 19h16M6 16V8M10 16V5M14 16v-4M18 16V7"
                                strokeWidth="1.8"
                                strokeLinecap="round" />
                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Liability risk
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        Could existing debt or financial obligations become difficult to service?
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
                                d="M4 19V9l4 3V7l4 3V5l8 5v9H4z"
                                strokeWidth="1.8"
                                strokeLinejoin="round" />
                        </svg>

                    </div>

                    <h3 className="mt-5 font-bold text-navy-900">
                        Goal risk
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        Which financial goals could be affected by an unexpected event?
                    </p>

                </div>

            </div>

        </div>

    </div>

</section>




<section
    id="need"
    className="scroll-mt-32 bg-white py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="max-w-3xl">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                02 · Protection need
            </p>

            <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                How much protection does the situation actually require?
            </h2>

            <p className="mt-5 text-lg leading-8 text-slate-600">
                The question is not simply whether a policy exists. The
                relevant question is whether the existing protection is
                sufficient for the financial exposure.
            </p>

        </div>


        <div className="mt-14 rounded-[28px] border border-slate-200 bg-slate-50 p-6 sm:p-8">

            <div className="grid gap-6 lg:grid-cols-3">

                <div className="rounded-2xl bg-white p-6 shadow-sm">

                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Financial exposure
                    </p>

                    <p className="mt-3 text-3xl font-extrabold text-navy-900">
                        ₹1.00Cr
                    </p>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        Example financial requirement arising from identified risks.
                    </p>

                </div>


                <div className="rounded-2xl bg-white p-6 shadow-sm">

                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Existing effective protection
                    </p>

                    <p className="mt-3 text-3xl font-extrabold text-navy-900">
                        ₹75L
                    </p>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        Existing protection that can meaningfully address the exposure.
                    </p>

                </div>


                <div className="rounded-2xl border border-teal-100 bg-teal-50 p-6">

                    <p className="text-xs font-bold uppercase tracking-wider text-teal-700">
                        Remaining gap
                    </p>

                    <p className="mt-3 text-3xl font-extrabold text-navy-900">
                        ₹25L
                    </p>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        The portion that may still require a financial response.
                    </p>

                </div>

            </div>


            <div className="mt-8 border-t border-slate-200 pt-7">

                <p className="text-sm leading-7 text-slate-500">
                    These figures are illustrative only. The underlying Planvesto
                    protection workflow calculates need, effective existing
                    protection and the resulting gap from the investor's
                    financial circumstances and selected methodology.
                </p>

            </div>

        </div>

    </div>

</section>




<section
    id="gap"
    className="scroll-mt-32 py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[1fr_1fr] lg:items-center">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    03 · Protection gap
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    Existing cover is only part of the picture.
                </h2>

                <p className="mt-5 text-lg leading-8 text-slate-600">
                    A protection review considers the effective protection
                    already available and the resources that may be usable
                    before determining the remaining gap.
                </p>

            </div>


            <div className="rounded-[28px] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">

                <div className="space-y-6">

                    <div className="flex items-start gap-4">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-navy-900 text-sm font-bold text-white">
                            01
                        </div>

                        <div>

                            <h3 className="font-bold text-navy-900">
                                Identify the exposure
                            </h3>

                            <p className="mt-1 text-sm leading-6 text-slate-500">
                                Understand what financial risk could affect the plan.
                            </p>

                        </div>

                    </div>


                    <div className="flex items-start gap-4">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-teal-600 text-sm font-bold text-white">
                            02
                        </div>

                        <div>

                            <h3 className="font-bold text-navy-900">
                                Review existing protection
                            </h3>

                            <p className="mt-1 text-sm leading-6 text-slate-500">
                                Consider current policies and other effective resources.
                            </p>

                        </div>

                    </div>


                    <div className="flex items-start gap-4">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-sm font-bold text-navy-900">
                            03
                        </div>

                        <div>

                            <h3 className="font-bold text-navy-900">
                                Identify the residual gap
                            </h3>

                            <p className="mt-1 text-sm leading-6 text-slate-500">
                                Determine what remains after existing protection is considered.
                            </p>

                        </div>

                    </div>


                    <div className="flex items-start gap-4">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-sm font-bold text-navy-900">
                            04
                        </div>

                        <div>

                            <h3 className="font-bold text-navy-900">
                                Map the affected goals
                            </h3>

                            <p className="mt-1 text-sm leading-6 text-slate-500">
                                Understand which financial objectives could be affected.
                            </p>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    </div>

</section>




<section
    id="strategy"
    className="scroll-mt-32 bg-navy-900 py-24 text-white lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-300">
                    04 · Protection strategy
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] sm:text-5xl">
                    There can be more than one way to address a gap.
                </h2>

                <p className="mt-6 max-w-xl text-base leading-7 text-slate-300">
                    A protection strategy considers the identified gap together
                    with cash flow, goals and the wider financial position.
                </p>

            </div>


            <div className="space-y-4">

                <div className="rounded-2xl border border-white/10 bg-white/5 p-6">

                    <div className="flex items-start gap-4">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white/10 text-sm font-bold">
                            A
                        </div>

                        <div>

                            <h3 className="font-bold text-white">
                                Transfer the risk
                            </h3>

                            <p className="mt-2 text-sm leading-6 text-slate-400">
                                Use suitable protection products to transfer part
                                of the identified financial exposure.
                            </p>

                        </div>

                    </div>

                </div>


                <div className="rounded-2xl border border-white/10 bg-white/5 p-6">

                    <div className="flex items-start gap-4">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white/10 text-sm font-bold">
                            B
                        </div>

                        <div>

                            <h3 className="font-bold text-white">
                                Self-fund part of the risk
                            </h3>

                            <p className="mt-2 text-sm leading-6 text-slate-400">
                                Existing usable resources may form part of the
                                response where appropriate.
                            </p>

                        </div>

                    </div>

                </div>


                <div className="rounded-2xl border border-white/10 bg-white/5 p-6">

                    <div className="flex items-start gap-4">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white/10 text-sm font-bold">
                            C
                        </div>

                        <div>

                            <h3 className="font-bold text-white">
                                Change the financial plan
                            </h3>

                            <p className="mt-2 text-sm leading-6 text-slate-400">
                                In some circumstances, changing goals, cash flow
                                or other financial actions can also affect the response.
                            </p>

                        </div>

                    </div>

                </div>


                <div className="rounded-2xl border border-teal-500/20 bg-teal-500/10 p-6">

                    <p className="text-sm font-bold text-teal-300">
                        The cost matters too.
                    </p>

                    <p className="mt-2 text-sm leading-6 text-slate-300">
                        Any protection strategy needs to be considered against
                        its effect on surplus, liquidity, goals and the wider plan.
                    </p>

                </div>

            </div>

        </div>

    </div>

</section>




<section className="py-24 lg:py-32">

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="text-center">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                Validate before deciding
            </p>

            <h2 className="mx-auto mt-4 max-w-3xl text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                More cover is not automatically a better decision.
            </h2>

            <p className="mx-auto mt-5 max-w-2xl text-lg leading-8 text-slate-600">
                The protection decision needs to work financially as well as
                address the underlying risk.
            </p>

        </div>


        <div className="mt-14 grid gap-5 md:grid-cols-2 lg:grid-cols-4">

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                <div className="text-xs font-bold uppercase tracking-wider text-teal-700">
                    Check 01
                </div>

                <h3 className="mt-4 font-bold text-navy-900">
                    Coverage fit
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    Does the protection address the identified exposure?
                </p>

            </div>


            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                <div className="text-xs font-bold uppercase tracking-wider text-teal-700">
                    Check 02
                </div>

                <h3 className="mt-4 font-bold text-navy-900">
                    Affordability
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    What does the premium do to available cash flow?
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
                    Does the decision leave adequate liquidity?
                </p>

            </div>


            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                <div className="text-xs font-bold uppercase tracking-wider text-teal-700">
                    Check 04
                </div>

                <h3 className="mt-4 font-bold text-navy-900">
                    Goal impact
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    Does the protection strategy interfere with important goals?
                </p>

            </div>

        </div>

    </div>

</section>




<section
    id="monitoring"
    className="scroll-mt-32 bg-white py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[0.85fr_1.15fr] lg:items-center">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    05 · Monitoring
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    Protection is not a one-time decision.
                </h2>

                <p className="mt-5 text-lg leading-8 text-slate-600">
                    Your financial position changes. Policies expire.
                    Coverage changes. Goals move. A protection plan therefore
                    needs to be reviewed as circumstances change.
                </p>

            </div>


            <div className="rounded-[28px] border border-slate-200 bg-slate-50 p-6 sm:p-8">

                <div className="space-y-4">

                    <div className="flex items-center justify-between rounded-2xl bg-white p-5 shadow-sm">

                        <div>

                            <p className="text-sm font-bold text-navy-900">
                                Coverage amount
                            </p>

                            <p className="mt-1 text-xs text-slate-400">
                                Compare required vs actual protection
                            </p>

                        </div>

                        <span className="rounded-lg bg-teal-50 px-3 py-1.5 text-xs font-bold text-teal-700">
                            Review
                        </span>

                    </div>


                    <div className="flex items-center justify-between rounded-2xl bg-white p-5 shadow-sm">

                        <div>

                            <p className="text-sm font-bold text-navy-900">
                                Policy expiry
                            </p>

                            <p className="mt-1 text-xs text-slate-400">
                                Track important dates
                            </p>

                        </div>

                        <span className="rounded-lg bg-slate-100 px-3 py-1.5 text-xs font-bold text-navy-900">
                            Track
                        </span>

                    </div>


                    <div className="flex items-center justify-between rounded-2xl bg-white p-5 shadow-sm">

                        <div>

                            <p className="text-sm font-bold text-navy-900">
                                Financial changes
                            </p>

                            <p className="mt-1 text-xs text-slate-400">
                                Income, goals, liabilities and assets
                            </p>

                        </div>

                        <span className="rounded-lg bg-slate-100 px-3 py-1.5 text-xs font-bold text-navy-900">
                            Update
                        </span>

                    </div>


                    <div className="flex items-center justify-between rounded-2xl bg-white p-5 shadow-sm">

                        <div>

                            <p className="text-sm font-bold text-navy-900">
                                Protection gap
                            </p>

                            <p className="mt-1 text-xs text-slate-400">
                                Reassess when circumstances change
                            </p>

                        </div>

                        <span className="rounded-lg bg-teal-50 px-3 py-1.5 text-xs font-bold text-teal-700">
                            Recheck
                        </span>

                    </div>

                </div>

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
                    How protection planning works
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] sm:text-5xl">
                    From risk to a practical response.
                </h2>

                <p className="mt-6 max-w-lg text-base leading-7 text-slate-300">
                    The protection process moves from identifying the financial
                    exposure to validating a response that fits the wider plan.
                </p>

            </div>


            <div className="space-y-7">

                <div className="risk-line flex gap-5">

                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        01
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Identify financial risks
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Understand the exposures arising from the financial position and goals.
                        </p>

                    </div>

                </div>


                <div className="risk-line flex gap-5">

                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        02
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Determine protection need
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Quantify the protection required using the applicable methodology.
                        </p>

                    </div>

                </div>


                <div className="risk-line flex gap-5">

                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        03
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Compare existing protection
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Establish effective cover and the residual protection gap.
                        </p>

                    </div>

                </div>


                <div className="risk-line flex gap-5">

                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        04
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Build possible strategies
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Consider different ways of addressing the identified gap.
                        </p>

                    </div>

                </div>


                <div className="risk-line flex gap-5">

                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-white/20 text-sm font-bold">
                        05
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Validate the financial impact
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Check affordability, liquidity, goals and portfolio effects.
                        </p>

                    </div>

                </div>


                <div className="flex gap-5">

                    <div className="relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-teal-600 text-sm font-bold">
                        06
                    </div>

                    <div>

                        <h3 className="text-lg font-bold">
                            Decide and monitor
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-slate-400">
                            Record the decision and review the protection as circumstances change.
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
                    Start your protection review
                </p>

                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-white sm:text-5xl">
                    Know what you are protecting — and what may still be exposed.
                </h2>

                <p className="mt-5 max-w-2xl text-base leading-7 text-slate-300">
                    Build the protection picture around your financial life,
                    rather than evaluating policies in isolation.
                </p>


                <div className="mt-8 flex flex-col gap-3 sm:flex-row">

                    <a
                        href="/login"
                        className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-6 py-3.5 text-sm font-bold text-navy-900 transition hover:bg-slate-100"
                    >
                        Start Protection Review
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
                            className="font-semibold text-navy-900"
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
