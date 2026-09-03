"use client";

import { useEffect } from "react";

export default function ClientShell({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const menuButton = document.getElementById("menuButton");
    const mobileMenu = document.getElementById("mobileMenu");
    const currentYear = document.getElementById("currentYear");
    if (currentYear) currentYear.textContent = String(new Date().getFullYear());

    const toggleMenu = () => {
      if (!menuButton || !mobileMenu) return;
      const isHidden = mobileMenu.classList.contains("hidden");
      mobileMenu.classList.toggle("hidden");
      menuButton.setAttribute("aria-expanded", String(isHidden));
    };
    menuButton?.addEventListener("click", toggleMenu);

    const closeLinks: Array<[Element, EventListener]> = [];
    mobileMenu?.querySelectorAll("a").forEach((link) => {
      const handler: EventListener = () => {
        mobileMenu.classList.add("hidden");
        menuButton?.setAttribute("aria-expanded", "false");
      };
      link.addEventListener("click", handler);
      closeLinks.push([link, handler]);
    });

    const searchInput = document.getElementById("searchInput") as HTMLInputElement | null;
    const noResults = document.getElementById("noResults");
    const articles = Array.from(document.querySelectorAll<HTMLElement>("[data-search]"));
    const searchHandler = () => {
      if (!searchInput || !articles.length) return;
      const query = searchInput.value.trim().toLowerCase();
      let visibleCount = 0;
      articles.forEach((article) => {
        const text = ((article.dataset.search || "") + " " + article.innerText).toLowerCase();
        const matches = query === "" || text.includes(query);
        article.classList.toggle("hidden", !matches);
        if (matches) visibleCount++;
      });
      noResults?.classList.toggle("hidden", visibleCount !== 0);
    };
    searchInput?.addEventListener("input", searchHandler);

    return () => {
      menuButton?.removeEventListener("click", toggleMenu);
      closeLinks.forEach(([link, handler]) => link.removeEventListener("click", handler));
      searchInput?.removeEventListener("input", searchHandler);
    };
  }, []);

  return <>{children}</>;
}
