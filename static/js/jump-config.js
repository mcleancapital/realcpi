// /static/js/jump-config.js
window.RC_JUMP_CONFIG = {
  // ---------- GLOBAL MENU (shown on all pages) ----------
  "*": [
    {
      label: "Daily Data",
      items: [
        { text: "10 Year Treasury Rate",     url: "/#ten-year" },
        { text: "S&P 500 Historical Prices", url: "/#sp500-prices" },
        { text: "High-Yield Credit Spread",  url: "/#credit-spread" },
        { text: "S&P 500 P/E Ratio",         url: "/#sp500-pe" },
        { text: "Magnificent 7 Returns",     url: "/#mag7" },
        { text: "S&P/TSX Historical Prices", url: "/#tsx-prices" },
        { text: "Canada Top 10 (YTD)",       url: "/#top10" },
        { text: "S&P 500 Sectors (YTD)",     url: "/#sectors" }
      ]
    },
    {
      label: "Stock Market Data",
      items: [
        // point at the small cards on /stocks.html
        { text: "S&P 500 P/E Ratio",         url: "/stocks.html#sp500-pe" },
        { text: "S&P 500 Prices",            url: "/stocks.html#sp500-prices" },
        { text: "High-Yield Credit Spread",  url: "/stocks.html#credit-spread" },
        { text: "S&P/TSX Prices",            url: "/stocks.html#tsx-prices" },
        { text: "Magnificent 7",             url: "/stocks.html#mag7" }
      ]
    },
    {
      label: "Real Estate",
      items: [
        { text: "Existing Home Sales",       url: "/realestate.html#home-sales" },
        { text: "Housing Starts",            url: "/realestate.html#housing-starts" }
      ]
    },
    {
      label: "Economic Dashboard",
      items: [
        { text: "Total Economy – Real GDP",  url: "/economy.html#total-gdp" },
        { text: "Inflation (CPI)",           url: "/economy.html#inflation-cpi" },
        { text: "PPI",                       url: "/economy.html#ppi" },
        { text: "Real GDP – QoQ",            url: "/economy.html#real-gdp-qoq" },
        { text: "Real GDP – YoY",            url: "/economy.html#real-gdp-yoy" },
        { text: "Nonfarm Payrolls",          url: "/economy.html#nonfarm" },
        { text: "Existing Home Sales",       url: "/economy.html#home-sales" },
        { text: "Housing Starts",            url: "/economy.html#housing-starts" }
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
