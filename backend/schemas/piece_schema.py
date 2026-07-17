"""Module: schemas/piece_schema.py"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PieceCreate(BaseModel):
    product_type: str
    material: str
    batch_id: str | None = None
    weight_expected: float | None = None


class PieceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    piece_id: str
    batch_id: str | None
    product_type: str
    material: str
    weight_expected: float | None
    current_stage: str
    status: str
    created_at: datetime