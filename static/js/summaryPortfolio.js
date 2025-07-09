const userId = localStorage.getItem("userEmail");
if (!userId) {
  alert("You must be logged in.");
  window.location.href = "/login.html";
}

const baseURL = "https://210jsf4oy1.execute-api.us-east-1.amazonaws.com";
const fmpApiKey = "y9Bthip8mNYaWhrHQp0eTtPX3KltVYPj";

let allHoldings = [];

function populatePortfolioDropdown(portfolios) {
  const dropdown = document.getElementById("portfolioSelect");
  dropdown.innerHTML = portfolios.map(p => `<option value="${p}">${p}</option>`).join("");
  dropdown.value = portfolios[0];
  dropdown.addEventListener("change", () => renderSummary(dropdown.value));
  renderSummary(dropdown.value);
}

async function loadHoldings() {
  const res = await fetch(`https://umd5byy4m3.execute-api.us-east-1.amazonaws.com/rcPortfolio?user_id=${encodeURIComponent(userId)}`);
  allHoldings = await res.json();
  const portfolios = [...new Set(allHoldings.map(i => i.portfolio).filter(Boolean))];
  populatePortfolioDropdown(portfolios);
}

async function renderSummary(selectedPortfolio) {
  const table = document.getElementById("summaryTable");
  table.innerHTML = "";

  let filtered = allHoldings.filter(i => i.portfolio === selectedPortfolio);
  if (filtered.length === 0) {
    table.innerHTML = `<tr><td colspan="2">No holdings in selected portfolio.</td></tr>`;
    return;
  }

  const tickers = [...new Set(filtered.map(i => (i.ticker || "").toUpperCase()))].join(",");
  const res = await fetch(`https://financialmodelingprep.com/api/v3/quote/${tickers}?apikey=${fmpApiKey}`);
  const quotes = await res.json();

  const priceMap = {}, moveMap = {}, nameMap = {}, currencyMap = {};
  quotes.forEach(q => {
    const sym = q.symbol.toUpperCase();
    priceMap[sym] = q.price;
    moveMap[sym] = ((q.price / q.previousClose - 1) * 100).toFixed(2);
    nameMap[sym] = q.name;
    currencyMap[sym] = q.currency || "USD";  // fallback to USD if missing
  });

  // Define custom currency priority
  const currencyOrder = { CAD: 0, USD: 1, EUR: 2, JPY: 3 };

  // Sort first by privacy, then by currency priority
filtered.sort((a, b) => {
  const privA = a.is_private === true ? 0 : (a.ticker?.includes('.') ? 1 : 2);
  const privB = b.is_private === true ? 0 : (b.ticker?.includes('.') ? 1 : 2);
  return privA - privB;
});


for (const item of filtered) {
  const ticker = (item.ticker || "").toUpperCase();
  const isPrivate = item.is_private === true;
  const name = isPrivate ? (item.name || ticker) : (nameMap[ticker] || ticker);
  const price = isPrivate ? item.custom_price : priceMap[ticker];
  const move = isPrivate ? "" : (moveMap[ticker] + "%");

  const row = document.createElement("tr");
  row.style.cursor = "pointer"; // Show clickable cursor

  // ✅ Add click event to trigger a ticker search
  row.addEventListener("click", () => {
    const input = document.getElementById("tickerInput");
    if (input) {
      input.value = ticker;
      input.dispatchEvent(new Event("input"));
      setTimeout(loadData, 200); // You can increase delay if needed
    }
  });

  row.innerHTML = `
    <td>
      <div class="ticker-name" style="color: ${isPrivate ? '#007BFF' : 'inherit'}">${ticker}</div>
      <div class="name">${name}</div>
    </td>
    <td>
      <div class="price">${price !== undefined ? "$" + parseFloat(price).toFixed(2) : "-"}</div>
      <div class="move" style="color: ${move.startsWith('-') ? 'red' : 'green'}">${move}</div>
    </td>
  `;

  table.appendChild(row);
}
}


loadHoldings();
