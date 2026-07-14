"""Module: services/passport_service.py"""
from sqlalchemy.orm import Session

from services.event_service import get_events_by_piece_id
from services.inspection_service import get_inspections_by_piece_id
from services.piece_service import get_piece_by_piece_id


# ---------------------------------------------------------
# BUILD DIGITAL PIECE PASSPORT
# ---------------------------------------------------------

def build_piece_passport(
    db: Session,
    piece_id: str
) -> dict:

    # -----------------------------------------------------
    # GET PIECE DETAILS
    # -----------------------------------------------------

    piece = get_piece_by_piece_id(
        db=db,
        piece_id=piece_id
    )

    # -----------------------------------------------------
    # RETURN NONE IF PIECE DOES NOT EXIST
    # -----------------------------------------------------

    if piece is None:
        return None

    # -----------------------------------------------------
    # GET PRODUCTION HISTORY
    # -----------------------------------------------------

    production_history = get_events_by_piece_id(
        db=db,
        piece_id=piece_id
    )

    # -----------------------------------------------------
    # GET INSPECTION HISTORY
    # -----------------------------------------------------

    inspections = get_inspections_by_piece_id(
        db=db,
        piece_id=piece_id
    )

    # -----------------------------------------------------
    # BUILD PASSPORT RESPONSE
    # -----------------------------------------------------

    return {
        "piece": piece,
        "production_history": production_history,
        "inspections": inspections
    }