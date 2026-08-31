"use client";

import { useState } from "react";
import { useSignupForm } from "../../hooks/useSignupForm";

export default function SignupPage() {

  useSignupForm();

  return (
    <>


<header className="border-b border-slate-200 bg-white">

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


        <div className="text-sm text-slate-500">

            Already have an account?

            <a
                href="/login"
                className="font-bold text-navy-900 hover:text-teal-700"
            >
                Login
            </a>

        </div>

    </div>

</header>


<main className="signup-grid relative flex min-h-[calc(100vh-80px)] items-center overflow-hidden py-12 lg:py-20">


    

    <div className="pointer-events-none absolute left-1/2 top-0 h-[500px] w-[700px] -translate-x-1/2 rounded-full bg-teal-100/50 blur-3xl"></div>


    <div className="relative mx-auto w-full max-w-[1200px] px-5 lg:px-8">


        <div className="mx-auto max-w-[500px]">


            

            <div className="mb-8 text-center">


                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-navy-900">

                    <svg
                        className="h-6 w-6 text-white"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >

                        <path
                            d="M16 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2"
                            strokeWidth="1.8"
                            strokeLinecap="round"
                            strokeLinejoin="round" />

                        <circle
                            cx="9"
                            cy="7"
                            r="4"
                            strokeWidth="1.8" />

                        <path
                            d="M19 8v6M16 11h6"
                            strokeWidth="1.8"
                            strokeLinecap="round" />

                    </svg>

                </div>


                <h1 className="mt-6 text-3xl font-extrabold tracking-tight text-navy-900 sm:text-4xl">
                    Create your account
                </h1>


                <p className="mt-3 text-sm leading-6 text-slate-500">
                    Start building a clearer picture of your financial life.
                </p>

            </div>


            

            <div className="signup-card rounded-[28px] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">


                <form
                    id="signupForm"
                    noValidate
                    className="space-y-5"
                >


                    

                    <div>

                        <label
                            htmlFor="fullName"
                            className="mb-2 block text-sm font-semibold text-navy-900"
                        >
                            Full name
                        </label>


                        <input
                            id="fullName"
                            name="fullName"
                            type="text"
                            autoComplete="name"
                            required
                            className="form-field w-full rounded-xl border border-slate-200 bg-white px-4 py-3.5 text-sm text-navy-900 placeholder:text-slate-400"
                            placeholder="Your full name" />


                        <p
                            id="nameError"
                            className="mt-2 hidden text-xs font-medium text-red-600"
                        >
                            Please enter your full name.
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
                            Enter a valid email address.
                        </p>

                    </div>


                    

                    <div>

                        <label
                            htmlFor="password"
                            className="mb-2 block text-sm font-semibold text-navy-900"
                        >
                            Create password
                        </label>


                        <div className="relative">

                            <input
                                id="password"
                                name="password"
                                type="password"
                                autoComplete="new-password"
                                required
                                minLength={8}
                                className="form-field w-full rounded-xl border border-slate-200 bg-white px-4 py-3.5 pr-12 text-sm text-navy-900 placeholder:text-slate-400"
                                placeholder="At least 8 characters" />


                            <button
                                id="togglePassword"
                                type="button"
                                className="absolute right-3 top-1/2 -translate-y-1/2 rounded-lg p-2 text-slate-400 transition hover:text-navy-900"
                                aria-label="Show password"
                            >

                                <svg
                                    className="h-5 w-5"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >

                                    <path
                                        d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6z"
                                        strokeWidth="1.7"
                                        strokeLinejoin="round" />

                                    <circle
                                        cx="12"
                                        cy="12"
                                        r="2.5"
                                        strokeWidth="1.7" />

                                </svg>

                            </button>

                        </div>


                        

                        <div className="mt-3">

                            <div className="h-1.5 overflow-hidden rounded-full bg-slate-100">

                                <div
                                    id="strengthBar"
                                    className="password-strength-bar h-full w-0 rounded-full"
                                ></div>

                            </div>


                            <p
                                id="strengthText"
                                className="mt-2 text-xs text-slate-400"
                            >
                                Use at least 8 characters.
                            </p>

                        </div>


                        <p
                            id="passwordError"
                            className="mt-2 hidden text-xs font-medium text-red-600"
                        >
                            Password must contain at least 8 characters.
                        </p>

                    </div>


                    

                    <div>

                        <label
                            htmlFor="confirmPassword"
                            className="mb-2 block text-sm font-semibold text-navy-900"
                        >
                            Confirm password
                        </label>


                        <input
                            id="confirmPassword"
                            name="confirmPassword"
                            type="password"
                            autoComplete="new-password"
                            required
                            className="form-field w-full rounded-xl border border-slate-200 bg-white px-4 py-3.5 text-sm text-navy-900 placeholder:text-slate-400"
                            placeholder="Re-enter your password" />


                        <p
                            id="confirmError"
                            className="mt-2 hidden text-xs font-medium text-red-600"
                        >
                            Passwords do not match.
                        </p>

                    </div>


                    

                    <div className="flex items-start gap-3 pt-1">

                        <input
                            id="terms"
                            name="terms"
                            type="checkbox"
                            required
                            className="mt-1 h-4 w-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500" />


                        <label
                            htmlFor="terms"
                            className="text-xs leading-5 text-slate-500"
                        >
                            I agree to the Planvesto

                            <a
                                href="/terms"
                                className="font-semibold text-slate-700 hover:text-navy-900"
                            >
                                Terms &amp; Conditions
                            </a>

                            and

                            <a
                                href="/privacy"
                                className="font-semibold text-slate-700 hover:text-navy-900"
                            >
                                Privacy Policy
                            </a>.
                        </label>

                    </div>


                    <p
                        id="termsError"
                        className="hidden text-xs font-medium text-red-600"
                    >
                        Please accept the Terms &amp; Conditions.
                    </p>


                    

                    <button
                        id="createButton"
                        type="submit"
                        className="flex w-full items-center justify-center gap-2 rounded-xl bg-navy-900 px-6 py-3.5 text-sm font-bold text-white transition hover:bg-navy-800 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                        Create Account
                        <span>→</span>
                    </button>


                    

                    <div
                        id="successMessage"
                        className="hidden rounded-xl border border-teal-100 bg-teal-50 p-4"
                    >

                        <p className="text-sm font-bold text-teal-700">
                            Account form validated.
                        </p>


                        <p className="mt-1 text-xs leading-5 text-slate-600">
                            Connect this form to the Planvesto authentication
                            service to create the account.
                        </p>

                    </div>

                </form>


                

                <div className="mt-7 border-t border-slate-100 pt-6 text-center">

                    <p className="text-sm text-slate-500">

                        Already have an account?

                        <a
                            href="/login"
                            className="font-bold text-navy-900 hover:text-teal-700"
                        >
                            Login
                        </a>

                    </p>

                </div>


            </div>


            <p className="mt-6 text-center text-xs leading-5 text-slate-400">
                Your information is handled according to the
                <a
                    href="/privacy"
                    className="font-semibold text-slate-600 hover:text-navy-900"
                >
                    Planvesto Privacy Policy
                </a>.
            </p>

        </div>

    </div>

</main>



    </>
  );
}
