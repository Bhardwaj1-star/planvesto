import { useEffect } from "react";

export function useArticleSearch() {
  useEffect(() => {
    const searchInput = document.getElementById("searchInput") as HTMLInputElement | null;
    const noResults = document.getElementById("noResults");
    const articles = Array.from(document.querySelectorAll<HTMLElement>(".article-item"));
    if (!searchInput) return;

    const handler = () => {
      const query = searchInput.value.trim().toLowerCase();
      let visibleCount = 0;
      articles.forEach((article) => {
        const searchableText = ((article.dataset.search || "") + " " + article.innerText).toLowerCase();
        const matches = query === "" || searchableText.includes(query);
        article.classList.toggle("hidden", !matches);
        if (matches) visibleCount++;
      });
      noResults?.classList.toggle("hidden", visibleCount !== 0);
    };

    searchInput.addEventListener("input", handler);
    return () => searchInput.removeEventListener("input", handler);
  }, []);
}
