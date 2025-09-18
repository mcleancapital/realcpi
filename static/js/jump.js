<script>
// /static/js/jump.js
(function () {
  function init() {
    const cfg = (window.RC_JUMP_CONFIG || {});
    const path = (location.pathname.replace(/\/+$/, "") || "/");

    // Ensure wrapper exists (create one in header if missing)
    let wrapper = document.getElementById("quick-jump-wrapper");
    if (!wrapper) {
      const header = document.querySelector("header") || document.body;
      wrapper = document.createElement("div");
      wrapper.id = "quick-jump-wrapper";
      wrapper.style.marginLeft = "auto";
      header.appendChild(wrapper);
      console.warn("[jump] #quick-jump-wrapper was missing; created automatically.");
    }

    const globalGroups = Array.isArray(cfg["*"]) ? cfg["*"] : [];
    const pageGroups   = Array.isArray(cfg[path]) ? cfg[path] : [];

    // Build the <select>
    const sel = document.createElement("select");
    sel.id = "quick-jump-select";
    sel.setAttribute("aria-label", "Quick navigation");
    sel.innerHTML = '<option value="">Jump to…</option>';
    wrapper.replaceChildren(sel); // clear + insert

    function addGroup(groups, mode) {
      groups.forEach(group => {
        const items = Array.isArray(group.items) ? group.items : [];
        if (!items.length) return;

        const og = document.createElement("optgroup");
        og.label = group.label || "";

        items.forEach(item => {
          // For on-page entries, attach the target id if possible
          if (mode === "page" && item.selector && item.hash) {
            const target = document.querySelector(item.selector);
            if (target) {
              const id = String(item.hash).replace(/^#/, "");
              if (id && !document.getElementById(id)) target.id = id;
            } else {
              console.warn("[jump] Selector not found on page:", item.selector);
            }
          }

          // Determine value
          let value = "";
          if (mode === "page" && item.hash) {
            value = String(item.hash);
          } else if (item.url) {
            value = String(item.url);
          } else {
            // Skip invalid entries
            console.warn("[jump] Skipping item without url/hash:", item);
            return;
          }

          const opt = document.createElement("option");
          opt.textContent = item.text || value;
          opt.value = value;
          og.appendChild(opt);
        });

        if (og.children.length) sel.appendChild(og);
      });
    }

    addGroup(globalGroups, "global");
    addGroup(pageGroups, "page");

    sel.addEventListener("change", e => {
      const v = e.target.value;
      if (!v) return;
      if (v.startsWith("#")) {
        const el = document.querySelector(v);
        if (el) {
          el.scrollIntoView({ behavior: "smooth", block: "start" });
          history.replaceState(null, "", v);
        }
      } else {
        window.location.href = v;
      }
      e.target.value = "";
    });
  }

  // Wait for DOM (and avoid races if defer is missing somewhere)
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
</script>
