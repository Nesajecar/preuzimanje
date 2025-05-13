 document.querySelector("form").addEventListener("submit", async function(e) {
  e.preventDefault();

  const email = document.querySelector('input[name="email-login"]').value;
  const password = document.querySelector('input[name="password-login"]').value;

  try {
    const response = await fetch("https://x8ki-letl-twmt.n7.xano.io/api:KX8HYdxj/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok) {
      const checkbox = document.querySelector('input[name="Checkbox"]');
      const remember = checkbox ? checkbox.checked : false;
			console.log("Remember me checked:", remember);
      const token = data.authToken?.token || data.authToken || null;
      if (!token) {
        alert("Token nije pronađen u odgovoru.");
        return;
      }

      // Čuvanje tokena
      if (remember) {
        localStorage.setItem("auth_token", token);
      } else {
        sessionStorage.setItem("auth_token", token);
      }

      window.location.href = "/dashboard";
    } else {
      alert(data.message || "Neuspešan login.");
    }
  } catch (err) {
    console.error(err);
    alert("Greška prilikom logovanja.");
  }
});
