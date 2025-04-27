# Student Information Chatbot System

The Student Information Chatbot is a web application that allows university students, faculty, and administrators to retrieve academic and administrative information through a conversational interface.

---
## Table of Contents
1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Environment Variables](#environment-variables)
7. [Database Bootstrap](#database-bootstrap)
8. [Running Locally](#running-locally)
9. [Testing Accounts](#testing-accounts)
10. [API Overview](#api-overview)

---
## Features
- Natural‑language queries are converted to SQL and executed against MySQL.
- Separate API endpoints for students, faculty, and administrators with role‑based access control.
- Responsive React user interface with login, chat, profile, help, and menu panels.
- Hot‑reload development experience for both backend and frontend.

## Technology Stack
| Layer | Technology |
|-------|------------|
| Backend | FastAPI, SQLAlchemy, MySQL, OpenAI SDK |
| Frontend | React 18, Tailwind CSS |
| Development | Python 3.8+, Node.js 18+, Git |

## Project Structure
```text
chatbot-env/
├── backend/
│   └── app/
│       ├── .env                # Backend secrets (not committed)
│       ├── create_tables.py    # One‑time DB schema creator
│       ├── database.py         # SQLAlchemy engine/session helpers
│       ├── main.py             # FastAPI entry point
│       ├── models.py           # ORM table definitions
│       ├── nl_to_sql.py        # Natural language to SQL logic
│       └── routers/
│           ├── student.py
│           ├── faculty.py
│           └── admin.py
└── frontend/
    └── src/
        ├── App.js
        ├── App.css
        └── components/
            ├── Auth/
            ├── Chat/
            ├── Icons/
            └── Panels/
```

## Prerequisites
- Python 3.8 or higher
- Node.js 18 LTS or higher and npm
- MySQL 8.0 (or compatible MariaDB)
- System build tools (GCC, Xcode command‑line tools, or Visual Studio Build Tools)

## Installation

### Backend
```bash
cd chatbot-env/backend/app
pip install -r requirements.txt
```

### Frontend
```bash
cd chatbot-env/frontend
npm install
```

## Environment Variables

**backend/app/.env**
```
DB_URL=mysql+mysqlconnector://<user>:<password>@localhost:3306/student_chatbot
OPENAI_API_KEY=sk-********************************
```

**frontend/.env**
```
REACT_APP_API_URL=http://127.0.0.1:8000
```

## Database Bootstrap
Run the following command once to create all tables:

```bash
cd chatbot-env/backend/app
python create_tables.py
```

## Running Locally
```bash
# Backend
uvicorn main:app --reload --port 8000

# Frontend
cd chatbot-env/frontend
npm start
```
The API will be available at `http://127.0.0.1:8000` and the React interface at `http://localhost:3000`.

## Testing Accounts
| Role | User ID | Password |
|------|---------|----------|
| Student | ID0003 | mia35 |
| Faculty | F005   | martinez123 |
| Admin   | adm_007| grace123 |

## API Overview
| Router | Base Path | Selected Endpoints |
|--------|-----------|--------------------|
| student | /student | GET /gpa/{student_id}, GET /tuition/{student_id} |
| faculty | /faculty | GET /personal/{student_id}, GET /attendance/{student_id} |
| admin   | /admin   | GET /tuition/{student_id}, GET /id_card/{student_id} |
