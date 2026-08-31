import { useEffect } from "react";

export function useContactForm() {
  useEffect(() => {
    const contactForm = document.getElementById("contactForm");
    const submitButton = document.getElementById("submitButton") as HTMLButtonElement | null;
    const successMessage = document.getElementById("successMessage");
    if (!contactForm) return;

    const handler = (event: Event) => {
      event.preventDefault();

      const name = document.getElementById("name") as HTMLInputElement | null;
      const email = document.getElementById("email") as HTMLInputElement | null;
      const topic = document.getElementById("topic") as HTMLSelectElement | null;
      const message = document.getElementById("message") as HTMLTextAreaElement | null;
      const consent = document.getElementById("consent") as HTMLInputElement | null;

      const nameError = document.getElementById("nameError");
      const emailError = document.getElementById("emailError");
      const topicError = document.getElementById("topicError");
      const messageError = document.getElementById("messageError");
      const consentError = document.getElementById("consentError");

      let valid = true;

      [nameError, emailError, topicError, messageError, consentError].forEach((element) => {
        element?.classList.add("hidden");
      });

      [name, email, topic, message].forEach((element) => {
        element?.classList.remove("border-red-400");
      });

      if (!name?.value.trim()) {
        nameError?.classList.remove("hidden");
        name?.classList.add("border-red-400");
        valid = false;
      }

      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!email?.value.trim() || !emailPattern.test(email.value.trim())) {
        emailError?.classList.remove("hidden");
        email?.classList.add("border-red-400");
        valid = false;
      }

      if (!topic?.value) {
        topicError?.classList.remove("hidden");
        topic?.classList.add("border-red-400");
        valid = false;
      }

      if (!message?.value.trim()) {
        messageError?.classList.remove("hidden");
        message?.classList.add("border-red-400");
        valid = false;
      }

      if (!consent?.checked) {
        consentError?.classList.remove("hidden");
        valid = false;
      }

      if (!valid) return;

      if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = "Message Checked ✓";
      }

      successMessage?.classList.remove("hidden");
      successMessage?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    };

    contactForm.addEventListener("submit", handler);
    return () => contactForm.removeEventListener("submit", handler);
  }, []);
}
