"use client";

import { useState } from "react";
import { useMobileMenuClose } from "../../hooks/useMobileMenuClose";
import { useArticleSearch } from "../../hooks/useArticleSearch";

export default function LearnPage() {
  const [menuOpen, setMenuOpen] = useState(false);

  useMobileMenuClose(setMenuOpen);
  useArticleSearch();

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
                className="text-sm font-bold text-navy-900"
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
                    className="rounded-lg px-3 py-3 text-sm font-medium hover:bg-slate-50"
                >
                    Decide
                </a>

                <a
                    href="/learn"
                    className="rounded-lg bg-slate-50 px-3 py-3 text-sm font-bold text-navy-900"
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

        <div className="mx-auto max-w-4xl text-center">


            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-teal-100 bg-teal-50 px-3.5 py-2">

                <span className="h-2 w-2 rounded-full bg-teal-600"></span>

                <span className="text-xs font-semibold tracking-wide text-teal-700">
                    Planvesto Learning
                </span>

            </div>


            <h1 className="text-5xl font-extrabold leading-[1.06] tracking-[-0.04em] text-navy-900 sm:text-6xl">

                Understand your money

                <span className="gradient-text">
                    before you act.
                </span>

            </h1>


            <p className="mx-auto mt-7 max-w-2xl text-lg leading-8 text-slate-600">
                Financial planning becomes easier when you understand the
                decisions behind the products, numbers and recommendations.
            </p>


            <div className="mx-auto mt-9 max-w-xl">

                <div className="relative">

                    <svg
                        className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >

                        <circle
                            cx="11"
                            cy="11"
                            r="7"
                            strokeWidth="1.8" />

                        <path
                            d="M20 20l-4-4"
                            strokeWidth="1.8"
                            strokeLinecap="round" />

                    </svg>


                    <input
                        id="searchInput"
                        type="search"
                        placeholder="Search financial topics..."
                        className="h-14 w-full rounded-2xl border border-slate-200 bg-white pl-12 pr-5 text-sm text-navy-900 outline-none shadow-card transition focus:border-teal-500 focus:ring-4 focus:ring-teal-500/10" />

                </div>

            </div>

        </div>

    </div>

</section>




<section className="border-y border-slate-200 bg-white">

    <div className="mx-auto max-w-[1200px] overflow-x-auto px-5 lg:px-8">

        <nav className="flex min-w-max items-center justify-center gap-7 py-4">

            <a
                href="#planning"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Planning
            </a>

            <a
                href="#investing"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Investing
            </a>

            <a
                href="#risk"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Risk
            </a>

            <a
                href="#decisions"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Decisions
            </a>

            <a
                href="#basics"
                className="text-sm font-semibold text-slate-500 transition hover:text-navy-900"
            >
                Basics
            </a>

        </nav>

    </div>

</section>




<section className="py-24 lg:py-32">

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">


        <div className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">

            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    Start here
                </p>

                <h2 className="mt-3 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    Financial thinking, explained simply.
                </h2>

            </div>


            <p className="max-w-md text-sm leading-6 text-slate-500">
                Start with the concepts that influence the biggest financial
                decisions in your life.
            </p>

        </div>


        <div
            id="articleGrid"
            className="mt-12 grid gap-5 lg:grid-cols-3"
        >


            

            <article
                className="article-card article-item rounded-[24px] border border-slate-200 bg-white p-7 shadow-card"
                data-search="financial planning financial plan goals money planning basics"
            >

                <div className="flex items-center justify-between">

                    <span className="rounded-lg bg-teal-50 px-2.5 py-1.5 text-xs font-bold text-teal-700">
                        Planning
                    </span>

                    <span className="text-xs text-slate-400">
                        8 min read
                    </span>

                </div>


                <h3 className="mt-6 text-2xl font-bold tracking-tight text-navy-900">
                    What is financial planning?
                </h3>


                <p className="mt-4 text-sm leading-7 text-slate-500">
                    Understand how your income, expenses, assets, liabilities,
                    goals, investments and protection fit into one financial picture.
                </p>


                <a
                    href="#planning"
                    className="mt-7 inline-flex items-center gap-2 text-sm font-bold text-navy-900"
                >
                    Read the basics
                    <span>→</span>
                </a>

            </article>


            

            <article
                className="article-card article-item rounded-[24px] border border-slate-200 bg-white p-7 shadow-card"
                data-search="investing investment products asset allocation portfolio risk return"
            >

                <div className="flex items-center justify-between">

                    <span className="rounded-lg bg-navy-900 px-2.5 py-1.5 text-xs font-bold text-white">
                        Investing
                    </span>

                    <span className="text-xs text-slate-400">
                        10 min read
                    </span>

                </div>


                <h3 className="mt-6 text-2xl font-bold tracking-tight text-navy-900">
                    Why investment planning comes before product selection
                </h3>


                <p className="mt-4 text-sm leading-7 text-slate-500">
                    Learn why the purpose, time horizon, risk and role of an
                    investment should be understood before choosing a product.
                </p>


                <a
                    href="#investing"
                    className="mt-7 inline-flex items-center gap-2 text-sm font-bold text-navy-900"
                >
                    Read the basics
                    <span>→</span>
                </a>

            </article>


            

            <article
                className="article-card article-item rounded-[24px] border border-slate-200 bg-white p-7 shadow-card"
                data-search="risk risk capacity risk tolerance investment volatility financial risk"
            >

                <div className="flex items-center justify-between">

                    <span className="rounded-lg bg-slate-100 px-2.5 py-1.5 text-xs font-bold text-navy-900">
                        Risk
                    </span>

                    <span className="text-xs text-slate-400">
                        9 min read
                    </span>

                </div>


                <h3 className="mt-6 text-2xl font-bold tracking-tight text-navy-900">
                    Risk capacity vs risk tolerance
                </h3>


                <p className="mt-4 text-sm leading-7 text-slate-500">
                    Understand why financial ability to absorb risk and personal
                    willingness to take risk are not necessarily the same thing.
                </p>


                <a
                    href="#risk"
                    className="mt-7 inline-flex items-center gap-2 text-sm font-bold text-navy-900"
                >
                    Read the basics
                    <span>→</span>
                </a>

            </article>

        </div>


        <div
            id="noResults"
            className="mt-8 hidden rounded-2xl border border-slate-200 bg-white p-8 text-center"
        >

            <p className="font-bold text-navy-900">
                No matching topics found.
            </p>

            <p className="mt-2 text-sm text-slate-500">
                Try searching for planning, investing, risk or decisions.
            </p>

        </div>

    </div>

</section>




<section
    id="planning"
    className="scroll-mt-32 bg-white py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">

        <div className="grid gap-14 lg:grid-cols-[0.8fr_1.2fr]">


            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    Planning
                </p>


                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    See the whole financial picture.
                </h2>


                <p className="mt-5 text-lg leading-8 text-slate-600">
                    Financial planning is not only about investments. It brings
                    the important parts of your financial life together so that
                    decisions can be considered in context.
                </p>


                <a
                    href="/plan"
                    className="mt-8 inline-flex items-center gap-2 text-sm font-bold text-navy-900"
                >
                    Explore financial planning
                    <span>→</span>
                </a>

            </div>


            <div className="grid gap-4 sm:grid-cols-2">


                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6">

                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Concept
                    </p>

                    <h3 className="mt-4 font-bold text-navy-900">
                        Financial health
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        Understand income, expenses, assets, liabilities,
                        liquidity and financial position.
                    </p>

                </div>


                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6">

                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Concept
                    </p>

                    <h3 className="mt-4 font-bold text-navy-900">
                        Financial goals
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        Define what your money needs to accomplish and when.
                    </p>

                </div>


                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6">

                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Concept
                    </p>

                    <h3 className="mt-4 font-bold text-navy-900">
                        Cash flow
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        Understand how current income and spending affect future choices.
                    </p>

                </div>


                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6">

                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
                        Concept
                    </p>

                    <h3 className="mt-4 font-bold text-navy-900">
                        Net worth
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                        See the relationship between what you own and what you owe.
                    </p>

                </div>

            </div>

        </div>

    </div>

</section>




<section
    id="investing"
    className="scroll-mt-32 py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">


        <div className="max-w-3xl">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                Investing
            </p>


            <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                Understand what your investments are supposed to do.
            </h2>


            <p className="mt-5 text-lg leading-8 text-slate-600">
                An investment should have a role within the financial plan.
                Learn the basic concepts behind asset allocation, portfolio
                construction, risk and investment selection.
            </p>

        </div>


        <div className="mt-14 grid gap-5 md:grid-cols-2 lg:grid-cols-4">


            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-navy-900 text-white">

                    <span className="text-sm font-extrabold">
                        01
                    </span>

                </div>

                <h3 className="mt-6 font-bold text-navy-900">
                    Asset allocation
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    Understand why portfolios may combine assets with different characteristics.
                </p>

            </div>


            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-teal-50 text-teal-700">

                    <span className="text-sm font-extrabold">
                        02
                    </span>

                </div>

                <h3 className="mt-6 font-bold text-navy-900">
                    Time horizon
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    Understand how the time available can affect investment decisions.
                </p>

            </div>


            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-100 text-navy-900">

                    <span className="text-sm font-extrabold">
                        03
                    </span>

                </div>

                <h3 className="mt-6 font-bold text-navy-900">
                    Volatility
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    Learn why investment values can fluctuate and why that matters.
                </p>

            </div>


            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-card">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-100 text-navy-900">

                    <span className="text-sm font-extrabold">
                        04
                    </span>

                </div>

                <h3 className="mt-6 font-bold text-navy-900">
                    Portfolio fit
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                    A product should be considered in relation to the rest of your portfolio.
                </p>

            </div>

        </div>


        <div className="mt-8">

            <a
                href="/invest"
                className="inline-flex items-center gap-2 rounded-xl bg-navy-900 px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-navy-800"
            >
                Explore Investment Planning
                <span>→</span>
            </a>

        </div>

    </div>

</section>




<section
    id="risk"
    className="scroll-mt-32 bg-white py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">


        <div className="grid gap-14 lg:grid-cols-2 lg:items-center">


            <div>

                <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                    Risk
                </p>


                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                    Risk is a financial concept, not just a feeling.
                </h2>


                <p className="mt-5 text-lg leading-8 text-slate-600">
                    Your reaction to market uncertainty matters, but so does
                    your actual financial ability to absorb adverse outcomes.
                </p>


                <a
                    href="/invest#risk"
                    className="mt-8 inline-flex items-center gap-2 text-sm font-bold text-navy-900"
                >
                    Explore risk in investment planning
                    <span>→</span>
                </a>

            </div>


            <div className="rounded-[28px] border border-slate-200 bg-slate-50 p-6 sm:p-8">


                <div className="space-y-6">


                    <div>

                        <div className="flex items-center justify-between">

                            <h3 className="font-bold text-navy-900">
                                Risk capacity
                            </h3>

                            <span className="text-xs font-bold text-teal-700">
                                Ability
                            </span>

                        </div>

                        <p className="mt-2 text-sm leading-6 text-slate-500">
                            The financial ability to absorb losses or uncertainty.
                        </p>

                    </div>


                    <div className="h-px bg-slate-200"></div>


                    <div>

                        <div className="flex items-center justify-between">

                            <h3 className="font-bold text-navy-900">
                                Risk tolerance
                            </h3>

                            <span className="text-xs font-bold text-teal-700">
                                Willingness
                            </span>

                        </div>

                        <p className="mt-2 text-sm leading-6 text-slate-500">
                            The degree of uncertainty or volatility a person is willing to accept.
                        </p>

                    </div>


                    <div className="h-px bg-slate-200"></div>


                    <div>

                        <div className="flex items-center justify-between">

                            <h3 className="font-bold text-navy-900">
                                Risk requirement
                            </h3>

                            <span className="text-xs font-bold text-teal-700">
                                Goal
                            </span>

                        </div>

                        <p className="mt-2 text-sm leading-6 text-slate-500">
                            The level of risk associated with pursuing a particular financial outcome.
                        </p>

                    </div>


                </div>

            </div>

        </div>

    </div>

</section>




<section
    id="decisions"
    className="scroll-mt-32 py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">


        <div className="max-w-3xl">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                Decisions
            </p>


            <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                Better decisions start with better questions.
            </h2>


            <p className="mt-5 text-lg leading-8 text-slate-600">
                Instead of asking only which product is best, understand the
                financial problem, available alternatives, constraints and
                consequences.
            </p>

        </div>


        <div className="mt-14 grid gap-5 lg:grid-cols-3">


            <article className="rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

                <div className="text-xs font-bold uppercase tracking-wider text-teal-700">
                    Question 01
                </div>

                <h3 className="mt-5 text-xl font-bold text-navy-900">
                    What am I trying to achieve?
                </h3>

                <p className="mt-3 text-sm leading-7 text-slate-500">
                    Start with the financial outcome rather than the product.
                </p>

            </article>


            <article className="rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

                <div className="text-xs font-bold uppercase tracking-wider text-teal-700">
                    Question 02
                </div>

                <h3 className="mt-5 text-xl font-bold text-navy-900">
                    What are my alternatives?
                </h3>

                <p className="mt-3 text-sm leading-7 text-slate-500">
                    A financial decision can have several possible approaches.
                </p>

            </article>


            <article className="rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

                <div className="text-xs font-bold uppercase tracking-wider text-teal-700">
                    Question 03
                </div>

                <h3 className="mt-5 text-xl font-bold text-navy-900">
                    What changes if I choose each one?
                </h3>

                <p className="mt-3 text-sm leading-7 text-slate-500">
                    Understand the trade-offs before selecting an approach.
                </p>

            </article>

        </div>


        <div className="mt-8">

            <a
                href="/decide"
                className="inline-flex items-center gap-2 rounded-xl bg-navy-900 px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-navy-800"
            >
                Explore Financial Decisions
                <span>→</span>
            </a>

        </div>

    </div>

</section>




<section
    id="basics"
    className="scroll-mt-32 bg-white py-24 lg:py-32"
>

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">


        <div className="text-center">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                Financial basics
            </p>


            <h2 className="mx-auto mt-4 max-w-3xl text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                Start with the numbers that describe your financial life.
            </h2>

        </div>


        <div className="mx-auto mt-14 grid max-w-5xl gap-4 sm:grid-cols-2 lg:grid-cols-4">


            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6">

                <p className="text-3xl font-extrabold text-navy-900">
                    Income
                </p>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Money coming into your financial life.
                </p>

            </div>


            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6">

                <p className="text-3xl font-extrabold text-navy-900">
                    Expenses
                </p>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Money required to maintain your current lifestyle and obligations.
                </p>

            </div>


            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6">

                <p className="text-3xl font-extrabold text-navy-900">
                    Assets
                </p>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Things of financial value that you own.
                </p>

            </div>


            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6">

                <p className="text-3xl font-extrabold text-navy-900">
                    Liabilities
                </p>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Financial obligations that you owe.
                </p>

            </div>

        </div>


        <div className="mx-auto mt-10 max-w-3xl rounded-2xl border border-teal-100 bg-teal-50 p-6 text-center">

            <p className="text-sm leading-7 text-slate-600">
                These basic elements provide the starting context for many
                financial planning and decision-making questions.
            </p>

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
                    Put knowledge into context
                </p>


                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-white sm:text-5xl">
                    Understanding is the first step. Planning comes next.
                </h2>


                <p className="mt-5 max-w-2xl text-base leading-7 text-slate-300">
                    Bring your financial position, goals, investments and
                    protection together and start building your financial plan.
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
                            className="transition hover:text-navy-900"
                        >
                            Decide
                        </a>
                    </li>

                    <li>
                        <a
                            href="/learn"
                            className="font-semibold text-navy-900"
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
