// /static/js/jump-config.js
window.RC_JUMP_CONFIG = {
  "/economy.html": [
    {
      label: "Overview (Top Grid)",
      items: [
        { text: "Total Economy – Real GDP",       hash: "#total-gdp",            selector: 'a.box[href="archive.html"]' },
        { text: "Food – US Grocery Sales",        hash: "#grocery-sales",        selector: 'a.box[href="/grocery-sales"]' },
        { text: "Healthcare",                      hash: "#healthcare",           selector: 'a.box[href="/healthcare"]' },
        { text: "Existing Home Sales",             hash: "#home-sales",           selector: 'a.box[href="/home-sales"]' },
        { text: "Travel – TSA Checkpoint",         hash: "#tsa",                  selector: 'a.box[href="/tsa-checkpoint"]' },
        { text: "Energy – Personal Consumption",   hash: "#energy",               selector: 'a.box[href="/energy"]' },
        { text: "Banking/Finance – Hours",         hash: "#finance-hours",        selector: 'a.box[href="/lending-hours"]' },
        { text: "Transportation – TSI",            hash: "#transportation",       selector: 'a.box[href="/freight"]' },
        { text: "Manufacturing – ISM PMI",         hash: "#pmi",                  selector: 'a.box[href="/pmi"]' },
        { text: "Automotive – Vehicle Sales",      hash: "#vehicle-sales",        selector: 'a.box[href="/vehicle-sales"]' },
        { text: "Home Construction – Starts",      hash: "#housing-starts",       selector: 'a.box[href="/housing-starts"]' },
        { text: "Clothing – Monthly Sales",        hash: "#apparel",              selector: 'a.box[href="/apparel"]' },
        { text: "AI Infrastructure – NVIDIA",      hash: "#ai-infrastructure",    selector: 'a.box[href="/ai"]' }
      ]
    },
    {
      label: "Inflation",
      items: [
        { text: "US CPI",                          hash: "#inflation-cpi",        selector: 'a.box[href="/inflation"]' },
        { text: "Producer Price Index (PPI)",      hash: "#ppi",                  selector: 'a.box[href="/ppi"]' },
        { text: "Commodities Inflation Index",     hash: "#commodities",          selector: 'a.box[href="/commodities"]' }
      ]
    },
    {
      label: "GDP (Productivity)",
      items: [
        { text: "Real GDP Growth QoQ",             hash: "#real-gdp-qoq",         selector: 'a.box[href="/us-real-gdp-growth-qoq"]' },
        { text: "Real GDP Growth YoY",             hash: "#real-gdp-yoy",         selector: 'a.box[href="/us-gdp-real-growth-rate"]' },
        { text: "Nominal GDP Growth",              hash: "#nominal-gdp-growth",   selector: 'a.box[href="/us-gdp-growth-rate"]' }
      ]
    },
    {
      label: "Labor",
      items: [
        { text: "Nonfarm Payrolls",                hash: "#nonfarm",              selector: 'a.box[href="/nonfarm-payrolls"]' },
        { text: "Average Hourly Earnings",         hash: "#wages",                selector: 'a.box[href="/wages"]' },
        { text: "Labor Force Participation",       hash: "#labor-participation",  selector: 'a.box[href="/labor-participation"]' },
        { text: "Unemployment",                    hash: "#unemployment",         selector: 'a.box[href="/unemployment"]' },
        { text: "Population",                      hash: "#population",           selector: 'a.box[href="/population"]' }
      ]
    },
    {
      label: "Debt",
      items: [
        { text: "Gov. Debt Service / GDP",         hash: "#gov-debt-service",     selector: 'a.box[href="/gov-debt-service"]' },
        { text: "Household Debt Service",          hash: "#household-debt-service", selector: 'a.box[href="/household-debt-service"]' }
      ]
    },
    {
      label: "Other Metrics",
      items: [
        { text: "Leading Economic Index (LEI)",    hash: "#lei",                  selector: 'a.box[href="/lei"]' },
        { text: "Federal Deficit / GDP",           hash: "#deficit-gdp",          selector: 'a.box[href="/us-deficit"]' },
        { text: "Consumer Sentiment",              hash: "#sentiment",            selector: 'a.box[href="/sentiment"]' },
        { text: "Retail Sales Growth",             hash: "#retail",               selector: 'a.box[href="/retail"]' },
        { text: "Cash Use % of Transactions",      hash: "#cash-use",             selector: 'a.box[href="/cash-use"]' },
        { text: "Aerospace",                       hash: "#aerospace",            selector: 'a.box[href="/aerospace"]' },
        { text: "Rail Freight Carloads",           hash: "#rail",                 selector: 'a.box[href="/rail"]' }
      ]
    }
  ]
};
