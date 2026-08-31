import { useEffect } from "react";

export function useMobileMenuClose(setMenuOpen: (open: boolean) => void) {
  useEffect(() => {
    const mobileMenu = document.getElementById("mobileMenu");
    const menuButton = document.getElementById("menuButton");
    if (!mobileMenu || !menuButton) return;

    const handlers = Array.from(mobileMenu.querySelectorAll("a")).map((link) => {
      const handler = () => {
        setMenuOpen(false);
        menuButton.setAttribute("aria-expanded", "false");
      };
      link.addEventListener("click", handler);
      return { link, handler };
    });

    return () => {
      handlers.forEach(({ link, handler }) => link.removeEventListener("click", handler));
    };
  }, [setMenuOpen]);
}
