"""Module: routes/inspection_routes.py"""
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.inspection_schema import InspectionResponse
from services.inspection_service import (
    create_inspection,
    get_all_inspections,
    get_inspections_by_piece_id,
)
from services.piece_service import get_piece_by_piece_id
from services.user_service import get_user_by_operator_id


# ---------------------------------------------------------
# INSPECTION ROUTER CONFIGURATION
# ---------------------------------------------------------

router = APIRouter(
    prefix="/api/inspections",
    tags=["Inspections"]
)


# ---------------------------------------------------------
# UPLOAD DIRECTORY CONFIGURATION
# ---------------------------------------------------------

UPLOAD_DIRECTORY = Path("uploads/inspections")

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# ALLOWED IMAGE TYPES
# ---------------------------------------------------------

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp"
}


# ---------------------------------------------------------
# CREATE INSPECTION WITH IMAGE UPLOAD
# ---------------------------------------------------------

@router.post(
    "",
    response_model=InspectionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_inspection(
    piece_id: str = Form(...),
    inspector_id: str = Form(...),
    image: UploadFile = File(...),
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
    # VALIDATE INSPECTOR
    # -----------------------------------------------------

    inspector = get_user_by_operator_id(
        db=db,
        operator_id=inspector_id
    )

    if inspector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inspector '{inspector_id}' not found"
        )

    # -----------------------------------------------------
    # VALIDATE IMAGE TYPE
    # -----------------------------------------------------

    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, and WebP images are allowed"
        )

    # -----------------------------------------------------
    # GENERATE UNIQUE IMAGE FILENAME
    # -----------------------------------------------------

    original_suffix = Path(
        image.filename or ""
    ).suffix.lower()

    unique_filename = (
        f"{piece_id}_{uuid4().hex}{original_suffix}"
    )

    file_path = (
        UPLOAD_DIRECTORY / unique_filename
    )

    # -----------------------------------------------------
    # SAVE IMAGE TO LOCAL STORAGE
    # -----------------------------------------------------

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                image.file,
                buffer
            )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save image: {str(error)}"
        )

    finally:
        image.file.close()

    # -----------------------------------------------------
    # CREATE INSPECTION DATABASE RECORD
    # -----------------------------------------------------

    inspection = create_inspection(
        db=db,
        piece_id=piece_id,
        inspector_id=inspector_id,
        image_path=file_path.as_posix()
    )

    return inspection


# ---------------------------------------------------------
# GET ALL INSPECTIONS
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[InspectionResponse]
)
def list_inspections(
    db: Session = Depends(get_db)
):
    return get_all_inspections(db=db)


# ---------------------------------------------------------
# GET INSPECTIONS FOR ONE PIECE
# ---------------------------------------------------------

@router.get(
    "/piece/{piece_id}",
    response_model=list[InspectionResponse]
)
def get_piece_inspections(
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
    # GET PIECE INSPECTION HISTORY
    # -----------------------------------------------------

    return get_inspections_by_piece_id(
        db=db,
        piece_id=piece_id
    )