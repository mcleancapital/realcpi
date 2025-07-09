function logout() {
  // Clear all relevant user info from localStorage
  localStorage.removeItem("idToken");
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
  localStorage.removeItem("userEmail");
  localStorage.removeItem("userName");
  localStorage.removeItem("baseCurrency");

  // Redirect to login page
  window.location.href = "/login";
}

function showUserSettings() {
  const modal = document.getElementById("user-settings-modal");
  const nameSpan = document.getElementById("user-name");

  // Prefill form fields from localStorage
  const nameParts = (localStorage.getItem("userName") || "").split(" ");
  document.getElementById("first-name-input").value = nameParts[0] || "";
  document.getElementById("last-name-input").value = nameParts[1] || "";
  document.getElementById("currency-input").value = localStorage.getItem("baseCurrency") || "USD";

  // Position the modal below the name element
  modal.style.display = "none";
  setTimeout(() => {
    const rect = nameSpan.getBoundingClientRect();
    modal.style.top = `${rect.bottom + window.scrollY + 6}px`;
    modal.style.left = `${rect.right + window.scrollX - 400}px`;
    modal.style.display = "block";
  }, 0);
}

function closeUserSettings() {
  document.getElementById("user-settings-modal").style.display = "none";
}

function saveUserSettings() {
  const first = document.getElementById("first-name-input").value.trim();
  const last = document.getElementById("last-name-input").value.trim();
  const currency = document.getElementById("currency-input").value;

  const fullName = `${first} ${last}`;
  localStorage.setItem("userName", fullName);
  localStorage.setItem("baseCurrency", currency);

  // Update UI
  const nameSpan = document.getElementById("user-name");
  if (nameSpan) nameSpan.textContent = fullName;

  // Optionally update in backend if needed
  updateUserInDatabase(first, last, currency);

  closeUserSettings();
}

async function updateUserInDatabase(firstName, lastName, currency) {
  const userEmail = localStorage.getItem("userEmail");
  if (!userEmail) return;

  const payload = {
    user_id: userEmail,
    first_name: firstName,
    last_name: lastName,
    base_currency: currency
  };

  try {
    const res = await fetch("https://210jsf4oy1.execute-api.us-east-1.amazonaws.com/updateUser", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error("Failed to update user profile.");
    console.log("User profile updated in DynamoDB.");
  } catch (err) {
    console.error("Error updating user profile:", err.message);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const email = localStorage.getItem("userEmail");
  const name = localStorage.getItem("userName");
  const userDiv = document.getElementById("user-status");

  const summarySection = document.querySelector(".summary-container");
  const centerColumn = document.querySelector(".center-column");

  if (!userDiv) return;

  if (!email) {
    // Not logged in
    userDiv.innerHTML = `
      <a href="/login" style="font-size: 14px; color: #0056b3; text-decoration: underline;">Log in</a>
    `;

    // Hide portfolio and expand center column
    if (summarySection) summarySection.style.display = "none";
    if (centerColumn) centerColumn.style.flex = "3";

    return;
  }

  // Logged in
  userDiv.innerHTML = `
    <div>
      <a id="user-name" href="rc_portfolio.html" style="font-weight: bold; color: #0056b3; text-decoration: none;">${name || "Logged in"}</a><br>
      <a href="#" onclick="logout()" style="font-size: 12px; color: #0056b3; text-decoration: underline;">Log out</a>
    </div>
  `;

});

