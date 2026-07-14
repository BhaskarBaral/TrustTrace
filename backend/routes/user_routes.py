from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.user_schema import UserCreate, UserResponse
from services.user_service import (
    create_user,
    get_all_users,
    get_user_by_email,
    get_user_by_operator_id,
)


router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_operator = get_user_by_operator_id(
        db=db,
        operator_id=user_data.operator_id
    )

    if existing_operator is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Operator ID '{user_data.operator_id}' already exists"
        )

    existing_email = get_user_by_email(
        db=db,
        email=user_data.email
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{user_data.email}' already exists"
        )

    return create_user(
        db=db,
        user_data=user_data
    )


@router.get(
    "",
    response_model=list[UserResponse]
)
def list_users(
    db: Session = Depends(get_db)
):
    return get_all_users(db=db)


@router.get(
    "/{operator_id}",
    response_model=UserResponse
)
def get_user(
    operator_id: str,
    db: Session = Depends(get_db)
):
    user = get_user_by_operator_id(
        db=db,
        operator_id=operator_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Operator '{operator_id}' not found"
        )

    return user