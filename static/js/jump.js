// /static/js/jump.js
(function () {
  function initJump() {
    // Make sure we have a wrapper; create one if missing.
    let wrapper = document.getElementById("quick-jump-wrapper");
    if (!wrapper) {
      const header = document.querySelector("header");
      if (!header) return;
      wrapper = document.createElement("div");
      wrapper.id = "quick-jump-wrapper";
      header.appendChild(wrapper);
    } else {
      wrapper.innerHTML = ""; // reset if we re-init
    }

    const path = (location.pathname.replace(/\/+$/, "") || "/");
    const cfg  = (window.RC_JUMP_CONFIG || {});
    const globalGroups = Array.isArray(cfg["*"]) ? cfg["*"] : [];
    const pageGroups   = Array.isArray(cfg[path]) ? cfg[path] : [];

    // Build the <select>
    const select = document.createElement("select");
    select.id = "quick-jump-select";
    select.setAttribute("aria-label", "Quick navigation");
    select.innerHTML = '<option value="">Jump to…</option>';
    wrapper.appendChild(select);

    function addGroup(groups, mode) {
      (groups || []).forEach(group => {
        const og = document.createElement("optgroup");
        og.label = group.label || "";
        (group.items || []).forEach(item => {
          // For on-page links: ensure the anchor exists on the target element
          if (mode === "page" && item.selector && item.hash) {
            const el = document.querySelector(item.selector);
            if (el) {
              const id = item.hash.replace(/^#/, "");
              if (!document.getElementById(id)) el.id = id;
            } else {
              // If the selector isn't found, skip adding this option
              return;
            }
          }
          const opt = document.createElement("option");
          opt.textContent = item.text;
          opt.value = (mode === "page" && item.hash) ? item.hash : item.url;
          og.appendChild(opt);
        });
        if (og.children.length) select.appendChild(og);
      });
    }

    // Global (all pages) first, then per-page additions
    addGroup(globalGroups, "global");
    addGroup(pageGroups, "page");

    // If there are no options beyond the placeholder, hide the control
    if (select.children.length <= 1) {
      wrapper.style.display = "none";
    } else {
      wrapper.style.display = "";
    }

    // Navigate
    select.addEventListener("change", e => {
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

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initJump);
  } else {
    initJump();
  }
})();
