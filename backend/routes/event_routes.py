"""Module: routes/event_routes.py"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.event_schema import EventCreate, EventResponse
from services.event_service import (
    create_event,
    get_all_events,
    get_events_by_piece_id,
)
from services.piece_service import get_piece_by_piece_id
from services.user_service import get_user_by_operator_id


# ---------------------------------------------------------
# EVENT ROUTER CONFIGURATION
# ---------------------------------------------------------

router = APIRouter(
    prefix="/api/events",
    tags=["Production Events"]
)


# ---------------------------------------------------------
# CREATE PRODUCTION EVENT
# ---------------------------------------------------------

@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_event(
    event_data: EventCreate,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # VALIDATE PIECE
    # -----------------------------------------------------

    piece = get_piece_by_piece_id(
        db=db,
        piece_id=event_data.piece_id
    )

    if piece is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Piece '{event_data.piece_id}' not found"
        )

    # -----------------------------------------------------
    # VALIDATE OPERATOR
    # -----------------------------------------------------

    operator = get_user_by_operator_id(
        db=db,
        operator_id=event_data.operator_id
    )

    if operator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Operator '{event_data.operator_id}' not found"
        )

    # -----------------------------------------------------
    # CREATE EVENT
    # -----------------------------------------------------

    return create_event(
        db=db,
        event_data=event_data
    )


# ---------------------------------------------------------
# GET ALL PRODUCTION EVENTS
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[EventResponse]
)
def list_events(
    db: Session = Depends(get_db)
):
    return get_all_events(db=db)


# ---------------------------------------------------------
# GET PRODUCTION HISTORY FOR ONE PIECE
# ---------------------------------------------------------

@router.get(
    "/piece/{piece_id}",
    response_model=list[EventResponse]
)
def get_piece_events(
    piece_id: str,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # VALIDATE PIECE
    # -----------------------------------------------------

    piece = get_piece_by_piece_id(
        db=db,
        piece_id=piece_id
    )

    if piece is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Piece '{piece_id}' not found"
        )

    # -----------------------------------------------------
    # GET PIECE PRODUCTION HISTORY
    # -----------------------------------------------------

    return get_events_by_piece_id(
        db=db,
        piece_id=piece_id
    )