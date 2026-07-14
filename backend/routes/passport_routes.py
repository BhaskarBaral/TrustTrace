"""Module: routes/passport_routes.py"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.passport_schema import PassportResponse
from services.passport_service import build_piece_passport


# ---------------------------------------------------------
# PASSPORT ROUTER CONFIGURATION
# ---------------------------------------------------------

router = APIRouter(
    prefix="/api/passport",
    tags=["Digital Piece Passport"]
)


# ---------------------------------------------------------
# GET DIGITAL PIECE PASSPORT
# ---------------------------------------------------------

@router.get(
    "/{piece_id}",
    response_model=PassportResponse
)
def get_piece_passport(
    piece_id: str,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # BUILD PASSPORT
    # -----------------------------------------------------

    passport = build_piece_passport(
        db=db,
        piece_id=piece_id
    )

    # -----------------------------------------------------
    # HANDLE UNKNOWN PIECE
    # -----------------------------------------------------

    if passport is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Piece '{piece_id}' not found"
        )

    # -----------------------------------------------------
    # RETURN COMPLETE PASSPORT
    # -----------------------------------------------------

    return passport