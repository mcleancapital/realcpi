// /static/js/jump.js
(function () {
  const path = location.pathname.replace(/\/+$/, "") || "/";
  const groups = (window.RC_JUMP_CONFIG && window.RC_JUMP_CONFIG[path]) || [];
  if (!groups.length) return;

  // 1) Attach IDs (anchors) to the target cards automatically
  groups.forEach(g =>
    g.items.forEach(item => {
      if (!item.selector || !item.hash || !item.hash.startsWith("#")) return;
      const el = document.querySelector(item.selector);
      if (el) {
        const id = item.hash.slice(1);
        if (!el.id) el.id = id; // anchor lives on the card itself
      }
    })
  );

  // 2) Build the dropdown UI
  const wrapper = document.getElementById("quick-jump-wrapper");
  if (!wrapper) return;

  const container = document.createElement("div");
  container.id = "quick-jump";
  container.style.padding = "8px 18px";

  const select = document.createElement("select");
  select.id = "quick-jump-select";
  select.innerHTML = `<option value="">Jump to…</option>`;
  select.style.fontSize = "14px";
  select.style.padding = "6px 8px";
  select.style.border = "1px solid #ccc";
  select.style.borderRadius = "6px";
  select.style.background = "#fff";
  select.style.maxWidth = "260px";

  groups.forEach(group => {
    const og = document.createElement("optgroup");
    og.label = group.label;
    group.items.forEach(item => {
      const opt = document.createElement("option");
      opt.value = item.hash;               // only in-page hashes for this page
      opt.textContent = item.text;
      og.appendChild(opt);
    });
    select.appendChild(og);
  });

  container.appendChild(select);
  wrapper.appendChild(container);

  // 3) Smooth scroll with header offset
  function scrollToHash(hash) {
    const id = (hash || "").replace(/^#/, "");
    if (!id) return;
    const el = document.getElementById(id);
    if (!el) {
      // Fallback: let the browser try
      location.hash = "#" + id;
      return;
    }

    const header = document.querySelector("header");
    const offset = header ? header.offsetHeight : 0;

    const y = el.getBoundingClientRect().top + window.scrollY - offset - 8;
    window.scrollTo({ top: y, behavior: "smooth" });

    // Keep URL clean and accurate without jumping
    history.replaceState(null, "", "#" + id);
  }

  select.addEventListener("change", (e) => {
    const hash = e.target.value;
    if (hash) scrollToHash(hash);
    e.target.value = "";
  });

  // 4) If someone lands with a hash already, honor it with offset
  if (location.hash) {
    // Wait a tick to ensure layout settled
    setTimeout(() => scrollToHash(location.hash), 0);
  }
})();
