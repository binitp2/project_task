# WhatsEase -  WhatsApp-like Chat App (FastAPI + React)

WhatsEase is a full-stack, WhatsApp-like web chat application with real-time messaging and an AI bot. It demonstrates Python (FastAPI) backend skills, PostgreSQL with SQLAlchemy, JWT authentication, WebSocket-based real-time updates, and a React frontend without UI frameworks.

### Features
- FastAPI backend with PostgreSQL (SQLAlchemy)
- JWT-based auth (register/login)
- RESTful CRUD for users and messages
- Real-time messaging over WebSockets (user↔user, user↔bot)
- AI bot (WhatsEase) with simple intents and context retention
- Activity log for user/bot events
- React frontend (no UI frameworks) with routing, accessibility, and responsive CSS
- Search/filter chats and users
- Seed data for quick testing

### Monorepo Layout
- `backend/` — FastAPI app, WebSocket, bot, DB models, JWT auth, logging
- `frontend/` — React app (Vite), chat UI, WebSocket client

---

Default users after seeding:
- alice@example.com / password@123
- bob@example.com / password@123
charlie@example.com / password@123

### Backend

1. Install dependencies:
   ```
   cd backend
   python -m venv .venv && . .venv/Scripts/activate    # Windows PowerShell: . .venv/Scripts/Activate.ps1
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
2. Seed data:
   ```
   python -m app.seed
   ```

### Frontend
Requirements: Node 18+

1. Setup env: `cp frontend/.env.example frontend/.env`
2. Install and run:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```
3. Visit `http://localhost:5173`

---

If you Cannot able to login due to some issue then check in WhatsEase API - Swagger UI: `http://127.0.0.1:8000/docs#`  
In WhatsEase API you can test your API using Adding Some value and check validation for Registering, Login etc.

## Environment Variables

### Backend (`backend/.env`)
- `DATABASE_URL`=postgresql+psycopg2://postgres:postgres@db:5432/whats_ease
- `JWT_SECRET`=change_me
- `ACCESS_TOKEN_EXPIRE_MINUTES`=1440
- `ALLOWED_ORIGINS`=http://localhost:5173
- `LOG_LEVEL`=INFO

### Frontend (`frontend/.env`)
- `VITE_API_BASE`=http://localhost:8000
- `VITE_WS_URL`=ws://localhost:8000/ws

---

## API Overview

- Auth
  - POST `/auth/register` — register
  - POST `/auth/login` — login → JWT token
- Users
  - GET `/users/me` — current user
  - GET `/users` — list users
- Messages
  - GET `/messages` — list by peer (query `peer`)
  - POST `/messages` — create
  - POST `/messages/{message_id}/read` — mark read
- Activity
  - GET `/activity` — recent events
- WebSocket
  - `GET ws://.../ws?token=JWT`
  - Client sends `{ type: "send_message", recipient, content }`
  - Server emits delivery/read updates and incoming messages

---



