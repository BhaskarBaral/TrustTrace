"""Module: services/event_service.py"""
from sqlalchemy.orm import Session

from database.models import Piece, ProductionEvent, StageWeightLog
from schemas.event_schema import EventCreate


def create_event(
    db: Session,
    event_data: EventCreate
) -> ProductionEvent:

    new_event = ProductionEvent(
        piece_id=event_data.piece_id,
        operator_id=event_data.operator_id,
        stage=event_data.stage,
        event_type=event_data.event_type,
        weight_in=event_data.weight_in,
        weight_out=event_data.weight_out,
        notes=event_data.notes,
    )

    piece = (
        db.query(Piece)
        .filter(Piece.piece_id == event_data.piece_id)
        .first()
    )

    if piece is not None:
        piece.current_stage = event_data.stage

    db.add(new_event)
    db.flush()

    if event_data.weight_in is not None and event_data.weight_out is not None:
        weight_log = StageWeightLog(
            piece_id=event_data.piece_id,
            stage=event_data.stage,
            operator_id=event_data.operator_id,
            weight_in=event_data.weight_in,
            weight_out=event_data.weight_out,
            expected_weight=piece.weight_expected if piece else None,
            variance=event_data.weight_out - event_data.weight_in,
        )
        db.add(weight_log)

    db.commit()
    db.refresh(new_event)

    return new_event


def get_all_events(
    db: Session
) -> list[ProductionEvent]:

    return (
        db.query(ProductionEvent)
        .order_by(ProductionEvent.timestamp.desc())
        .all()
    )


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


def get_events_by_stage(
    db: Session,
    stage: str
) -> list[ProductionEvent]:

    return (
        db.query(ProductionEvent)
        .filter(ProductionEvent.stage == stage)
        .order_by(ProductionEvent.timestamp.desc())
        .all()
    )
