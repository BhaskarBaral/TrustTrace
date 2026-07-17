"""Module: schemas/quality_schema.py"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class QualityGateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    piece_id: str
    stage: str
    inspector_id: str
    image_path: str
    ai_verdict: str
    defect_type: str | None
    confidence: float | None
    human_review: str | None
    reviewed_by: str | None
    created_at: datetime


class QualityGateSummary(BaseModel):
    stage: str
    total_gates: int
    pass_count: int
    flag_count: int
    fail_count: int
    pass_rate: float
    top_defects: list[str]


class HumanReviewRequest(BaseModel):
    verdict: str
    reviewer_id: str
