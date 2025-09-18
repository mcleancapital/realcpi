// /static/js/jump.js
(function () {
  // ---- find config for current path (robust to /economy vs /economy.html) ----
  const rawPath = (location.pathname || "/").replace(/\/+$/, "") || "/";
  const candidates = Array.from(new Set([
    rawPath,
    rawPath.replace(/\.html$/i, ""),
    rawPath + ".html",
    rawPath === "/" ? "/index.html" : rawPath + "/index.html",
    "/index.html"
  ]));

  const CFG = (window.RC_JUMP_CONFIG || {});
  let groups = [];
  for (const key of candidates) {
    if (Array.isArray(CFG[key]) && CFG[key].length) { groups = CFG[key]; break; }
  }

  // ---- ensure wrapper exists and is inside header ----
  let wrapper = document.getElementById("quick-jump-wrapper");
  const header = document.querySelector("header");
  if (!wrapper && header) {
    wrapper = document.createElement("div");
    wrapper.id = "quick-jump-wrapper";
    wrapper.style.marginLeft = "auto";
    header.appendChild(wrapper);
  }
  if (!wrapper) return; // nowhere to mount

  // ---- fallback: auto-discover cards on the page if no config found ----
  if (!groups.length) {
    const cards = document.querySelectorAll('a.box[href]');
    const items = [];
    const usedIds = new Set();

    function slugify(s) {
      return (s || "")
        .toLowerCase()
        .replace(/https?:\/\/[^/]+/g, "")
        .replace(/[^\w-]+/g, "-")
        .replace(/-+/g, "-")
        .replace(/(^-|-$)/g, "");
    }

    cards.forEach((card, idx) => {
      const h3 = card.querySelector("h3");
      const text = (h3 ? h3.textContent.trim() : card.getAttribute("href")).replace(/\s+/g, " ");
      // Prefer href path to generate a stable id; fall back to text
      const base = slugify(card.getAttribute("href")) || slugify(text) || ("card-" + (idx + 1));
      let id = base.replace(/^\//, "");
      // ensure unique
      let n = 2;
      while (usedIds.has(id) || document.getElementById(id)) { id = base + "-" + (n++); }
      usedIds.add(id);

      items.push({ text, hash: "#" + id, selector: null, _el: card, _id: id });
    });

    // Attach ids right here
    items.forEach(it => { if (!it._el.id) it._el.id = it._id; });

    groups = [{ label: "On this page", items: items.map(({text, hash}) => ({ text, hash })) }];
  } else {
    // attach IDs to elements per config
    groups.forEach(group => group.items.forEach(item => {
      if (!item.hash || !item.hash.startsWith("#")) return;
      const id = item.hash.slice(1);
      const el = item.selector ? document.querySelector(item.selector) : null;
      if (el && !el.id) el.id = id;
    }));
  }

  // ---- build the dropdown UI ----
  const container = document.createElement("div");
  container.id = "quick-jump";
  container.style.padding = "8px 18px";
  const select = document.createElement("select");
  select.id = "quick-jump-select";
  select.innerHTML = `<option value="">Jump to…</option>`;
  Object.assign(select.style, {
    fontSize: "14px", padding: "6px 8px",
    border: "1px solid #ccc", borderRadius: "6px",
    background: "#fff", maxWidth: "260px"
  });

  groups.forEach(group => {
    const og = document.createElement("optgroup");
    og.label = group.label;
    group.items.forEach(item => {
      const opt = document.createElement("option");
      opt.value = item.hash; // in-page
      opt.textContent = item.text;
      og.appendChild(opt);
    });
    select.appendChild(og);
  });

  container.appendChild(select);
  wrapper.appendChild(container);

  // ---- smooth scroll with header offset ----
  function scrollToHash(hash) {
    const id = (hash || "").replace(/^#/, "");
    if (!id) return;
    const el = document.getElementById(id);
    if (!el) { location.hash = "#" + id; return; }
    const headerEl = document.querySelector("header");
    const offset = headerEl ? headerEl.offsetHeight : 0;
    const y = el.getBoundingClientRect().top + window.scrollY - offset - 8;
    window.scrollTo({ top: y, behavior: "smooth" });
    history.replaceState(null, "", "#" + id);
  }

  select.addEventListener("change", e => {
    if (e.target.value) scrollToHash(e.target.value);
    e.target.value = "";
  });

  // Honor incoming #hash
  if (location.hash) setTimeout(() => scrollToHash(location.hash), 0);
})();
