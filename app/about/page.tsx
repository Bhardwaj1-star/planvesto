"use client";

import { useState } from "react";
import { useMobileMenuClose } from "../../hooks/useMobileMenuClose";

export default function AboutPage() {
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
                className="text-sm font-bold text-navy-900"
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
                    className="rounded-lg bg-slate-50 px-3 py-3 text-sm font-bold text-navy-900"
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

    <div className="absolute inset-x-0 top-0 -z-10 h-[580px] bg-gradient-to-b from-teal-50/80 to-transparent"></div>


    <div className="mx-auto max-w-[1200px] px-5 pb-24 lg:px-8 lg:pb-32">

        <div className="mx-auto max-w-4xl text-center">


            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-teal-100 bg-teal-50 px-3.5 py-2">

                <span className="h-2 w-2 rounded-full bg-teal-600"></span>

                <span className="text-xs font-semibold tracking-wide text-teal-700">
                    About Planvesto
                </span>

            </div>


            <h1 className="text-5xl font-extrabold leading-[1.06] tracking-[-0.04em] text-navy-900 sm:text-6xl">

                Financial planning should help you

                <span className="gradient-text">
                    make better decisions.
                </span>

            </h1>


            <p className="mx-auto mt-7 max-w-2xl text-lg leading-8 text-slate-600">
                Planvesto is built around a simple idea: financial planning
                should begin with understanding the person's financial
                situation and what they are trying to achieve—not with a product.
            </p>


            <div className="mt-9 flex flex-col justify-center gap-3 sm:flex-row">

                <a
                    href="/plan"
                    className="inline-flex items-center justify-center gap-2 rounded-xl bg-navy-900 px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-navy-800"
                >
                    Explore Planvesto
                    <span>→</span>
                </a>


                <a
                    href="#why"
                    className="inline-flex items-center justify-center rounded-xl border border-slate-300 bg-white px-6 py-3.5 text-sm font-semibold text-navy-900 transition hover:bg-slate-50"
                >
                    Why we built it
                </a>

            </div>

        </div>

    </div>

</section>




<section
    id="why"
    className="scroll-mt-32 bg-white py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[0.75fr_1.25fr] lg:items-center">


            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    Why Planvesto
                </p>


                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    Move financial planning from products to decisions.
                </h2>

            </div>


            <div>

                <p className="text-lg leading-8 text-slate-600">
                    People are often presented with investments, insurance
                    products or financial solutions before the underlying
                    financial problem has been clearly understood.
                </p>


                <p className="mt-5 text-lg leading-8 text-slate-600">
                    Planvesto takes the opposite approach. Understand the
                    financial position. Define the goals. Identify constraints.
                    Consider risk and protection. Then evaluate the strategies
                    that can address the actual need.
                </p>


                <p className="mt-5 text-lg leading-8 text-slate-600">
                    The objective is not to make financial decisions more
                    complicated. It is to make the reasoning behind them clearer.
                </p>

            </div>

        </div>

    </div>

</section>




<section className="py-24 lg:py-32">

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">


        <div className="max-w-3xl">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                What Planvesto is
            </p>


            <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                A financial planning and decision platform.
            </h2>


            <p className="mt-5 text-lg leading-8 text-slate-600">
                Planvesto brings financial information, planning, investment
                decisions, protection and financial strategies into one
                connected experience.
            </p>

        </div>


        <div className="mt-14 grid gap-5 md:grid-cols-2 lg:grid-cols-3">


            

            <div className="value-card rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-teal-50 text-teal-700">

                    <svg
                        className="h-5 w-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >

                        <path
                            d="M5 19V8M12 19V5M19 19v-9"
                            strokeWidth="1.8"
                            strokeLinecap="round" />

                    </svg>

                </div>


                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Plan
                </h3>


                <p className="mt-3 text-sm leading-7 text-slate-500">
                    Understand your current financial position and translate
                    your goals into a financial plan.
                </p>


                <a
                    href="/plan"
                    className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-navy-900"
                >
                    Explore Plan
                    <span>→</span>
                </a>

            </div>


            

            <div className="value-card rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-navy-900 text-white">

                    <svg
                        className="h-5 w-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >

                        <path
                            d="M5 17l5-5 3 3 6-7"
                            strokeWidth="1.8"
                            strokeLinecap="round"
                            strokeLinejoin="round" />

                        <path
                            d="M15 8h4v4"
                            strokeWidth="1.8"
                            strokeLinecap="round"
                            strokeLinejoin="round" />

                    </svg>

                </div>


                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Invest
                </h3>


                <p className="mt-3 text-sm leading-7 text-slate-500">
                    Understand the role investments play in achieving financial
                    goals and managing risk.
                </p>


                <a
                    href="/invest"
                    className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-navy-900"
                >
                    Explore Invest
                    <span>→</span>
                </a>

            </div>


            

            <div className="value-card rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

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


                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Protect
                </h3>


                <p className="mt-3 text-sm leading-7 text-slate-500">
                    Consider financial risks and the protection required to
                    keep important goals on track.
                </p>


                <a
                    href="/protect"
                    className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-navy-900"
                >
                    Explore Protect
                    <span>→</span>
                </a>

            </div>


            

            <div className="value-card rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-teal-50 text-teal-700">

                    <svg
                        className="h-5 w-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >

                        <circle
                            cx="12"
                            cy="12"
                            r="8"
                            strokeWidth="1.8" />

                        <path
                            d="M12 8v4l3 2"
                            strokeWidth="1.8"
                            strokeLinecap="round" />

                    </svg>

                </div>


                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Decide
                </h3>


                <p className="mt-3 text-sm leading-7 text-slate-500">
                    Compare relevant strategies and understand the trade-offs
                    before selecting a financial path.
                </p>


                <a
                    href="/decide"
                    className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-navy-900"
                >
                    Explore Decide
                    <span>→</span>
                </a>

            </div>


            

            <div className="value-card rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-100 text-navy-900">

                    <svg
                        className="h-5 w-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >

                        <path
                            d="M4 5.5A2.5 2.5 0 016.5 3H20v16H6.5A2.5 2.5 0 014 16.5v-11z"
                            strokeWidth="1.8"
                            strokeLinejoin="round" />

                        <path
                            d="M8 7h8M8 11h6"
                            strokeWidth="1.8"
                            strokeLinecap="round" />

                    </svg>

                </div>


                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Learn
                </h3>


                <p className="mt-3 text-sm leading-7 text-slate-500">
                    Build the financial understanding needed to participate
                    meaningfully in your own decisions.
                </p>


                <a
                    href="/learn"
                    className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-navy-900"
                >
                    Explore Learn
                    <span>→</span>
                </a>

            </div>


            

            <div className="value-card rounded-[24px] border border-teal-100 bg-teal-50 p-7">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-white text-teal-700">

                    <svg
                        className="h-5 w-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >

                        <circle
                            cx="6"
                            cy="12"
                            r="2.5"
                            strokeWidth="1.8" />

                        <circle
                            cx="18"
                            cy="6"
                            r="2.5"
                            strokeWidth="1.8" />

                        <circle
                            cx="18"
                            cy="18"
                            r="2.5"
                            strokeWidth="1.8" />

                        <path
                            d="M8.3 10.8l7.4-3.6M8.3 13.2l7.4 3.6"
                            strokeWidth="1.8"
                            strokeLinecap="round" />

                    </svg>

                </div>


                <h3 className="mt-6 text-xl font-bold text-navy-900">
                    Connected thinking
                </h3>


                <p className="mt-3 text-sm leading-7 text-slate-600">
                    The different parts of financial planning are considered
                    together rather than as isolated product decisions.
                </p>

            </div>

        </div>

    </div>

</section>




<section className="bg-navy-900 py-24 text-white lg:py-32">

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">


        <div className="grid gap-14 lg:grid-cols-[0.8fr_1.2fr]">


            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-300">
                    Our approach
                </p>


                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] sm:text-5xl">
                    The sequence matters.
                </h2>


                <p className="mt-6 max-w-lg text-base leading-7 text-slate-300">
                    Planvesto is designed around the idea that financial
                    planning works better when decisions follow a logical sequence.
                </p>

            </div>


            <div className="space-y-4">


                <div className="rounded-2xl border border-white/10 bg-white/5 p-6">

                    <div className="flex gap-5">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-white/10 text-sm font-bold">
                            01
                        </div>

                        <div>

                            <h3 className="font-bold">
                                Understand
                            </h3>

                            <p className="mt-2 text-sm leading-6 text-slate-400">
                                Understand the financial position, goals,
                                constraints and relevant risks.
                            </p>

                        </div>

                    </div>

                </div>


                <div className="rounded-2xl border border-white/10 bg-white/5 p-6">

                    <div className="flex gap-5">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-white/10 text-sm font-bold">
                            02
                        </div>

                        <div>

                            <h3 className="font-bold">
                                Diagnose
                            </h3>

                            <p className="mt-2 text-sm leading-6 text-slate-400">
                                Identify the financial problem or opportunity
                                that needs to be addressed.
                            </p>

                        </div>

                    </div>

                </div>


                <div className="rounded-2xl border border-white/10 bg-white/5 p-6">

                    <div className="flex gap-5">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-white/10 text-sm font-bold">
                            03
                        </div>

                        <div>

                            <h3 className="font-bold">
                                Evaluate
                            </h3>

                            <p className="mt-2 text-sm leading-6 text-slate-400">
                                Consider strategies and compare the consequences
                                of relevant alternatives.
                            </p>

                        </div>

                    </div>

                </div>


                <div className="rounded-2xl border border-teal-500/30 bg-teal-500/10 p-6">

                    <div className="flex gap-5">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-teal-600 text-sm font-bold">
                            04
                        </div>

                        <div>

                            <h3 className="font-bold">
                                Act
                            </h3>

                            <p className="mt-2 text-sm leading-6 text-slate-300">
                                Translate the selected financial plan into
                                implementation actions and review it as circumstances change.
                            </p>

                        </div>

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
                Principles
            </p>


            <h2 className="mx-auto mt-4 max-w-3xl text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                What we believe good financial planning should do.
            </h2>

        </div>


        <div className="mt-14 grid gap-5 md:grid-cols-2">


            <div className="rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

                <span className="text-sm font-bold text-teal-700">
                    01
                </span>

                <h3 className="mt-5 text-xl font-bold text-navy-900">
                    Start with the person, not the product.
                </h3>

                <p className="mt-3 text-sm leading-7 text-slate-500">
                    Financial recommendations should make sense in the context
                    of the person's financial situation and goals.
                </p>

            </div>


            <div className="rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

                <span className="text-sm font-bold text-teal-700">
                    02
                </span>

                <h3 className="mt-5 text-xl font-bold text-navy-900">
                    Consider the whole picture.
                </h3>

                <p className="mt-3 text-sm leading-7 text-slate-500">
                    Investment, protection, cash flow, goals and risk can
                    influence each other.
                </p>

            </div>


            <div className="rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

                <span className="text-sm font-bold text-teal-700">
                    03
                </span>

                <h3 className="mt-5 text-xl font-bold text-navy-900">
                    Compare before deciding.
                </h3>

                <p className="mt-3 text-sm leading-7 text-slate-500">
                    A decision becomes more meaningful when alternatives and
                    their trade-offs can be understood.
                </p>

            </div>


            <div className="rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

                <span className="text-sm font-bold text-teal-700">
                    04
                </span>

                <h3 className="mt-5 text-xl font-bold text-navy-900">
                    Make the reasoning visible.
                </h3>

                <p className="mt-3 text-sm leading-7 text-slate-500">
                    People should be able to understand why a financial
                    direction makes sense for their situation.
                </p>

            </div>

        </div>

    </div>

</section>




<section className="bg-white py-24 lg:py-32">

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">


        <div className="mx-auto max-w-3xl text-center">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                The experience
            </p>


            <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                Simple for the user. Structured underneath.
            </h2>


            <p className="mt-5 text-lg leading-8 text-slate-600">
                The complexity of financial planning should not become the
                complexity of the user's experience.
            </p>

        </div>


        <div className="mt-14 grid gap-5 md:grid-cols-3">


            <div className="rounded-[24px] border border-slate-200 bg-slate-50 p-7 text-center">

                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-white text-navy-900 shadow-sm">

                    <span className="font-extrabold">
                        1
                    </span>

                </div>


                <h3 className="mt-6 font-bold text-navy-900">
                    Tell us about your situation
                </h3>


                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Provide the information needed to understand your financial position.
                </p>

            </div>


            <div className="rounded-[24px] border border-slate-200 bg-slate-50 p-7 text-center">

                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-teal-50 text-teal-700 shadow-sm">

                    <span className="font-extrabold">
                        2
                    </span>

                </div>


                <h3 className="mt-6 font-bold text-navy-900">
                    Understand the plan
                </h3>


                <p className="mt-3 text-sm leading-6 text-slate-500">
                    See goals, decisions, strategies and actions in one connected context.
                </p>

            </div>


            <div className="rounded-[24px] border border-slate-200 bg-slate-50 p-7 text-center">

                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-white text-navy-900 shadow-sm">

                    <span className="font-extrabold">
                        3
                    </span>

                </div>


                <h3 className="mt-6 font-bold text-navy-900">
                    Take action
                </h3>


                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Implement the selected financial plan and revisit it when circumstances change.
                </p>

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
                    Start with your financial picture
                </p>


                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-white sm:text-5xl">
                    Your financial plan should make sense to you.
                </h2>


                <p className="mt-5 max-w-2xl text-base leading-7 text-slate-300">
                    Start by understanding where you are, what you want to
                    achieve and which financial decisions matter most.
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
                        href="/contact"
                        className="inline-flex items-center justify-center rounded-xl border border-white/20 px-6 py-3.5 text-sm font-bold text-white transition hover:bg-white/10"
                    >
                        Contact Planvesto
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
                            className="font-semibold text-navy-900"
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
