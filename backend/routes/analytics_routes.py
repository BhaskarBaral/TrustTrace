"""Module: routes/analytics_routes.py"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from services.groq_service import generate_insights
from services.piece_service import get_wip_summary
from services.quality_service import get_quality_summary
from services.weight_service import get_overall_reconciliation

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
)


@router.get("/wip")
def get_wip_status(
    db: Session = Depends(get_db),
):
    return {"wip": get_wip_summary(db)}


@router.get("/quality")
def get_quality_analytics(
    stage: str | None = None,
    db: Session = Depends(get_db),
):
    return get_quality_summary(db, stage)


@router.get("/gold-reconciliation")
def get_gold_reconciliation(
    db: Session = Depends(get_db),
):
    return get_overall_reconciliation(db)


@router.get("/insights")
def get_production_insights(
    db: Session = Depends(get_db),
):
    """AI-generated natural language production insights using Groq reasoning model."""
    wip = get_wip_summary(db)
    quality = get_quality_summary(db)
    gold = get_overall_reconciliation(db)

    insights = generate_insights(wip, quality, gold)

    return {
        "wip": wip,
        "quality": quality,
        "gold_reconciliation": gold,
        "ai_insights": insights,
    }


@router.get("/operator/{operator_id}")
def get_operator_analytics(
    operator_id: str,
    db: Session = Depends(get_db),
):
    from database.models import ProductionEvent, StageWeightLog, QualityGate
    from services.user_service import get_user_by_operator_id

    user = get_user_by_operator_id(db, operator_id)
    if user is None:
        return {"error": "Operator not found"}

    events = db.query(ProductionEvent).filter(ProductionEvent.operator_id == operator_id).all()
    weight_logs = db.query(StageWeightLog).filter(StageWeightLog.operator_id == operator_id).all()
    gates = db.query(QualityGate).filter(QualityGate.inspector_id == operator_id).all()

    total_pieces = len(set(e.piece_id for e in events))
    total_events = len(events)
    average_wastage = sum(w.variance or 0 for w in weight_logs) / len(weight_logs) if weight_logs else 0
    pass_count = sum(1 for g in gates if g.ai_verdict == "PASS")
    gate_count = len(gates)

    return {
        "operator_id": operator_id,
        "name": user.name,
        "total_pieces_worked": total_pieces,
        "total_events": total_events,
        "average_wastage": average_wastage,
        "quality_gates_reviewed": gate_count,
        "quality_pass_rate": pass_count / gate_count if gate_count else 0,
    }
