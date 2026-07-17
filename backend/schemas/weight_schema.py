"""Module: schemas/weight_schema.py"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StageWeightResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    piece_id: str
    stage: str
    operator_id: str
    weight_in: float
    weight_out: float
    expected_weight: float | None
    variance: float | None
    timestamp: datetime


class StageReconciliationResponse(BaseModel):
    stage: str
    total_pieces: int
    total_weight_in: float
    total_weight_out: float
    total_expected: float | None
    total_variance: float
    average_variance_per_piece: float


class OverallReconciliationResponse(BaseModel):
    stages: list[StageReconciliationResponse]
    total_variance: float
