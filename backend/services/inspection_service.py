"""Module: services/inspection_service.py"""
from sqlalchemy.orm import Session

from database.models import Inspection


# ---------------------------------------------------------
# CREATE INSPECTION RECORD
# ---------------------------------------------------------

def create_inspection(
    db: Session,
    piece_id: str,
    inspector_id: str,
    image_path: str
) -> Inspection:

    # -----------------------------------------------------
    # CREATE INSPECTION DATABASE OBJECT
    # -----------------------------------------------------

    new_inspection = Inspection(
        piece_id=piece_id,
        inspector_id=inspector_id,
        image_path=image_path,
        defect_detected=False,
        defect_type=None,
        confidence=None,
        inspection_status="Pending AI Analysis"
    )

    # -----------------------------------------------------
    # SAVE INSPECTION
    # -----------------------------------------------------

    db.add(new_inspection)
    db.commit()
    db.refresh(new_inspection)

    return new_inspection


# ---------------------------------------------------------
# GET ALL INSPECTIONS
# ---------------------------------------------------------

def get_all_inspections(
    db: Session
) -> list[Inspection]:

    return (
        db.query(Inspection)
        .order_by(Inspection.created_at.desc())
        .all()
    )


# ---------------------------------------------------------
# GET INSPECTIONS FOR ONE PIECE
# ---------------------------------------------------------

def get_inspections_by_piece_id(
    db: Session,
    piece_id: str
) -> list[Inspection]:

    return (
        db.query(Inspection)
        .filter(Inspection.piece_id == piece_id)
        .order_by(Inspection.created_at.asc())
        .all()
    )