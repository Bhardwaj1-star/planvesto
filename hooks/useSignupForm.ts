import { useEffect } from "react";
import { supabase } from "../lib/supabase";

export function useSignupForm() {
  useEffect(() => {
    const signupForm = document.getElementById("signupForm") as HTMLFormElement | null;
    const email = document.getElementById("email") as HTMLInputElement | null;
    const password = document.getElementById("password") as HTMLInputElement | null;
    const confirmPassword = document.getElementById("confirmPassword") as HTMLInputElement | null;
    const terms = document.getElementById("terms") as HTMLInputElement | null;
    const createButton = document.getElementById("createButton") as HTMLButtonElement | null;
    const emailError = document.getElementById("emailError");
    const passwordError = document.getElementById("passwordError");
    const confirmError = document.getElementById("confirmError");
    const termsError = document.getElementById("termsError");
    const successMessage = document.getElementById("successMessage");
    const strengthBar = document.getElementById("strengthBar") as HTMLElement | null;
    const strengthText = document.getElementById("strengthText");
    const togglePassword = document.getElementById("togglePassword");
    const toggleConfirm = document.getElementById("toggleConfirm");

    togglePassword?.addEventListener("click", () => {
      if (!password) return;
      password.type = password.type === "password" ? "text" : "password";
    });

    toggleConfirm?.addEventListener("click", () => {
      if (!confirmPassword) return;
      confirmPassword.type = confirmPassword.type === "password" ? "text" : "password";
    });

    password?.addEventListener("input", () => {
      const value = password.value;
      let score = 0;
      if (value.length >= 8) score++;
      if (/[A-Z]/.test(value)) score++;
      if (/[0-9]/.test(value)) score++;
      if (/[^A-Za-z0-9]/.test(value)) score++;
      const widths = ["0%", "25%", "50%", "75%", "100%"];
      const colors = ["#E2E8F0", "#F87171", "#FBBF24", "#34D399", "#0F766E"];
      const labels = ["", "Weak", "Fair", "Good", "Strong"];
      if (strengthBar) {
        strengthBar.style.width = widths[score];
        strengthBar.style.backgroundColor = colors[score];
      }
      if (strengthText) strengthText.textContent = labels[score] || "";
    });

    if (!signupForm || !email || !password || !confirmPassword || !createButton) return;

    const handler = async (event: Event) => {
      event.preventDefault();
      const fullName = document.getElementById("fullName") as HTMLInputElement | null;
  const fullNameValue = fullName?.value.trim() || "";
  const emailValue = email.value.trim();
      const passwordValue = password.value;
      const confirmValue = confirmPassword.value;
      let valid = true;

      [emailError, passwordError, confirmError, termsError].forEach((el) => el?.classList.add("hidden"));
      [email, password, confirmPassword].forEach((el) => el?.classList.remove("border-red-400"));
      successMessage?.classList.add("hidden");

      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailValue || !emailPattern.test(emailValue)) {
        emailError?.classList.remove("hidden");
        email.classList.add("border-red-400");
        valid = false;
      }
      if (passwordValue.length < 8) {
        passwordError?.classList.remove("hidden");
        password.classList.add("border-red-400");
        valid = false;
      }
      if (!confirmValue || confirmValue !== passwordValue) {
        confirmError?.classList.remove("hidden");
        confirmPassword.classList.add("border-red-400");
        valid = false;
      }
      if (!terms?.checked) {
        termsError?.classList.remove("hidden");
        valid = false;
      }
      if (!valid) return;

      createButton.disabled = true;
      createButton.innerHTML = "Creating Accountâ€¦";

      const { data, error } = await supabase.auth.signUp({
        email: emailValue,
    password: passwordValue,
    options: {
      data: {
        full_name: fullNameValue,
      },
    },
  });

      createButton.disabled = false;
      createButton.innerHTML = "Create Account <span>â†’</span>";

      if (error) {
        alert(error.message);
        return;
      }

      successMessage?.classList.remove("hidden");
      successMessage?.scrollIntoView({ behavior: "smooth", block: "nearest" });

      const redirectTo = new URLSearchParams(window.location.search).get("redirectTo");
      if (redirectTo && data.session) window.location.assign(redirectTo);
    };

    signupForm.addEventListener("submit", handler);
    return () => signupForm.removeEventListener("submit", handler);
  }, []);
}



