import { useState } from "react";
import { supabase } from "../lib/supabase";
import { getSafeRedirect } from "../lib/safe-redirect";
import { getPlanningUnitId } from "../lib/planning-unit";

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

    try {
      await getPlanningUnitId();
    } catch (workspaceError) {
      setErrorMessage(
        workspaceError instanceof Error
          ? "Login succeeded, but your financial workspace could not be initialized: " + workspaceError.message
          : "Login succeeded, but your financial workspace could not be initialized.",
      );
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
