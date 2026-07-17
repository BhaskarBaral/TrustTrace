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


def verify_password(plain: str, hashed: str) -> bool:
    return password_context.verify(plain, hashed)


def create_user(
    db: Session,
    user_data: UserCreate
) -> User:
    new_user = User(
        name=user_data.name,
        operator_id=user_data.operator_id,
        email=user_data.email,
        password=hash_password(user_data.password),
        pin_hash=hash_password(user_data.pin) if user_data.pin else None,
        role=user_data.role,
        station_id=user_data.station_id,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def assign_station(
    db: Session,
    operator_id: str,
    station_id: str,
) -> User | None:
    user = get_user_by_operator_id(db, operator_id)

    if user is None:
        return None

    user.station_id = station_id
    db.commit()
    db.refresh(user)
    return user


def verify_pin_login(
    db: Session,
    operator_id: str,
    pin: str,
) -> User | None:
    user = get_user_by_operator_id(db, operator_id)

    if user is None or user.pin_hash is None:
        return None

    if verify_password(pin, user.pin_hash):
        return user
    return None


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


def get_users_by_station(
    db: Session,
    station_id: str,
) -> list[User]:
    return (
        db.query(User)
        .filter(User.station_id == station_id)
        .all()
    )
