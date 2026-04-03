from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.skill import Skill
from app.schemas.career import SkillBase

router = APIRouter()


@router.get("/", response_model=list[SkillBase])
def list_skills(db: Session = Depends(get_db)) -> list[SkillBase]:
    skills = db.scalars(select(Skill).order_by(Skill.name.asc())).all()
    return [SkillBase.model_validate(skill) for skill in skills]
