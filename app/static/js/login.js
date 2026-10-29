const loginForm = document.getElementById("login-form");
const loginMessage = document.getElementById("login-message");
const loginButton = document.getElementById("login-button");

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    loginMessage.className = "message";
    loginMessage.textContent = "";

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    loginButton.disabled = true;
    loginButton.innerHTML = "<span>Signing in...</span>";

    try {
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Login failed. Please try again."
            );
        }

localStorage.setItem("access_token", data.access_token);

loginMessage.textContent = "Login successful! Redirecting...";
loginMessage.classList.add("success");

try {
    const profileResponse = await fetch("/auth/me", {
        headers: {
            Authorization: `Bearer ${data.access_token}`
        }
    });

    if (!profileResponse.ok) {
        throw new Error("Unable to retrieve your user profile.");
    }

    const user = await profileResponse.json();

    setTimeout(() => {
        if (user.role === "admin") {
            window.location.href = "/admin-dashboard";
        } else {
            window.location.href = "/dashboard";
        }
    }, 700);

} catch (error) {
    localStorage.removeItem("access_token");

    loginMessage.textContent =
        error.message || "Unable to complete login.";

    loginMessage.className = "message error";
}

    } catch (error) {
        loginMessage.textContent =
            error.message || "Unable to connect to the server.";

        loginMessage.classList.add("error");

    } finally {
        loginButton.disabled = false;
        loginButton.innerHTML =
            "<span>Sign in</span><span aria-hidden=\"true\">→</span>";
    }
});