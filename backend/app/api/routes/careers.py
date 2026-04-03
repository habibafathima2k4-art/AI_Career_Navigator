from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.career import CareerDetailResponse, CareerResponse
from app.services.career_service import get_career_by_id, list_active_careers

router = APIRouter()

@router.get("/", response_model=list[CareerResponse])
def list_careers(db: Session = Depends(get_db)) -> list[CareerResponse]:
    careers = list_active_careers(db)
    return [CareerResponse.model_validate(career) for career in careers]


@router.get("/{career_id}", response_model=CareerDetailResponse)
def get_career(career_id: int, db: Session = Depends(get_db)) -> CareerDetailResponse:
    career = get_career_by_id(db, career_id)
    if career is None:
        raise HTTPException(status_code=404, detail="Career not found.")
    return CareerDetailResponse.model_validate(career)
