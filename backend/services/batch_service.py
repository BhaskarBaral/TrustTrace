"""Module: services/batch_service.py"""
from sqlalchemy.orm import Session

from database.models import Batch, Piece


def generate_batch_id(db: Session) -> str:
    latest = (
        db.query(Batch)
        .order_by(Batch.id.desc())
        .first()
    )

    next_number = 1 if latest is None else latest.id + 1
    return f"BT-{next_number:06d}"


def create_batch(
    db: Session,
    product_type: str,
    material: str,
    piece_count: int,
    gold_lot: str | None = None,
    alloy_batch: str | None = None,
    stone_parcel: str | None = None,
) -> Batch:
    batch = Batch(
        batch_id=generate_batch_id(db),
        product_type=product_type,
        material=material,
        piece_count=piece_count,
        gold_lot=gold_lot,
        alloy_batch=alloy_batch,
        stone_parcel=stone_parcel,
    )

    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def create_pieces_from_batch(
    db: Session,
    batch_id: str,
    piece_count: int,
) -> list[Piece]:
    batch = (
        db.query(Batch)
        .filter(Batch.batch_id == batch_id)
        .first()
    )

    if batch is None:
        return []

    pieces = []
    for _ in range(piece_count):
        latest = (
            db.query(Piece)
            .order_by(Piece.id.desc())
            .first()
        )
        next_number = 1 if latest is None else latest.id + 1
        piece_id = f"TT-{next_number:06d}"

        piece = Piece(
            piece_id=piece_id,
            batch_id=batch.batch_id,
            product_type=batch.product_type,
            material=batch.material,
        )
        db.add(piece)
        db.flush()
        pieces.append(piece)

    db.commit()
    for piece in pieces:
        db.refresh(piece)

    return pieces


def get_batch_by_id(db: Session, batch_id: str) -> Batch | None:
    return (
        db.query(Batch)
        .filter(Batch.batch_id == batch_id)
        .first()
    )


def get_pieces_by_batch(db: Session, batch_id: str) -> list[Piece]:
    return (
        db.query(Piece)
        .filter(Piece.batch_id == batch_id)
        .order_by(Piece.id.asc())
        .all()
    )


def get_all_batches(db: Session) -> list[Batch]:
    return (
        db.query(Batch)
        .order_by(Batch.created_at.desc())
        .all()
    )
