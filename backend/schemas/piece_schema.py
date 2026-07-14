"""Module: schemas/piece_schema.py"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PieceCreate(BaseModel):
    product_type: str
    material: str


class PieceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    piece_id: str
    product_type: str
    material: str
    current_stage: str
    status: str
    created_at: datetime