from sqlalchemy import select

from app.core.database import SessionLocal
from app.db.seed_data import build_seed_entities
from app.models.career import Career
from app.models.skill import Skill


def seed_db() -> None:
    with SessionLocal() as session:
        existing_career = session.scalar(select(Career.id).limit(1))
        existing_skill = session.scalar(select(Skill.id).limit(1))

        if existing_career or existing_skill:
            print("Seed skipped: database already contains careers or skills.")
            return

        skills, careers = build_seed_entities()
        session.add_all(skills)
        session.add_all(careers)
        session.commit()
        print(f"Seeded {len(skills)} skills and {len(careers)} careers.")


if __name__ == "__main__":
    seed_db()
