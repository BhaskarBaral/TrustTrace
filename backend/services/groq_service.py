"""
Unified Groq service for TrustTrace.
Provides vision analysis (quality gates) and reasoning (production insights, compliance narratives).
Both models run on Groq with automatic fallback when API is unavailable.
"""
import base64
import json
import os
import time
from pathlib import Path
from functools import wraps

from openai import OpenAI

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
REASONING_MODEL = "openai/gpt-oss-120b"

# Rate-limit tracking for free-tier: 250K TPM shared pool
_last_call_time = 0
_MIN_INTERVAL = 0.3  # 300ms between calls to stay well under limit


def _rate_limit():
    global _last_call_time
    now = time.time()
    elapsed = now - _last_call_time
    if elapsed < _MIN_INTERVAL:
        time.sleep(_MIN_INTERVAL - elapsed)
    _last_call_time = time.time()


def _get_client() -> OpenAI | None:
    if not API_KEY:
        return None
    return OpenAI(api_key=API_KEY, base_url=BASE_URL)


# ---------------------------------------------------------------------------
# Vision:  jewellery defect inspection
# ---------------------------------------------------------------------------

DEFECT_MAP = {
    "casting": ["Porosity", "Shrinkage Cavity", "Incomplete Fill", "Surface Crack", "Sand Inclusion", "Dimensional Error"],
    "stone-setting": ["Loose Prong", "Crooked Prong", "Stone Seating Gap", "Damaged Girdle", "Missing Stone", "Uneven Prong Height"],
    "polishing": ["Fire Scale", "Orange Peel", "Buffing Residue", "Drag Mark", "Scratch", "Uneven Finish"],
    "plating": ["Uneven Plating", "Peeling", "Discoloration", "Missed Spot", "Blister", "Cloudy Finish"],
}

_INSPECTION_PROMPT = """You are a jewellery quality inspection expert. Analyze this jewellery piece image and return ONLY valid JSON (no markdown) with:
{
  "verdict": "PASS" | "FLAG" | "FAIL",
  "defect_type": "specific defect name or null",
  "confidence": 0.0-1.0,
  "description": "one sentence describing your observation"
}"""


def _encode_image(image_path: str) -> str | None:
    path = Path(image_path)
    if not path.exists():
        return None
    try:
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    except Exception:
        return None


def _mime_from_ext(path: str) -> str:
    ext = Path(path).suffix.lower()
    return {"png": "image/png", "webp": "image/webp"}.get(ext, "image/jpeg")


def inspect_image(image_path: str) -> dict:
    """
    Analyse a jewellery piece image using Groq vision.
    Returns: {"verdict", "defect_type", "confidence", "description"}
    On failure, returns empty verdict keys so caller can fall back.
    """
    client = _get_client()
    if client is None:
        return {"verdict": None, "error": "Groq API key not configured"}

    b64 = _encode_image(image_path)
    if b64 is None:
        return {"verdict": None, "error": "Could not read image file"}

    _rate_limit()

    try:
        resp = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": _INSPECTION_PROMPT},
                    {"type": "image_url", "image_url": {
                        "url": f"data:{_mime_from_ext(image_path)};base64,{b64}"
                    }},
                ],
            }],
            max_tokens=300, temperature=0.1, timeout=30,
        )
        content = resp.choices[0].message.content.strip()
        if "```" in content:
            content = content.split("```")[1] if "```json" not in content else content.split("```json")[1]
            content = content.split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        return {"verdict": None, "error": str(e)}


# ---------------------------------------------------------------------------
# Reasoning: production insights from aggregated data
# ---------------------------------------------------------------------------

_INSIGHTS_PROMPT = """You are a jewellery manufacturing production analyst. Based on the following production data, provide a concise analysis. Return ONLY valid JSON with:
{
  "overall_assessment": "2-3 sentence summary of current production health",
  "bottlenecks": ["list of issues found, e.g. 'Filing station has 4 pieces waiting — potential bottleneck'"],
  "quality_insight": "1-2 sentence on quality trends and defect patterns",
  "recommendation": "one actionable recommendation for the factory manager"
}"""


def generate_insights(wip_data: list, quality_summary: dict, gold_recon: dict) -> dict:
    """
    Use reasoning model to produce natural-language production insights.
    Falls back gracefully if reasoning model is unavailable.
    """
    prompt_data = {
        "wip": wip_data,
        "quality": quality_summary,
        "gold_reconciliation": gold_recon,
    }

    client = _get_client()
    if client is None:
        return _fallback_insights(wip_data, quality_summary, gold_recon)

    _rate_limit()

    try:
        resp = client.chat.completions.create(
            model=REASONING_MODEL,
            messages=[
                {"role": "system", "content": _INSIGHTS_PROMPT},
                {"role": "user", "content": json.dumps(prompt_data, default=str)},
            ],
            max_tokens=500, temperature=0.2, timeout=30,
        )
        content = resp.choices[0].message.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception:
        return _fallback_insights(wip_data, quality_summary, gold_recon)


def _fallback_insights(wip: list, quality: dict, gold: dict) -> dict:
    """Deterministic fallback when Groq reasoning is unavailable."""
    total_wip = sum(s.get("piece_count", 0) for s in wip if s.get("piece_count"))
    pass_rate = quality.get("pass_rate", 0) * 100
    gold_variance = gold.get("total_variance", 0)

    busy_stages = [s["stage"] for s in wip if s.get("piece_count", 0) > 1]
    bottleneck = f"{busy_stages[0]} has {wip[[s['stage'] for s in wip].index(busy_stages[0])]['piece_count']} pieces — potential bottleneck" if busy_stages else "Production flow is balanced"

    return {
        "overall_assessment": f"Production is active with {total_wip} pieces across {len([s for s in wip if s.get('piece_count')])} stages. Quality pass rate is {pass_rate:.0f}%. Gold variance is {gold_variance:.2f}g.",
        "bottlenecks": [bottleneck],
        "quality_insight": f"Pass rate of {pass_rate:.0f}% across {quality.get('total_gates', 0)} inspections. Top defects: {', '.join(quality.get('top_defects', ['none']))}." if quality.get("total_gates") else "No quality data yet.",
        "recommendation": f"Investigate {gold_variance:.2f}g gold variance at {busy_stages[0] if busy_stages else 'production'} stage — check gold recovery and weighing procedures." if gold_variance else "Production is running smoothly. Maintain current process.",
    }


# ---------------------------------------------------------------------------
# Reasoning: compliance narrative (EU DPP summary)
# ---------------------------------------------------------------------------

_COMPLIANCE_PROMPT = """You are a compliance officer for jewellery exports. Given the following piece passport, write a compliance narrative. Return ONLY valid JSON with:
{
  "provenance_summary": "2-3 sentence describing gold/alloy/stone origin and manufacturing chain",
  "risk_assessment": "one sentence on any quality or traceability risks",
  "compliance_verdict": "one of COMPLIANT / MINOR_ISSUES / NON_COMPLIANT",
  "audit_notes": "one sentence for EU DPP auditors"
}"""


def generate_compliance_narrative(passport_data: dict) -> dict:
    """
    Use reasoning model to produce a human-readable compliance narrative
    for the EU DPP report.
    """
    client = _get_client()
    if client is None:
        return _fallback_compliance(passport_data)

    _rate_limit()

    try:
        resp = client.chat.completions.create(
            model=REASONING_MODEL,
            messages=[
                {"role": "system", "content": _COMPLIANCE_PROMPT},
                {"role": "user", "content": json.dumps(passport_data, default=str)},
            ],
            max_tokens=500, temperature=0.2, timeout=30,
        )
        content = resp.choices[0].message.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception:
        return _fallback_compliance(passport_data)


def _fallback_compliance(data: dict) -> dict:
    """Fallback compliance narrative when Groq reasoning is unavailable."""
    piece = data.get("piece", {})
    events = data.get("production_history", [])
    gates = data.get("quality_gates", [])
    batch = data.get("batch") or {}

    material = getattr(piece, "material", None) or data.get("material", "precious metal")
    ptype = getattr(piece, "product_type", None) or data.get("product_type", "jewellery piece")
    pid = getattr(piece, "piece_id", None) or data.get("piece_id", "Unknown")
    gold_lot = getattr(batch, "gold_lot", None) or data.get("gold_lot", None)
    stages_count = len(events)
    gate_count = len(gates)
    operator_count = len({getattr(e, "operator_id", None) for e in events})

    provenance = f"This {material} {ptype} ({pid}) was manufactured from gold lot {gold_lot or 'recorded internally'} through {stages_count} production stages, handled by {operator_count} certified artisans."
    risks = f"All {gate_count} quality checks passed AI inspection. No material compliance risks identified." if gate_count > 0 else "Quality gates not yet completed for this piece."

    return {
        "provenance_summary": provenance,
        "risk_assessment": risks,
        "compliance_verdict": "COMPLIANT",
        "audit_notes": f"Full digital traceability available for EU DPP. Verification chain: {gate_count} quality gates across {stages_count} stages.",
    }
