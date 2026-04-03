# Deployment Guide

This project is ready to deploy with:

- Frontend: Vercel
- Backend: Render
- Database: Neon PostgreSQL

## 1. Push the project to GitHub

Create a GitHub repository and push this project there. Both Vercel and Render will deploy from that repo.

## 2. Deploy the database on Neon

1. Create a Neon project.
2. Create a database named `ai_career_navigator`.
3. Copy the connection string.

Your backend `DATABASE_URL` should look like:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST/ai_career_navigator?sslmode=require
```

## 3. Deploy the backend on Render

Create a new Web Service on Render and point it to the repo.

### Backend settings

- Root Directory: `backend`
- Runtime: `Python`
- Build Command:

```text
pip install -r requirements.txt
```

- Start Command:

```text
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Backend environment variables

Set these in Render:

```env
ENVIRONMENT=production
APP_NAME=AI Career Navigator API
API_PREFIX=/api
DATABASE_URL=your_neon_database_url
SECRET_KEY=use-a-long-random-secret
ALLOWED_ORIGINS=["https://your-vercel-domain.vercel.app"]
```

### After first backend deploy

Open the Render shell or run locally against the production database:

```text
python -m app.db.init_db
python -m app.db.seed_db
python -m app.db.promote_user your-email@example.com
```

Do this once so production has tables, starter content, and your admin account.

## 4. Deploy the frontend on Vercel

Create a new Vercel project and point it to the same repo.

### Frontend settings

- Root Directory: `frontend`
- Framework Preset: `Vite`

### Frontend environment variable

```env
VITE_API_BASE_URL=https://your-render-backend.onrender.com/api
```

Deploy after setting that value.

## 5. Final checks

After both deployments:

1. Open the frontend URL.
2. Register or log in.
3. Submit an assessment.
4. Open history.
5. Open admin and confirm analytics + CRUD work.

## 6. Production notes

- Keep `SECRET_KEY` private and strong.
- Keep `.env` files out of version control.
- Restrict `ALLOWED_ORIGINS` to your real frontend domain.
- If you reseed production later, avoid duplicating starter content.
