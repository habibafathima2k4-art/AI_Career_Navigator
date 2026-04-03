import sys

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.enums import RoleEnum
from app.models.user import User


def promote_user(email: str) -> None:
    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.email == email.lower()))
        if user is None:
            print(f"No user found for {email}")
            return

        user.role = RoleEnum.ADMIN
        session.add(user)
        session.commit()
        print(f"Promoted {user.email} to admin.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m app.db.promote_user <email>")
        raise SystemExit(1)

    promote_user(sys.argv[1])
