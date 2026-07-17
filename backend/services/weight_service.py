"""Module: services/weight_service.py"""
from sqlalchemy.orm import Session

from database.models import StageWeightLog


def create_weight_log(
    db: Session,
    piece_id: str,
    stage: str,
    operator_id: str,
    weight_in: float,
    weight_out: float,
    expected_weight: float | None = None,
) -> StageWeightLog:
    variance = weight_out - weight_in
    if expected_weight is not None:
        variance = weight_out - expected_weight

    log = StageWeightLog(
        piece_id=piece_id,
        stage=stage,
        operator_id=operator_id,
        weight_in=weight_in,
        weight_out=weight_out,
        expected_weight=expected_weight,
        variance=variance,
    )

    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_weight_logs_by_piece(
    db: Session,
    piece_id: str,
) -> list[StageWeightLog]:
    return (
        db.query(StageWeightLog)
        .filter(StageWeightLog.piece_id == piece_id)
        .order_by(StageWeightLog.timestamp.asc())
        .all()
    )


def get_weight_logs_by_stage(
    db: Session,
    stage: str,
) -> list[StageWeightLog]:
    return (
        db.query(StageWeightLog)
        .filter(StageWeightLog.stage == stage)
        .order_by(StageWeightLog.timestamp.desc())
        .all()
    )


def get_stage_reconciliation(
    db: Session,
    stage: str,
) -> dict:
    logs = get_weight_logs_by_stage(db, stage)

    if not logs:
        return {
            "stage": stage,
            "total_pieces": 0,
            "total_weight_in": 0,
            "total_weight_out": 0,
            "total_expected": None,
            "total_variance": 0,
            "average_variance_per_piece": 0,
        }

    total_in = sum(log.weight_in for log in logs)
    total_out = sum(log.weight_out for log in logs)
    total_variance = sum(log.variance or 0 for log in logs)
    expected_values = [log.expected_weight for log in logs if log.expected_weight is not None]
    total_expected = sum(expected_values) if expected_values else None

    return {
        "stage": stage,
        "total_pieces": len(logs),
        "total_weight_in": total_in,
        "total_weight_out": total_out,
        "total_expected": total_expected,
        "total_variance": total_variance,
        "average_variance_per_piece": total_variance / len(logs) if logs else 0,
    }


def get_overall_reconciliation(db: Session) -> dict:
    stages = ["Casting", "Filing", "Stone Setting", "Polishing", "Plating"]
    stage_results = [get_stage_reconciliation(db, stage) for stage in stages]
    total_variance = sum(r["total_variance"] for r in stage_results)

    return {
        "stages": stage_results,
        "total_variance": total_variance,
    }
