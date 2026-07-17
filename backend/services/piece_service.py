"""Module: services/piece_service.py"""
from sqlalchemy.orm import Session

from database.models import Piece
from schemas.piece_schema import PieceCreate


def generate_piece_id(db: Session) -> str:
    latest_piece = (
        db.query(Piece)
        .order_by(Piece.id.desc())
        .first()
    )

    if latest_piece is None:
        next_number = 1
    else:
        next_number = latest_piece.id + 1

    return f"TT-{next_number:06d}"


def create_piece(db: Session, piece_data: PieceCreate) -> Piece:
    new_piece = Piece(
        piece_id=generate_piece_id(db),
        batch_id=piece_data.batch_id,
        product_type=piece_data.product_type,
        material=piece_data.material,
        weight_expected=piece_data.weight_expected,
        current_stage="Registered",
        status="In Production",
    )

    db.add(new_piece)
    db.commit()
    db.refresh(new_piece)

    return new_piece


def get_all_pieces(db: Session) -> list[Piece]:
    return (
        db.query(Piece)
        .order_by(Piece.created_at.desc())
        .all()
    )


def get_piece_by_piece_id(
    db: Session,
    piece_id: str
) -> Piece | None:
    return (
        db.query(Piece)
        .filter(Piece.piece_id == piece_id)
        .first()
    )


def get_pieces_by_stage(
    db: Session,
    stage: str
) -> list[Piece]:
    return (
        db.query(Piece)
        .filter(Piece.current_stage == stage)
        .order_by(Piece.created_at.desc())
        .all()
    )


def get_wip_summary(db: Session) -> list[dict]:
    stages = ["Registered", "Casting", "Filing", "Stone Setting", "Polishing", "Plating"]
    result = []

    for stage in stages:
        pieces = get_pieces_by_stage(db, stage)
        result.append({
            "stage": stage,
            "piece_count": len(pieces),
            "pieces": [p.piece_id for p in pieces],
        })

    return result
