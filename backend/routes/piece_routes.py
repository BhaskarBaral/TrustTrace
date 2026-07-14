"""Module: routes/piece_routes.py"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.piece_schema import PieceCreate, PieceResponse
from services.piece_service import (
    create_piece,
    get_all_pieces,
    get_piece_by_piece_id,
)


router = APIRouter(
    prefix="/api/pieces",
    tags=["Pieces"]
)


@router.post(
    "",
    response_model=PieceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_piece(
    piece_data: PieceCreate,
    db: Session = Depends(get_db)
):
    return create_piece(
        db=db,
        piece_data=piece_data
    )


@router.get(
    "",
    response_model=list[PieceResponse]
)
def list_pieces(
    db: Session = Depends(get_db)
):
    return get_all_pieces(db=db)


@router.get(
    "/{piece_id}",
    response_model=PieceResponse
)
def get_piece(
    piece_id: str,
    db: Session = Depends(get_db)
):
    piece = get_piece_by_piece_id(
        db=db,
        piece_id=piece_id
    )

    if piece is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Piece '{piece_id}' not found"
        )

    return piece