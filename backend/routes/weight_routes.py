"""Module: routes/weight_routes.py"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from services.piece_service import get_piece_by_piece_id
from services.weight_service import (
    get_overall_reconciliation,
    get_stage_reconciliation,
    get_weight_logs_by_piece,
)

router = APIRouter(
    prefix="/api/weights",
    tags=["Weight Tracking"],
)


@router.get("/piece/{piece_id}")
def get_piece_weights(
    piece_id: str,
    db: Session = Depends(get_db),
):
    piece = get_piece_by_piece_id(db, piece_id)

    if piece is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Piece '{piece_id}' not found",
        )

    return get_weight_logs_by_piece(db, piece_id)


@router.get("/stage/{stage}")
def get_stage_weights(
    stage: str,
    db: Session = Depends(get_db),
):
    return get_stage_reconciliation(db, stage)


@router.get("/reconciliation")
def get_full_reconciliation(
    db: Session = Depends(get_db),
):
    return get_overall_reconciliation(db)
