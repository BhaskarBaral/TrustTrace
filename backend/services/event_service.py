"""Module: services/event_service.py"""
from sqlalchemy.orm import Session

from database.models import Piece, ProductionEvent
from schemas.event_schema import EventCreate


# ---------------------------------------------------------
# CREATE PRODUCTION EVENT
# ---------------------------------------------------------

def create_event(
    db: Session,
    event_data: EventCreate
) -> ProductionEvent:

    # -----------------------------------------------------
    # CREATE EVENT DATABASE OBJECT
    # -----------------------------------------------------

    new_event = ProductionEvent(
        piece_id=event_data.piece_id,
        operator_id=event_data.operator_id,
        stage=event_data.stage,
        event_type=event_data.event_type,
        notes=event_data.notes
    )

    # -----------------------------------------------------
    # FIND THE RELATED PIECE
    # -----------------------------------------------------

    piece = (
        db.query(Piece)
        .filter(Piece.piece_id == event_data.piece_id)
        .first()
    )

    # -----------------------------------------------------
    # UPDATE THE PIECE'S CURRENT PRODUCTION STAGE
    # -----------------------------------------------------

    if piece is not None:
        piece.current_stage = event_data.stage

    # -----------------------------------------------------
    # SAVE EVENT AND PIECE UPDATE
    # -----------------------------------------------------

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


# ---------------------------------------------------------
# GET ALL PRODUCTION EVENTS
# ---------------------------------------------------------

def get_all_events(
    db: Session
) -> list[ProductionEvent]:

    return (
        db.query(ProductionEvent)
        .order_by(ProductionEvent.timestamp.desc())
        .all()
    )


# ---------------------------------------------------------
# GET EVENTS FOR ONE PIECE
# ---------------------------------------------------------

def get_events_by_piece_id(
    db: Session,
    piece_id: str
) -> list[ProductionEvent]:

    return (
        db.query(ProductionEvent)
        .filter(ProductionEvent.piece_id == piece_id)
        .order_by(ProductionEvent.timestamp.asc())
        .all()
    )