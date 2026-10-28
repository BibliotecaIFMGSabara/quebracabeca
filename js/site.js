(() => {
  "use strict";

  const normalize = (value) => value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();

  const searchInput = document.querySelector("#game-search");
  const filterButtons = [...document.querySelectorAll(".filter-button")];
  const cards = [...document.querySelectorAll(".game-card")];
  const resultCount = document.querySelector("#result-count");
  const totalGameCount = document.querySelector("#total-game-count");
  const emptyState = document.querySelector("#empty-state");
  const clearFilters = document.querySelector("#clear-filters");
  let activeFilter = "todos";

  function applyFilters() {
    // Derive both counters from the rendered catalog, never from a manually
    // maintained number. The build step keeps these cards in sync with data.
    if (totalGameCount) totalGameCount.textContent = String(cards.length);
    if (!cards.length) {
      if (resultCount) resultCount.textContent = "0";
      return;
    }
    const query = normalize(searchInput?.value || "");
    let visible = 0;

    cards.forEach((card) => {
      const matchesCategory = activeFilter === "todos" || card.dataset.category === activeFilter;
      const matchesSearch = !query || normalize(card.dataset.search || "").includes(query);
      const show = matchesCategory && matchesSearch;
      card.hidden = !show;
      if (show) visible += 1;
    });

    if (resultCount) resultCount.textContent = String(visible);
    if (emptyState) emptyState.hidden = visible !== 0;
  }

  searchInput?.addEventListener("input", applyFilters);

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      activeFilter = button.dataset.filter || "todos";
      filterButtons.forEach((item) => {
        const selected = item === button;
        item.classList.toggle("is-active", selected);
        item.setAttribute("aria-pressed", String(selected));
      });
      applyFilters();
    });
  });

  clearFilters?.addEventListener("click", () => {
    activeFilter = "todos";
    if (searchInput) searchInput.value = "";
    filterButtons.forEach((item) => {
      const selected = item.dataset.filter === "todos";
      item.classList.toggle("is-active", selected);
      item.setAttribute("aria-pressed", String(selected));
    });
    applyFilters();
    searchInput?.focus();
  });

  // Initialize the displayed count from the actual cards on page load.
  applyFilters();

  const shareButton = document.querySelector(".share-button");
  const shareToast = document.querySelector("#share-toast");

  async function showToast(message) {
    if (!shareToast) return;
    shareToast.textContent = message;
    shareToast.hidden = false;
    window.setTimeout(() => { shareToast.hidden = true; }, 2200);
  }

  shareButton?.addEventListener("click", async () => {
    const data = {
      title: shareButton.dataset.shareTitle || document.title,
      text: document.querySelector('meta[name="description"]')?.content || "",
      url: window.location.href
    };

    try {
      if (navigator.share) {
        await navigator.share(data);
        return;
      }
      await navigator.clipboard.writeText(data.url);
      await showToast("Link copiado.");
    } catch (error) {
      if (error?.name !== "AbortError") await showToast("Não foi possível copiar o link.");
    }
  });
})();
