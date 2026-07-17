from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    name: str
    operator_id: str
    email: EmailStr
    password: str
    pin: str | None = None
    role: str = "operator"
    station_id: str | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    operator_id: str
    email: EmailStr
    role: str
    station_id: str | None
    created_at: datetime


class StationAssignRequest(BaseModel):
    station_id: str


class PinLoginRequest(BaseModel):
    operator_id: str
    pin: str