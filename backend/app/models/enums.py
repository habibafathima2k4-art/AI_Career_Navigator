from enum import Enum


class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"


class EducationLevelEnum(str, Enum):
    UG = "ug"
    PG = "pg"
    DIPLOMA = "diploma"


class ExperienceLevelEnum(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class InterestAreaEnum(str, Enum):
    TECH = "tech"
    DESIGN = "design"
    BUSINESS = "business"
    DATA = "data"
    MANAGEMENT = "management"


class WorkStyleEnum(str, Enum):
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    COLLABORATIVE = "collaborative"
    STRUCTURED = "structured"


class SkillCategoryEnum(str, Enum):
    TECHNICAL = "technical"
    SOFT = "soft"
    DOMAIN = "domain"
    TOOL = "tool"


class ProficiencyLevelEnum(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ImportanceLevelEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ResourceTypeEnum(str, Enum):
    COURSE = "course"
    VIDEO = "video"
    ARTICLE = "article"
    PROJECT = "project"
    CERTIFICATION = "certification"
    DOCUMENTATION = "documentation"


class ProgressStatusEnum(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
