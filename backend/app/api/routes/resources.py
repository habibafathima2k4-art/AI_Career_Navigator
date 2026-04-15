from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.resource import (
    LearningResourceResponse,
    ResourceProgressResponse,
    ResourceProgressUpdate,
)
from app.services.resource_service import (
    delete_user_resource_progress,
    get_resource,
    list_resources,
    list_user_resource_progress,
    upsert_user_resource_progress,
)

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


@router.get("/progress", response_model=list[ResourceProgressResponse])
def get_resource_progress(
    career_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ResourceProgressResponse]:
    progress_entries = list_user_resource_progress(db, user_id=current_user.id, career_id=career_id)
    return [ResourceProgressResponse.model_validate(progress) for progress in progress_entries]


@router.put("/{resource_id}/progress", response_model=ResourceProgressResponse)
def update_resource_progress(
    resource_id: int,
    payload: ResourceProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResourceProgressResponse:
    resource = get_resource(db, resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found.")

    progress = upsert_user_resource_progress(
        db,
        user_id=current_user.id,
        resource_id=resource_id,
        status=payload.status,
    )
    return ResourceProgressResponse.model_validate(progress)


@router.delete("/{resource_id}/progress", status_code=status.HTTP_204_NO_CONTENT)
def clear_resource_progress(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    resource = get_resource(db, resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found.")

    delete_user_resource_progress(db, user_id=current_user.id, resource_id=resource_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
