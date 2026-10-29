const accessToken = localStorage.getItem("access_token");

const adminName = document.getElementById("admin-name");
const adminEmail = document.getElementById("admin-email");
const adminAvatar = document.getElementById("admin-avatar");

const ticketsTableBody = document.getElementById(
    "admin-tickets-table-body"
);

const dashboardMessage = document.getElementById(
    "admin-dashboard-message"
);

const ticketModal = document.getElementById("admin-ticket-modal");
const ticketForm = document.getElementById("admin-ticket-form");

let allTickets = [];
let selectedTicket = null;


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


// Display dashboard messages.
function showDashboardMessage(message, type = "") {
    dashboardMessage.textContent = message;
    dashboardMessage.className = "message";

    if (type) {
        dashboardMessage.classList.add(type);
    }
}


// Display form messages.
function showFormMessage(message, type = "") {
    const element = document.getElementById(
        "admin-ticket-form-message"
    );

    element.textContent = message;
    element.className = "message";

    if (type) {
        element.classList.add(type);
    }
}


// Read API error messages safely.
async function getErrorMessage(response, fallback) {
    try {
        const data = await response.json();

        if (typeof data.detail === "string") {
            return data.detail;
        }

        if (Array.isArray(data.detail)) {
            return data.detail
                .map(error => error.msg || "Invalid input")
                .join(", ");
        }
    } catch {
        // The response may not contain JSON.
    }

    return fallback;
}


// Load the logged-in user and verify the admin role.
async function loadAdminProfile() {
    const response = await apiRequest("/auth/me");

    if (!response.ok) {
        throw new Error(
            await getErrorMessage(response, "Unable to load your profile.")
        );
    }

    const user = await response.json();

    if (user.role !== "admin") {
        localStorage.removeItem("access_token");
        window.location.replace("/");
        return false;
    }

    adminName.textContent = user.name;
    adminEmail.textContent = user.email;

    adminAvatar.textContent =
        user.name.trim().charAt(0).toUpperCase() || "A";

    return true;
}


// Format status text.
function formatStatus(status) {
    return String(status || "unknown")
        .replaceAll("_", " ")
        .replace(/\b\w/g, character => character.toUpperCase());
}


// Create a safe table cell.
function createCell(value) {
    const cell = document.createElement("td");
    cell.textContent = value ?? "—";
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


// Create a status or priority badge.
function createBadge(value, prefix) {
    const normalizedValue = String(value || "unknown").toLowerCase();

    const badge = document.createElement("span");
    badge.className = `${prefix}-badge ${prefix}-${normalizedValue}`;
    badge.textContent = formatStatus(normalizedValue);

    return badge;
}


// Update admin statistics.
function updateStatistics(tickets) {
    document.getElementById("admin-total-tickets").textContent =
        tickets.length;

    document.getElementById("admin-open-tickets").textContent =
        tickets.filter(ticket => ticket.status === "open").length;

    document.getElementById("admin-progress-tickets").textContent =
        tickets.filter(ticket => ticket.status === "in_progress").length;

    document.getElementById("admin-resolved-tickets").textContent =
        tickets.filter(ticket => ticket.status === "resolved").length;
}


// Display all tickets in the table.
function renderTickets(tickets) {
    ticketsTableBody.replaceChildren();

    if (tickets.length === 0) {
        const row = document.createElement("tr");
        const cell = createCell("No support tickets found.");

        cell.colSpan = 7;
        cell.className = "empty-state";

        row.appendChild(cell);
        ticketsTableBody.appendChild(row);

        return;
    }

    tickets.forEach(ticket => {
        const row = document.createElement("tr");

        row.appendChild(createTicketTitleCell(ticket));

        // TicketResponse may expose customer_id without customer details.
        row.appendChild(
            createCell(
                ticket.customer_name ||
                (ticket.customer_id != null
                    ? `Customer #${ticket.customer_id}`
                    : "Unknown customer")
            )
        );

        row.appendChild(
            createCell(ticket.category || "Pending")
        );

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

        const actionCell = document.createElement("td");
        const actionContainer = document.createElement("div");

        actionContainer.className = "admin-ticket-actions";

        const viewButton = document.createElement("button");
        viewButton.type = "button";
        viewButton.className = "admin-view-button";
        viewButton.textContent = "View";

        viewButton.addEventListener("click", () => {
            openTicketDetails(ticket.id);
        });

        actionContainer.appendChild(viewButton);
        actionCell.appendChild(actionContainer);
        row.appendChild(actionCell);

        ticketsTableBody.appendChild(row);
    });
}


// Load all tickets from the admin-only endpoint.
async function loadTickets() {
    ticketsTableBody.replaceChildren();

    const loadingRow = document.createElement("tr");
    const loadingCell = createCell("Loading tickets...");

    loadingCell.colSpan = 7;
    loadingCell.className = "empty-state";

    loadingRow.appendChild(loadingCell);
    ticketsTableBody.appendChild(loadingRow);

    try {
        const response = await apiRequest("/tickets/");

        if (!response.ok) {
            throw new Error(
                await getErrorMessage(
                    response,
                    "Unable to load support tickets."
                )
            );
        }

        allTickets = await response.json();

        updateStatistics(allTickets);
        renderTickets(allTickets);

        showDashboardMessage(
            `Loaded ${allTickets.length} support ticket(s).`,
            "success"
        );

    } catch (error) {
        showDashboardMessage(error.message, "error");

        ticketsTableBody.replaceChildren();

        const row = document.createElement("tr");
        const cell = createCell("Could not load tickets.");

        cell.colSpan = 7;
        cell.className = "empty-state";

        row.appendChild(cell);
        ticketsTableBody.appendChild(row);
    }
}


// Open the details modal for a selected ticket.
function openTicketDetails(ticketId) {
    selectedTicket = allTickets.find(
        ticket => ticket.id === ticketId
    );

    if (!selectedTicket) {
        showDashboardMessage("Ticket not found.", "error");
        return;
    }

    document.getElementById("admin-modal-title").textContent =
        `Ticket #${selectedTicket.id}`;

    document.getElementById("detail-customer").textContent =
        selectedTicket.customer_name ||
        (selectedTicket.customer_id != null
            ? `Customer #${selectedTicket.customer_id}`
            : "Unknown customer");

    document.getElementById("detail-subject").textContent =
        selectedTicket.subject || "Untitled ticket";

    document.getElementById("detail-description").textContent =
        selectedTicket.description || "No description provided.";

    document.getElementById("detail-suggestion").textContent =
        selectedTicket.suggested_response ||
        "No AI suggestion available.";

    document.getElementById("admin-ticket-status").value =
        selectedTicket.status || "open";

    document.getElementById("admin-final-response").value =
        selectedTicket.final_response || "";

    showFormMessage("");

    ticketModal.hidden = false;
}


// Close the details modal.
function closeTicketModal() {
    ticketModal.hidden = true;
    selectedTicket = null;
}

document.getElementById("admin-close-modal")
    .addEventListener("click", closeTicketModal);

document.getElementById("admin-cancel-modal")
    .addEventListener("click", closeTicketModal);

ticketModal.addEventListener("click", function (event) {
    if (event.target === ticketModal) {
        closeTicketModal();
    }
});


// Save status changes or resolve a ticket with a final response.
ticketForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    if (!selectedTicket) {
        showFormMessage("Please select a ticket first.", "error");
        return;
    }

    const saveButton = document.getElementById(
        "admin-save-ticket-button"
    );

    const desiredStatus = document.getElementById(
        "admin-ticket-status"
    ).value;

    const finalResponse = document.getElementById(
        "admin-final-response"
    ).value.trim();

    // A resolution response should not be empty.
    if (desiredStatus === "resolved" && !finalResponse) {
        showFormMessage(
            "Enter a final response before resolving this ticket.",
            "error"
        );
        return;
    }

    saveButton.disabled = true;
    saveButton.textContent = "Saving...";

    try {
        // The response endpoint saves the response, marks the ticket
        // resolved, and attempts to send the customer an email.
        if (desiredStatus === "resolved") {
            const responseResult = await apiRequest(
                `/tickets/${selectedTicket.id}/response`,
                {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        final_response: finalResponse
                    })
                }
            );

            if (!responseResult.ok) {
                throw new Error(
                    await getErrorMessage(
                        responseResult,
                        "Unable to resolve this ticket."
                    )
                );
            }

        } else {
            // Update status without sending a resolution email.
            const statusResult = await apiRequest(
                `/tickets/${selectedTicket.id}/status`,
                {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        status: desiredStatus
                    })
                }
            );

            if (!statusResult.ok) {
                throw new Error(
                    await getErrorMessage(
                        statusResult,
                        "Unable to update ticket status."
                    )
                );
            }
        }

        closeTicketModal();

        showDashboardMessage(
            desiredStatus === "resolved"
                ? "Ticket resolved. Email notification was attempted."
                : "Ticket status updated successfully.",
            "success"
        );

        await loadTickets();

    } catch (error) {
        showFormMessage(error.message, "error");

    } finally {
        saveButton.disabled = false;
        saveButton.textContent = "Save Changes";
    }
});


// Refresh tickets.
document.getElementById("admin-refresh-button")
    .addEventListener("click", loadTickets);


// Sign out.
document.getElementById("admin-logout-button")
    .addEventListener("click", function () {
        localStorage.removeItem("access_token");
        window.location.replace("/");
    });


// Initialize the admin dashboard.
async function initializeAdminDashboard() {
    if (!accessToken) {
        return;
    }

    try {
        const isAdmin = await loadAdminProfile();

        if (isAdmin) {
            await loadTickets();
        }

    } catch (error) {
        showDashboardMessage(error.message, "error");
    }
}

initializeAdminDashboard();