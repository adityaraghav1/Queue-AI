const accessToken = localStorage.getItem("access_token");

const userNameElement = document.getElementById("user-name");
const userEmailElement = document.getElementById("user-email");
const userAvatarElement = document.getElementById("user-avatar");

const ticketsTableBody = document.getElementById("tickets-table-body");
const dashboardMessage = document.getElementById("dashboard-message");

const ticketModal = document.getElementById("ticket-modal");
const ticketForm = document.getElementById("ticket-form");
const ticketFormMessage = document.getElementById("ticket-form-message");


// Redirect to login if no token exists.
if (!accessToken) {
    window.location.replace("/");
}


// Make authenticated API requests.
async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            ...options.headers,
            Authorization: `Bearer ${accessToken}`
        }
    });

    if (response.status === 401) {
        localStorage.removeItem("access_token");
        window.location.replace("/");
        throw new Error("Your session has expired. Please sign in again.");
    }

    return response;
}


// Display a message on the dashboard.
function showDashboardMessage(message, type = "") {
    dashboardMessage.textContent = message;
    dashboardMessage.className = "message";

    if (type) {
        dashboardMessage.classList.add(type);
    }
}


// Load the logged-in user's profile.
async function loadCurrentUser() {
    const response = await apiRequest("/auth/me");

    if (!response.ok) {
        throw new Error("Unable to load your profile.");
    }

    const user = await response.json();

    userNameElement.textContent = user.name;
    userEmailElement.textContent = user.email;
    userAvatarElement.textContent =
        user.name.trim().charAt(0).toUpperCase() || "U";
}


// Convert status values into readable text.
function formatStatus(status) {
    return status
        .replaceAll("_", " ")
        .replace(/\b\w/g, character => character.toUpperCase());
}


// Create a table cell safely.
function createCell(text) {
    const cell = document.createElement("td");
    cell.textContent = text ?? "—";
    return cell;
}


// Create a ticket title cell.
function createTicketTitleCell(ticket) {
    const cell = document.createElement("td");

    const title = document.createElement("div");
    title.className = "ticket-title";
    title.textContent = ticket.subject || "Untitled ticket";

    const ticketId = document.createElement("small");
    ticketId.className = "ticket-id";
    ticketId.textContent = `ID: #${ticket.id}`;

    cell.append(title, ticketId);

    return cell;
}


// Create a styled status or priority badge.
function createBadge(value, prefix) {
    const badge = document.createElement("span");

    const normalizedValue = String(value || "unknown").toLowerCase();

    badge.className = `${prefix}-badge ${prefix}-${normalizedValue}`;
    badge.textContent = formatStatus(normalizedValue);

    return badge;
}


// Load tickets belonging to the current customer.
async function loadTickets() {
    ticketsTableBody.replaceChildren();

    const loadingRow = document.createElement("tr");
    const loadingCell = createCell("Loading your tickets...");
    loadingCell.colSpan = 5;
    loadingCell.className = "empty-state";

    loadingRow.appendChild(loadingCell);
    ticketsTableBody.appendChild(loadingRow);

    try {
        const response = await apiRequest("/tickets/my");

        if (!response.ok) {
            throw new Error("Unable to load your tickets.");
        }

        const tickets = await response.json();

        // Update dashboard statistics.
        document.getElementById("total-tickets").textContent =
            tickets.length;

        document.getElementById("open-tickets").textContent =
            tickets.filter(ticket => ticket.status === "open").length;

        document.getElementById("progress-tickets").textContent =
            tickets.filter(ticket => ticket.status === "in_progress").length;

        document.getElementById("resolved-tickets").textContent =
            tickets.filter(ticket => ticket.status === "resolved").length;

        ticketsTableBody.replaceChildren();

        if (tickets.length === 0) {
            const row = document.createElement("tr");
            const cell = createCell(
                "No tickets yet. Create your first support ticket!"
            );

            cell.colSpan = 5;
            cell.className = "empty-state";

            row.appendChild(cell);
            ticketsTableBody.appendChild(row);

            return;
        }

        // Show the newest tickets first.
        tickets.forEach(ticket => {
            const row = document.createElement("tr");

            row.appendChild(createTicketTitleCell(ticket));
            row.appendChild(createCell(ticket.category || "Pending"));

            const priorityCell = document.createElement("td");
            priorityCell.appendChild(
                createBadge(ticket.priority || "unknown", "priority")
            );
            row.appendChild(priorityCell);

            const statusCell = document.createElement("td");
            statusCell.appendChild(
                createBadge(ticket.status, "status")
            );
            row.appendChild(statusCell);

            const createdAt = ticket.created_at
                ? new Date(ticket.created_at).toLocaleDateString()
                : "—";

            row.appendChild(createCell(createdAt));

            ticketsTableBody.appendChild(row);
        });

    } catch (error) {
        showDashboardMessage(error.message, "error");

        ticketsTableBody.replaceChildren();

        const row = document.createElement("tr");
        const cell = createCell("Could not load tickets.");

        cell.colSpan = 5;
        cell.className = "empty-state";

        row.appendChild(cell);
        ticketsTableBody.appendChild(row);
    }
}


// Open and close the ticket creation modal.
function openTicketModal() {
    ticketFormMessage.textContent = "";
    ticketFormMessage.className = "message";
    ticketModal.hidden = false;

    document.getElementById("ticket-subject").focus();
}

function closeTicketModal() {
    ticketModal.hidden = true;
}

document.getElementById("open-ticket-button")
    .addEventListener("click", openTicketModal);

document.getElementById("header-create-button")
    .addEventListener("click", openTicketModal);

document.getElementById("close-ticket-button")
    .addEventListener("click", closeTicketModal);

document.getElementById("cancel-ticket-button")
    .addEventListener("click", closeTicketModal);

ticketModal.addEventListener("click", function (event) {
    if (event.target === ticketModal) {
        closeTicketModal();
    }
});


// Create a new ticket through the backend.
ticketForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const submitButton = document.getElementById("submit-ticket-button");

    const subject = document.getElementById("ticket-subject").value.trim();
    const description =
        document.getElementById("ticket-description").value.trim();

    if (!subject || !description) {
        ticketFormMessage.textContent =
            "Please enter both a subject and description.";

        ticketFormMessage.className = "message error";
        return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Submitting...";

    ticketFormMessage.textContent = "";
    ticketFormMessage.className = "message";

    try {
        const response = await apiRequest("/tickets", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                subject: subject,
                description: description
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to create the ticket."
            );
        }

        ticketForm.reset();

        closeTicketModal();

        showDashboardMessage(
            "Ticket created successfully! AI triage has been requested.",
            "success"
        );

        await loadTickets();

    } catch (error) {
        ticketFormMessage.textContent =
            error.message || "Unable to connect to the server.";

        ticketFormMessage.className = "message error";

    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Submit Ticket →";
    }
});


// Refresh tickets.
document.getElementById("refresh-tickets")
    .addEventListener("click", loadTickets);


// Sign out.
document.getElementById("logout-button")
    .addEventListener("click", function () {
        localStorage.removeItem("access_token");
        window.location.replace("/");
    });


// Initialize the dashboard.
async function initializeDashboard() {
    if (!accessToken) {
        return;
    }

    try {
        await loadCurrentUser();
        await loadTickets();

    } catch (error) {
        showDashboardMessage(error.message, "error");
    }
}

initializeDashboard();