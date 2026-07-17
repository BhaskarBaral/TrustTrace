"""Module: routes/passport_routes.py"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.passport_schema import ComplianceReportResponse, PassportResponse
from services.passport_service import build_compliance_report, build_piece_passport

router = APIRouter(
    prefix="/api/passport",
    tags=["Digital Piece Passport"]
)


@router.get(
    "/{piece_id}",
    response_model=PassportResponse
)
def get_piece_passport(
    piece_id: str,
    db: Session = Depends(get_db)
):
    passport = build_piece_passport(db=db, piece_id=piece_id)

    if passport is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Piece '{piece_id}' not found"
        )

    return passport


@router.get(
    "/{piece_id}/compliance",
    response_model=ComplianceReportResponse
)
def get_compliance_report(
    piece_id: str,
    db: Session = Depends(get_db),
):
    report = build_compliance_report(db, piece_id)

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Piece '{piece_id}' not found"
        )

    return report
