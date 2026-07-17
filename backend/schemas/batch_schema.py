"""Module: schemas/batch_schema.py"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BatchCreate(BaseModel):
    product_type: str
    material: str
    piece_count: int
    gold_lot: str | None = None
    alloy_batch: str | None = None
    stone_parcel: str | None = None


class BatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    batch_id: str
    product_type: str
    material: str
    piece_count: int
    gold_lot: str | None
    alloy_batch: str | None
    stone_parcel: str | None
    created_at: datetime
