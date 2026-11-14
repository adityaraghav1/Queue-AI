# QueueAI

AI-powered customer support ticket management and triage platform built with **FastAPI**, **Groq**, and a responsive vanilla **HTML / CSS / JavaScript** frontend.

**Live Demo:** [queueai-mhlw.onrender.com](https://queueai-mhlw.onrender.com/)

---

## Overview

QueueAI streamlines customer support by automatically analyzing incoming tickets—detecting category, priority, and sentiment—and generating draft replies for support administrators to review, edit, and send.

## Key Features

- **JWT Authentication & Role-Based Access:** Separate workspaces and permissions for customers and administrators.
- **Customer Dashboard:** Submit support tickets, view real-time ticket metrics, and track status updates (`Open`, `In Progress`, `Resolved`, `Closed`).
- **AI Ticket Triage:** Automatically classifies category, urgency/priority, and sentiment on ticket creation using the Groq API.
- **AI Response Drafts:** Generates suggested replies for each ticket inside the admin review modal.
- **Admin Console:** Monitor overall ticket metrics, inspect customer requests, update ticket statuses, and publish final responses.
- **Email Notifications:** Sends automated email updates to customers when a ticket is resolved.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database | SQLAlchemy, SQLite |
| Auth | JWT (Bearer tokens) |
| AI Triage | Groq API |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Hosting | Render |

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/adityaraghav1/Queue-AI.git
cd Queue-AI
