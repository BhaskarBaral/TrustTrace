"""Module: schemas/event_schema.py"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventCreate(BaseModel):
    piece_id: str
    operator_id: str
    stage: str
    event_type: str
    notes: str | None = None


class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    piece_id: str
    operator_id: str
    stage: str
    event_type: str
    notes: str | None
    timestamp: datetime