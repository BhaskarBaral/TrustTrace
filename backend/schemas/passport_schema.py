from pydantic import BaseModel

from schemas.event_schema import EventResponse
from schemas.inspection_schema import InspectionResponse
from schemas.piece_schema import PieceResponse


# ---------------------------------------------------------
# DIGITAL PIECE PASSPORT RESPONSE SCHEMA
# ---------------------------------------------------------

class PassportResponse(BaseModel):
    piece: PieceResponse
    production_history: list[EventResponse]
    inspections: list[InspectionResponse]