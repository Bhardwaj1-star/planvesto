"use client";

import { useState } from "react";
import { useMobileMenuClose } from "../../hooks/useMobileMenuClose";
import { useContactForm } from "../../hooks/useContactForm";

export default function ContactPage() {
  const [menuOpen, setMenuOpen] = useState(false);

  useMobileMenuClose(setMenuOpen);
  useContactForm();

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

    <div className="absolute inset-x-0 top-0 -z-10 h-[560px] bg-gradient-to-b from-teal-50/80 to-transparent"></div>


    <div className="mx-auto max-w-[1200px] px-5 pb-20 lg:px-8 lg:pb-28">


        <div className="mx-auto max-w-4xl text-center">


            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-teal-100 bg-teal-50 px-3.5 py-2">

                <span className="h-2 w-2 rounded-full bg-teal-600"></span>

                <span className="text-xs font-semibold tracking-wide text-teal-700">
                    Contact Planvesto
                </span>

            </div>


            <h1 className="text-5xl font-extrabold leading-[1.06] tracking-[-0.04em] text-navy-900 sm:text-6xl">

                Have a question?

                <span className="gradient-text">
                    Let's talk.
                </span>

            </h1>


            <p className="mx-auto mt-7 max-w-2xl text-lg leading-8 text-slate-600">
                Whether you have a question about Planvesto, financial
                planning or the platform, send us a message and we'll help
                you find the right information.
            </p>

        </div>

    </div>

</section>




<section className="relative -mt-2 pb-24 lg:pb-32">

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">


        <div className="grid gap-6 lg:grid-cols-[0.75fr_1.25fr]">


            

            <div className="space-y-5">


                <div className="contact-card rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-teal-50 text-teal-700">

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


                    <h2 className="mt-6 text-xl font-bold text-navy-900">
                        Questions about Planvesto?
                    </h2>


                    <p className="mt-3 text-sm leading-7 text-slate-500">
                        Ask us about the platform, how it works, financial
                        planning or anything else you want to understand.
                    </p>


                    <a
                        href="#contact-form"
                        className="mt-6 inline-flex items-center gap-2 text-sm font-bold text-navy-900"
                    >
                        Send a message
                        <span>→</span>
                    </a>

                </div>


                <div className="contact-card rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-100 text-navy-900">

                        <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >

                            <path
                                d="M4 6h16v12H4z"
                                strokeWidth="1.8"
                                strokeLinejoin="round" />

                            <path
                                d="M4 7l8 6 8-6"
                                strokeWidth="1.8"
                                strokeLinejoin="round" />

                        </svg>

                    </div>


                    <h2 className="mt-6 text-xl font-bold text-navy-900">
                        General enquiries
                    </h2>


                    <p className="mt-3 text-sm leading-7 text-slate-500">
                        For general questions, partnership enquiries or
                        information about Planvesto.
                    </p>


                    <p className="mt-5 text-sm font-semibold text-navy-900">
                        hello@planvesto.com
                    </p>

                </div>


                <div className="contact-card rounded-[24px] border border-slate-200 bg-white p-7 shadow-card">

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
                                r="8"
                                strokeWidth="1.8" />

                            <path
                                d="M12 8v4l3 2"
                                strokeWidth="1.8"
                                strokeLinecap="round" />

                        </svg>

                    </div>


                    <h2 className="mt-6 text-xl font-bold text-navy-900">
                        Need help getting started?
                    </h2>


                    <p className="mt-3 text-sm leading-7 text-slate-500">
                        Start your financial planning journey directly from
                        the platform.
                    </p>


                    <a
                        href="/login"
                        className="mt-6 inline-flex items-center gap-2 rounded-xl bg-navy-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-navy-800"
                    >
                        Start Planning
                        <span>→</span>
                    </a>

                </div>

            </div>


            

            <div
                id="contact-form"
                className="scroll-mt-28 rounded-[28px] border border-slate-200 bg-white p-6 shadow-soft sm:p-8 lg:p-10"
            >


                <div>

                    <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                        Send us a message
                    </p>


                    <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-navy-900">
                        How can we help?
                    </h2>


                    <p className="mt-3 text-sm leading-6 text-slate-500">
                        Fill in the form below and provide enough detail for
                        us to understand your question.
                    </p>

                </div>


                <form
                    id="contactForm"
                    className="mt-8 space-y-6"
                    noValidate
                >


                    

                    <div>

                        <label
                            htmlFor="name"
                            className="mb-2 block text-sm font-semibold text-navy-900"
                        >
                            Full name
                        </label>


                        <input
                            id="name"
                            name="name"
                            type="text"
                            autoComplete="name"
                            required
                            className="form-field w-full rounded-xl border border-slate-200 bg-white px-4 py-3.5 text-sm text-navy-900 placeholder:text-slate-400"
                            placeholder="Your name" />


                        <p
                            id="nameError"
                            className="mt-2 hidden text-xs font-medium text-red-600"
                        >
                            Please enter your name.
                        </p>

                    </div>


                    

                    <div>

                        <label
                            htmlFor="email"
                            className="mb-2 block text-sm font-semibold text-navy-900"
                        >
                            Email address
                        </label>


                        <input
                            id="email"
                            name="email"
                            type="email"
                            autoComplete="email"
                            required
                            className="form-field w-full rounded-xl border border-slate-200 bg-white px-4 py-3.5 text-sm text-navy-900 placeholder:text-slate-400"
                            placeholder="you@example.com" />


                        <p
                            id="emailError"
                            className="mt-2 hidden text-xs font-medium text-red-600"
                        >
                            Please enter a valid email address.
                        </p>

                    </div>


                    

                    <div>

                        <label
                            htmlFor="topic"
                            className="mb-2 block text-sm font-semibold text-navy-900"
                        >
                            What is your question about?
                        </label>


                        <select
                            id="topic"
                            name="topic"
                            required
                            className="form-field w-full appearance-none rounded-xl border border-slate-200 bg-white px-4 py-3.5 text-sm text-navy-900"
                        >

                            <option value="">
                                Select a topic
                            </option>

                            <option value="financial-planning">
                                Financial Planning
                            </option>

                            <option value="investment-planning">
                                Investment Planning
                            </option>

                            <option value="risk">
                                Risk & Protection
                            </option>

                            <option value="platform">
                                Planvesto Platform
                            </option>

                            <option value="partnership">
                                Partnership
                            </option>

                            <option value="other">
                                Other
                            </option>

                        </select>


                        <p
                            id="topicError"
                            className="mt-2 hidden text-xs font-medium text-red-600"
                        >
                            Please select a topic.
                        </p>

                    </div>


                    

                    <div>

                        <label
                            htmlFor="message"
                            className="mb-2 block text-sm font-semibold text-navy-900"
                        >
                            Message
                        </label>


                        <textarea
                            id="message"
                            name="message"
                            rows={6}
                            required
                            className="form-field w-full resize-none rounded-xl border border-slate-200 bg-white px-4 py-3.5 text-sm leading-6 text-navy-900 placeholder:text-slate-400"
                            placeholder="Tell us what you'd like to know..."
                        ></textarea>


                        <p
                            id="messageError"
                            className="mt-2 hidden text-xs font-medium text-red-600"
                        >
                            Please enter your message.
                        </p>

                    </div>


                    

                    <div className="flex items-start gap-3">

                        <input
                            id="consent"
                            name="consent"
                            type="checkbox"
                            required
                            className="mt-1 h-4 w-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500" />


                        <label
                            htmlFor="consent"
                            className="text-xs leading-5 text-slate-500"
                        >
                            I agree that Planvesto may use the information
                            submitted here to respond to my enquiry.
                        </label>

                    </div>


                    <p
                        id="consentError"
                        className="hidden text-xs font-medium text-red-600"
                    >
                        Please confirm before submitting.
                    </p>


                    

                    <button
                        id="submitButton"
                        type="submit"
                        className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-navy-900 px-6 py-3.5 text-sm font-bold text-white transition hover:bg-navy-800 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                        Send Message
                        <span>→</span>
                    </button>


                    

                    <div
                        id="successMessage"
                        className="hidden rounded-xl border border-teal-100 bg-teal-50 p-4"
                    >

                        <p className="text-sm font-bold text-teal-700">
                            Message ready to send.
                        </p>

                        <p className="mt-1 text-xs leading-5 text-slate-600">
                            Your enquiry has passed the form checks. Connect
                            this form to the Planvesto backend or email service
                            to complete delivery.
                        </p>

                    </div>

                </form>

            </div>

        </div>

    </div>

</section>




<section className="border-y border-slate-200 bg-white py-24 lg:py-32">

    <div className="mx-auto max-w-[1000px] px-5 lg:px-8">


        <div className="text-center">

            <p className="text-sm font-bold uppercase tracking-widest text-teal-700">
                Frequently asked
            </p>


            <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-navy-900 sm:text-5xl">
                Before you contact us.
            </h2>

        </div>


        <div className="mt-12 space-y-3">


            <details
                className="group rounded-2xl border border-slate-200 bg-slate-50"
            >

                <summary
                    className="flex cursor-pointer list-none items-center justify-between gap-5 px-6 py-5"
                >

                    <span className="text-sm font-bold text-navy-900">
                        What is Planvesto?
                    </span>

                    <span className="text-xl text-slate-400 transition group-open:rotate-45">
                        +
                    </span>

                </summary>


                <div className="border-t border-slate-200 px-6 py-5">

                    <p className="text-sm leading-7 text-slate-500">
                        Planvesto is a financial planning and decision platform
                        designed to connect financial position, goals,
                        investments, protection and financial decisions.
                    </p>

                </div>

            </details>


            <details
                className="group rounded-2xl border border-slate-200 bg-slate-50"
            >

                <summary
                    className="flex cursor-pointer list-none items-center justify-between gap-5 px-6 py-5"
                >

                    <span className="text-sm font-bold text-navy-900">
                        Does Planvesto start with investment products?
                    </span>

                    <span className="text-xl text-slate-400 transition group-open:rotate-45">
                        +
                    </span>

                </summary>


                <div className="border-t border-slate-200 px-6 py-5">

                    <p className="text-sm leading-7 text-slate-500">
                        The public-facing approach begins with the financial
                        situation, goals, constraints and decisions before
                        moving into product implementation.
                    </p>

                </div>

            </details>


            <details
                className="group rounded-2xl border border-slate-200 bg-slate-50"
            >

                <summary
                    className="flex cursor-pointer list-none items-center justify-between gap-5 px-6 py-5"
                >

                    <span className="text-sm font-bold text-navy-900">
                        Can I learn about financial planning without signing up?
                    </span>

                    <span className="text-xl text-slate-400 transition group-open:rotate-45">
                        +
                    </span>

                </summary>


                <div className="border-t border-slate-200 px-6 py-5">

                    <p className="text-sm leading-7 text-slate-500">
                        Yes. The Learn section provides educational material
                        about financial planning, investing, risk and
                        financial decisions.
                    </p>

                </div>

            </details>


            <details
                className="group rounded-2xl border border-slate-200 bg-slate-50"
            >

                <summary
                    className="flex cursor-pointer list-none items-center justify-between gap-5 px-6 py-5"
                >

                    <span className="text-sm font-bold text-navy-900">
                        How do I start using Planvesto?
                    </span>

                    <span className="text-xl text-slate-400 transition group-open:rotate-45">
                        +
                    </span>

                </summary>


                <div className="border-t border-slate-200 px-6 py-5">

                    <p className="text-sm leading-7 text-slate-500">
                        Use the Start Planning or Login buttons to enter the
                        product experience.
                    </p>

                </div>

            </details>


        </div>

    </div>

</section>




<section className="py-24 lg:py-32">

    <div className="mx-auto max-w-[1200px] px-5 lg:px-8">


        <div className="relative overflow-hidden rounded-[32px] bg-navy-900 px-7 py-14 sm:px-12 lg:px-16 lg:py-16">


            <div className="absolute -right-20 -top-20 h-72 w-72 rounded-full bg-teal-500/10 blur-3xl"></div>


            <div className="relative max-w-3xl">

                <p className="text-sm font-bold uppercase tracking-widest text-teal-300">
                    Ready to begin?
                </p>


                <h2 className="mt-4 text-4xl font-extrabold tracking-[-0.03em] text-white sm:text-5xl">
                    Start with your financial picture.
                </h2>


                <p className="mt-5 max-w-2xl text-base leading-7 text-slate-300">
                    Understand your position, define your goals and begin
                    making financial decisions in context.
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
                        href="/learn"
                        className="inline-flex items-center justify-center rounded-xl border border-white/20 px-6 py-3.5 text-sm font-bold text-white transition hover:bg-white/10"
                    >
                        Learn First
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
                            className="transition hover:text-navy-900"
                        >
                            About Planvesto
                        </a>
                    </li>

                    <li>
                        <a
                            href="/contact"
                            className="font-semibold text-navy-900"
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
