from sqlalchemy import select

from app.core.database import SessionLocal
from app.db.seed_data import CAREERS, SKILLS
from app.models.career import Career, CareerSkill
from app.models.learning_resource import LearningResource
from app.models.skill import Skill


def seed_db() -> None:
    with SessionLocal() as session:
        existing_skills = {
            skill.name: skill
            for skill in session.scalars(select(Skill)).all()
        }
        existing_careers = {
            career.slug: career
            for career in session.scalars(select(Career)).all()
        }

        created_skills = 0
        created_careers = 0
        created_resources = 0
        created_links = 0

        for entry in SKILLS:
            if entry["name"] in existing_skills:
                continue
            skill = Skill(**entry)
            session.add(skill)
            existing_skills[skill.name] = skill
            created_skills += 1

        session.flush()

        for career_entry in CAREERS:
            career = existing_careers.get(career_entry["slug"])
            if career is None:
                career = Career(
                    title=career_entry["title"],
                    slug=career_entry["slug"],
                    description=career_entry["description"],
                    industry=career_entry["industry"],
                    growth_outlook=career_entry["growth_outlook"],
                    salary_min=career_entry["salary_min"],
                    salary_max=career_entry["salary_max"],
                    is_active=True,
                )
                session.add(career)
                session.flush()
                existing_careers[career.slug] = career
                created_careers += 1

            linked_skill_names = {
                link.skill.name
                for link in career.required_skills
                if link.skill is not None
            }
            existing_resource_titles = {
                resource.title
                for resource in career.learning_resources
            }

            for skill_name, importance, is_required, weight in career_entry["skills"]:
                if skill_name in linked_skill_names:
                    continue
                career.required_skills.append(
                    CareerSkill(
                        skill=existing_skills[skill_name],
                        importance_level=importance,
                        is_required=is_required,
                        weight=weight,
                    )
                )
                created_links += 1

            for resource_entry in career_entry["resources"]:
                existing_resource = next(
                    (
                        resource
                        for resource in career.learning_resources
                        if resource.title == resource_entry["title"]
                    ),
                    None,
                )
                if existing_resource is not None:
                    existing_resource.resource_type = resource_entry["resource_type"]
                    existing_resource.url = resource_entry["url"]
                    existing_resource.provider = resource_entry["provider"]
                    existing_resource.difficulty_level = resource_entry["difficulty_level"]
                    continue
                career.learning_resources.append(LearningResource(**resource_entry))
                created_resources += 1

        session.commit()
        print(
            "Seed complete: "
            f"{created_skills} skills, "
            f"{created_careers} careers, "
            f"{created_links} career-skill links, "
            f"{created_resources} resources added."
        )


if __name__ == "__main__":
    seed_db()
