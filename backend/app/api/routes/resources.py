from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.resource import LearningResourceResponse
from app.services.resource_service import list_resources

router = APIRouter()


@router.get("/", response_model=list[LearningResourceResponse])
def get_resources(
    career_id: int | None = Query(default=None, gt=0),
    skill_id: int | None = Query(default=None, gt=0),
    limit: int | None = Query(default=None, gt=0, le=20),
    db: Session = Depends(get_db),
) -> list[LearningResourceResponse]:
    resources = list_resources(db, career_id=career_id, skill_id=skill_id, limit=limit)
    return [LearningResourceResponse.model_validate(resource) for resource in resources]
