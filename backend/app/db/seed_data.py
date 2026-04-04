from app.models.career import Career, CareerSkill
from app.models.enums import ImportanceLevelEnum, ResourceTypeEnum, SkillCategoryEnum
from app.models.learning_resource import LearningResource
from app.models.skill import Skill


SKILLS = [
    {
        "name": "Python",
        "category": SkillCategoryEnum.TECHNICAL,
        "description": "Use Python for automation, data work, and application logic.",
    },
    {
        "name": "SQL",
        "category": SkillCategoryEnum.TECHNICAL,
        "description": "Query, transform, and model structured data effectively.",
    },
    {
        "name": "Excel",
        "category": SkillCategoryEnum.TOOL,
        "description": "Create reports, dashboards, and spreadsheet-based analysis.",
    },
    {
        "name": "Statistics",
        "category": SkillCategoryEnum.DOMAIN,
        "description": "Apply descriptive and inferential statistics to decision making.",
    },
    {
        "name": "Machine Learning",
        "category": SkillCategoryEnum.DOMAIN,
        "description": "Train, evaluate, and improve predictive models.",
    },
    {
        "name": "Communication",
        "category": SkillCategoryEnum.SOFT,
        "description": "Explain ideas, present findings, and collaborate clearly.",
    },
    {
        "name": "Product Thinking",
        "category": SkillCategoryEnum.DOMAIN,
        "description": "Understand users, business goals, and product tradeoffs.",
    },
    {
        "name": "Power BI",
        "category": SkillCategoryEnum.TOOL,
        "description": "Build interactive business dashboards and share data stories clearly.",
    },
    {
        "name": "Tableau",
        "category": SkillCategoryEnum.TOOL,
        "description": "Turn datasets into visual dashboards and exploratory reports.",
    },
    {
        "name": "Data Visualization",
        "category": SkillCategoryEnum.DOMAIN,
        "description": "Present insights through charts, storytelling, and visual structure.",
    },
    {
        "name": "Prompt Engineering",
        "category": SkillCategoryEnum.DOMAIN,
        "description": "Design reliable prompts and workflows for LLM-powered applications.",
    },
    {
        "name": "API Development",
        "category": SkillCategoryEnum.TECHNICAL,
        "description": "Build and integrate backend APIs for products and automations.",
    },
    {
        "name": "Cloud Basics",
        "category": SkillCategoryEnum.TECHNICAL,
        "description": "Understand deployment, hosting, and cloud service fundamentals.",
    },
    {
        "name": "UI/UX Design",
        "category": SkillCategoryEnum.DOMAIN,
        "description": "Shape user flows, interfaces, and interaction patterns with empathy.",
    },
    {
        "name": "Leadership",
        "category": SkillCategoryEnum.SOFT,
        "description": "Guide teams, align priorities, and move collaborative work forward.",
    },
    {
        "name": "Problem Solving",
        "category": SkillCategoryEnum.SOFT,
        "description": "Break down complex challenges and move toward practical solutions.",
    },
    {
        "name": "Market Research",
        "category": SkillCategoryEnum.DOMAIN,
        "description": "Analyze user behavior, competitors, and market signals for decisions.",
    },
]


CAREERS = [
    {
        "title": "Data Analyst",
        "slug": "data-analyst",
        "description": "Turn raw data into insights, dashboards, and business decisions.",
        "industry": "Technology",
        "growth_outlook": "High",
        "salary_min": 500000,
        "salary_max": 1200000,
        "skills": [
            ("SQL", ImportanceLevelEnum.HIGH, True, 3),
            ("Excel", ImportanceLevelEnum.HIGH, True, 3),
            ("Statistics", ImportanceLevelEnum.MEDIUM, True, 2),
            ("Communication", ImportanceLevelEnum.MEDIUM, False, 1),
        ],
        "resources": [
            {
                "title": "SQL for Data Analysis",
                "resource_type": ResourceTypeEnum.COURSE,
                "url": "https://example.com/sql-data-analysis",
                "provider": "Internal Catalog",
                "difficulty_level": "beginner",
            },
            {
                "title": "Build a Sales Dashboard Project",
                "resource_type": ResourceTypeEnum.PROJECT,
                "url": "https://example.com/sales-dashboard-project",
                "provider": "Internal Catalog",
                "difficulty_level": "intermediate",
            },
        ],
    },
    {
        "title": "AI Engineer",
        "slug": "ai-engineer",
        "description": "Build intelligent systems, model pipelines, and production AI workflows.",
        "industry": "Artificial Intelligence",
        "growth_outlook": "Very High",
        "salary_min": 900000,
        "salary_max": 2200000,
        "skills": [
            ("Python", ImportanceLevelEnum.HIGH, True, 3),
            ("Machine Learning", ImportanceLevelEnum.HIGH, True, 3),
            ("Statistics", ImportanceLevelEnum.HIGH, True, 2),
            ("Communication", ImportanceLevelEnum.MEDIUM, False, 1),
        ],
        "resources": [
            {
                "title": "Python for Machine Learning",
                "resource_type": ResourceTypeEnum.COURSE,
                "url": "https://example.com/python-ml",
                "provider": "Internal Catalog",
                "difficulty_level": "intermediate",
            },
            {
                "title": "Deploy an Inference API",
                "resource_type": ResourceTypeEnum.PROJECT,
                "url": "https://example.com/inference-api-project",
                "provider": "Internal Catalog",
                "difficulty_level": "advanced",
            },
        ],
    },
    {
        "title": "Product Manager",
        "slug": "product-manager",
        "description": "Guide products from user need to shipped outcome with clear priorities.",
        "industry": "Software",
        "growth_outlook": "High",
        "salary_min": 1000000,
        "salary_max": 2400000,
        "skills": [
            ("Communication", ImportanceLevelEnum.HIGH, True, 3),
            ("Product Thinking", ImportanceLevelEnum.HIGH, True, 3),
            ("Excel", ImportanceLevelEnum.MEDIUM, False, 1),
        ],
        "resources": [
            {
                "title": "Product Strategy Fundamentals",
                "resource_type": ResourceTypeEnum.COURSE,
                "url": "https://example.com/product-strategy",
                "provider": "Internal Catalog",
                "difficulty_level": "beginner",
            }
        ],
    },
]


def build_seed_entities() -> tuple[list[Skill], list[Career]]:
    skill_map: dict[str, Skill] = {}
    for entry in SKILLS:
        skill = Skill(**entry)
        skill_map[skill.name] = skill

    careers: list[Career] = []
    for career_entry in CAREERS:
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

        for skill_name, importance, is_required, weight in career_entry["skills"]:
            career.required_skills.append(
                CareerSkill(
                    skill=skill_map[skill_name],
                    importance_level=importance,
                    is_required=is_required,
                    weight=weight,
                )
            )

        for resource_entry in career_entry["resources"]:
            career.learning_resources.append(LearningResource(**resource_entry))

        careers.append(career)

    return list(skill_map.values()), careers
