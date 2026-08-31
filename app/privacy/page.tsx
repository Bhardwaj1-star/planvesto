"use client";

import { useState } from "react";
import { useMobileMenuClose } from "../../hooks/useMobileMenuClose";

export default function PrivacyPage() {
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
                Privacy Policy
            </h1>


            <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-600">
                How Planvesto handles information provided through its website
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
                    1. Introduction
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Planvesto respects the privacy of individuals who use its
                    website, applications and financial planning services.
                    This Privacy Policy explains the general categories of
                    information that may be collected, how that information
                    may be used and the choices available to users.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    By using the Planvesto website or platform, you acknowledge
                    that information may be handled as described in this policy.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    2. Information we may collect
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Depending on how you use Planvesto, information may include:
                </p>


                <ul className="mt-5 space-y-3 text-sm leading-7 text-slate-600">

                    <li className="flex gap-3">

                        <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600"></span>

                        <span>
                            Basic identification and contact information,
                            such as name and email address.
                        </span>

                    </li>


                    <li className="flex gap-3">

                        <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600"></span>

                        <span>
                            Information that you provide while using financial
                            planning features.
                        </span>

                    </li>


                    <li className="flex gap-3">

                        <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600"></span>

                        <span>
                            Information about your goals, preferences,
                            financial position or other information that you
                            voluntarily provide for planning purposes.
                        </span>

                    </li>


                    <li className="flex gap-3">

                        <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600"></span>

                        <span>
                            Technical information associated with your use of
                            the website or platform.
                        </span>

                    </li>

                </ul>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    3. How information may be used
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Information may be used to provide, operate and improve
                    Planvesto's services and user experience.
                </p>


                <ul className="mt-5 space-y-3 text-sm leading-7 text-slate-600">

                    <li className="flex gap-3">

                        <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600"></span>

                        <span>
                            To create and maintain your account.
                        </span>

                    </li>


                    <li className="flex gap-3">

                        <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600"></span>

                        <span>
                            To provide financial planning and related platform functionality.
                        </span>

                    </li>


                    <li className="flex gap-3">

                        <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600"></span>

                        <span>
                            To communicate with you regarding your account,
                            enquiries or requested services.
                        </span>

                    </li>


                    <li className="flex gap-3">

                        <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600"></span>

                        <span>
                            To maintain security, prevent misuse and protect
                            the integrity of the platform.
                        </span>

                    </li>


                    <li className="flex gap-3">

                        <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-teal-600"></span>

                        <span>
                            To improve the website, platform and services.
                        </span>

                    </li>

                </ul>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    4. Financial information
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Financial planning may require users to provide information
                    about income, expenses, assets, liabilities, investments,
                    goals, protection needs and other relevant circumstances.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Such information is used in connection with the financial
                    planning experience and related services for which it was
                    provided.
                </p>


                <div className="mt-6 rounded-2xl border border-teal-100 bg-teal-50 p-5">

                    <p className="text-sm leading-7 text-slate-600">
                        Users should provide only information that is reasonably
                        necessary for the intended financial planning purpose
                        and should keep account information accurate and current.
                    </p>

                </div>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    5. Information sharing
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Planvesto does not treat user information as public
                    information. Information may be shared with service
                    providers or other parties where necessary to operate
                    the platform, provide requested services, maintain
                    security, comply with applicable law or fulfil another
                    legitimate purpose.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Where third-party service providers are used, access to
                    information should be limited to what is reasonably
                    necessary for the relevant service.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    6. Data security
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Planvesto is intended to use reasonable technical and
                    organisational measures to protect information against
                    unauthorised access, misuse, alteration or disclosure.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    No internet-based system can guarantee absolute security.
                    Users should also take reasonable steps to protect their
                    passwords, devices and account credentials.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    7. Cookies and technical information
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Planvesto may use cookies, local storage or similar
                    technologies where necessary to operate the website,
                    remember preferences, understand usage and improve the
                    user experience.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Browser settings may allow you to control certain cookies.
                    Disabling some technologies may affect website functionality.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    8. Data retention
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Information may be retained for as long as reasonably
                    necessary for the purposes for which it was collected,
                    including account management, service delivery,
                    security, legal obligations and legitimate business purposes.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    9. Your choices and rights
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Depending on applicable law, you may have rights relating
                    to your personal information, including rights to request
                    access, correction, deletion or information about how your
                    information is processed.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    Requests can be made using the contact details provided
                    on the Planvesto website.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    10. Children's privacy
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    Planvesto's services are not intended to be used by
                    individuals where use would be prohibited by applicable
                    law. We do not knowingly seek to collect personal
                    information from children without appropriate legal
                    basis or consent where required.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    11. Changes to this policy
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    This Privacy Policy may be updated from time to time to
                    reflect changes in the Planvesto platform, applicable
                    requirements or the way information is handled.
                </p>


                <p className="mt-4 text-sm leading-7 text-slate-600">
                    The latest version will be made available on this page
                    together with the applicable update date.
                </p>

            </section>


            <div className="my-10 h-px bg-slate-200"></div>


            

            <section>

                <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">
                    12. Contact
                </h2>


                <p className="mt-5 text-sm leading-7 text-slate-600">
                    If you have questions about this Privacy Policy or how
                    your information is handled, contact Planvesto.
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
                    and replaced with Planvesto's legally approved Privacy
                    Policy before the website is published.
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
                    className="font-semibold text-navy-900"
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
