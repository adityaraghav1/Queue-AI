const registerForm = document.getElementById("register-form");
const registerMessage = document.getElementById("register-message");
const registerButton = document.getElementById("register-button");

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    registerMessage.className = "message";
    registerMessage.textContent = "";

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    registerButton.disabled = true;
    registerButton.innerHTML = "<span>Creating account...</span>";

    try {
        const response = await fetch("/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            const detail = data.detail;

            let errorMessage = "Registration failed. Please try again.";

            if (typeof detail === "string") {
                errorMessage = detail;
            } else if (Array.isArray(detail)) {
                errorMessage = detail
                    .map(item => item.msg)
                    .join(", ");
            }

            throw new Error(errorMessage);
        }

        registerMessage.textContent =
            "Account created successfully! Redirecting to login...";

        registerMessage.classList.add("success");

        registerForm.reset();

        setTimeout(function () {
            window.location.href = "/";
        }, 1500);

    } catch (error) {
        registerMessage.textContent =
            error.message || "Unable to connect to the server.";

        registerMessage.classList.add("error");

    } finally {
        registerButton.disabled = false;
        registerButton.innerHTML =
            "<span>Create account</span><span aria-hidden=\"true\">→</span>";
    }
});