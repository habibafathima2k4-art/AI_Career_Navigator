# AI Career Navigator

AI Career Navigator is a full-stack career guidance platform with:

- React + Vite frontend
- FastAPI backend
- PostgreSQL database
- assessment-driven recommendations
- roadmap resources
- private user history
- admin CRUD + analytics

## Project structure

```text
frontend/  React client
backend/   FastAPI app
```

## Local development

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

### Backend

```powershell
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Database setup

```powershell
cd backend
python -m app.db.init_db
python -m app.db.seed_db
```

### Promote an admin user

```powershell
cd backend
python -m app.db.promote_user your-email@example.com
```

## Environment files

### Backend example

Copy `backend/.env.example` to `backend/.env` and fill in production-safe values.

Key values:

- `ENVIRONMENT=development` or `production`
- `DATABASE_URL=postgresql+psycopg://...`
- `SECRET_KEY=<long random secret>`
- `ALLOWED_ORIGINS=["https://your-frontend-domain.com"]`

### Frontend example

Copy `frontend/.env.example` to `frontend/.env`.

- `VITE_API_BASE_URL=https://your-backend-domain.com/api`

## Deployment options

### Recommended simple deployment

Frontend:

- deploy `frontend` to Vercel or Netlify
- set `VITE_API_BASE_URL` to your deployed backend URL

Backend:

- deploy `backend` to Render, Railway, or Fly.io
- start command:

```text
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Database:

- use managed PostgreSQL from Render, Railway, Neon, or Supabase
- set `DATABASE_URL` in backend environment variables

### Optional Docker deployment

This repo includes:

- `backend/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml`

Run locally with Docker:

```powershell
docker compose up --build
```

Then initialize and seed the database from the backend container or your local backend shell.

## Production checklist

Before going live:

1. Set a strong `SECRET_KEY`
2. Use a managed PostgreSQL instance
3. Replace local `ALLOWED_ORIGINS` with your frontend domain
4. Confirm admin access is limited to your own account
5. Build the frontend with the production API URL
6. Keep `.env` files out of version control

## Recommended deployment stack

Use:

- Vercel for `frontend`
- Render for `backend`
- Neon for PostgreSQL

Detailed steps are in [DEPLOYMENT.md](C:\Users\WIN11\OneDrive\Desktop\AI_Career_Navigator\DEPLOYMENT.md).
