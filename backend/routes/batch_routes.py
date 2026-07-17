"""Module: routes/batch_routes.py"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.batch_schema import BatchCreate, BatchResponse
from services.batch_service import (
    create_batch,
    create_pieces_from_batch,
    get_all_batches,
    get_batch_by_id,
    get_pieces_by_batch,
)

router = APIRouter(
    prefix="/api/batches",
    tags=["Batches"],
)


@router.post(
    "",
    response_model=BatchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_batch(
    batch_data: BatchCreate,
    db: Session = Depends(get_db),
):
    return create_batch(
        db=db,
        product_type=batch_data.product_type,
        material=batch_data.material,
        piece_count=batch_data.piece_count,
        gold_lot=batch_data.gold_lot,
        alloy_batch=batch_data.alloy_batch,
        stone_parcel=batch_data.stone_parcel,
    )


@router.post("/{batch_id}/pieces")
def generate_pieces_from_batch(
    batch_id: str,
    db: Session = Depends(get_db),
):
    batch = get_batch_by_id(db, batch_id)

    if batch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Batch '{batch_id}' not found",
        )

    pieces = create_pieces_from_batch(
        db=db,
        batch_id=batch_id,
        piece_count=batch.piece_count,
    )

    return {
        "batch_id": batch_id,
        "pieces_created": len(pieces),
        "piece_ids": [p.piece_id for p in pieces],
    }


@router.get("")
def list_batches(
    db: Session = Depends(get_db),
):
    return get_all_batches(db=db)


@router.get("/{batch_id}")
def get_batch(
    batch_id: str,
    db: Session = Depends(get_db),
):
    batch = get_batch_by_id(db, batch_id)

    if batch is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Batch '{batch_id}' not found",
        )

    pieces = get_pieces_by_batch(db, batch_id)

    return {
        "batch": batch,
        "pieces": pieces,
    }
