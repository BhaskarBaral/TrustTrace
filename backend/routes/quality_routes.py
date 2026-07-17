"""Module: routes/quality_routes.py"""
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.quality_schema import HumanReviewRequest, QualityGateResponse
from services.piece_service import get_piece_by_piece_id
from services.quality_service import (
    create_quality_gate,
    get_all_quality_gates,
    get_quality_gates_by_piece,
    get_quality_summary,
    run_ai_inspection,
    submit_human_review,
)
from services.user_service import get_user_by_operator_id

router = APIRouter(
    prefix="/api/quality",
    tags=["Quality Gates"],
)

UPLOAD_DIRECTORY = Path("uploads/quality_gates")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


@router.post(
    "/gates",
    response_model=QualityGateResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_quality_gate(
    piece_id: str = Form(...),
    stage: str = Form(...),
    inspector_id: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    piece = get_piece_by_piece_id(db, piece_id)
    if piece is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Piece '{piece_id}' not found",
        )

    inspector = get_user_by_operator_id(db, inspector_id)
    if inspector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inspector '{inspector_id}' not found",
        )

    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, and WebP images are allowed",
        )

    suffix = Path(image.filename or "").suffix.lower()
    filename = f"{piece_id}_{stage}_{uuid4().hex}{suffix}"
    file_path = UPLOAD_DIRECTORY / filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save image: {str(error)}",
        )
    finally:
        image.file.close()

    gate = create_quality_gate(
        db=db,
        piece_id=piece_id,
        stage=stage,
        inspector_id=inspector_id,
        image_path=file_path.as_posix(),
    )

    gate = run_ai_inspection(db=db, gate_id=gate.id)

    return gate


@router.patch("/gates/{gate_id}/review")
def review_quality_gate(
    gate_id: int,
    review_data: HumanReviewRequest,
    db: Session = Depends(get_db),
):
    gate = submit_human_review(
        db=db,
        gate_id=gate_id,
        verdict=review_data.verdict,
        reviewer_id=review_data.reviewer_id,
    )

    if gate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quality gate '{gate_id}' not found",
        )

    return gate


@router.get("/gates")
def list_quality_gates(
    db: Session = Depends(get_db),
):
    return get_all_quality_gates(db=db)


@router.get("/gates/piece/{piece_id}")
def get_piece_quality_gates(
    piece_id: str,
    db: Session = Depends(get_db),
):
    piece = get_piece_by_piece_id(db, piece_id)

    if piece is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Piece '{piece_id}' not found",
        )

    return get_quality_gates_by_piece(db, piece_id)


@router.get("/summary/{stage}")
def get_stage_quality_summary(
    stage: str,
    db: Session = Depends(get_db),
):
    return get_quality_summary(db, stage)


@router.get("/summary")
def get_overall_quality_summary(
    db: Session = Depends(get_db),
):
    return get_quality_summary(db)
