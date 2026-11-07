# QueueAI 🎫
### AI-Powered Support Ticket Management System

QueueAI is an AI-powered support ticket management system built using FastAPI. It helps support teams efficiently manage customer complaints by automating ticket classification, priority detection, sentiment analysis, and response suggestions.

## 🚀 Live Demo

[**Visit QueueAI**](https://queueai-mhlw.onrender.com/)

## Features

- **User Authentication:** Secure registration and login using JWT authentication.
- **Role-Based Access Control:** Separate access and permissions for customers and administrators.
- **Ticket Management:** Create, view, and track support tickets.
- **AI Ticket Triage:** Automatically analyze tickets to identify category, priority, and customer sentiment.
- **AI Response Suggestions:** Generate suggested responses to customer complaints.
- **Admin Dashboard:** View all tickets, monitor ticket statistics, and manage ticket statuses.
- **Email Notifications:** Automated email notifications for important ticket updates.
- **Responsive Interface:** Clean dashboard interface for customers and administrators.

##  Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| SQLAlchemy | Database ORM |
| SQLite | Database |
| JWT | Authentication |
| Groq API | AI-powered ticket analysis |
| HTML, CSS, JavaScript | Frontend |
| Render | Deployment |


## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/adityaraghav1/Queue-AI.git
cd Queue-AI
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```env
DATABASE_URL=sqlite:///./queueai.db
SECRET_KEY=your_secret_key
GROQ_API_KEY=your_groq_api_key
```

Add SMTP configuration if email notifications are enabled.

### 5. Start the application

```bash
uvicorn app.main:app --reload
```

Visit **http://127.0.0.1:8000** to access QueueAI.

API documentation is available at **http://127.0.0.1:8000/docs**.

## 📂 Project Structure

```text
Queue-AI/
├── app/
│   ├── routes/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── templates/
│   ├── static/
│   ├── database.py
│   └── main.py
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## 👨‍💻 Author

**Aditya Raghav**

---

⭐ If you find QueueAI interesting, consider giving this repository a star!
