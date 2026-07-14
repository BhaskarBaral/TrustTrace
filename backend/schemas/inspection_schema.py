"""Module: schemas/inspection_schema.py"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------
# INSPECTION RESPONSE SCHEMA
# ---------------------------------------------------------

class InspectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    piece_id: str
    inspector_id: str
    image_path: str
    defect_detected: bool
    defect_type: str | None
    confidence: float | None
    inspection_status: str
    created_at: datetime