"use client";

import { useState } from "react";
import { useMobileMenuClose } from "../../hooks/useMobileMenuClose";

export default function TermsPage() {
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
                Terms &amp; Conditions
            </h1>


            <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-600">
                The terms that govern your use of the Planvesto website
                and platform.
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


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    1. Acceptance of these terms
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    By accessing or using the Planvesto website, applications
                    or platform, you agree to comply with these Terms &
                    Conditions and any additional terms that may apply to
                    specific services.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    If you do not agree with these terms, you should not use
                    the applicable Planvesto services.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    2. About Planvesto
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Planvesto provides a financial planning and decision
                    platform intended to help users organise financial
                    information, understand goals, evaluate financial
                    considerations and make more informed decisions.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    The specific functionality available to you may depend
                    on the product, service, account or version of the
                    platform that you use.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    3. Financial information and decisions
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Financial planning involves assumptions, estimates,
                    changing circumstances and information supplied by the
                    user. You remain responsible for reviewing information
                    entered into the platform and for decisions you make
                    based on your circumstances.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Planvesto does not represent that any financial outcome,
                    return, goal or projection is guaranteed unless a
                    specific product or service expressly provides otherwise.
                </p>


                <div className="mt-6 rounded-2xl border border-teal-100 bg-teal-50 p-5">

                    <p className="text-sm leading-7 text-slate-600">
                        Information presented through the platform should be
                        considered in the context in which it is provided.
                        It should not automatically be interpreted as a
                        promise of future financial performance.
                    </p>

                </div>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    4. User accounts
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Some Planvesto functionality may require an account.
                    You are responsible for maintaining the confidentiality
                    of your account credentials and for activity carried
                    out through your account.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    You should provide accurate information and update it
                    when necessary so that your financial planning experience
                    remains based on reasonably current information.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    5. Acceptable use
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    You agree not to misuse the Planvesto website or platform,
                    interfere with its operation, attempt unauthorised access,
                    introduce malicious code or use the service in a manner
                    that violates applicable law.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    You may not copy, reproduce, modify, distribute or exploit
                    Planvesto content or functionality except where expressly
                    permitted.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    6. Intellectual property
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Unless otherwise stated, the Planvesto name, branding,
                    website design, software, content, graphics and other
                    materials are owned by or licensed to Planvesto and are
                    protected by applicable intellectual property laws.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Use of the platform does not transfer ownership of these
                    rights to the user.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    7. Third-party services
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Planvesto may rely on third-party services, information
                    sources or integrations to provide certain functionality.
                    Third-party services may be governed by their own terms
                    and privacy policies.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Planvesto is not responsible for the independent operation
                    or policies of third-party services outside its control.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    8. Availability and changes
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Planvesto may update, modify, suspend or discontinue
                    portions of the website or platform from time to time.
                    Features may also change as the product develops.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Reasonable efforts may be made to maintain availability,
                    but continuous or uninterrupted access cannot be guaranteed.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    9. Disclaimers
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    The website and platform are provided subject to the
                    terms and limitations applicable to the relevant service.
                    Information may depend on user inputs, assumptions,
                    external information and changing market or personal
                    circumstances.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    To the extent permitted by applicable law, Planvesto does
                    not guarantee that information will always be complete,
                    current, error-free or suitable for every individual's
                    circumstances.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    10. Limitation of liability
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    To the maximum extent permitted by applicable law,
                    Planvesto will not be responsible for losses arising
                    from matters outside its reasonable control or from
                    decisions made by a user based on incomplete, inaccurate
                    or outdated information supplied by the user or another
                    source.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Nothing in these terms is intended to exclude or limit
                    liability where such exclusion or limitation is prohibited
                    by applicable law.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    11. Suspension or termination
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Planvesto may restrict, suspend or terminate access where
                    reasonably necessary to protect the platform, users,
                    service providers or other parties, including where
                    these terms have been breached.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Users may stop using the platform at any time, subject
                    to any applicable contractual obligations.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    12. Changes to these terms
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    These Terms &amp; Conditions may be updated from time to time.
                    The latest version will be published on this page with
                    its applicable update date.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Continued use of the applicable services after an update
                    may constitute acceptance of the revised terms to the
                    extent permitted by applicable law.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    13. Governing law
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    These terms and the relationship between you and Planvesto
                    will be subject to the applicable laws and jurisdiction
                    specified in the final legally approved version of these
                    terms.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    14. Contact
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    If you have questions about these Terms &amp; Conditions,
                    contact Planvesto.
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
                    and replaced with Planvesto's legally approved Terms &
                    Conditions before publication.
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
                    className="font-semibold text-navy-900"
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
