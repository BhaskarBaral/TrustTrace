from pydantic import BaseModel

from schemas.batch_schema import BatchResponse
from schemas.event_schema import EventResponse
from schemas.inspection_schema import InspectionResponse
from schemas.piece_schema import PieceResponse
from schemas.quality_schema import QualityGateResponse
from schemas.weight_schema import StageWeightResponse


class PassportResponse(BaseModel):
    piece: PieceResponse
    batch: BatchResponse | None
    production_history: list[EventResponse]
    weight_logs: list[StageWeightResponse]
    quality_gates: list[QualityGateResponse]
    inspections: list[InspectionResponse]
    ai_summary: dict | None


class ComplianceReportResponse(BaseModel):
    piece_id: str
    product_type: str
    material: str
    gold_lot: str | None
    alloy_batch: str | None
    stone_parcel: str | None
    operator_chain: list[str]
    manufacturing_stages: list[dict]
    quality_results: list[dict]
    created_at: str
    completed_at: str | None
    ai_narrative: dict | None
