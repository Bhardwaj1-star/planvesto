"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useLoginForm } from "../../hooks/useLoginForm";

export default function LoginPage() {
  const { isSubmitting, errorMessage, showPassword, setShowPassword, submit } = useLoginForm();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [validationError, setValidationError] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!email.trim()) return setValidationError("Enter your email address.");
    if (!password) return setValidationError("Enter your password.");
    if (password.length < 6) return setValidationError("Password must contain at least 6 characters.");
    setValidationError("");
    await submit(email, password);
  };

  const message = validationError || errorMessage;

  return (
    <>
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex h-20 max-w-[1200px] items-center justify-between px-5 lg:px-8">
          <Link href="/" className="flex items-center gap-2.5" aria-label="Planvesto Home">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-900" aria-hidden="true">
              <svg className="h-5 w-5 text-white" viewBox="0 0 24 24" fill="none">
                <path d="M5 17L10 12L13 15L19 8" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M15 8H19V12" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <span className="text-xl font-extrabold tracking-tight text-navy-900">planvesto</span>
          </Link>
          <Link href="/contact" className="text-sm font-semibold text-slate-600 transition hover:text-navy-900">Need help?</Link>
        </div>
      </header>

      <main className="login-grid relative flex min-h-[calc(100vh-80px)] items-center overflow-hidden py-12 lg:py-20">
        <div className="pointer-events-none absolute left-1/2 top-0 h-[500px] w-[700px] -translate-x-1/2 rounded-full bg-teal-100/50 blur-3xl" aria-hidden="true" />
        <div className="relative mx-auto w-full max-w-[1200px] px-5 lg:px-8">
          <div className="mx-auto max-w-[460px]">
            <div className="mb-8 text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-navy-900" aria-hidden="true">
                <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="3" strokeWidth="1.8" />
                  <path d="M19.4 15a1.7 1.7 0 00.34 1.87l.06.06-1.7 1.7-.06-.06a1.7 1.7 0 00-1.87-.34 1.7 1.7 0 00-1.04 1.56V20h-2.4v-.21a1.7 1.7 0 00-1.04-1.56 1.7 1.7 0 00-1.87.34l-.06.06-1.7-1.7.06-.06A1.7 1.7 0 008.46 15a1.7 1.7 0 00-1.56-1.04H6.7v-2.4h.2A1.7 1.7 0 008.46 10a1.7 1.7 0 00-.34-1.87l-.06-.06 1.7-1.7.06.06a1.7 1.7 0 001.87.34 1.7 1.7 0 001.04-1.56V5h2.4v.21a1.7 1.7 0 001.04 1.56 1.7 1.7 0 001.87-.34l.06-.06 1.7 1.7-.06.06a1.7 1.7 0 00-.34 1.87 1.7 1.7 0 001.56 1.04h.21v2.4h-.21A1.7 1.7 0 0019.4 15z" strokeWidth="1.5" strokeLinejoin="round" />
                </svg>
              </div>
              <h1 className="mt-6 text-3xl font-extrabold tracking-tight text-navy-900 sm:text-4xl">Welcome back</h1>
              <p className="mt-3 text-sm leading-6 text-slate-500">Login to continue your financial planning journey.</p>
            </div>

            <div className="login-card rounded-[28px] border border-slate-200 bg-white p-6 shadow-soft sm:p-8">
              <form noValidate className="space-y-5" onSubmit={handleSubmit}>
                <div>
                  <label htmlFor="email" className="mb-2 block text-sm font-semibold text-navy-900">Email address</label>
                  <input id="email" name="email" type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} aria-invalid={Boolean(message)} className="form-field w-full rounded-xl border border-slate-200 bg-white px-4 py-3.5 text-sm text-navy-900 placeholder:text-slate-400" placeholder="you@example.com" />
                </div>

                <div>
                  <div className="mb-2 flex items-center justify-between">
                    <label htmlFor="password" className="block text-sm font-semibold text-navy-900">Password</label>
                    <Link href="/forgot-password" className="text-xs font-semibold text-teal-700 transition hover:text-navy-900">Forgot password?</Link>
                  </div>
                  <div className="relative">
                    <input id="password" name="password" type={showPassword ? "text" : "password"} autoComplete="current-password" minLength={6} value={password} onChange={(e) => setPassword(e.target.value)} aria-invalid={Boolean(message)} className="form-field w-full rounded-xl border border-slate-200 bg-white px-4 py-3.5 pr-12 text-sm text-navy-900 placeholder:text-slate-400" placeholder="Enter your password" />
                    <button type="button" onClick={() => setShowPassword((current) => !current)} className="password-toggle absolute right-3 top-1/2 -translate-y-1/2 rounded-lg p-2 text-slate-400" aria-label={showPassword ? "Hide password" : "Show password"} aria-pressed={showPassword}>
                      <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6z" strokeWidth="1.7" strokeLinejoin="round" />
                        <circle cx="12" cy="12" r="2.5" strokeWidth="1.7" />
                      </svg>
                    </button>
                  </div>
                </div>

                {message && (
                  <div role="alert" aria-live="polite" className="rounded-xl border border-red-100 bg-red-50 p-4">
                    <p className="text-sm font-bold text-red-700">{validationError ? "Check your details." : "Login failed."}</p>
                    <p className="mt-1 text-xs leading-5 text-red-600">{message}</p>
                  </div>
                )}

                <button type="submit" disabled={isSubmitting} className="flex w-full items-center justify-center gap-2 rounded-xl bg-navy-900 px-6 py-3.5 text-sm font-bold text-white transition hover:bg-navy-800 disabled:cursor-not-allowed disabled:opacity-60">
                  {isSubmitting ? "Signing in…" : "Login"}
                  {!isSubmitting && <span aria-hidden="true">→</span>}
                </button>
              </form>

              <div className="my-7 flex items-center gap-4" aria-hidden="true">
                <div className="h-px flex-1 bg-slate-200" />
                <span className="text-xs font-medium text-slate-400">OR</span>
                <div className="h-px flex-1 bg-slate-200" />
              </div>

              <Link href="/signup?redirectTo=%2Finvestor" className="flex w-full items-center justify-center rounded-xl border border-slate-200 px-6 py-3.5 text-sm font-bold text-navy-900 transition hover:bg-slate-50">
                Create an account
              </Link>
            </div>

            <p className="mt-6 text-center text-xs leading-5 text-slate-400">
              By continuing, you agree to Planvesto&apos;s{" "}
              <Link href="/terms" className="font-semibold text-slate-600 hover:text-navy-900">Terms &amp; Conditions</Link>{" "}
              and{" "}
              <Link href="/privacy" className="font-semibold text-slate-600 hover:text-navy-900">Privacy Policy</Link>.
            </p>
          </div>
        </div>
      </main>
    </>
  );
}
