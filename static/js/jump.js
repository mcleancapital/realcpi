<script>
// /static/js/jump.js
(function () {
  const wrapper = document.getElementById("quick-jump-wrapper");
  if (!wrapper) return;

  const path = (location.pathname.replace(/\/+$/, "") || "/");
  const cfg = (window.RC_JUMP_CONFIG || {});
  const globalGroups = cfg["*"] || [];
  const pageGroups = cfg[path] || [];

  // Create the <select>
  const select = document.createElement("select");
  select.id = "quick-jump-select";
  select.setAttribute("aria-label", "Quick navigation");
  select.innerHTML = '<option value="">Jump to…</option>';
  wrapper.appendChild(select);

  function addGroup(groups, mode) {
    groups.forEach(group => {
      const og = document.createElement("optgroup");
      og.label = group.label || "";
      (group.items || []).forEach(item => {
        // If it's an on-page item, ensure the anchor exists
        if (mode === "page" && item.selector && item.hash) {
          const el = document.querySelector(item.selector);
          if (el) {
            const id = item.hash.replace(/^#/, "");
            if (!document.getElementById(id)) el.id = id;
          }
        }
        const opt = document.createElement("option");
        opt.textContent = item.text;
        // On-page: value is just "#id"; Global: value is a full URL path + hash
        opt.value = (mode === "page" && item.hash) ? item.hash : item.url;
        og.appendChild(opt);
      });
      if (og.children.length) select.appendChild(og);
    });
  }

  // Build global first (available on all pages)
  addGroup(globalGroups, "global");
  // Then add per-page group (if any)
  addGroup(pageGroups, "page");

  // Handle navigation
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
})();
</script>
