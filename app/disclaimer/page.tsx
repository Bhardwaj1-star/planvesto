"use client";

import { useState } from "react";
import { useMobileMenuClose } from "../../hooks/useMobileMenuClose";

export default function DisclaimerPage() {
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
                href="/login"
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
                        href="/login"
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

    <div className="absolute inset-x-0 top-0 -z-10 h-[480px] bg-gradient-to-b from-teal-50/80 to-transparent"></div>


    <div className="mx-auto max-w-[1200px] px-5 pb-20 lg:px-8 lg:pb-24">

        <div className="mx-auto max-w-4xl text-center">


            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-teal-100 bg-teal-50 px-3.5 py-2">

                <span className="h-2 w-2 rounded-full bg-teal-600"></span>

                <span className="text-xs font-semibold tracking-wide text-teal-700">
                    Legal
                </span>

            </div>


            <h1 className="text-5xl font-extrabold leading-[1.06] tracking-[-0.04em] text-navy-900 sm:text-6xl">
                Disclaimer
            </h1>


            <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-600">
                Important information about the nature and limitations of
                information provided through Planvesto.
            </p>


            <p className="mt-5 text-sm font-medium text-slate-400">
                Last updated: August 30, 2026
            </p>

        </div>

    </div>

</section>




<section className="pb-24 lg:pb-32">

    <div className="mx-auto max-w-[1000px] px-5 lg:px-8">


        <div className="rounded-[28px] border border-slate-200 bg-white p-7 shadow-sm sm:p-10 lg:p-14">


            

            <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6">

                <div className="flex gap-4">

                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-amber-100 text-amber-700">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >

                            <path
                                d="M12 8v4"
                                strokeWidth="2"
                                strokeLinecap="round" />

                            <circle
                                cx="12"
                                cy="16"
                                r="1"
                                fill="currentColor" />

                            <path
                                d="M10.3 4.5L3.1 17a2 2 0 001.7 3h14.4a2 2 0 001.7-3L13.7 4.5a2 2 0 00-3.4 0z"
                                strokeWidth="1.8"
                                strokeLinejoin="round" />

                        </svg>

                    </div>


                    <div>

                        <h2 className="font-bold text-amber-800">
                            Important
                        </h2>


                        <p className="mt-2 text-sm leading-6 text-slate-600">
                            Financial decisions involve risk and depend on
                            individual circumstances. Information available
                            through Planvesto should not be understood as a
                            guarantee of future financial outcomes.
                        </p>

                    </div>

                </div>

            </div>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    1. General information
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    The Planvesto website and platform may provide educational,
                    analytical, planning and informational content relating
                    to personal finance, investments, financial goals,
                    protection and related subjects.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Such information is intended to support understanding
                    and financial planning. It should be considered together
                    with the user's own circumstances and other relevant
                    information.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    2. No guarantee of financial outcomes
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Financial markets, investments, interest rates, inflation,
                    taxation and personal circumstances can change over time.
                    Past performance does not necessarily indicate future results.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Any projections, illustrations, calculations or scenarios
                    presented through Planvesto are subject to the assumptions
                    used and may differ materially from actual outcomes.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    3. Personal circumstances matter
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    A financial strategy that may be appropriate in one
                    situation may not be appropriate in another. Financial
                    decisions can depend on income, expenses, assets,
                    liabilities, goals, time horizon, liquidity needs,
                    risk considerations, taxation and many other factors.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Users should consider whether information is appropriate
                    for their own circumstances before acting on it.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    4. Investment risk
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Investments can involve loss of capital, fluctuations in
                    value, liquidity constraints, market risk, credit risk,
                    interest-rate risk, inflation risk and other forms of risk.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    The presence of an investment or strategy on the Planvesto
                    platform does not mean that it is risk-free or suitable
                    for every investor.
                </p>


                <div className="mt-6 rounded-2xl border border-slate-200 bg-slate-50 p-5">

                    <p className="text-sm font-semibold leading-6 text-navy-900">
                        There is no universal investment that is appropriate
                        for every financial situation.
                    </p>

                </div>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    5. Illustrations and calculations
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Calculations displayed by Planvesto may rely on assumptions
                    such as expected returns, inflation, time periods,
                    contributions, withdrawals or other user-provided values.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Changing one or more assumptions can materially change
                    the resulting illustration. An illustration should
                    therefore not be treated as a prediction of an actual
                    financial result.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    6. Product information
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Where Planvesto provides information about financial
                    products or investment options, the information may be
                    provided for comparison, planning or educational purposes.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Product features, costs, taxation, eligibility, terms and
                    other characteristics may change. Users should review
                    current official product documentation before making
                    a transaction.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    7. Tax information
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Tax treatment can depend on individual circumstances and
                    applicable laws, regulations and interpretations.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Tax information presented through Planvesto should not
                    be treated as a substitute for advice from an appropriately
                    qualified tax professional.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    8. Third-party information
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Planvesto may display information obtained from external
                    sources. While reasonable efforts may be made to use
                    reliable information, Planvesto cannot guarantee that
                    every external data point will always be complete,
                    accurate or current.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    9. User-provided information
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Financial planning results can be affected by information
                    supplied by the user. Incorrect, incomplete or outdated
                    information can produce results that do not accurately
                    reflect the user's actual circumstances.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Users are responsible for reviewing the information they
                    enter and correcting it when circumstances change.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    10. Professional advice
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    The nature of the services available through Planvesto
                    will determine whether a particular interaction is
                    educational information, financial planning, product
                    information or regulated financial advice.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Where professional or regulated advice is required,
                    users should rely on the appropriately authorised or
                    qualified professional responsible for providing that service.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    11. No assurance of completeness
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Financial planning is broader than any single calculation,
                    recommendation, product comparison or platform output.
                    Planvesto cannot represent that every possible factor
                    relevant to an individual's circumstances will always
                    be identified through the platform.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    12. Changes to this disclaimer
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    This Disclaimer may be updated from time to time to reflect
                    changes in Planvesto's services, platform functionality or
                    applicable requirements.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    13. Contact
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    If you have questions about this Disclaimer or the
                    information provided through Planvesto, contact us.
                </p>


                <a
                    href="/contact"
                    className="mt-6 inline-flex items-center gap-2 rounded-xl bg-navy-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-navy-800"
                >
                    Contact Planvesto
                    <span>→</span>
                </a>

            </section>


            

            <div className="mt-12 rounded-2xl border border-amber-200 bg-amber-50 p-5">

                <p className="text-xs font-bold uppercase tracking-wider text-amber-700">
                    Legal review required
                </p>


                <p className="mt-2 text-sm leading-6 text-slate-600">
                    This page is a frontend template and should be reviewed
                    and replaced with Planvesto's legally approved Disclaimer
                    before publication.
                </p>

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
                    className="font-semibold text-navy-900"
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
