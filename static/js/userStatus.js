// /static/js/userStatus.js

function logout() {
  localStorage.removeItem("idToken");
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
  localStorage.removeItem("userEmail");
  localStorage.removeItem("userName");
  localStorage.removeItem("baseCurrency");
  window.location.href = "/login";
}

async function checkLoginStatusAndRenderName() {
  const token = localStorage.getItem("idToken");
  const email = localStorage.getItem("userEmail");
  const userDiv = document.getElementById("user-status");

  if (!token || !email || !userDiv) return;

  try {
    const res = await fetch("https://vx4p0qzss7.execute-api.us-east-1.amazonaws.com/default/getUserName", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": token
      },
      body: JSON.stringify({ email })
    });

    const data = await res.json();
    const name = data.first_name && data.last_name ? `${data.first_name} ${data.last_name}` : "Logged in";

    userDiv.innerHTML = `
      <div style="font-weight: bold; font-size: 14px;">${name}</div>
      <a href="#" onclick="logout()" style="font-size: 12px; color: #0056b3; text-decoration: underline;">Log out</a>
    `;
  } catch (err) {
    userDiv.innerHTML = `
      <div style="font-weight: bold; font-size: 14px;">Logged in</div>
      <a href="#" onclick="logout()" style="font-size: 12px; color: #0056b3; text-decoration: underline;">Log out</a>
    `;
  }
}

document.addEventListener("DOMContentLoaded", checkLoginStatusAndRenderName);
