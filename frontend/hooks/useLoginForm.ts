import { useState } from "react";
import { supabase } from "../lib/supabase";

function getSafeRedirect(value: string | null): string {
  if (!value) return "/investor";

  try {
    const url = new URL(value, window.location.origin);
    if (url.origin !== window.location.origin) return "/investor";
    return url.pathname + url.search + url.hash;
  } catch {
    return "/investor";
  }
}

export function useLoginForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const submit = async (email: string, password: string) => {
    setErrorMessage("");
    setIsSubmitting(true);

    const { error } = await supabase.auth.signInWithPassword({
      email: email.trim(),
      password,
    });

    if (error) {
      setErrorMessage(error.message);
      setIsSubmitting(false);
      return;
    }

    const redirectTo = getSafeRedirect(
      new URLSearchParams(window.location.search).get("redirectTo"),
    );

    window.location.assign(redirectTo);
  };

  return {
    isSubmitting,
    errorMessage,
    showPassword,
    setShowPassword,
    submit,
  };
}
