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
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

- **Windows:** `.venv\Scripts\activate`
- **macOS / Linux:** `source .venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (see `.env.example` for optional SMTP email settings):

```env
DATABASE_URL=sqlite:///./queueai.db
SECRET_KEY=your_secret_key
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

- App: `http://127.0.0.1:8000`
- Interactive API Docs (Swagger): `http://127.0.0.1:8000/docs`

## Project Structure

```text
Queue-AI/
├── app/
│   ├── models/        # SQLAlchemy database models
│   ├── routes/        # Auth, ticket, and page routes
│   ├── schemas/       # Pydantic request/response schemas
│   ├── services/      # AI triage and email services
│   ├── static/        # CSS, JS, and favicon assets
│   ├── templates/     # HTML views (login, register, dashboards)
│   ├── database.py    # Database session & engine setup
│   └── main.py        # FastAPI application entry point
├── tests/             # Automated tests
├── .env.example
├── requirements.txt
└── README.md
```

## Author

**Aditya Raghav** 
