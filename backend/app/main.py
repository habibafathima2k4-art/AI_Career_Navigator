from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import admin, assessments, auth, careers, health, resources, skills
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    openapi_url=f"{settings.api_prefix}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.api_prefix, tags=["health"])
app.include_router(auth.router, prefix=f"{settings.api_prefix}/auth", tags=["auth"])
app.include_router(admin.router, prefix=f"{settings.api_prefix}/admin", tags=["admin"])
app.include_router(
    careers.router, prefix=f"{settings.api_prefix}/careers", tags=["careers"]
)
app.include_router(skills.router, prefix=f"{settings.api_prefix}/skills", tags=["skills"])
app.include_router(
    resources.router, prefix=f"{settings.api_prefix}/resources", tags=["resources"]
)
app.include_router(
    assessments.router,
    prefix=f"{settings.api_prefix}/assessments",
    tags=["assessments"],
)


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    return {"message": f"{settings.app_name} backend is running."}
