from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.enums import RoleEnum
from app.models.user import User
from app.services.auth_service import get_user_by_id

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User | None:
    if credentials is None:
        return None

    subject = decode_access_token(credentials.credentials)
    if subject is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    try:
        user_id = int(subject)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid token subject.") from exc

    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found.")
    return user


def get_current_user(user: User | None = Depends(get_current_user_optional)) -> User:
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required.")
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required.")
    return current_user
