import { useEffect } from "react";
import { supabase } from "../lib/supabase";

export function useLoginForm() {
  useEffect(() => {
    const loginForm = document.getElementById("loginForm") as HTMLFormElement | null;
    const email = document.getElementById("email") as HTMLInputElement | null;
    const password = document.getElementById("password") as HTMLInputElement | null;
    const remember = document.getElementById("remember") as HTMLInputElement | null;
    const loginButton = document.getElementById("loginButton") as HTMLButtonElement | null;
    const emailError = document.getElementById("emailError");
    const passwordError = document.getElementById("passwordError");
    const loginMessage = document.getElementById("loginMessage");
    const loginMessageTitle = document.getElementById("loginMessageTitle");
    const loginMessageText = document.getElementById("loginMessageText");
    const togglePassword = document.getElementById("togglePassword");
    const forgotToggle = document.getElementById("forgotToggle");
    const forgotPanel = document.getElementById("forgotPanel");
    const loginPanel = document.getElementById("loginPanel");

    togglePassword?.addEventListener("click", () => {
      if (!password) return;
      password.type = password.type === "password" ? "text" : "password";
    });

    forgotToggle?.addEventListener("click", (e: Event) => {
      e.preventDefault();
      loginPanel?.classList.add("hidden");
      forgotPanel?.classList.remove("hidden");
    });

    document.getElementById("backToLogin")?.addEventListener("click", (e: Event) => {
      e.preventDefault();
      forgotPanel?.classList.add("hidden");
      loginPanel?.classList.remove("hidden");
    });

    if (!loginForm || !email || !password || !loginButton) return;

    const handler = async (event: Event) => {
      event.preventDefault();
      const emailValue = email.value.trim();
      const passwordValue = password.value;
      let valid = true;

      emailError?.classList.add("hidden");
      passwordError?.classList.add("hidden");
      loginMessage?.classList.add("hidden");
      email.classList.remove("border-red-400");
      password.classList.remove("border-red-400");

      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailValue || !emailPattern.test(emailValue)) {
        emailError?.classList.remove("hidden");
        email.classList.add("border-red-400");
        valid = false;
      }
      if (!passwordValue) {
        if (passwordError) passwordError.textContent = "Enter your password.";
        passwordError?.classList.remove("hidden");
        password.classList.add("border-red-400");
        valid = false;
      } else if (passwordValue.length < 6) {
        if (passwordError) passwordError.textContent = "Password must contain at least 6 characters.";
        passwordError?.classList.remove("hidden");
        password.classList.add("border-red-400");
        valid = false;
      }
      if (!valid) return;

      loginButton.disabled = true;
      loginButton.innerHTML = "Signing in…";

      const { error } = await supabase.auth.signInWithPassword({
        email: emailValue,
        password: passwordValue,
      });

      loginButton.disabled = false;
      loginButton.innerHTML = "Login <span>→</span>";

      if (error) {
        if (loginMessageTitle) loginMessageTitle.textContent = "Login failed.";
        if (loginMessageText) loginMessageText.textContent = error.message;
        loginMessage?.classList.remove("hidden");
        return;
      }

      if (loginMessageTitle) loginMessageTitle.textContent = "Signed in successfully.";
      if (loginMessageText) loginMessageText.textContent = "Welcome back.";
      loginMessage?.classList.remove("hidden");

      const redirectTo = new URLSearchParams(window.location.search).get("redirectTo") || "/investor";
      window.location.assign(redirectTo);
    };

    loginForm.addEventListener("submit", handler);
    return () => loginForm.removeEventListener("submit", handler);
  }, []);
}
