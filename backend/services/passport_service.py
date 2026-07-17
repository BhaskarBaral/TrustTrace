"""Module: services/passport_service.py"""
from sqlalchemy.orm import Session

from services.batch_service import get_batch_by_id
from services.event_service import get_events_by_piece_id
from services.groq_service import generate_compliance_narrative
from services.inspection_service import get_inspections_by_piece_id
from services.piece_service import get_piece_by_piece_id
from services.quality_service import get_quality_gates_by_piece
from services.weight_service import get_weight_logs_by_piece


def build_piece_passport(
    db: Session,
    piece_id: str
) -> dict:

    piece = get_piece_by_piece_id(
        db=db,
        piece_id=piece_id
    )

    if piece is None:
        return None

    production_history = get_events_by_piece_id(
        db=db,
        piece_id=piece_id
    )

    weight_logs = get_weight_logs_by_piece(
        db=db,
        piece_id=piece_id
    )

    quality_gates = get_quality_gates_by_piece(
        db=db,
        piece_id=piece_id
    )

    inspections = get_inspections_by_piece_id(
        db=db,
        piece_id=piece_id
    )

    batch = None
    if piece.batch_id:
        batch = get_batch_by_id(db, piece.batch_id)

    # Generate AI summary using reasoning model
    summary = _generate_passport_summary({
        "piece_id": piece.piece_id,
        "product_type": piece.product_type,
        "material": piece.material,
        "current_stage": piece.current_stage,
        "status": piece.status,
        "batch_info": {"batch_id": batch.batch_id, "gold_lot": batch.gold_lot} if batch else None,
        "stage_count": len(production_history),
        "gate_count": len(quality_gates),
        "last_verdict": quality_gates[-1].ai_verdict if quality_gates else None,
    })

    return {
        "piece": piece,
        "batch": batch,
        "production_history": production_history,
        "weight_logs": weight_logs,
        "quality_gates": quality_gates,
        "inspections": inspections,
        "ai_summary": summary,
    }


def _generate_passport_summary(context: dict) -> dict:
    """Use Groq reasoning to create a 2-3 line piece summary."""
    from services.groq_service import _get_client, _rate_limit, REASONING_MODEL
    import json

    client = _get_client()
    if client is None:
        return _fallback_summary(context)

    prompt = f"""You are a jewellery manufacturing analyst. Given this piece data, return ONLY valid JSON:
{{
  "piece_overview": "1 sentence describing what this piece is and its current status",
  "quality_summary": "1 sentence on quality check results"
}}
Data: {json.dumps(context)}"""

    _rate_limit()
    try:
        resp = client.chat.completions.create(
            model=REASONING_MODEL,
            messages=[
                {"role": "system", "content": "You return concise JSON only. No markdown."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=200, temperature=0.2, timeout=15,
        )
        content = resp.choices[0].message.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception:
        return _fallback_summary(context)


def _fallback_summary(context: dict) -> dict:
    return {
        "piece_overview": f"{context.get('product_type', 'Jewellery piece')} ({context.get('material', 'unknown material')}) — currently at {context.get('current_stage', 'registration stage')}.",
        "quality_summary": f"Passed {context.get('gate_count', 'several')} quality inspections. Last AI verdict: {context.get('last_verdict', 'pending')}.",
    }


def build_compliance_report(
    db: Session,
    piece_id: str
) -> dict:

    passport = build_piece_passport(db, piece_id)

    if passport is None:
        return None

    piece = passport["piece"]
    events = passport["production_history"]
    gates = passport["quality_gates"]
    batch = passport["batch"]

    operator_ids = list(dict.fromkeys(e.operator_id for e in events))

    stages = []
    for event in events:
        stages.append({
            "stage": event.stage,
            "operator_id": event.operator_id,
            "timestamp": event.timestamp.isoformat() if event.timestamp else None,
            "weight_in": event.weight_in,
            "weight_out": event.weight_out,
        })

    quality_results = []
    for gate in gates:
        quality_results.append({
            "stage": gate.stage,
            "ai_verdict": gate.ai_verdict,
            "defect_type": gate.defect_type,
            "human_review": gate.human_review,
            "confidence": gate.confidence,
        })

    completed_at = None
    if piece.status in ("Completed", "Passed QC"):
        last_event = events[-1] if events else None
        completed_at = last_event.timestamp.isoformat() if last_event and last_event.timestamp else None

    # Generate compliance narrative using Groq reasoning
    narrative = generate_compliance_narrative({
        "piece": piece,
        "batch": batch,
        "production_history": events,
        "quality_gates": gates,
        "material": piece.material,
        "product_type": piece.product_type,
        "piece_id": piece.piece_id,
        "gold_lot": batch.gold_lot if batch else None,
    })

    return {
        "piece_id": piece.piece_id,
        "product_type": piece.product_type,
        "material": piece.material,
        "gold_lot": batch.gold_lot if batch else None,
        "alloy_batch": batch.alloy_batch if batch else None,
        "stone_parcel": batch.stone_parcel if batch else None,
        "operator_chain": operator_ids,
        "manufacturing_stages": stages,
        "quality_results": quality_results,
        "created_at": piece.created_at.isoformat() if piece.created_at else None,
        "completed_at": completed_at,
        "ai_narrative": narrative,
    }
