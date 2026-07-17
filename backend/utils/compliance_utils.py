"""Module: utils/compliance_utils.py"""
from datetime import datetime, timezone


def build_eu_dpp_json(passport: dict) -> dict:
    piece = passport.get("piece", {})
    batch = passport.get("batch") or {}
    events = passport.get("production_history", [])
    gates = passport.get("quality_gates", [])

    return {
        "dpp_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "product": {
            "identifier": getattr(piece, "piece_id", None),
            "product_type": getattr(piece, "product_type", None),
            "material": getattr(piece, "material", None),
        },
        "material_provenance": {
            "gold_lot": getattr(batch, "gold_lot", None),
            "alloy_batch": getattr(batch, "alloy_batch", None),
            "stone_parcel": getattr(batch, "stone_parcel", None),
        },
        "manufacturing_chain": [
            {
                "stage": getattr(e, "stage", None),
                "operator_id": getattr(e, "operator_id", None),
                "timestamp": getattr(e, "timestamp", None).isoformat()
                if getattr(e, "timestamp", None) else None,
                "weight_in": getattr(e, "weight_in", None),
                "weight_out": getattr(e, "weight_out", None),
            }
            for e in events
        ],
        "quality_checks": [
            {
                "stage": getattr(g, "stage", None),
                "ai_verdict": getattr(g, "ai_verdict", None),
                "defect_type": getattr(g, "defect_type", None),
                "human_review": getattr(g, "human_review", None),
                "confidence": getattr(g, "confidence", None),
            }
            for g in gates
        ],
    }
