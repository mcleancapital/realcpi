// /static/js/jump-config.js
window.RC_JUMP_CONFIG = {
  // ---------- GLOBAL MENU (shown on all pages) ----------
  "*": [
    {
      label: "Daily Data",
      items: [
        { text: "10 Year Treasury Rate",           url: "/10-year-treasury-rate#chart" },
        { text: "S&P 500 Historical Prices",       url: "/s-p-500-historical-prices#chart" },
        { text: "High-Yield Credit Spread",        url: "/credit-spread#chart" }
      ]
    },
    {
      label: "Stock Market Data",
      items: [
        { text: "S&P 500 P/E Ratio",               url: "/s-p-500-pe-ratio#chart" },
        { text: "Magnificent 7 Returns",           url: "/mag7#pie" },
        { text: "S&P/TSX Historical Prices",       url: "/tsx-historical-prices#chart" }
      ]
    },
    {
      label: "Real Estate",
      items: [
        { text: "Existing Home Sales",             url: "/home-sales#chart" },
        { text: "Housing Starts",                   url: "/housing-starts#chart" }
      ]
    },
    {
      label: "Economic Dashboard",
      items: [
        { text: "Inflation (CPI)",                 url: "/economy.html#inflation-cpi" },
        { text: "Real GDP – QoQ",                  url: "/economy.html#real-gdp-qoq" },
        { text: "Real GDP – YoY",                  url: "/economy.html#real-gdp-yoy" },
        { text: "Nonfarm Payrolls",                url: "/economy.html#nonfarm" }
      ]
    }
  ],

  // ---------- PER-PAGE ADDITIONS (optional) ----------
  "/economy.html": [
    {
      label: "On this page",
      items: [
        // Ensure the first card’s selector matches your HTML structure
        { text: "Total Economy – Real GDP",       selector: 'a[href="archive.html"] .box', hash: "#total-gdp" },
        { text: "US CPI",                         selector: 'a.box[href="/inflation"]',              hash: "#inflation-cpi" },
        { text: "Producer Price Index (PPI)",     selector: 'a.box[href="/ppi"]',                    hash: "#ppi" },
        { text: "Real GDP – QoQ",                 selector: 'a.box[href="/us-real-gdp-growth-qoq"]', hash: "#real-gdp-qoq" },
        { text: "Real GDP – YoY",                 selector: 'a.box[href="/us-gdp-real-growth-rate"]',hash: "#real-gdp-yoy" },
        { text: "Nonfarm Payrolls",               selector: 'a.box[href="/nonfarm-payrolls"]',       hash: "#nonfarm" }
        // …add more as you like
      ]
    }
  ]
};

// Handy aliases (optional)
window.RC_JUMP_CONFIG["/economy"]  = window.RC_JUMP_CONFIG["/economy.html"];
window.RC_JUMP_CONFIG["/"]         = window.RC_JUMP_CONFIG["/"] || [];
window.RC_JUMP_CONFIG["/index"]    = window.RC_JUMP_CONFIG["/"];
window.RC_JUMP_CONFIG["/index.html"]= window.RC_JUMP_CONFIG["/"];
