# AI Career Navigator

AI Career Navigator is a full-stack web application that helps users discover suitable career paths through guided assessment, ranked recommendations, roadmap resources, and progress tracking.

The platform is built for students and early professionals who want clearer direction about which career fits their profile, what skills they already have, what gaps remain, and which learning resources can help them move forward.

## Live Deployment

- Frontend: [AI Career Navigator](https://ai-career-navigator-gules.vercel.app)
- Backend API: [Render Backend](https://ai-career-navigator-backend-ax95.onrender.com)
- API Docs: [Swagger UI](https://ai-career-navigator-backend-ax95.onrender.com/docs)
- Source Code: [GitHub Repository](https://github.com/habibafathima2k4-art/AI_Career_Navigator)

## Key Features

- User registration and login
- Guided career assessment based on interests, education, experience, work style, salary goals, and skills
- Ranked career recommendations with fit score and confidence score
- Career detail pages with salary range, growth outlook, core skills, and support skills
- Roadmap resources across courses, projects, articles, videos, certifications, and documentation
- Roadmap progress tracking with saved, in-progress, and completed states
- Assessment history and progress summary dashboard
- Admin dashboard for managing careers, skills, and roadmap resources
- Backend API documentation through Swagger

## Technology Stack

### Frontend

- React
- Vite
- React Router
- Custom CSS

### Backend

- FastAPI
- SQLAlchemy
- Pydantic
- Psycopg

### Database and Deployment

- PostgreSQL
- Neon
- Render
- Vercel
- GitHub

## Project Structure

```text
AI_Career_Navigator/
├── backend/      FastAPI backend application
├── frontend/     React + Vite frontend
├── docs/         Diagrams and documentation assets
├── dataset/      Project dataset files
├── README.md
└── DEPLOYMENT.md
```

## Core Modules

### 1. Authentication Module

Handles user registration, login, protected access, and account-based history.

### 2. Assessment Module

Collects user profile inputs such as interest area, education level, experience level, preferred domain, work style, salary goal, and skill inventory.

### 3. Recommendation Engine

Matches user assessment data against stored careers and required skills to generate ranked recommendations.

### 4. Career Detail and Roadmap Module

Displays salary outlook, core and support skills, roadmap resources, resume suggestions, and project ideas for each career.

### 5. Progress and History Module

Stores resource progress and assessment history so users can revisit and continue their roadmap.

### 6. Admin Module

Allows admin users to manage careers, skills, and learning resources through CRUD operations.

## Database Design

Important tables used in the project:

- `users`
- `assessments`
- `skills`
- `careers`
- `career_skills`
- `learning_resources`
- `recommendations`
- `recommendation_skill_gaps`
- `user_progress`

## Local Setup

## 1. Clone the repository

```powershell
git clone https://github.com/habibafathima2k4-art/AI_Career_Navigator.git
cd AI_Career_Navigator
```

## 2. Backend setup

```powershell
cd backend
pip install -r requirements.txt
```

Create `backend/.env` from `backend/.env.example` and set:

```env
ENVIRONMENT=development
APP_NAME=AI Career Navigator API
API_PREFIX=/api
DATABASE_URL=postgresql+psycopg://...
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=["http://localhost:5173"]
```

Initialize and seed the database:

```powershell
python -m app.db.init_db
python -m app.db.seed_db
```

Start the backend:

```powershell
python -m uvicorn app.main:app --reload
```

## 3. Frontend setup

Open a new terminal:

```powershell
cd frontend
npm install
```

Create `frontend/.env` from `frontend/.env.example` and set:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

Start the frontend:

```powershell
npm run dev
```

## 4. Promote an admin user

After registering your account, you can promote it locally with:

```powershell
cd backend
python -m app.db.promote_user your-email@example.com
```

## Deployment

Recommended production stack:

- Frontend: Vercel
- Backend: Render
- Database: Neon PostgreSQL

Detailed deployment instructions are available in [DEPLOYMENT.md](C:\Users\WIN11\OneDrive\Desktop\AI_Career_Navigator\DEPLOYMENT.md).

## Testing

Backend progress API tests are included in:

- [backend/tests/test_resource_progress_api.py](C:\Users\WIN11\OneDrive\Desktop\AI_Career_Navigator\backend\tests\test_resource_progress_api.py)

Run tests with:

```powershell
cd backend
python -m pytest tests\test_resource_progress_api.py -q
```

## Sample User Flow

1. User registers or logs in.
2. User completes the career assessment.
3. User selects existing skills.
4. System generates ranked career recommendations.
5. User opens a career detail page.
6. User explores roadmap resources and tracks progress.
7. User revisits assessment history and continues roadmap work.

## Future Scope

- Career comparison view
- Export recommendations as PDF
- Notification or reminder support
- Expanded backend test coverage
- More advanced recommendation scoring

## Author

Developed as a full-stack academic project for career guidance and roadmap planning.
