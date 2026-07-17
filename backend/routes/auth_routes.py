from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.auth_schema import LoginRequest, TokenResponse
from services.auth_service import authenticate_user, create_access_token

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token({
        "sub": user.operator_id,
        "role": user.role,
    })

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.operator_id,
        role=user.role,
    )
