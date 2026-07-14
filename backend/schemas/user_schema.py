from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    name: str
    operator_id: str
    email: EmailStr
    password: str
    role: str = "operator"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    operator_id: str
    email: EmailStr
    role: str
    created_at: datetime