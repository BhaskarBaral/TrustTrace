from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database.models import User
from schemas.user_schema import UserCreate


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return password_context.hash(password)


def create_user(
    db: Session,
    user_data: UserCreate
) -> User:
    new_user = User(
        name=user_data.name,
        operator_id=user_data.operator_id,
        email=user_data.email,
        password=hash_password(user_data.password),
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all_users(db: Session) -> list[User]:
    return (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )


def get_user_by_operator_id(
    db: Session,
    operator_id: str
) -> User | None:
    return (
        db.query(User)
        .filter(User.operator_id == operator_id)
        .first()
    )


def get_user_by_email(
    db: Session,
    email: str
) -> User | None:
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )